from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT_ID = "2546"
BRANCH_ID = "MTS_R2FR_BOUNDARY_TERM_CLASSIFICATION_EXACT_VS_CORNER_REFERENCE_2546"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2546-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2546_SOURCE_REGISTER.csv",
    "classification": RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_TERM_CLASSIFICATION.csv",
    "certificates": RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_CERTIFICATE_MATRIX.csv",
    "triage": RESIDUALS / "P8_Y5_NO_SHADOW_2546_ACTUAL_TERM_TRIAGE.csv",
    "bounds": RESIDUALS / "P8_Y5_NO_SHADOW_2546_BREM_BOUND_ROWS.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2546_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2546_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2546_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2546_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2546_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2546_VALIDATION.csv",
}

BRANCH_COPIES = {
    "classification": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Boundary_term_classification_2546_NONCLAIM.csv",
    "bounds": POST_ROOT / "source-intake" / "local_bounds" / "Brem_bound_rows_2546_NONCLAIM.csv",
    "certificates": POST_ROOT / "source-intake" / "hamiltonian-source" / "Boundary_certificate_matrix_2546_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "FIXED_REFERENCE_SELECTOR2547_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    (
        "SRC2546_00_2545_doc",
        "2545-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md",
        ["EIC2545_4_boundary_component", "BRR2545_5_total", "NEXT2545_0_selected"],
        "immediate 2545 exact-improvement cancellation and Bzero remainder split",
    ),
    (
        "SRC2546_01_2545_validation",
        "source-intake/mts_residuals/P8_Y5_BRR545_2545_VALIDATION.csv",
        ["VAL2545_OVERALL,PASS"],
        "2545 validation anchor",
    ),
    (
        "SRC2546_02_2545_reduction",
        "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_BZERO_RESIDUAL_REDUCTION.csv",
        ["BRR2545_0_exact_improvement", "BRR2545_4_reference", "BRR2545_5_total"],
        "machine-readable current Bzero residual vector",
    ),
    (
        "SRC2546_03_2545_next",
        "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_NEXT_TARGET.csv",
        ["NEXT2545_0_selected", "exact-mu"],
        "explicit selected target for this checkpoint",
    ),
    (
        "SRC2546_04_2381_doc",
        "2381-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md",
        ["BTC2381_7_total", "NEXT2381_0_selected"],
        "older boundary classification precedent",
    ),
    (
        "SRC2546_05_1019_exactness",
        "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        ["Exactness plus Stokes", "neither is parent-signed"],
        "exactness/Stokes source-pack precedent",
    ),
    (
        "SRC2546_06_1020_domain",
        "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
        ["weighted-Stokes theorem", "closed/corner-free domain"],
        "domain, cohomology, harmonic, and corner requirements",
    ),
    (
        "SRC2546_07_1771_boundary_reference",
        "1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
        ["boundary/reference/improvement", "fixed before readout"],
        "boundary/reference residual sector warning",
    ),
    (
        "SRC2546_08_1772_source_equality",
        "1772-Y5-R2FR-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        ["Pi_M J_H = J_M_top + dB_zero", "wrong conserved object"],
        "Hilbert/topological source-equality guard",
    ),
    (
        "SRC2546_09_2447_boundary_reference",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2447_BOUNDARY_REFERENCE_S_EQ_ZERO_THEOREM_GATE.csv",
        ["BZ2447_1_Bref_qblind_superselection", "reference subtraction is a contract"],
        "boundary reference zero theorem gate",
    ),
    (
        "SRC2546_10_2448_owner_contract",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2448_BREF_RELATIVE_BOUNDARY_OWNER_CONTRACT.csv",
        ["RBO2448_0_parent_boundary_action", "unique parent principle selecting B_ref"],
        "relative boundary class and B_ref owner contract",
    ),
    (
        "SRC2546_11_2455_embedding",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2455_BOUNDARY_REFERENCE_EMBEDDING_DERIVATION.csv",
        ["EMB2455_2_zero_condition", "D_a B_ref=0"],
        "source-blind boundary reference embedding condition",
    ),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "row_id": source_id,
                    "source_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "needles": "; ".join(needles),
                    "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                    "source_role": role,
                }
            )
        )
    return rows


def classification_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "BTC2546_0_exact_improvement",
            "class": "exact_improvement",
            "candidate_form": "B = d mu or boundary momentum B_X = d_S b_X with closed weight",
            "classification": "CONDITIONAL_ZERO_CLASS",
            "current_evidence": "2545 derives k_tau invariance for exact improvements; 1019/1020 give Stokes/domain clauses",
            "missing_certificate": "explicit parent primitive mu or b_X for actual MTS boundary term, fixed tau, fixed surface, no corner, no harmonic/topological part",
            "residual_if_missing": "Delta_exact_commutator_or_edge_residual",
            "claim_effect": "component zero only after actual term is classified as exact in a certified boundary class",
        },
        {
            "row_id": "BTC2546_1_corner",
            "class": "corner_codimension_two",
            "candidate_form": "corner charge Q_C or codimension-two contribution to Q_tau/theta",
            "classification": "LIVE_REMAINDER",
            "current_evidence": "1020 and 2381 require corner-free surfaces or explicit corner charge accounting",
            "missing_certificate": "corner-free surface, or all corners included with fixed convention before variation",
            "residual_if_missing": "epsilon_corner_abs",
            "claim_effect": "blocks Bzero zero theorem",
        },
        {
            "row_id": "BTC2546_2_topological_nonexact",
            "class": "topological_or_nonexact",
            "candidate_form": "closed but non-exact h_X, harmonic edge mode, or fixed cohomology class",
            "classification": "LIVE_REMAINDER",
            "current_evidence": "1020 decomposes exact, harmonic, and residual boundary pieces",
            "missing_certificate": "h_X=0, projected silent, or separately source-bounded in same boundary class",
            "residual_if_missing": "epsilon_top_abs",
            "claim_effect": "exact-improvement algebra cannot erase harmonic/topological charge",
        },
        {
            "row_id": "BTC2546_3_field_dependent_tau_surface",
            "class": "field_dependent_tau_or_surface",
            "candidate_form": "[delta,i_tau]mu, delta S_outer, moving readout surface, radial profile",
            "classification": "LIVE_REMAINDER",
            "current_evidence": "2545 cancellation assumes fixed tau and fixed surface",
            "missing_certificate": "delta tau=0, delta S_outer=0, no readout-induced surface retuning",
            "residual_if_missing": "epsilon_delta_tau_abs",
            "claim_effect": "the 2545 exact-improvement cancellation no longer follows",
        },
        {
            "row_id": "BTC2546_4_fixed_reference",
            "class": "unfixed_reference_counterterm",
            "candidate_form": "H_ref, B_ref, C_top, or counterterm class selected after source/readout",
            "classification": "PRIMARY_LIVE_REMAINDER",
            "current_evidence": "1771, 2447, 2448, and 2455 all keep source-blind/fixed-before-readout reference selection unsigned",
            "missing_certificate": "source-independent H_ref/B_ref/C_top selector fixed before source/readout and shared across the boundary class",
            "residual_if_missing": "Delta_ref_over_MH",
            "claim_effect": "can fake charge closure; selected as next primary derivation target",
        },
        {
            "row_id": "BTC2546_5_nonintegrable_flux",
            "class": "nonintegrable_flux",
            "candidate_form": "field-space curl of delta Q_tau - i_tau theta or flux through open annulus",
            "classification": "LIVE_REMAINDER",
            "current_evidence": "2545 reduces exact improvements but does not close the remaining Hamiltonian one-form",
            "missing_certificate": "closed one-form on field space after exact/corner/reference split",
            "residual_if_missing": "Delta_H_res_over_MH",
            "claim_effect": "H_tau and M_H_ref remain placeholders if nonintegrable",
        },
        {
            "row_id": "BTC2546_6_source_measure_equality",
            "class": "source_measure_equality_remainder",
            "candidate_form": "Pi_M J_H - J_M_top - dB_zero",
            "classification": "PARALLEL_ROOT_REMAINDER",
            "current_evidence": "1772 shows a closed topological current can be the wrong measured source",
            "missing_certificate": "Pi_M J_H = J_M_top + dB_zero with same compact-source worldtube and same M_H_ref",
            "residual_if_missing": "R_eq_integral_over_MH",
            "claim_effect": "Newton/GR source normalization cannot be claimed from boundary zero alone",
        },
        {
            "row_id": "BTC2546_7_total",
            "class": "Bzero_remainder_total",
            "candidate_form": "B_rem = B_corner + B_top + B_delta_tau + B_ref + B_nonintegrable + B_source_measure",
            "classification": "REDUCED_BUT_NOT_CLOSED",
            "current_evidence": "2545 exact component is conditionally silent; all other buckets remain live",
            "missing_certificate": "all live classes zeroed or finite source-bounded with positive same-frame M_H_ref",
            "residual_if_missing": "epsilon_Brem_abs",
            "claim_effect": "Bzero is structured into gates but remains nonclaim",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def certificate_rows() -> list[dict[str, object]]:
    rows = [
        ("BCC2546_0_parent_primitive", "explicit exact primitive", "exact_improvement zero", "MISSING_PARENT_PRIMITIVE", "write mu or b_X from parent L/theta/Q, not by posterior fitting", "BTC2546_0_exact_improvement"),
        ("BCC2546_1_surface_corner", "corner-free compact linked surface", "Stokes/no-corner zero", "MISSING_CORNER_CERTIFICATE", "partial boundary of S is zero or all corners included with fixed Q_C", "BTC2546_1_corner"),
        ("BCC2546_2_cohomology", "relative cohomology/harmonic silence", "topological/non-exact zero", "MISSING_COHOMOLOGY_CERTIFICATE", "h_X=0 or h_X source-bounded in same boundary class", "BTC2546_2_topological_nonexact"),
        ("BCC2546_3_tau_surface_lock", "fixed tau and fixed S_outer", "2545 k_tau cancellation", "MISSING_TAU_SURFACE_LOCK", "delta tau=0, delta S_outer=0, no fitted readout surface", "BTC2546_3_field_dependent_tau_surface"),
        ("BCC2546_4_fixed_reference", "fixed H_ref/B_ref/C_top selector", "no cancellation knob and same boundary class", "MISSING_FIXED_REFERENCE_SELECTOR", "selector fixed before source/readout and independent of residual sign/magnitude", "BTC2546_4_fixed_reference"),
        ("BCC2546_5_integrability", "closed Hamiltonian one-form", "H_tau and M_H_ref", "MISSING_HTAU_INTEGRABILITY", "delta(k_tau)=0 on reduced branch, or finite Delta_H_res row", "BTC2546_5_nonintegrable_flux"),
        ("BCC2546_6_source_measure", "Hilbert/topological source equality", "Newton/GR source normalization", "MISSING_SOURCE_MEASURE_EQUALITY", "Pi_M J_H = J_M_top + dB_zero before orbital GM import", "BTC2546_6_source_measure_equality"),
        ("BCC2546_7_MHref", "positive same-frame M_H_ref", "normalized residual scoring", "MISSING_POSITIVE_MHREF", "finite positive H_tau[S_outer]-H_ref with source/equation path", "all normalized rows"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "certificate": certificate,
                    "needed_for": needed_for,
                    "current_status": status,
                    "test": test,
                    "blocks": blocks,
                }
            )
        )
        for row_id, certificate, needed_for, status, test, blocks in rows
    ]


def actual_term_triage_rows() -> list[dict[str, object]]:
    rows = [
        ("ATI2546_0_exact", "B_exact_improvement", "BRR2545_0_exact_improvement", "BTC2546_0_exact_improvement", "CONDITIONAL_ZERO_IF_CERTIFIED", "parent primitive and domain certificates still missing", "Delta_exact_commutator_or_edge_residual"),
        ("ATI2546_1_corner", "B_corner", "BRR2545_1_corner", "BTC2546_1_corner", "LIVE_REMAINDER", "corner certificate missing", "epsilon_corner_abs"),
        ("ATI2546_2_topological", "B_topological_or_nonexact", "BRR2545_2_topological", "BTC2546_2_topological_nonexact", "LIVE_REMAINDER", "cohomology/harmonic silence missing", "epsilon_top_abs"),
        ("ATI2546_3_delta_tau", "B_delta_tau", "BRR2545_3_field_dependent_tau", "BTC2546_3_field_dependent_tau_surface", "LIVE_REMAINDER", "fixed tau/surface lock missing", "epsilon_delta_tau_abs"),
        ("ATI2546_4_reference", "B_reference_unfixed", "BRR2545_4_reference", "BTC2546_4_fixed_reference", "PRIMARY_LIVE_REMAINDER", "fixed source-blind reference selector missing", "Delta_ref_over_MH"),
        ("ATI2546_5_nonintegrable", "B_nonintegrable_flux", "BRR2545_5_total", "BTC2546_5_nonintegrable_flux", "LIVE_REMAINDER", "Hamiltonian one-form integrability missing", "Delta_H_res_over_MH"),
        ("ATI2546_6_source_measure", "Pi_M J_H - J_M_top - dB_zero", "1772 source equality guard", "BTC2546_6_source_measure_equality", "PARALLEL_ROOT_REMAINDER", "Hilbert/topological equality missing", "R_eq_integral_over_MH"),
        ("ATI2546_7_denominator", "M_H_ref", "MHR2545_0_denominator", "BCC2546_7_MHref", "MISSING_DENOMINATOR", "positive same-frame denominator missing", "all normalized residual rows blocked"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "term": term,
                    "source_row": source_row,
                    "assigned_bucket": bucket,
                    "triage_status": status,
                    "missing_proof": missing,
                    "residual_row": residual,
                }
            )
        )
        for row_id, term, source_row, bucket, status, missing, residual in rows
    ]


def bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "BRB2546_0_epsilon_Brem",
            "quantity": "epsilon_Brem_abs",
            "formula": "(abs(B_corner)+abs(B_top)+abs(B_delta_tau)+abs(Delta_ref)+abs(Delta_H_res)+abs(R_eq_component))/M_H_ref",
            "units": "dimensionless after same-frame M_H_ref normalization",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "required_inputs": "component numerators; units; source paths; fixed H_ref; positive M_H_ref; no-cancellation guard",
        },
        {
            "row_id": "BRB2546_1_Delta_ref",
            "quantity": "Delta_ref_over_MH",
            "formula": "abs(H_ref_shift_or_unfixed_counterterm)/M_H_ref",
            "units": "dimensionless after same-frame M_H_ref normalization",
            "status": "PRIMARY_NEXT_BOUND_IF_SELECTOR_FAILS",
            "required_inputs": "H_ref selector or finite reference-shift numerator; M_H_ref; source-blindness guard",
        },
        {
            "row_id": "BRB2546_2_Delta_H_res",
            "quantity": "Delta_H_res_over_MH",
            "formula": "norm(delta(k_tau_reduced))/M_H_ref",
            "units": "dimensionless after same-frame M_H_ref normalization",
            "status": "INTEGRABILITY_BOUND_SCHEMA_ONLY",
            "required_inputs": "reduced k_tau one-form; field-space curl; M_H_ref; source paths",
        },
        {
            "row_id": "BRB2546_3_R_eq",
            "quantity": "R_eq_integral_over_MH",
            "formula": "abs(int_W(Pi_M J_H - J_M_top - dB_zero))/M_H_ref",
            "units": "dimensionless after same-frame M_H_ref normalization",
            "status": "SOURCE_EQUALITY_BOUND_SCHEMA_ONLY",
            "required_inputs": "worldtube W; Hilbert current; topological current; Bzero residual; M_H_ref",
        },
        {
            "row_id": "BRB2546_4_exact_switch",
            "quantity": "B_exact_improvement_zero_switch",
            "formula": "true iff B=dmu or d_S b_X and all exact/domain/corner/cohomology/tau certificates pass",
            "units": "boolean theorem switch",
            "status": "SWITCH_BLOCKED_PENDING_PARENT_PRIMITIVE_AND_CERTIFICATES",
            "required_inputs": "explicit parent primitive plus BCC2546_0 through BCC2546_3",
        },
    ]
    return [stamp(no_claim({**row, "score_ready": "false"})) for row in rows]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "DEC2546_0_classification_result",
            "decision": "accept boundary classification as structured nonclaim progress",
            "reason": "2545 gives a conditional exact-improvement zero, but non-exact, corner, tau/surface, reference, nonintegrable, and source-equality pieces remain live",
            "consequence": "Bzero becomes a finite residual vector rather than a single mystery blocker",
            "status": "CLASSIFICATION_BUILT_NONCLAIM",
        },
        {
            "row_id": "DEC2546_1_actual_term_triage",
            "decision": "map the 2545 residual vector into named buckets",
            "reason": "this prevents circling back to a generic M_H_ref first-row and gives each obstruction a proof or bound target",
            "consequence": "actual-term triage now selects Delta_ref/MHref/source-equality as the hard live pieces",
            "status": "ANTI_CIRCLING_STRUCTURE_ADDED",
        },
        {
            "row_id": "DEC2546_2_primary_next",
            "decision": "attack fixed reference selector next",
            "reason": "an unfixed H_ref/B_ref can fake charge closure and contaminate every normalized residual",
            "consequence": "2547 should derive source-independent H_ref/B_ref/C_top selection or stage Delta_ref_over_MH",
            "status": "SELECT_2547_FIXED_REFERENCE",
        },
        {
            "row_id": "DEC2546_3_no_public_claim",
            "decision": "do not push or frame this as local GR/Newton evidence",
            "reason": "component cancellation and classification are real progress, not a source measure or denominator derivation",
            "consequence": "private goal work continues; GitHub remains paused",
            "status": "GLOBAL_CLAIMS_BLOCKED",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG2546_0_inventory", "known 2545 boundary residuals assigned to buckets", "PASS_INVENTORY_ONLY", "classification covers the current residual vector but does not zero it"),
        ("CG2546_1_exact_component", "exact-improvement component zero", "PASS_CONDITIONAL_COMPONENT_ONLY", "usable only after explicit parent primitive and domain certificates"),
        ("CG2546_2_fixed_reference", "source-independent fixed H_ref/B_ref/C_top selector", "FAIL", "Delta_ref remains selected blocker"),
        ("CG2546_3_MHref", "positive same-frame M_H_ref", "FAIL", "epsilon_Brem_abs and local bound rows cannot be scored"),
        ("CG2546_4_source_measure", "Hilbert/topological source equality", "FAIL", "Newton/GR source normalization remains unproved"),
        ("CG2546_5_local_GR_Newton", "local GR/Newton recovery", "FAIL_NONCLAIM", "boundary/reference/source-measure bridges remain open"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "gate": gate,
                    "gate_status": status,
                    "claim_effect": effect,
                }
            )
        )
        for row_id, gate, status, effect in rows
    ]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        ("REF2546_0_Stokes_overclaim", "exact/Stokes route kills every boundary term", "false", "corner, harmonic/topological, moving-surface, reference, flux, and source-equality pieces remain live", "BTC2546_1_corner;BTC2546_2_topological_nonexact;BTC2546_3_field_dependent_tau_surface;BTC2546_4_fixed_reference"),
        ("REF2546_1_reference_fit", "choose B_ref/H_ref after readout to cancel B_rem", "false", "reference must be fixed before source/readout or it becomes a fitted cancellation knob", "BCC2546_4_fixed_reference;CG2546_2_fixed_reference"),
        ("REF2546_2_closed_wrong_object", "closed topological charge is enough for measured GM/Newton", "false", "the topological current can be the wrong conserved object without Hilbert/source equality", "BTC2546_6_source_measure_equality;BCC2546_6_source_measure"),
        ("REF2546_3_public_checkpoint", "publish this as local GR/Newton pass", "false", "classification is progress, not closure; values and certificates are missing", "CG2546_2_fixed_reference;CG2546_3_MHref;CG2546_5_local_GR_Newton"),
        ("REF2546_4_repeat_MHref_staging", "do another generic M_H_ref first-row next", "false", "2545 and 2381 already staged it; next must derive selector or a concrete Delta_ref bound row", "DEC2546_1_actual_term_triage;DEC2546_2_primary_next"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "claim": claim,
                    "allowed": allowed,
                    "reason": reason,
                    "blocking_rows": blockers,
                }
            )
        )
        for row_id, claim, allowed, reason, blockers in rows
    ]


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "NEXT2546_0_selected",
            "priority": "selected",
            "next_file": "2547-Y5-R2FR-fixed-reference-selector-or-Delta-ref-row.md",
            "next_script": "scripts/Y5_R2FR_fixed_reference_selector_or_Delta_ref_row_2547.py",
            "success_condition": "derive a source-independent H_ref/B_ref/C_top selector fixed before source/readout and compatible with 2545 exact-improvement cancellation",
            "fallback_condition": "stage Delta_ref_over_MH with source path, units, no-cancellation guard, and valid_for_claim=false",
        },
        {
            "row_id": "NEXT2546_1_parallel",
            "priority": "parallel",
            "next_file": "2547b-Y5-R2FR-parent-primitive-mu-or-boundary-residual-source-pack.md",
            "next_script": "scripts/Y5_R2FR_parent_primitive_mu_or_boundary_residual_source_pack_2547b.py",
            "success_condition": "write explicit parent primitive mu or b_X for actual MTS boundary terms",
            "fallback_condition": "retain exact switch blocked and source-pack every unowned boundary term",
        },
        {
            "row_id": "NEXT2546_2_parallel",
            "priority": "parallel",
            "next_file": "2547c-Y5-R2FR-Hilbert-topological-source-equality-or-Req-bound.md",
            "next_script": "scripts/Y5_R2FR_Hilbert_topological_source_equality_or_Req_bound_2547c.py",
            "success_condition": "prove Pi_M J_H = J_M_top + dB_zero in the same compact-source boundary class",
            "fallback_condition": "retain R_eq_integral_over_MH and I_commutator bound rows",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def branch_copy_rows() -> list[dict[str, object]]:
    copies = {
        BRANCH_COPIES["classification"]: classification_rows(),
        BRANCH_COPIES["bounds"]: bound_rows(),
        BRANCH_COPIES["certificates"]: certificate_rows(),
        BRANCH_COPIES["next"]: next_rows(),
    }
    rows: list[dict[str, object]] = []
    for path, payload in copies.items():
        write_csv(path, payload)
        rows.append(
            stamp(
                {
                    "row_id": f"COPY2546_{len(rows)}",
                    "copy_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "purpose": "nonclaim branch handoff copy",
                }
            )
        )
    return rows


def csv_has(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def all_flags_false(paths: list[Path]) -> bool:
    watched = {"valid_for_claim", "claim_allowed", "score_ready", "parent_signed", "theorem_zero", "numeric_prediction_present"}
    for path in paths:
        for row in read_csv(path):
            for key in watched.intersection(row):
                if str(row[key]).strip().lower() in {"true", "yes", "1", "pass_for_claim"}:
                    return False
    return True


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = list(outputs.values())
    generated_before_validation = [path for key, path in outputs.items() if key != "validation"]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2546_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist"))
    checks.append(("VAL2546_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found"))
    checks.append(("VAL2546_02_outputs_exist", all(path.exists() for path in generated_before_validation), "all 2546 output files written before validation"))
    csv_parse_ok = True
    for path in generated_before_validation:
        try:
            csv_parse_ok = csv_parse_ok and len(read_csv(path)) > 0
        except Exception:
            csv_parse_ok = False
    checks.append(("VAL2546_03_csv_parse", csv_parse_ok, "all generated CSV files parse and contain rows"))
    classes = outputs["classification"].read_text(encoding="utf-8", errors="replace") if outputs["classification"].exists() else ""
    required_classes = ["exact_improvement", "corner_codimension_two", "topological_or_nonexact", "field_dependent_tau_or_surface", "unfixed_reference_counterterm", "nonintegrable_flux", "source_measure_equality_remainder"]
    checks.append(("VAL2546_04_all_classes_present", all(item in classes for item in required_classes), "boundary classes cover exact/corner/topological/tau/reference/flux/source-measure"))
    triage = outputs["triage"].read_text(encoding="utf-8", errors="replace") if outputs["triage"].exists() else ""
    required_terms = ["B_exact_improvement", "B_corner", "B_topological_or_nonexact", "B_delta_tau", "B_reference_unfixed", "B_nonintegrable_flux", "M_H_ref"]
    checks.append(("VAL2546_05_actual_terms_triaged", all(item in triage for item in required_terms), "2545 residual vector mapped into named buckets"))
    checks.append(("VAL2546_06_reference_selected", csv_has(outputs["decision"], "SELECT_2547_FIXED_REFERENCE") and csv_has(outputs["next"], "NEXT2546_0_selected"), "fixed reference selector selected next"))
    checks.append(("VAL2546_07_bound_rows_nonready", csv_has(outputs["bounds"], "SCHEMA_READY_VALUES_MISSING") and not csv_has(outputs["bounds"], ",true,true,"), "Brem/Delta_ref rows remain non-score-ready"))
    checks.append(("VAL2546_08_global_gates_blocked", csv_has(outputs["claims"], "CG2546_5_local_GR_Newton") and csv_has(outputs["claims"], "FAIL_NONCLAIM"), "global/local claims remain blocked"))
    checks.append(("VAL2546_09_refusals_block_claims", csv_has(outputs["refusal"], "REF2546_3_public_checkpoint") and csv_has(outputs["refusal"], "REF2546_4_repeat_MHref_staging"), "public claim and circular restage refused"))
    checks.append(("VAL2546_10_branch_copies", all(path.exists() for path in BRANCH_COPIES.values()), "all nonclaim branch copies exist"))
    checks.append(("VAL2546_11_no_positive_claim_flags", all_flags_false(generated_before_validation + list(BRANCH_COPIES.values())), "all generated claim/readiness flags remain negative"))
    checks.append(("VAL2546_12_formalization_untouched", FORMALIZATION_WORKBENCH.exists() and all(str(path).startswith(str(POST_ROOT)) for path in generated + list(BRANCH_COPIES.values()) + [DOC_PATH]), "generator writes only under post-checkpoint-work"))
    checks.append(("VAL2546_13_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(ok for _, ok, _ in checks)
    rows = [
        stamp(
            {
                "row_id": row_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )
        for row_id, ok, detail in checks
    ]
    rows.append(
        stamp(
            {
                "row_id": "VAL2546_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2546 classifies the 2545 boundary remainder into proof/bound buckets, selects fixed-reference derivation next, and keeps local-GR/Newton/public claims blocked",
            }
        )
    )
    return rows


def table(columns: list[str], rows: list[dict[str, object]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    sources = read_csv(outputs["source"])
    classification = read_csv(outputs["classification"])
    certificates = read_csv(outputs["certificates"])
    triage = read_csv(outputs["triage"])
    bounds = read_csv(outputs["bounds"])
    decision = read_csv(outputs["decision"])
    claims = read_csv(outputs["claims"])
    refusals = read_csv(outputs["refusal"])
    next_target = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2546 - boundary term classification exact vs corner/reference

## Result

2546 turns the 2545 boundary problem into a finite proof/bound matrix.

The clean win remains narrow but real: exact boundary improvements are conditionally silent in `delta H_tau` when the
primitive is parent-owned, `tau` and the surface are fixed, and no corner or topological/harmonic class sneaks in.

The important non-circling move is that the rest is no longer one foggy "boundary term".  The live remainder is now
classified as corner, topological/non-exact, field-dependent tau/surface, unfixed reference, nonintegrable flux, and
Hilbert/topological source-measure equality.  The selected next attack is fixed reference selection because an unfixed
`H_ref/B_ref/C_top` can counterfeit charge closure.

No `B_zero_flux=0`, `M_H_ref`, Newton, local-GR, PPN, clock, orbital, R10, or GitHub/public claim is made.

## Source Register

{table(["row_id", "source_path", "exists", "needles_found", "source_role"], sources)}

## Boundary Term Classification

{table(["row_id", "class", "candidate_form", "classification", "missing_certificate", "residual_if_missing", "claim_effect"], classification)}

## Boundary Certificate Matrix

{table(["row_id", "certificate", "needed_for", "current_status", "test", "blocks"], certificates)}

## Actual Term Triage

{table(["row_id", "term", "source_row", "assigned_bucket", "triage_status", "missing_proof", "residual_row"], triage)}

## Brem Bound Rows

{table(["row_id", "quantity", "formula", "units", "status", "required_inputs", "score_ready"], bounds)}

## Decision Ledger

{table(["row_id", "decision", "reason", "consequence", "status"], decision)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], claims)}

## Refusal Runner

{table(["row_id", "claim", "allowed", "reason", "blocking_rows"], refusals)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_target)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["classification"])}`
- `{rel(outputs["certificates"])}`
- `{rel(outputs["triage"])}`
- `{rel(outputs["bounds"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is not a final leap to local GR, but it is useful footwork.  We now know where the next punch should land:
derive a fixed, source-blind reference selector or admit `Delta_ref_over_MH` as a live residual.  If that fails, no
amount of exact-improvement algebra can save the local branch, because the reference term can always hide a fitted
cancellation.  If it succeeds, the boundary problem shrinks to source equality, integrability, and a positive
same-frame denominator.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["classification"], classification_rows())
    write_csv(OUTPUTS["certificates"], certificate_rows())
    write_csv(OUTPUTS["triage"], actual_term_triage_rows())
    write_csv(OUTPUTS["bounds"], bound_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

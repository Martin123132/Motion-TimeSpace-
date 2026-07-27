from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_BOUNDARY_TERM_CLASSIFICATION_EXACT_VS_CORNER_REFERENCE_2381"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2381-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "row_id": "SRC2381_00_2380_doc",
            "source_key": "2380_doc",
            "source_path": POST_ROOT / "2380-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md",
            "needles": ["`B_zero_flux` is now split", "exact boundary improvements do not change"],
            "source_role": "2380 exact-improvement cancellation law and Bzero split",
        },
        {
            "row_id": "SRC2381_01_2380_bzero_reduction",
            "source_key": "2380_bzero_reduction",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2380_BZERO_RESIDUAL_REDUCTION.csv",
            "needles": ["BRR2380_0_exact_improvement", "B_corner", "B_topological_or_nonexact", "B_reference_unfixed"],
            "source_role": "machine-readable 2380 remainder vector",
        },
        {
            "row_id": "SRC2381_02_1019_doc",
            "source_key": "1019_doc",
            "source_path": POST_ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needles": ["Exactness plus Stokes can kill", "neither is parent-signed"],
            "source_role": "older exactness/Stokes and projector orthogonality precedent",
        },
        {
            "row_id": "SRC2381_03_1019_exactness_csv",
            "source_key": "1019_exactness_csv",
            "source_path": RESIDUALS / "P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
            "needles": ["BE1019_0_domain", "BE1019_1_BX_exact", "BE1019_4_counterterm"],
            "source_role": "exactness/counterterm clause source",
        },
        {
            "row_id": "SRC2381_04_1020_doc",
            "source_key": "1020_doc",
            "source_path": POST_ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needles": ["weighted-Stokes theorem", "closed/corner-free domain"],
            "source_role": "domain/cohomology/corner classification precedent",
        },
        {
            "row_id": "SRC2381_05_1020_domain_csv",
            "source_key": "1020_domain_csv",
            "source_path": RESIDUALS / "P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv",
            "needles": ["BDC1020_0_surface_manifold", "BDC1020_1_boundary_class", "BDC1020_2_relative_cohomology"],
            "source_role": "boundary domain certificate rows",
        },
        {
            "row_id": "SRC2381_06_1020_weighted_stokes_csv",
            "source_key": "1020_weighted_stokes_csv",
            "source_path": RESIDUALS / "P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
            "needles": ["ETB1020_0_decomposition", "ETB1020_2_zero_conditions", "ETB1020_5_verdict"],
            "source_role": "exact/harmonic/residual decomposition source",
        },
        {
            "row_id": "SRC2381_07_1771_doc",
            "source_key": "1771_doc",
            "source_path": POST_ROOT / "1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
            "needles": ["boundary/reference/improvement", "fixed before readout"],
            "source_role": "boundary/reference as known local residual sector",
        },
        {
            "row_id": "SRC2381_08_1772_doc",
            "source_key": "1772_doc",
            "source_path": POST_ROOT / "1772-Y5-R2FR-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            "needles": ["Pi_M J_H = J_M_top + dB_zero", "wrong conserved object"],
            "source_role": "Hilbert/topological equality guard connected to B_zero",
        },
        {
            "row_id": "SRC2381_09_2379_doc",
            "source_key": "2379_doc",
            "source_path": POST_ROOT / "2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md",
            "needles": ["B_zero_flux=0 theorem derived", "positive same-frame M_H_ref exists"],
            "source_role": "current Bzero theorem gate failure and denominator gate",
        },
    ]
    rows: list[dict[str, object]] = []
    for source in sources:
        path = Path(source["source_path"])
        needles = list(source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": source["row_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": str(path.exists()).lower(),
                "required": "true",
                "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                "needles": "; ".join(needles),
                "source_role": source["source_role"],
                "valid_for_claim": no_claim(),
            }
        )
    return rows


def classification_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BTC2381_0_exact_improvement",
            "class": "exact_improvement",
            "candidate_form": "B = d mu or boundary momentum B_X = d_S b_X with closed weight",
            "classification": "CONDITIONAL_ZERO_CLASS",
            "current_evidence": "2380 proves k_tau invariance for exact mu; 1019/1020 give weighted-Stokes clauses",
            "missing_certificate": "explicit parent primitive mu/b_X, fixed tau, fixed surface, closed kernel/weight, no corner, no harmonic part",
            "residual_if_missing": "Delta_exact_commutator or edge residual source pack",
            "claim_effect": "component can be zero only after actual term classification",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BTC2381_1_corner",
            "class": "corner_codimension_two",
            "candidate_form": "corner charge Q_C or codimension-two contribution to Q_tau/theta",
            "classification": "LIVE_REMAINDER",
            "current_evidence": "1020 requires no active corner boundary or explicit Q_C",
            "missing_certificate": "corner-free surface or included corner charge with fixed convention",
            "residual_if_missing": "epsilon_corner_abs",
            "claim_effect": "blocks Bzero zero theorem",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BTC2381_2_topological_nonexact",
            "class": "topological_or_nonexact",
            "candidate_form": "closed but non-exact h_X, harmonic edge mode, or fixed cohomology class",
            "classification": "LIVE_REMAINDER",
            "current_evidence": "1020 decomposes B_X = d_S b_X + h_X + r_X",
            "missing_certificate": "h_X=0, projected silent, or separately source-bounded in same boundary class",
            "residual_if_missing": "epsilon_top_abs",
            "claim_effect": "exactness cannot erase harmonic/topological charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BTC2381_3_field_dependent_tau_surface",
            "class": "field_dependent_tau_or_surface",
            "candidate_form": "[delta,i_tau]mu, delta S_outer, moving readout surface, radial profile",
            "classification": "LIVE_REMAINDER",
            "current_evidence": "2380 cancellation needs fixed tau and fixed surface",
            "missing_certificate": "delta tau=0, delta S_outer=0, same-frame surface lock before variation",
            "residual_if_missing": "epsilon_delta_tau_abs",
            "claim_effect": "exact-improvement cancellation no longer follows",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BTC2381_4_fixed_reference",
            "class": "unfixed_reference_counterterm",
            "candidate_form": "H_ref or B_ref chosen/shifted after source/readout",
            "classification": "PRIMARY_LIVE_REMAINDER",
            "current_evidence": "1771 and 2379 keep fixed-before-readout reference missing; 2380 says exact improvements cannot be fitted knobs",
            "missing_certificate": "source-independent H_ref/B_ref selector fixed before readout and shared boundary class",
            "residual_if_missing": "Delta_ref_over_MH",
            "claim_effect": "can fake charge closure if not fixed, so it is the selected next attack",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BTC2381_5_nonintegrable_flux",
            "class": "nonintegrable_flux",
            "candidate_form": "field-space curl of delta Q_tau - i_tau theta or flux through open annulus",
            "classification": "LIVE_REMAINDER",
            "current_evidence": "2339/2340/2379 keep H_tau integrability missing",
            "missing_certificate": "closed one-form on field space after exact/corner/reference split",
            "residual_if_missing": "Delta_H_res_over_MH",
            "claim_effect": "H_tau and M_H_ref remain placeholder if nonintegrable",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BTC2381_6_Hilbert_topological_equality",
            "class": "source_measure_equality_remainder",
            "candidate_form": "Pi_M J_H - J_M_top - dB_zero",
            "classification": "PARALLEL_ROOT_REMAINDER",
            "current_evidence": "1772 warns a closed topological current can be the wrong conserved object",
            "missing_certificate": "Pi_M J_H = J_M_top + dB_zero with silent/included Bzero and same M_H_ref",
            "residual_if_missing": "R_eq_integral and I_commutator remain",
            "claim_effect": "Newton/GR source normalization cannot be claimed from boundary zero alone",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BTC2381_7_total",
            "class": "Bzero_remainder_total",
            "candidate_form": "B_rem = B_corner + B_top + B_delta_tau + B_ref + B_nonintegrable + B_source_measure",
            "classification": "REDUCED_BUT_NOT_CLOSED",
            "current_evidence": "2380 plus 1019/1020/1772",
            "missing_certificate": "all live classes zeroed or finite source-bounded with positive same-frame M_H_ref",
            "residual_if_missing": "epsilon_Brem_abs",
            "claim_effect": "Bzero is now structured but still nonclaim",
            "valid_for_claim": no_claim(),
        },
    ]


def certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BCC2381_0_parent_primitive",
            "certificate": "explicit exact primitive",
            "needed_for": "exact_improvement zero",
            "current_status": "MISSING_PARENT_PRIMITIVE",
            "test": "write mu or b_X from parent L/theta/Q, not by posterior fitting",
            "blocks": "BTC2381_0_exact_improvement",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BCC2381_1_surface",
            "certificate": "corner-free compact linked surface",
            "needed_for": "Stokes/no-corner zero",
            "current_status": "MISSING_CORNER_CERTIFICATE",
            "test": "partial S=0 or all corners included with Q_C",
            "blocks": "BTC2381_1_corner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BCC2381_2_cohomology",
            "certificate": "relative cohomology/harmonic silence",
            "needed_for": "topological/non-exact zero",
            "current_status": "MISSING_COHOMOLOGY_CERTIFICATE",
            "test": "h_X=0 or h_X sourced as finite residual in same boundary class",
            "blocks": "BTC2381_2_topological_nonexact",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BCC2381_3_tau_surface_lock",
            "certificate": "fixed tau and fixed S_outer",
            "needed_for": "2380 k_tau cancellation",
            "current_status": "MISSING_TAU_SURFACE_LOCK",
            "test": "delta tau=0, delta S_outer=0, no readout-induced surface retuning",
            "blocks": "BTC2381_3_field_dependent_tau_surface",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BCC2381_4_fixed_reference",
            "certificate": "fixed H_ref/B_ref selector",
            "needed_for": "no cancellation knob and same boundary class",
            "current_status": "MISSING_FIXED_REFERENCE_SELECTOR",
            "test": "H_ref/B_ref fixed before source/readout and independent of residual sign/magnitude",
            "blocks": "BTC2381_4_fixed_reference",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BCC2381_5_integrability",
            "certificate": "closed Hamiltonian one-form",
            "needed_for": "H_tau and M_H_ref",
            "current_status": "MISSING_HTAU_INTEGRABILITY",
            "test": "delta(k_tau)=0 on reduced branch, or finite Delta_H_res row",
            "blocks": "BTC2381_5_nonintegrable_flux",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BCC2381_6_source_measure",
            "certificate": "Hilbert/topological source equality",
            "needed_for": "Newton/GR source normalization",
            "current_status": "MISSING_SOURCE_MEASURE_EQUALITY",
            "test": "Pi_M J_H = J_M_top + dB_zero and same charge gives Poisson/Gauss source before orbital GM",
            "blocks": "BTC2381_6_Hilbert_topological_equality",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BCC2381_7_MHref",
            "certificate": "positive same-frame M_H_ref",
            "needed_for": "normalized residual scoring",
            "current_status": "MISSING_POSITIVE_MHREF",
            "test": "finite positive H_tau[S_outer]-H_ref with source/equation path and no orbital-GM import",
            "blocks": "all normalized rows",
            "valid_for_claim": no_claim(),
        },
    ]


def bound_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRB2381_0_epsilon_Brem",
            "quantity": "epsilon_Brem_abs",
            "formula": "(abs(B_corner)+abs(B_top)+abs(B_delta_tau)+abs(Delta_ref)+abs(Delta_H_res)+abs(R_eq_component))/M_H_ref",
            "units": "dimensionless after same-frame M_H_ref normalization",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "required_inputs": "component numerators; units; source paths; fixed H_ref; positive M_H_ref; no-cancellation guard",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRB2381_1_exact_switch",
            "quantity": "B_exact_improvement_zero_switch",
            "formula": "true iff B=B_exact, tau/S fixed, no corner, no harmonic/topological class, closed weight",
            "units": "boolean theorem switch",
            "status": "SWITCH_BLOCKED_PENDING_TERM_CLASSIFICATION",
            "required_inputs": "explicit parent primitive and boundary class certificates",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRB2381_2_Delta_ref",
            "quantity": "Delta_ref_over_MH",
            "formula": "abs(H_ref_shift_or_unfixed_counterterm)/M_H_ref",
            "units": "dimensionless after same-frame M_H_ref normalization",
            "status": "PRIMARY_NEXT_BOUND_IF_SELECTOR_FAILS",
            "required_inputs": "H_ref selector or finite reference-shift numerator, M_H_ref, no-cancellation guard",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2381_0_classification_result",
            "decision": "classify Bzero into exact, corner, topological, tau/surface, reference, nonintegrable and source-measure pieces",
            "reason": "2380 makes exact improvements algebraically silent, but 1019/1020/1772 show exactness is not enough without domain/cohomology/reference/source equality",
            "consequence": "the boundary blocker is structured into certificates and residual rows",
            "status": "CLASSIFICATION_BUILT_NONCLAIM",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2381_1_primary_next",
            "decision": "attack fixed boundary class and H_ref selector next",
            "reason": "unfixed reference can fake charge closure and is repeatedly listed as the practical boundary hazard",
            "consequence": "2382 should derive a pre-readout H_ref/B_ref selector or stage Delta_ref_over_MH",
            "status": "SELECT_2382_FIXED_REFERENCE",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2381_2_no_claim",
            "decision": "do not claim Bzero/local GR/Newton",
            "reason": "all certificate classes except the abstract exact-improvement algebra are still unsigned or missing values",
            "consequence": "private derivation route continues; no GitHub update",
            "status": "GLOBAL_CLAIMS_BLOCKED",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2381_0_term_classification",
            "gate": "all actual MTS boundary/reference terms classified",
            "gate_status": "FAIL_PARTIAL_CLASSIFICATION_ONLY",
            "claim_effect": "cannot set Bzero=0 globally",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2381_1_exact_component",
            "gate": "exact-improvement component zero",
            "gate_status": "PASS_CONDITIONAL_COMPONENT_ONLY",
            "claim_effect": "usable after explicit parent primitive and domain certificates",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2381_2_fixed_reference",
            "gate": "fixed H_ref/B_ref selector",
            "gate_status": "FAIL",
            "claim_effect": "Delta_ref remains selected blocker",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2381_3_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "epsilon_Brem_abs cannot be scored",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2381_4_local_GR_Newton",
            "gate": "local GR/Newton recovery",
            "gate_status": "FAIL_NONCLAIM",
            "claim_effect": "boundary and source-measure bridges remain open",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2381_0_Stokes_overclaim",
            "claim": "exact/Stokes route kills every boundary term",
            "allowed": "false",
            "reason": "corner, harmonic/topological, non-owned residual, moving surface and fixed-reference conditions remain",
            "blocking_rows": "BTC2381_1_corner;BTC2381_2_topological_nonexact;BTC2381_3_field_dependent_tau_surface;BTC2381_4_fixed_reference",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2381_1_reference_fit",
            "claim": "choose B_ref/H_ref after readout to cancel B_rem",
            "allowed": "false",
            "reason": "reference must be selected before source/readout or it becomes a fitted cancellation knob",
            "blocking_rows": "BCC2381_4_fixed_reference;CG2381_2_fixed_reference",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2381_2_closed_wrong_object",
            "claim": "closed topological charge is enough for measured GM/Newton",
            "allowed": "false",
            "reason": "1772 shows the topological current can be the wrong conserved object without Hilbert/source equality",
            "blocking_rows": "BTC2381_6_Hilbert_topological_equality;BCC2381_6_source_measure",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2381_3_public_checkpoint",
            "claim": "publish this as a local GR/Newton pass",
            "allowed": "false",
            "reason": "classification is progress, not closure; values and certificates are missing",
            "blocking_rows": "CG2381_0_term_classification;CG2381_3_MHref;CG2381_4_local_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2381_0_selected",
            "next_file": "2382-Y5-R2FR-fixed-boundary-class-and-Href-selector-or-Delta-ref-row.md",
            "success_condition": "derive a source-independent boundary class plus H_ref/B_ref selector fixed before source/readout and compatible with exact-improvement cancellation",
            "fallback_condition": "stage Delta_ref_over_MH with source path, units, no-cancellation guard and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2381_1_parallel",
            "next_file": "2382b-Y5-R2FR-parent-primitive-mu-or-boundary-residual-source-pack.md",
            "success_condition": "write the explicit parent primitive mu/b_X for actual MTS boundary terms",
            "fallback_condition": "retain exact switch blocked and source-pack every unowned boundary term",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2381_2_parallel",
            "next_file": "2382c-Y5-R2FR-Hilbert-topological-source-equality-or-Req-bound.md",
            "success_condition": "prove Pi_M J_H = J_M_top + dB_zero in the same boundary class",
            "fallback_condition": "retain R_eq_integral and I_commutator bound rows",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2381_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2381_BOUNDARY_TERM_CLASSIFICATION.csv": classification_rows,
    "P8_Y5_PARENT_QLOC_2381_BOUNDARY_CERTIFICATE_MATRIX.csv": certificate_rows,
    "P8_Y5_PARENT_QLOC_2381_BREM_BOUND_ROWS.csv": bound_rows,
    "P8_Y5_PARENT_QLOC_2381_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2381_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2381_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2381_NEXT_TARGET.csv": next_target_rows,
}


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            continue
        for row in read_csv(path):
            if str(row.get("valid_for_claim", "")).strip().lower() == "true":
                return False
    return True


def validation_rows() -> list[dict[str, object]]:
    csv_paths = [RESIDUALS / name for name in CSV_BUILDERS]
    rows: list[dict[str, object]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": no_claim(),
            }
        )

    sources = source_register()
    add("VAL2381_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2381_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    classes = classification_rows()
    class_names = {row["class"] for row in classes}
    add(
        "VAL2381_02_all_remainder_classes",
        {"exact_improvement", "corner_codimension_two", "topological_or_nonexact", "field_dependent_tau_or_surface", "unfixed_reference_counterterm", "nonintegrable_flux", "source_measure_equality_remainder"}.issubset(class_names),
        "boundary classes cover exact/corner/topological/tau/reference/flux/source-measure",
    )
    add(
        "VAL2381_03_reference_selected",
        any(row["row_id"] == "BTC2381_4_fixed_reference" and row["classification"] == "PRIMARY_LIVE_REMAINDER" for row in classes),
        "fixed reference selected as primary live remainder",
    )
    certificates = certificate_rows()
    add(
        "VAL2381_04_certificates_blocked",
        all("MISSING" in row["current_status"] for row in certificates),
        "all required certificates remain explicit missing gates",
    )
    bounds = bound_rows()
    add(
        "VAL2381_05_bound_rows_nonready",
        all(row["score_ready"] == "false" for row in bounds),
        "Brem/Delta_ref bound rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2381_06_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2381_1_exact_component"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2381_07_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths if path.exists()),
        "generated CSVs parse and have rows",
    )
    add("VAL2381_08_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2381_09_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2381_10_next_selected",
        any(row["row_id"] == "NEXT2381_0_selected" for row in next_target_rows()),
        "fixed boundary class/H_ref selector selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2381_OVERALL",
        overall,
        "2381 classifies the Bzero remainder, keeps exact-improvement zero conditional, selects fixed-reference/Href selector next, and blocks all public/local claims",
    )
    return rows


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2381_SOURCE_REGISTER.csv")
    classes = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2381_BOUNDARY_TERM_CLASSIFICATION.csv")
    certificates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2381_BOUNDARY_CERTIFICATE_MATRIX.csv")
    bounds = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2381_BREM_BOUND_ROWS.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2381_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2381_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2381_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2381_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2381_VALIDATION.csv")

    body = f"""# 2381 - boundary term classification exact vs corner/reference

## Result

2381 classifies the boundary problem exposed by 2379 and partially reduced by 2380.

The exact-improvement component is the good news: if an actual MTS boundary term is `d mu`/`d_S b_X`, with fixed `tau`,
fixed surface, no corner, no harmonic/topological part, and closed weight, it is conditionally silent in the Hamiltonian
variation.  That is the cleanest derived route so far for one chunk of `B_zero_flux`.

The bad-but-useful news is that the actual boundary remainder is not empty yet.  It splits into corner, topological or
non-exact, field-dependent tau/surface, unfixed reference, nonintegrable flux, and Hilbert/topological source-equality
pieces.  The selected next attack is therefore the fixed boundary class plus `H_ref/B_ref` selector, because an unfixed
reference can fake charge closure.

No `B_zero_flux=0`, `M_H_ref`, Newton, local-GR, PPN, orbital, clock, R10, or GitHub/public claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Boundary Term Classification

{markdown_table(classes, ["row_id", "class", "candidate_form", "classification", "current_evidence", "missing_certificate", "residual_if_missing", "claim_effect", "valid_for_claim"])}

## Boundary Certificate Matrix

{markdown_table(certificates, ["row_id", "certificate", "needed_for", "current_status", "test", "blocks", "valid_for_claim"])}

## Brem Bound Rows

{markdown_table(bounds, ["row_id", "quantity", "formula", "units", "status", "required_inputs", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is the non-circling branch.  We did not just say "boundary term missing" again.  The boundary term now has bins,
switches, and residual names.  The exact part has a real mathematical cancellation route; the reference part is the
most dangerous unresolved piece because it can masquerade as a solved source charge if selected after readout.

So the next best strike is `2382`: derive a fixed pre-readout boundary/reference selector, or admit `Delta_ref_over_MH`
as the honest residual.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2381_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2381_VALIDATION.csv'}")


if __name__ == "__main__":
    main()

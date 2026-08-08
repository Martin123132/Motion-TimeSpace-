from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_PARENT_THETA_QTAU_FIXED_REFERENCE_OR_MHREF_FIRST_ROW_2380"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2380-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md"
SCRIPT_PATH = POST_ROOT / "scripts" / "Y5_R2FR_parent_theta_Qtau_fixed_reference_or_MHref_first_row_2380.py"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(POST_ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


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


def no_claim(value: object = False) -> str:
    if isinstance(value, str):
        return "false" if value.lower() not in {"true", "claim", "pass_claim"} else "false"
    return "false"


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "row_id": "SRC2380_00_2379_doc",
            "source_key": "2379_doc",
            "source_path": POST_ROOT / "2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md",
            "needles": [
                "Next target is parent theta/Qtau + fixed reference + `M_H_ref`",
                "B_zero_flux=0 theorem derived",
            ],
            "source_role": "current branch selected parent charge/fixed-reference/MHref as next blocker",
        },
        {
            "row_id": "SRC2380_01_2379_bzero_audit",
            "source_key": "2379_bzero_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_BZERO_NOFLUX_THEOREM_AUDIT.csv",
            "needles": ["MISSING_PARENT_THETA_QTAU", "MISSING_FIXED_REFERENCE", "MISSING_MHREF"],
            "source_role": "current Bzero theorem obstruction rows",
        },
        {
            "row_id": "SRC2380_02_2379_bzero_row",
            "source_key": "2379_bzero_row",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_BZERO_FIRST_BOUND_ROW.csv",
            "needles": ["epsilon_Bzero_abs", "SCHEMA_READY_VALUES_MISSING"],
            "source_role": "current nonclaim Bzero numerator/denominator row",
        },
        {
            "row_id": "SRC2380_03_2339_doc",
            "source_key": "2339_doc",
            "source_path": POST_ROOT / "2339-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md",
            "needles": ["M_H_ref first row", "MISSING_PARENT_THETA_QTAU"],
            "source_role": "older exact target attempt; prevents duplicate circling",
        },
        {
            "row_id": "SRC2380_04_2340_doc",
            "source_key": "2340_doc",
            "source_path": POST_ROOT / "2340-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md",
            "needles": ["EH-anchor parent charge extraction spine", "residual charge zero/source-measure next"],
            "source_role": "older parent charge extraction route; identifies EH-anchor residual route",
        },
        {
            "row_id": "SRC2380_05_2378_doc",
            "source_key": "2378_doc",
            "source_path": POST_ROOT / "2378-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md",
            "needles": ["Boundary/improvement flux is not solved by SRNG", "primary live blocker"],
            "source_role": "boundary/improvement flux status before 2379",
        },
        {
            "row_id": "SRC2380_06_2377_doc",
            "source_key": "2377_doc",
            "source_path": POST_ROOT / "2377-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md",
            "needles": ["private working observation clause", "proof debt"],
            "source_role": "private SRNG/OFC branch status used only as conditional background",
        },
        {
            "row_id": "SRC2380_07_2339_validation",
            "source_key": "2339_validation",
            "source_path": RESIDUALS / "P8_Y5_BRR545_2339_VALIDATION.csv",
            "needles": ["VAL2339_OVERALL", "PASS"],
            "source_role": "older same-target validation",
        },
        {
            "row_id": "SRC2380_08_2340_validation",
            "source_key": "2340_validation",
            "source_path": RESIDUALS / "P8_Y5_BRR545_2340_VALIDATION.csv",
            "needles": ["VAL2340_OVERALL", "PASS"],
            "source_role": "older parent extraction validation",
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


def exact_improvement_derivation_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "EIC2380_0_setup",
            "derivation_step": "exact boundary improvement setup",
            "statement": "Let L_prime = L + d mu for a boundary/improvement (n-1)-form mu.",
            "condition": "mu is a genuine exact improvement on the same field bundle and boundary class",
            "result": "only the theta and Q_tau representatives shift; equations of motion are unchanged",
            "remaining_obstruction": "non-exact, corner, topological, or readout-dependent pieces are not covered",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EIC2380_1_theta_shift",
            "derivation_step": "symplectic potential shift",
            "statement": "delta L_prime = E_A delta Phi^A + d(theta + delta mu), so theta_prime = theta + delta mu.",
            "condition": "single parent variation exists and delta acts on fields, not on the chosen generator tau",
            "result": "exact improvement contribution to theta is delta mu",
            "remaining_obstruction": "parent MTS theta still not globally extracted sector-by-sector",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EIC2380_2_charge_shift",
            "derivation_step": "Noether charge representative shift",
            "statement": "J_tau_prime = theta_prime(L_tau Phi) - i_tau L_prime = J_tau + d(i_tau mu), hence Q_tau_prime = Q_tau + i_tau mu up to exact/corner terms.",
            "condition": "tau is fixed, the Cartan identity is used in the same boundary class, and corner ambiguities are absent or separately retained",
            "result": "exact improvement contribution to Q_tau is i_tau mu",
            "remaining_obstruction": "field-dependent tau, corner terms, and global cohomology can create residuals",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EIC2380_3_k_invariance",
            "derivation_step": "Hamiltonian surface one-form cancellation",
            "statement": "k_tau_prime = delta Q_tau_prime - i_tau theta_prime = k_tau + delta(i_tau mu) - i_tau(delta mu) = k_tau when [delta,i_tau]=0.",
            "condition": "fixed tau, fixed surface embedding, no anomalous corner/codimension-two contribution",
            "result": "exact boundary improvements do not change delta H_tau",
            "remaining_obstruction": "if tau or the surface/readout is field-dependent, a commutator residual remains",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EIC2380_4_boundary_component",
            "derivation_step": "Bzero exact-improvement component",
            "statement": "B_zero_flux_exact := integral_S(delta(i_tau mu)-i_tau(delta mu)) = 0 under the fixed-tau exact-improvement clauses.",
            "condition": "every candidate Bzero term is classified as exact mu with no corner/topological/field-dependent remainder",
            "result": "the exact-improvement part of B_zero_flux is conditionally zero",
            "remaining_obstruction": "classification of actual MTS boundary/reference terms is still missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EIC2380_5_not_MHref",
            "derivation_step": "denominator caveat",
            "statement": "The cancellation law reduces a numerator channel only; it does not create H_tau, H_ref, M_H_ref, or the source-measure bridge.",
            "condition": "none",
            "result": "local GR/Newton remains blocked until M_H_ref and source equality are derived or bounded",
            "remaining_obstruction": "positive same-frame M_H_ref and Pi_M J_H = J_M_top + dB_zero",
            "valid_for_claim": no_claim(),
        },
    ]


def theta_qtau_gate_recheck_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQR2380_0_no_circle",
            "gate": "same target already attempted",
            "status_before_2380": "2339/2340 staged theta_Qtau_Htau_Href/MHref rows but did not promote",
            "new_2380_result": "do not repeat the first-row table; extract one exact boundary-improvement cancellation law",
            "claim_effect": "component reduction only, not global closure",
            "next_action": "classify actual boundary/reference terms into exact/corner/topological/field-dependent classes",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQR2380_1_parent_variation",
            "gate": "single parent current-chain variation",
            "status_before_2380": "MISSING_SINGLE_PARENT_VARIATION",
            "new_2380_result": "exact-improvement algebra is available once a parent variation and mu term are identified",
            "claim_effect": "not enough to own theta_MTS globally",
            "next_action": "sector certificates for EH anchor, matter/source, boundary/reference, extra/projector/glue",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQR2380_2_theta_Qtau",
            "gate": "theta_MTS and Q_tau^MTS extraction",
            "status_before_2380": "MISSING_PARENT_THETA_QTAU",
            "new_2380_result": "boundary exact-improvement shifts are algebraically controlled",
            "claim_effect": "Q_tau total remains unowned outside the exact-improvement component",
            "next_action": "write component ledger: Q_EH, Q_matter/source, Q_boundary_exact, Q_corner, Q_extra, Q_projector",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQR2380_3_fixed_reference",
            "gate": "fixed H_ref/counterterm before readout",
            "status_before_2380": "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "new_2380_result": "exact improvements cannot be used as post-hoc cancellation knobs in delta H",
            "claim_effect": "H_ref still must be fixed by a source-independent selector",
            "next_action": "derive or bound Delta_ref for unfixed/non-exact reference choices",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQR2380_4_integrability",
            "gate": "H_tau integrability",
            "status_before_2380": "MISSING_HTAU_INTEGRABILITY",
            "new_2380_result": "exact improvement does not spoil delta H_tau when [delta,i_tau]=0",
            "claim_effect": "other nonintegrable sector pieces still block H_tau",
            "next_action": "compute residual one-form Delta_H_res over sector matrix",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQR2380_5_MHref",
            "gate": "positive same-frame M_H_ref",
            "status_before_2380": "MISSING_POSITIVE_MHREF",
            "new_2380_result": "unchanged: denominator missing",
            "claim_effect": "Bzero/R_eq/I_commutator/PPN rows remain non-score-ready",
            "next_action": "fill H_tau-H_ref from parent charge or keep MHref row nonclaim",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQR2380_6_source_measure",
            "gate": "Hamiltonian charge equals measured source normalization",
            "status_before_2380": "MISSING_SOURCE_MEASURE_BRIDGE",
            "new_2380_result": "unchanged: exact boundary-improvement cancellation is not the Poisson/Gauss bridge",
            "claim_effect": "Newton/GR recovery cannot be claimed from a conserved charge alone",
            "next_action": "prove Pi_M J_H = J_M_top + dB_zero or retain R_eq",
            "valid_for_claim": no_claim(),
        },
    ]


def bzero_residual_reduction_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRR2380_0_exact_improvement",
            "component": "B_exact_improvement",
            "formula": "integral_S(delta(i_tau mu)-i_tau(delta mu))",
            "status": "CONDITIONAL_ZERO_DERIVED",
            "zero_condition": "mu exact; tau fixed; surface fixed; no corner anomaly; [delta,i_tau]=0",
            "residual_if_condition_fails": "Delta_exact_commutator",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRR2380_1_corner",
            "component": "B_corner",
            "formula": "corner/codimension-two contribution to Q_tau or theta",
            "status": "UNCLASSIFIED_RETAINS_BOUND_ROW",
            "zero_condition": "corner term absent or paired by fixed corner convention",
            "residual_if_condition_fails": "epsilon_corner_abs",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRR2380_2_topological",
            "component": "B_topological_or_nonexact",
            "formula": "closed-but-not-exact or topological boundary representative",
            "status": "UNCLASSIFIED_RETAINS_BOUND_ROW",
            "zero_condition": "cohomology class fixed and source-independent or projected silent",
            "residual_if_condition_fails": "epsilon_top_abs",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRR2380_3_field_dependent_tau",
            "component": "B_delta_tau",
            "formula": "delta(i_tau mu)-i_tau(delta mu) when delta tau != 0 or readout surface moves",
            "status": "UNCLASSIFIED_RETAINS_BOUND_ROW",
            "zero_condition": "tau and S_outer locked before variation",
            "residual_if_condition_fails": "epsilon_delta_tau_abs",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRR2380_4_reference",
            "component": "B_reference_unfixed",
            "formula": "H_ref shift or post-readout counterterm choice",
            "status": "MISSING_FIXED_REFERENCE",
            "zero_condition": "H_ref selector fixed before source/readout and independent of fitted residual",
            "residual_if_condition_fails": "Delta_ref_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRR2380_5_total",
            "component": "B_zero_flux_reduced",
            "formula": "B_zero_flux = B_exact_improvement_zero + B_corner + B_topological + B_delta_tau + B_reference + B_nonintegrable_flux",
            "status": "REDUCED_NOT_CLOSED",
            "zero_condition": "all non-exact/corner/tau/reference/flux pieces vanish or are bounded with M_H_ref",
            "residual_if_condition_fails": "epsilon_Bzero_abs remains non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


def mhref_update_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR2380_0_denominator",
            "quantity": "M_H_ref",
            "formula": "M_H_ref := H_tau[S_outer] - H_ref",
            "status": "STILL_MISSING_VALUES",
            "update_from_2380": "no denominator derived; exact-improvement cancellation only reduces a numerator component",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR2380_1_bzero_reduced_numerator",
            "quantity": "B_zero_flux_remainder",
            "formula": "B_rem := B_corner + B_topological + B_delta_tau + B_reference + B_nonintegrable_flux",
            "status": "REMAINDER_VECTOR_DEFINED",
            "update_from_2380": "exact-improvement piece removed from the hard numerator if classification succeeds",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR2380_2_claim_switch",
            "quantity": "epsilon_Bzero_abs",
            "formula": "abs(B_rem)/M_H_ref",
            "status": "NON_SCORE_READY",
            "update_from_2380": "requires classified B_rem and positive same-frame M_H_ref",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2380_0_derivation_gain",
            "decision": "keep exact-improvement cancellation law",
            "reason": "it is a real local algebraic result for theta/Q_tau shifts: exact boundary improvements cancel from delta H_tau under fixed tau",
            "consequence": "B_zero_flux is reduced to a remainder classification problem, not one undifferentiated mystery term",
            "status": "COMPONENT_DERIVATION_ACCEPTED_CONDITIONALLY",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2380_1_no_global_promotion",
            "decision": "do not claim B_zero_flux=0, M_H_ref, local GR or Newton recovery",
            "reason": "actual MTS boundary/reference terms are not yet classified and denominator/source-measure bridge is still missing",
            "consequence": "2379 Bzero row remains nonclaim but now has a sharper numerator decomposition",
            "status": "GLOBAL_CLAIMS_BLOCKED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2380_2_no_circling",
            "decision": "do not repeat 2339/2340 first-row staging as the next step",
            "reason": "older line already staged M_H_ref and parent charge rows; the new work must classify the boundary pieces or derive fixed reference",
            "consequence": "2381 selected as boundary term classification/fixed-reference selector, not another generic MHref audit",
            "status": "ANTI_CIRCLING_ROUTE_SELECTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2380_3_github_policy",
            "decision": "no GitHub update from 2380",
            "reason": "useful private derivation progress, but still no stable public claim",
            "consequence": "continue private goal until a clean derived/conditional/blocked checkpoint exists",
            "status": "NO_GITHUB",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2380_0_exact_improvement_component",
            "gate": "exact boundary improvement cancellation derived under fixed-tau assumptions",
            "gate_status": "PASS_CONDITIONAL_COMPONENT_ONLY",
            "claim_effect": "can remove exact-improvement numerator component only after term classification",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2380_1_boundary_classification",
            "gate": "all actual MTS boundary/reference terms classified as exact or residual",
            "gate_status": "FAIL_PENDING_CLASSIFICATION",
            "claim_effect": "B_zero_flux global zero not allowed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2380_2_fixed_reference",
            "gate": "fixed H_ref/counterterm selector before readout",
            "gate_status": "FAIL",
            "claim_effect": "Delta_ref remains live",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2380_3_MHref",
            "gate": "positive same-frame M_H_ref denominator",
            "gate_status": "FAIL",
            "claim_effect": "normalized local residuals remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2380_4_source_measure",
            "gate": "Hamiltonian charge equals measured source charge",
            "gate_status": "FAIL",
            "claim_effect": "Newton/GR source normalization bridge remains blocked",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2380_5_local_GR_Newton",
            "gate": "local GR/Newton recovery",
            "gate_status": "FAIL_NONCLAIM",
            "claim_effect": "private derivation progress only",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2380_0_exact_to_global",
            "claim": "declare B_zero_flux=0 because exact improvements cancel",
            "allowed": "false",
            "reason": "the actual MTS boundary/reference stack may include corner, topological, field-dependent tau, unfixed reference, or nonintegrable flux pieces",
            "blocking_rows": "BRR2380_1_corner;BRR2380_2_topological;BRR2380_3_field_dependent_tau;BRR2380_4_reference;CG2380_1_boundary_classification",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2380_1_MHref_from_orbit",
            "claim": "fill M_H_ref using observed orbital GM before deriving source-measure bridge",
            "allowed": "false",
            "reason": "this would borrow Newton to prove Newton/GR recovery",
            "blocking_rows": "TQR2380_5_MHref;TQR2380_6_source_measure;CG2380_4_source_measure",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2380_2_reference_cancellation",
            "claim": "choose H_ref after seeing B_zero_flux to cancel the residual",
            "allowed": "false",
            "reason": "fixed reference must be selected before source/readout and cannot be a fitted knob",
            "blocking_rows": "TQR2380_3_fixed_reference;CG2380_2_fixed_reference",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2380_3_public_claim",
            "claim": "publish 2380 as local GR/Newton evidence",
            "allowed": "false",
            "reason": "component derivation is promising but global denominator and source bridge remain absent",
            "blocking_rows": "CG2380_3_MHref;CG2380_4_source_measure;CG2380_5_local_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2380_0_selected",
            "next_file": "2381-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md",
            "success_condition": "classify every actual MTS boundary/reference/improvement term into exact-mu, corner, topological/non-exact, field-dependent-tau, unfixed-reference, or nonintegrable-flux classes",
            "fallback_condition": "retain a finite B_rem vector with one row per unclassified/non-exact component and keep epsilon_Bzero_abs nonclaim",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2380_1_parallel",
            "next_file": "2381b-Y5-R2FR-fixed-reference-selector-or-Delta-ref-row.md",
            "success_condition": "derive a source-independent H_ref/counterterm selector fixed before readout",
            "fallback_condition": "stage Delta_ref_over_MH as a nonclaim residual row",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2380_2_parallel",
            "next_file": "2381c-Y5-R2FR-Htau-integrability-one-form-or-DeltaH-row.md",
            "success_condition": "prove the reduced k_tau one-form is closed on the private branch after exact improvements cancel",
            "fallback_condition": "stage Delta_H_res/M_H_ref nonclaim component",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2380_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2380_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv": exact_improvement_derivation_rows,
    "P8_Y5_PARENT_QLOC_2380_THETA_QTAU_GATE_RECHECK.csv": theta_qtau_gate_recheck_rows,
    "P8_Y5_PARENT_QLOC_2380_BZERO_RESIDUAL_REDUCTION.csv": bzero_residual_reduction_rows,
    "P8_Y5_PARENT_QLOC_2380_MHREF_FIRST_ROW_UPDATE.csv": mhref_update_rows,
    "P8_Y5_PARENT_QLOC_2380_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2380_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2380_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2380_NEXT_TARGET.csv": next_target_rows,
}


def output_paths() -> list[Path]:
    return [RESIDUALS / name for name in CSV_BUILDERS] + [DOC_PATH]


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv" or not path.exists():
            continue
        for row in read_csv(path):
            value = row.get("valid_for_claim", "")
            if str(value).strip().lower() == "true":
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

    source_rows = source_register()
    add(
        "VAL2380_00_sources_exist",
        all(row["exists"] == "true" for row in source_rows),
        "all required source paths exist",
    )
    add(
        "VAL2380_01_needles_found",
        all(row["needles_found"] == "true" for row in source_rows),
        "all source needles found",
    )
    exact_rows = exact_improvement_derivation_rows()
    add(
        "VAL2380_02_exact_improvement_law_present",
        any(row["row_id"] == "EIC2380_3_k_invariance" for row in exact_rows)
        and any(row["row_id"] == "EIC2380_4_boundary_component" for row in exact_rows),
        "exact-improvement k_tau cancellation and boundary component rows present",
    )
    reduction_rows = bzero_residual_reduction_rows()
    add(
        "VAL2380_03_remainder_classes_present",
        {"B_corner", "B_topological_or_nonexact", "B_delta_tau", "B_reference_unfixed"}.issubset(
            {row["component"] for row in reduction_rows}
        ),
        "corner/topological/tau/reference remainders retained",
    )
    mhref_rows = mhref_update_rows()
    add(
        "VAL2380_04_MHref_not_promoted",
        all(row["score_ready"] == "false" for row in mhref_rows),
        "M_H_ref rows remain non-score-ready",
    )
    claim_rows = claim_gate_rows()
    add(
        "VAL2380_05_global_gates_blocked",
        all(
            row["gate_status"] != "PASS"
            for row in claim_rows
            if row["row_id"] != "CG2380_0_exact_improvement_component"
        ),
        "global Bzero/MHref/source/local-GR gates remain blocked",
    )
    next_rows = next_target_rows()
    add(
        "VAL2380_06_next_selected",
        any(row["row_id"] == "NEXT2380_0_selected" for row in next_rows),
        "boundary term classification selected next",
    )
    add(
        "VAL2380_07_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths if path.exists()),
        "generated CSVs parse and have rows",
    )
    add(
        "VAL2380_08_no_claim_flags",
        check_no_positive_claim_flags(csv_paths),
        "no generated row has valid_for_claim=true",
    )
    add(
        "VAL2380_09_formalization_untouched_by_script",
        all(FORMALIZATION_WORKBENCH not in path.parents for path in output_paths()),
        "script writes only post-checkpoint-work outputs",
    )

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2380_OVERALL",
        overall,
        "2380 derives the exact-improvement cancellation component, keeps global/local claims blocked, and selects boundary classification/fixed-reference next",
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
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_SOURCE_REGISTER.csv")
    exact_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv")
    recheck_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_THETA_QTAU_GATE_RECHECK.csv")
    reduction_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_BZERO_RESIDUAL_REDUCTION.csv")
    mhref_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_MHREF_FIRST_ROW_UPDATE.csv")
    decision = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2380_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2380_VALIDATION.csv")

    body = f"""# 2380 - parent theta/Qtau fixed-reference or M_H_ref first row

## Result

2380 is not another table-circle.  It reopens the 2379 parent theta/Qtau/fixed-reference/MHref target, checks the older
2339/2340 attempts, and extracts one real algebraic gain:

`L' = L + d mu`, `theta' = theta + delta mu`, `Q'_tau = Q_tau + i_tau mu`, so

`k'_tau = delta Q'_tau - i_tau theta' = k_tau + delta(i_tau mu) - i_tau(delta mu) = k_tau`

whenever `tau` and the integration surface are fixed and there are no corner/topological/anomalous pieces.  In plain
terms: exact boundary improvements do not change the Hamiltonian surface one-form.  That gives a conditional zero for
the exact-improvement part of `B_zero_flux`.

This does **not** derive `M_H_ref`, `H_ref`, full `theta_MTS`, full `Q_tau^MTS`, the source-measure bridge, or local
GR/Newton recovery.  The gain is narrower but real: `B_zero_flux` is now split into an exact piece that can cancel
algebraically and a remainder vector that must be classified or bounded.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Exact Improvement Cancellation Derivation

{markdown_table(exact_rows, ["row_id", "derivation_step", "statement", "condition", "result", "remaining_obstruction", "valid_for_claim"])}

## Theta/Qtau Gate Recheck

{markdown_table(recheck_rows, ["row_id", "gate", "status_before_2380", "new_2380_result", "claim_effect", "next_action", "valid_for_claim"])}

## Bzero Residual Reduction

{markdown_table(reduction_rows, ["row_id", "component", "formula", "status", "zero_condition", "residual_if_condition_fails", "valid_for_claim"])}

## M_H_ref First Row Update

{markdown_table(mhref_rows, ["row_id", "quantity", "formula", "status", "update_from_2380", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is a genuine small derivation win.  We are not smuggling GR in; we used the standard current-chain algebra that any
acceptable parent action must satisfy.  The exact-improvement part of the boundary problem can disappear by algebra,
but only after the actual MTS boundary/reference terms are classified as exact improvements with fixed `tau`.  If they
are corners, topological terms, field-dependent readout/surface terms, or unfixed references, they stay as residuals.

The project is therefore slightly less grim than 2379: the boundary blocker has structure now.  But it is not solved.
The next useful shot is to classify the actual boundary/reference terms, not to stage another generic `M_H_ref` row.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2380_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2380_VALIDATION.csv'}")


if __name__ == "__main__":
    main()

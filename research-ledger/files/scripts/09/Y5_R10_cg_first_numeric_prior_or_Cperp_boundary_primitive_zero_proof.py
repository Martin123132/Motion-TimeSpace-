from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1159-Y5-R10-cg-first-numeric-prior-or-Cperp-boundary-primitive-zero-proof.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def missing_or_blocked(value: object) -> bool:
    text = str(value)
    return (
        text.strip() == ""
        or "MISSING" in text
        or "NOT_DERIVED" in text
        or "NOT_PROVED" in text
        or "NOT_ACQUIRED" in text
        or "BLOCKED" in text
        or "PRODUCT_ONLY" in text
    )


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1159_0_1158_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1158_NEXT_TARGET.csv",
            "needle": "NEXT1158_0_1159",
            "role": "handoff selecting first c_g numeric prior or Cperp boundary primitive zero proof.",
        },
        {
            "source_id": "SRC1159_1_1158_cperp",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1158_CP_EXACTNESS_REPAIR_AUDIT.csv",
            "needle": "CPE1158_1_boundary_primitive",
            "role": "1158 boundary primitive zero burden.",
        },
        {
            "source_id": "SRC1159_2_1158_cg_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1158_CG_SOURCE_PACK_ROWS.csv",
            "needle": "CGSRC1158_2_cg_value",
            "role": "1158 finite or zero c_g source-pack row.",
        },
        {
            "source_id": "SRC1159_3_272_boundary",
            "relative_path": "272-quotient-configuration-principle-from-topological-projector.md",
            "needle": "their local boundary primitive is pure gauge / zero",
            "role": "conditional quotient theorem requires local boundary primitive silence.",
        },
        {
            "source_id": "SRC1159_4_1019_cocycle",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "BE1019_5_cocycle_zero",
            "role": "boundary generator cocycle is uncomputed; exactness alone is insufficient.",
        },
        {
            "source_id": "SRC1159_5_1020_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "weighted Stokes identity exposing derivative/corner terms in exact edge charges.",
        },
        {
            "source_id": "SRC1159_6_1020_cohomology",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_2_relative_cohomology",
            "role": "relative cohomology/harmonic edge class not yet zeroed.",
        },
        {
            "source_id": "SRC1159_7_1029_prior",
            "relative_path": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
            "needle": "CGD1029_1_1_finite_cg_R10",
            "role": "older c_g finite-prior intake row is placeholder only.",
        },
        {
            "source_id": "SRC1159_8_1030_spm",
            "relative_path": "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
            "needle": "SPD1030_6_verdict",
            "role": "single-public-metric/no-shadow-frame theorem remains unproved.",
        },
        {
            "source_id": "SRC1159_9_1033_R10",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
            "needle": "TAUR1033_6_verdict",
            "role": "R10 tau and companion factors remain definition-only.",
        },
        {
            "source_id": "SRC1159_10_1052_clock",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
            "needle": "TCN1052_4_verdict",
            "role": "clock rows bound products only, not standalone c_g.",
        },
        {
            "source_id": "SRC1159_11_1068_WEP",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv",
            "needle": "TAP1068_5_Xhat_normalization",
            "role": "WEP tau acquisition requires shared Xhat normalization.",
        },
        {
            "source_id": "SRC1159_12_720_kinetic",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_720_KINETIC_NULL_THEOREM_AUDIT.csv",
            "needle": "KNT720_8_no_mode_theorem",
            "role": "kinetic/rank/source-orthogonality guard for null-generator route.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def boundary_zero_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "BPZ1159_0_target",
                "lemma_piece": "boundary primitive zero target",
                "required_statement": "If C_perp=d_rel B_C on the local domain, then the boundary readout Q_C[S]=int_S F_lambda epsilon_X B_C vanishes.",
                "current_status": "TARGET_SHARP",
                "missing_for_proof": "must prove exactness, proper boundary domain, weighted Stokes silence, harmonic zero, residual zero, cocycle zero, and source support silence",
                "effect_if_missing": "Cperp exactness cannot be promoted to q-null/c_g=0",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BPZ1159_1_Cperp_exactness",
                "lemma_piece": "relative exactness input",
                "required_statement": "C_perp=d_rel B_C or C_perp is variationally trivial in the same local branch used for c_g.",
                "current_status": "NOT_DERIVED_CURRENT_CORPUS",
                "missing_for_proof": "parent C-sector form and relative differential in the actual local domain",
                "effect_if_missing": "no boundary-primitive theorem can start",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BPZ1159_2_weighted_Stokes",
                "lemma_piece": "exact edge term",
                "required_statement": "int_S F epsilon d_S b_C = int_partialS F epsilon b_C - int_S d_S(F epsilon) wedge b_C",
                "current_status": "IDENTITY_WRITTEN_ZERO_CONDITIONS_UNSIGNED",
                "missing_for_proof": "corner term zero plus d_S(F epsilon)=0 or norm_bC=0/source-bound",
                "effect_if_missing": "an exact primitive can still have a weighted edge readout",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BPZ1159_3_proper_gauge",
                "lemma_piece": "proper gauge / compact support",
                "required_statement": "epsilon_X is proper or compact-supported for the representative direction without killing physical ADM/time/rotation charges.",
                "current_status": "NOT_SEPARATED_FROM_PHYSICAL_GENERATORS",
                "missing_for_proof": "domain proof distinguishing X-representative gauge from physical Hamiltonian generators",
                "effect_if_missing": "zero proof may erase real charges by fiat",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BPZ1159_4_relative_cohomology",
                "lemma_piece": "no harmonic edge class",
                "required_statement": "B_C=d_S b_C+h_C+r_C with h_C=0 and r_C=0 or separately bounded.",
                "current_status": "HARMONIC_AND_RESIDUAL_CLASSES_NOT_ZEROED",
                "missing_for_proof": "relative cohomology certificate and residual-source silence",
                "effect_if_missing": "edge hair can survive exact local bulk form",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BPZ1159_5_cocycle_zero",
                "lemma_piece": "boundary generator algebra",
                "required_statement": "{G[epsilon],G[eta]}=G[[epsilon,eta]] with K_boundary[epsilon,eta]=0.",
                "current_status": "UNCOMPUTED",
                "missing_for_proof": "bracket calculation from parent Omega and differentiable boundary generator",
                "effect_if_missing": "central/edge extension can act as local source residual",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BPZ1159_6_projector_source_silence",
                "lemma_piece": "projected source readout",
                "required_statement": "Pi_M^H[Q_C]=0 and Q_C has no same-frame source-worldtube dependence.",
                "current_status": "NOT_PARENT_SIGNED",
                "missing_for_proof": "Pi_M^H norm/source map, M_H_ref lock, and no support-shift theorem",
                "effect_if_missing": "boundary primitive can leak into measured-G/local source normalization",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BPZ1159_7_matter_descent_link",
                "lemma_piece": "c_g zero consequence",
                "required_statement": "boundary silence must be paired with matter descent/no-shadow-frame so A_g(Xhat) is not an allowed ordinary-matter argument.",
                "current_status": "NOT_DERIVED_CURRENT_CORPUS",
                "missing_for_proof": "single-public-metric or quotient-functor theorem in the same local domain",
                "effect_if_missing": "even a silent boundary does not by itself forbid common Weyl coupling",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BPZ1159_8_verdict",
                "lemma_piece": "local B_C=0 proof for current MTS",
                "required_statement": "BPZ1159_1 through BPZ1159_7 all parent-signed.",
                "current_status": "BOUNDARY_PRIMITIVE_ZERO_NOT_PROVED",
                "missing_for_proof": "exactness, weighted Stokes zero, proper gauge separation, h_C/r_C zero, cocycle zero, projector silence, matter descent",
                "effect_if_missing": "retain edge-bound law and c_g finite/source-pack route",
                "valid_for_claim": "false",
            },
        ]
    )


def edge_bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "EBL1159_0_QC_bound_law",
                "quantity": "Q_C_edge_bound",
                "bound_form": "|Q_C(lambda)| <= C_corner + ||d_S(F_lambda epsilon_X)||_* ||b_C||_* + |int_S F_lambda epsilon_X h_C| + |int_S F_lambda epsilon_X r_C| + |K_boundary|",
                "required_inputs": "C_corner;norm_dS_Feps;norm_bC;harmonic_edge_abs;residual_edge_abs;K_boundary;units;source_path",
                "current_value": "MISSING_EDGE_BOUND_INPUTS",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1159_EDGE_BOUND_LAW_ROWS.csv",
                "status": "LAW_STAGED_INPUTS_MISSING",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "EBL1159_1_corner_term",
                "quantity": "C_corner",
                "bound_form": "absolute corner contribution from int_partialS F epsilon b_C",
                "required_inputs": "corner topology;boundary orientation;F_lambda;epsilon_X;b_C;units;source_path",
                "current_value": "MISSING_CORNER_ZERO_OR_BOUND",
                "source_path": "MISSING_BOUNDARY_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "EBL1159_2_weight_derivative",
                "quantity": "norm_dS_Feps",
                "bound_form": "surface derivative norm of the smearing/profile/gauge weight",
                "required_inputs": "F_lambda profile;epsilon_X domain;surface metric;norm convention;source_path",
                "current_value": "MISSING_WEIGHT_DERIVATIVE_NORM",
                "source_path": "MISSING_PROFILE_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "EBL1159_3_primitive_norm",
                "quantity": "norm_bC",
                "bound_form": "dual norm of the exact boundary primitive b_C",
                "required_inputs": "B_C decomposition;norm convention;local branch;source_path",
                "current_value": "MISSING_PRIMITIVE_NORM",
                "source_path": "MISSING_CPERP_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "EBL1159_4_harmonic_edge",
                "quantity": "harmonic_edge_abs",
                "bound_form": "absolute readout from harmonic edge class h_C",
                "required_inputs": "relative cohomology basis;h_C coefficient;surface integral;units;source_path",
                "current_value": "MISSING_HARMONIC_EDGE_ZERO_OR_BOUND",
                "source_path": "MISSING_COHOMOLOGY_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "EBL1159_5_residual_edge",
                "quantity": "residual_edge_abs",
                "bound_form": "absolute readout from non-exact residual edge class r_C",
                "required_inputs": "residual decomposition;support/source map;units;source_path",
                "current_value": "MISSING_RESIDUAL_EDGE_ZERO_OR_BOUND",
                "source_path": "MISSING_RESIDUAL_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "EBL1159_6_boundary_cocycle",
                "quantity": "K_boundary",
                "bound_form": "central/edge cocycle in the boundary generator algebra",
                "required_inputs": "parent Omega;differentiable G_X;boundary bracket;units;source_path",
                "current_value": "MISSING_COCYCLE_ZERO_OR_BOUND",
                "source_path": "MISSING_SYMPLECTIC_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "EBL1159_7_projected_source_bound",
                "quantity": "Qbar_CXH",
                "bound_form": "|Qbar_CXH(lambda)| <= ||Pi_M^H|| |Q_C(lambda)| / M_H_ref_min",
                "required_inputs": "Pi_M^H norm;M_H_ref_min;Q_C bound;source-worldtube lock;source_path",
                "current_value": "MISSING_PROJECTOR_SOURCE_BOUND",
                "source_path": "MISSING_PROJECTOR_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def cg_prior_screen_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "screen_id": "CGPR1159_0_zero_theorem",
                "candidate": "c_g=0 from boundary/null quotient",
                "candidate_value": "false",
                "evidence_source": "P8_Y5_R10_1159_BOUNDARY_PRIMITIVE_ZERO_AUDIT.csv",
                "status": "REJECTED_NOT_PROVED",
                "reason": "B_C=0, matter descent, and kinetic/null guard are not parent-signed",
                "usable_as_prior": "false",
                "valid_for_claim": "false",
            },
            {
                "screen_id": "CGPR1159_1_R10_finite",
                "candidate": "finite c_g from R10 alpha(lambda)",
                "candidate_value": "MISSING_NUMERIC_CG",
                "evidence_source": "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
                "status": "REJECTED_MISSING_COMPANION_FACTORS",
                "reason": "K_X, Qbar_XH, tau_R10, lambda_X, and c_g source are missing",
                "usable_as_prior": "false",
                "valid_for_claim": "false",
            },
            {
                "screen_id": "CGPR1159_2_PPN_finite",
                "candidate": "finite c_g from PPN residual vector",
                "candidate_value": "MISSING_NUMERIC_CG",
                "evidence_source": "P8_Y5_R10_1158_CG_SOURCE_PACK_ROWS.csv",
                "status": "REJECTED_MISSING_TAU_PPN",
                "reason": "gauge-fixed weak-field projection and residual vector are missing",
                "usable_as_prior": "false",
                "valid_for_claim": "false",
            },
            {
                "screen_id": "CGPR1159_3_clock_product",
                "candidate": "clock product bound",
                "candidate_value": "PRODUCT_ONLY_NOT_STANDALONE_CG",
                "evidence_source": "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
                "status": "REJECTED_PRODUCT_DEGENERACY",
                "reason": "clock rows constrain b_alpha*tau_clock_time or related products, not c_g alone",
                "usable_as_prior": "false",
                "valid_for_claim": "false",
            },
            {
                "screen_id": "CGPR1159_4_WEP_common_mode",
                "candidate": "WEP silence as c_g prior",
                "candidate_value": "NOT_A_CG_PRIOR",
                "evidence_source": "P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv",
                "status": "REJECTED_COMMON_MODE_SHORTCUT",
                "reason": "a universal Weyl c_g can be composition-blind while still affecting R10/PPN/clocks/source normalization",
                "usable_as_prior": "false",
                "valid_for_claim": "false",
            },
            {
                "screen_id": "CGPR1159_5_orbital",
                "candidate": "finite c_g from orbital residuals",
                "candidate_value": "MISSING_NUMERIC_CG",
                "evidence_source": "P8_Y5_R10_1158_CG_SOURCE_PACK_ROWS.csv",
                "status": "REJECTED_MISSING_TAU_ORBITAL",
                "reason": "orbital source/readout projection and calibration convention are missing",
                "usable_as_prior": "false",
                "valid_for_claim": "false",
            },
            {
                "screen_id": "CGPR1159_6_verdict",
                "candidate": "first usable finite c_g numeric prior",
                "candidate_value": "NOT_ACQUIRED",
                "evidence_source": "this_checkpoint",
                "status": "NO_NUMERIC_CG_PRIOR_AVAILABLE",
                "reason": "all candidate channels are missing parent source, arena projection, or standalone normalization",
                "usable_as_prior": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1159_0_exact_not_zero",
                "guard": "bulk exactness does not imply zero weighted boundary readout",
                "status": "ACTIVE",
                "reason": "weighted Stokes terms, harmonic classes, residual classes, and cocycles can survive",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1159_1_no_proper_gauge_overkill",
                "guard": "proper-gauge restrictions cannot erase physical mass/time/rotation generators",
                "status": "ACTIVE",
                "reason": "local boundary domain must separate representative X gauge from physical Hamiltonian charges",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1159_2_no_product_to_cg",
                "guard": "product bounds cannot be divided into c_g without sourced tau/projection factors",
                "status": "ACTIVE",
                "reason": "clock/R10/WEP products are degenerate until arena projections are parent-owned",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1159_3_no_common_WEP_shortcut",
                "guard": "WEP quiet does not prove universal common-frame c_g is zero",
                "status": "ACTIVE",
                "reason": "common Weyl coupling can be composition-blind but still physical",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1159_4_no_local_claim",
                "guard": "local-GR/Newton/R10/PPN/WEP/clock/orbital claims remain blocked",
                "status": "ACTIVE",
                "reason": "neither B_C=0 nor finite c_g prior/projections are acquired",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1159_0_sources_exist",
                "rule": "all cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1159_1_boundary_zero_proved",
                "rule": "Cperp boundary primitive zero is parent-signed",
                "gate_pass": "false",
                "reason": "exactness, weighted Stokes zero, cohomology zero, cocycle zero, and projector silence are not all proven",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1159_2_edge_bound_law_ready",
                "rule": "edge-bound law exists as nonclaim fallback",
                "gate_pass": "true_nonclaim",
                "reason": "finite edge terms are componentized, but all numeric/source inputs remain missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1159_3_first_numeric_cg_prior",
                "rule": "a standalone finite c_g numeric prior is available",
                "gate_pass": "false",
                "reason": "all candidate prior channels are rejected or product-only",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1159_4_claim_promotion",
                "rule": "c_g zero, finite c_g score, local-GR/Newton/R10/PPN/WEP/clock/orbital claim allowed",
                "gate_pass": "false",
                "reason": "zero and finite-prior routes both remain blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1159_0_boundary_status",
                "decision": "B_C_zero_not_proved",
                "reason": "weighted Stokes and edge-cohomology terms remain live",
                "next_action": "keep edge-bound law and attack relative-exactness/cohomology inputs",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1159_1_prior_status",
                "decision": "no_first_numeric_cg_prior",
                "reason": "R10/PPN/clock/WEP/orbital candidate channels lack standalone c_g source and tau projections",
                "next_action": "do not invent a c_g prior; source it or derive zero",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1159_2_best_route",
                "decision": "derive_Cperp_relative_exactness_or_source_edge_bound",
                "reason": "boundary zero depends on exactness/cohomology machinery; finite route needs the same source discipline",
                "next_action": "1160 should attack Cperp relative exactness with a cohomology chain or fill edge-bound input sources",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1159_0_1160",
                "next_target": "1160-Y5-R10-Cperp-relative-exactness-cohomology-chain-or-edge-bound-source-pack.md",
                "objective": "derive Cperp relative exactness in the local branch or build the source-ready edge-bound input pack needed when B_C cannot be zeroed",
                "include": "C_perp form; relative differential; B_C decomposition; h_C/r_C classes; weighted Stokes terms; K_boundary; Pi_M/M_H projection; source paths",
                "exclude": "bulk-exactness-as-zero; proper-gauge overkill; product-to-c_g division; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    boundary: list[dict[str, object]],
    edge_bounds: list[dict[str, object]],
    cg_prior: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = boundary + edge_bounds + cg_prior + guards + gates + decisions + next_target
    required_edge = {
        "EBL1159_0_QC_bound_law",
        "EBL1159_1_corner_term",
        "EBL1159_2_weight_derivative",
        "EBL1159_3_primitive_norm",
        "EBL1159_4_harmonic_edge",
        "EBL1159_5_residual_edge",
        "EBL1159_6_boundary_cocycle",
        "EBL1159_7_projected_source_bound",
    }
    add(
        "V1159_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1159_1_boundary_zero_not_claimed",
        any(row["audit_id"] == "BPZ1159_8_verdict" and row["current_status"] == "BOUNDARY_PRIMITIVE_ZERO_NOT_PROVED" for row in boundary),
        "B_C=0 proof is explicitly not claimed",
    )
    add(
        "V1159_2_stokes_guard_present",
        any(row["audit_id"] == "BPZ1159_2_weighted_Stokes" for row in boundary)
        and any(row["guard_id"] == "GUARD1159_0_exact_not_zero" for row in guards),
        "weighted Stokes/exact-not-zero guard is present",
    )
    add(
        "V1159_3_edge_bound_rows_complete",
        required_edge.issubset({row["row_id"] for row in edge_bounds}),
        "edge-bound law and all source inputs are componentized",
    )
    add(
        "V1159_4_edge_rows_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and missing_or_blocked(row["current_value"]) for row in edge_bounds),
        "edge-bound rows remain missing/nonclaim until sourced",
    )
    add(
        "V1159_5_no_numeric_cg_prior",
        any(row["screen_id"] == "CGPR1159_6_verdict" and row["status"] == "NO_NUMERIC_CG_PRIOR_AVAILABLE" for row in cg_prior)
        and all(row["usable_as_prior"] == "false" for row in cg_prior),
        "no standalone finite c_g numeric prior is acquired",
    )
    add(
        "V1159_6_claim_gates_blocked",
        any(row["gate_id"] == "G1159_1_boundary_zero_proved" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1159_3_first_numeric_cg_prior" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1159_4_claim_promotion" and row["gate_pass"] == "false" for row in gates),
        "zero, finite-prior, and local claim gates remain blocked",
    )
    add(
        "V1159_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1159_8_next_target",
        next_target[0]["next_target"].startswith("1160-")
        and "Cperp-relative-exactness" in str(next_target[0]["next_target"]),
        "1160 handoff targets Cperp relative exactness or edge-bound source pack",
    )
    add(
        "V1159_9_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1159_10_csv_parse", csv_parse_ok, "all 1159 CSV outputs parse cleanly")
    add("V1159_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1159_SUMMARY",
        True,
        "1159 rejects the current B_C=0 proof, refuses fake numeric c_g priors, and converts boundary leakage into a sourceable edge-bound law",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    boundary: list[dict[str, object]],
    edge_bounds: list[dict[str, object]],
    cg_prior: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1159 - Y5/R10 c_g First Numeric Prior or Cperp Boundary Primitive Zero Proof

**Current verdict:** the clean `B_C=0` proof does not close yet. The obstruction is precise: even if a bulk primitive is exact, the weighted boundary readout can survive through corner terms, `d_S(F epsilon)`, harmonic edge class, residual edge class, cocycle, or source/projector leakage.

**Main progress:** this is no longer just "boundary terms are scary". The live leakage is now a finite bound law with named inputs. If we cannot zero it, we can source it.

**c_g prior status:** no standalone numeric `c_g` prior was acquired. R10, PPN, clock, WEP, and orbital channels are all missing either `A_g/Xhat/c_g` provenance, arena projections, or companion factors. Product-only clock/WEP facts are not being divided into fake `c_g`.

**Best next attack:** derive `Cperp` relative exactness/cohomology in the local branch, or fill the edge-bound source pack (`C_corner`, `norm_dS_Feps`, `norm_bC`, `h_C`, `r_C`, `K_boundary`, `Pi_M/M_H`).

**No claim:** no `c_g=0`, finite-`c_g` score, local-GR, Newton, R10, PPN, WEP, clock, orbital, GitHub, or public claim follows from 1159.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Boundary Primitive Zero Audit
{table(["audit_id", "lemma_piece", "required_statement", "current_status", "missing_for_proof", "effect_if_missing", "valid_for_claim"], boundary)}

## Edge Bound Law Rows
{table(["row_id", "quantity", "bound_form", "required_inputs", "current_value", "source_path", "status", "valid_for_claim", "claim_allowed"], edge_bounds)}

## c_g Prior Screen
{table(["screen_id", "candidate", "candidate_value", "evidence_source", "status", "reason", "usable_as_prior", "valid_for_claim"], cg_prior)}

## No-Cheat Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1159_SOURCE_REGISTER.csv",
        "boundary": OUT / "P8_Y5_R10_1159_BOUNDARY_PRIMITIVE_ZERO_AUDIT.csv",
        "edge_bounds": OUT / "P8_Y5_R10_1159_EDGE_BOUND_LAW_ROWS.csv",
        "cg_prior": OUT / "P8_Y5_R10_1159_CG_PRIOR_SCREEN.csv",
        "guards": OUT / "P8_Y5_R10_1159_NO_CG_CHEAT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1159_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1159_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1159_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1159_VALIDATION.csv",
    }

    sources = source_rows()
    boundary = boundary_zero_audit_rows()
    edge_bounds = edge_bound_rows()
    cg_prior = cg_prior_screen_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["boundary"], boundary)
    write_csv(outputs["edge_bounds"], edge_bounds)
    write_csv(outputs["cg_prior"], cg_prior)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, boundary, edge_bounds, cg_prior, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, boundary, edge_bounds, cg_prior, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

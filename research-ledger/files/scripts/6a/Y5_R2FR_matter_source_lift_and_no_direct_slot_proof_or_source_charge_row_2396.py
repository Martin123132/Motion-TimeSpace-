from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_MATTER_SOURCE_LIFT_AND_NO_DIRECT_SLOT_PROOF_OR_SOURCE_CHARGE_ROW_2396"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2396-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


SOURCES = [
    {
        "source_id": "SRC2396_2395_doc",
        "path": str(POST_ROOT / "2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md"),
        "needed_for": "2395 selected matter/source lift next",
        "needles": "NEXT2395_0_selected|matter/source lift|hidden source/coupling charge|VAL2395_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2396_2389_doc",
        "path": str(POST_ROOT / "2389-Y5-R2FR-parent-matter-action-current-density-or-JH-owner-leak-values.md"),
        "needed_for": "observed-frame matter action and Hilbert current grammar",
        "needles": "S_m[Phi,psi_m]|delta L_m = E_m delta psi_m|J_H[tau]|MCD2389_3_vertical_descent_zero",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2396_2389_certificate",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv"),
        "needed_for": "matter/source ownership blockers",
        "needles": "OCC2389_2_Lm_density|OCC2389_4_matter_lift|OCC2389_5_no_direct_slots|OCC2389_7_MHref",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2396_2389_leaks",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_JH_OWNER_LEAK_VALUES.csv"),
        "needed_for": "matter/source residual rows",
        "needles": "epsilon_hidden_source_slot|epsilon_marker_matter_lift|Delta_JH_owner_total_over_MH",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2396_1760_doc",
        "path": str(POST_ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md"),
        "needed_for": "matter/worldtube quotient descent theorem and A_matter interface",
        "needles": "MWD1760_1_conditional_theorem|CR1760_6_direct_vertex|PRE1760_4_no_shadow_prefactor|AM1760_8_A_matter",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2396_1771_sector_csv",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1771_SECTOR_ACTION_VARIATION_LEDGER.csv"),
        "needed_for": "nonminimal coupling sector warning",
        "needles": "SAV1771_3_nonminimal|S_nonmin = int sqrt(-g)|A(X)J_m|MUST_CLASSIFY_NOT_FORBIDDEN",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2396_2394_sector_csv",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2394_SECTOR_VARIATION_LEDGER.csv"),
        "needed_for": "matter/source sector in total Qv split",
        "needles": "SVL2394_1_matter_source|MISSING_MATTER_THETA_DESCENT|MISSING_SOURCE_CONSTRAINT_CHARGE_SPLIT",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2396_2390_certificate",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv"),
        "needed_for": "same-frame matter/readout requirements",
        "needles": "SFC2390_2_same_readout|SFC2390_4_no_shadow_frame|SFC2390_5_projector_support",
        "valid_for_claim": no_claim(),
    },
]


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSL2396_0_matter_action_grammar",
            "claim": "ordinary matter must be an observed-frame quotient functor",
            "statement": "Use S_matter=sum_A int L_A(e_obs(q(Phi)),psi_A,D_omega[e_obs(q)]psi_A;theta_A)+dB_A, with no independent residual/source/worldtube slot.",
            "derivation_status": "CONDITIONAL_GR_COMPATIBLE_GRAMMAR",
            "consequence": "matter sees the same geometry as GR and cannot source the vertical residual except through q",
            "missing_for_current_claim": "explicit parent L_m densities and q/Obs_e ownership remain unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSL2396_1_vertical_variation_decomposition",
            "claim": "vertical matter variation decomposes into named leak channels",
            "statement": "delta_v S_matter = G_e[v]+G_psi[v]+G_theta[v]+G_direct[v]+G_W[v]+G_B[v]+G_nonHilbert[v].",
            "derivation_status": "DECOMPOSITION_CONTRACT",
            "consequence": "no hidden matter-source term can disappear without being assigned to a channel",
            "missing_for_current_claim": "component values and common normalization are not supplied",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSL2396_2_geometry_chain_zero",
            "claim": "geometry part vanishes for pure vertical v",
            "statement": "If Dq(v)=0 and e_obs=Obs_e(q(Phi)), then G_e[v]=int T_a wedge delta_v e_obs^a=0; connection terms vanish when omega_obs is built from e_obs.",
            "derivation_status": "CONDITIONAL_CHAIN_RULE_PROOF",
            "consequence": "matter does not feel residual vertical motion through the metric/coframe channel",
            "missing_for_current_claim": "basic coframe, connection descent, and same-frame readout are unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSL2396_3_lift_and_constants_zero",
            "claim": "matter lift and constants carry no vertical marker",
            "statement": "If delta_v psi_A=0 up to owned gauge/local-Lorentz transformations, and delta_v theta_A=0 for representation constants/material standards, then G_psi[v]+G_theta[v]=0 modulo ordinary constraints.",
            "derivation_status": "CONDITIONAL_LIFT_PROOF",
            "consequence": "vertical residuals cannot hide as material labels, species standards, or changing constants",
            "missing_for_current_claim": "matter lift/no-marker and constant-superselection signatures remain unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSL2396_4_no_direct_slot_zero",
            "claim": "direct matter/source coupling is forbidden",
            "statement": "If the parent grammar forbids V_m[X,rho_A,W_source,C_top], A_A(X)L_A, A(X)J_H, species-frame factors, and source-only prefactors outside q/Obs_e, then G_direct[v]=0.",
            "derivation_status": "CONDITIONAL_NO_SLOT_THEOREM",
            "consequence": "this is the coupling choke point: without it, matter can reintroduce a fifth-force/source charge while looking GR-like",
            "missing_for_current_claim": "no-direct-slot/coupling grammar is not parent-derived",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSL2396_5_worldtube_support_zero",
            "claim": "source worldtube descends through Hilbert support",
            "statement": "If W_source=closure(supp J_H[tau]) with J_H and tau derived before readout from the same e_obs branch, then delta_v W_source=0 for regular compact sources.",
            "derivation_status": "CONDITIONAL_SUPPORT_PROOF",
            "consequence": "source support cannot be retuned to absorb residual fields",
            "missing_for_current_claim": "support regularity, tau ownership, projector descent, and tail bounds remain unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSL2396_6_Qv_matter_zero",
            "claim": "matter/source vertical Qv is constraint-only or zero",
            "statement": "When MSL2396_0 through MSL2396_5 hold and boundary terms are silent, Theta_matter(v)-mu_matter[v] contributes no physical vertical kernel charge, so Q_v^matter=0 up to ordinary constraints.",
            "derivation_status": "CONDITIONAL_MATTER_QV_ZERO",
            "consequence": "the matter/source door can close without fitting if the coupling grammar is signed",
            "missing_for_current_claim": "boundary, source support, no-direct-slot, and M_H_ref clauses are not signed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSL2396_7_verdict",
            "claim": "matter/source sector status",
            "statement": "2396 gives the exact sufficient theorem for matter/source invisibility, but current MTS does not pass because the no-direct coupling/source slot, matter lift, worldtube support, and M_H_ref remain unsigned.",
            "derivation_status": "CONDITIONAL_ROUTE_EXACT_NOT_PROMOTED",
            "consequence": "the next bottleneck is the parent coupling/no-direct-slot grammar, not more vague source language",
            "missing_for_current_claim": "OCC2389_4_matter_lift;OCC2389_5_no_direct_slots;SAV1771_3_nonminimal;OCC2389_7_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def certificate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSC2396_0_Lm_density",
            "certificate": "explicit observed-frame matter Lagrangian density",
            "required_test": "L_A(e_obs,psi_A,Dpsi_A;theta_A) is written and varied before readout",
            "status": "MISSING_EXPLICIT_LM_DENSITY",
            "residual_if_missing": "epsilon_JH_owner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSC2396_1_q_eobs_connection",
            "certificate": "q/e_obs/omega descent",
            "required_test": "e_obs and omega_obs are functors of q(Phi), so Dq(v)=0 kills geometry and connection variation",
            "status": "MISSING_Q_EOBS_CONNECTION_DESCENT",
            "residual_if_missing": "A_geom_matter",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSC2396_2_matter_lift",
            "certificate": "matter lift/no-marker proof",
            "required_test": "vertical v does not independently move psi_A, constants, species labels, material standards, or representation data",
            "status": "MISSING_MATTER_LIFT_NO_MARKER_PROOF",
            "residual_if_missing": "epsilon_marker_matter_lift",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSC2396_3_no_direct_slot",
            "certificate": "no direct residual matter/source coupling",
            "required_test": "forbid V_m[X,rho_A,W_source,C_top], A_A(X)L_A, A(X)J_H, source prefactors, and shadow species frames outside q/Obs_e",
            "status": "MISSING_NO_DIRECT_SLOT_GRAMMAR",
            "residual_if_missing": "epsilon_hidden_source_slot",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSC2396_4_worldtube_support",
            "certificate": "Hilbert worldtube support owner",
            "required_test": "W_source is closure(supp J_H[tau]) with compact/regular support, not an after-fit mask",
            "status": "MISSING_SUPPORT_OR_TAIL_THEOREM",
            "residual_if_missing": "epsilon_support_tail",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSC2396_5_boundary",
            "certificate": "matter/source boundary silence",
            "required_test": "matter boundary/worldtube exact terms are zero, proper, compact-support silent, or explicitly bounded",
            "status": "MISSING_MATTER_BOUNDARY_NOFLUX_OR_BOUND",
            "residual_if_missing": "A_boundary_matter",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSC2396_6_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "normalize source and charge rows by the same parent Hilbert/GR reference branch",
            "status": "MISSING_POSITIVE_MHREF",
            "residual_if_missing": "all normalized source rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MSC2396_7_matter_zero_ready",
            "certificate": "matter/source vertical zero theorem readiness",
            "required_test": "MSC2396_0 through MSC2396_6 pass together",
            "status": "CONDITIONAL_THEOREM_READY_BUT_UNSIGNED",
            "residual_if_missing": "epsilon_Qv_matter_source_retained",
            "valid_for_claim": no_claim(),
        },
    ]


def source_charge_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_matter_source",
            "definition": "matter/source contribution to vertical kernel charge",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "0 if MSC2396_0..MSC2396_6 pass; otherwise retained as source-charge row",
            "current_value_status": "CONDITIONAL_ZERO_UNSIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_hidden_source_slot",
            "definition": "direct residual coupling to matter/source/worldtube slot",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "abs(partial_X V_m[X,rho_A,W_source,C_top]|_{X=0})/M_H_ref",
            "current_value_status": "MISSING_NO_DIRECT_SLOT_PROOF",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_nonminimal_coupling_slot",
            "definition": "A_A(X)L_A, A(X)J_H, species-frame, or source-prefactor coupling leak",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "||delta_X S_nonmin||/M_H_ref",
            "current_value_status": "MISSING_COUPLING_GRAMMAR_OR_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_marker_matter_lift",
            "definition": "vertical movement of matter representation data, constants, species labels, or material standards",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "abs(delta_v psi_A contribution + delta_v theta_A contribution + marker terms)/M_H_ref",
            "current_value_status": "MISSING_MATTER_LIFT_NO_MARKER_PROOF",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_support_tail",
            "definition": "worldtube support/readout-tail contribution to source charge",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "||delta_v W_source or exterior Hilbert tail||/M_H_ref",
            "current_value_status": "MISSING_SUPPORT_OR_TAIL_THEOREM",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "Delta_matter_source_total_over_MH",
            "definition": "total unclosed matter/source vertical charge channel",
            "units": "dimensionless",
            "formula_or_bound": "epsilon_Qv_matter_source + epsilon_hidden_source_slot + epsilon_nonminimal_coupling_slot + epsilon_marker_matter_lift + epsilon_support_tail",
            "current_value_status": "COMPONENTS_MISSING",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2396_0_accept_conditional_matter_zero",
            "decision": "accept quotient-only observed-frame matter as the clean local-GR route",
            "reason": "if matter only sees e_obs(q) and fixed representation data, vertical residuals do not source ordinary matter",
            "consequence": "the matter problem becomes a parent grammar/coupling-signature problem",
            "status": "CONDITIONAL_MATTER_ZERO_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2396_1_coupling_is_root_bottleneck",
            "decision": "treat no-direct coupling/source slot as the next root bottleneck",
            "reason": "A(X)L_m, A(X)J_H, source-prefactors, or species frames would defeat the vertical zero while looking like ordinary matter",
            "consequence": "do not bury coupling inside generic matter prose",
            "status": "COUPLING_SLOT_HUNT_SELECTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2396_2_no_current_promotion",
            "decision": "do not claim matter/source pass for current MTS",
            "reason": "L_m, lift, no-direct-slot, support, boundary, and M_H_ref certificates are unsigned",
            "consequence": "epsilon_Qv_matter_source and coupling leak rows remain nonclaim",
            "status": "MATTER_ZERO_NOT_PROMOTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2396_3_next",
            "decision": "attack no-direct matter coupling grammar next",
            "reason": "this is the smallest decisive clause that can close or expose the coupling leak",
            "consequence": "2397 should forbid direct residual matter/source slots or convert them into sourced bound rows",
            "status": "SELECT_2397_NO_DIRECT_COUPLING_GRAMMAR",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2396_0_matter_source_zero",
            "gate": "matter/source vertical Qv zero",
            "gate_status": "CONDITIONAL_BLOCKED",
            "claim_effect": "the theorem is exact if clauses pass, but current MTS has not signed them",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2396_1_no_direct_coupling",
            "gate": "no direct residual matter/source coupling",
            "gate_status": "BLOCKED",
            "claim_effect": "coupling leak remains live",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2396_2_total_Qv",
            "gate": "total vertical Qv extracted",
            "gate_status": "BLOCKED",
            "claim_effect": "extra/projector/boundary/coupling sectors remain unclosed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2396_3_GR_Newton",
            "gate": "local GR/Newton reduction",
            "gate_status": "BLOCKED",
            "claim_effect": "matter/source zero is necessary but not sufficient",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2396_0_claim_matter_zero",
            "claim": "matter/source vertical charge vanishes for current MTS",
            "allowed": "false",
            "reason": "the proof requires unsigned L_m, q/e_obs, matter lift, no-direct-slot, support, boundary, and M_H_ref clauses",
            "blocking_rows": "MSC2396_0_Lm_density;MSC2396_2_matter_lift;MSC2396_3_no_direct_slot;MSC2396_4_worldtube_support;MSC2396_6_MHref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2396_1_claim_no_coupling_leak",
            "claim": "there is no hidden matter/source coupling leak",
            "allowed": "false",
            "reason": "S_nonmin, A(X)L_m, A(X)J_H, source prefactors, and species frames are not forbidden by a parent grammar yet",
            "blocking_rows": "MSC2396_3_no_direct_slot;epsilon_nonminimal_coupling_slot",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2396_2_claim_local_GR",
            "claim": "local GR/Newton is derived from 2396",
            "allowed": "false",
            "reason": "2396 only handles the matter/source sufficient theorem conditionally; total Qv, PPN, Newtonian limit, projector, boundary, and extra sectors remain",
            "blocking_rows": "CG2396_2_total_Qv;CG2396_3_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2396_0_selected",
            "next_file": "2397-Y5-R2FR-no-direct-matter-coupling-grammar-or-coupling-charge-row.md",
            "success_condition": "prove the parent action grammar forbids A(X)L_m, A(X)J_H, species-frame factors, source-prefactors, material markers, and V_m[X,rho_A,W_source]",
            "fallback_condition": "retain epsilon_nonminimal_coupling_slot and epsilon_hidden_source_slot as sourced nonclaim bound rows",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2396_1_parallel",
            "next_file": "2397b-Y5-R2FR-explicit-standard-matter-Lm-sidecar-and-variation-conventions.md",
            "success_condition": "write explicit dust/scalar/EM matter sidecar Lagrangians and variation conventions in the observed frame",
            "fallback_condition": "keep epsilon_JH_owner non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2396_2_later",
            "next_file": "2397c-Y5-R2FR-worldtube-support-tail-and-MHref-source-normalization.md",
            "success_condition": "derive W_source, support compactness/tails, tau, and positive M_H_ref from one parent branch",
            "fallback_condition": "retain epsilon_support_tail and all normalized source rows as non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2396_SOURCE_REGISTER.csv": lambda: SOURCES,
    "P8_Y5_PARENT_QLOC_2396_MATTER_SOURCE_LIFT_THEOREM.csv": theorem_rows,
    "P8_Y5_PARENT_QLOC_2396_MATTER_ZERO_CERTIFICATE.csv": certificate_rows,
    "P8_Y5_PARENT_QLOC_2396_SOURCE_CHARGE_ROWS.csv": source_charge_rows,
    "P8_Y5_PARENT_QLOC_2396_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2396_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2396_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2396_NEXT_TARGET.csv": next_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    missing_sources = [src["path"] for src in SOURCES if not Path(src["path"]).exists()]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_00_sources_exist",
            "status": "PASS" if not missing_sources else "FAIL",
            "detail": "all required source paths exist" if not missing_sources else ";".join(missing_sources),
            "valid_for_claim": no_claim(),
        }
    )

    missing_needles: list[str] = []
    for src in SOURCES:
        path = Path(src["path"])
        for needle in src["needles"].split("|"):
            if not contains(path, needle):
                missing_needles.append(f"{src['source_id']}::{needle}")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_01_needles_found",
            "status": "PASS" if not missing_needles else "FAIL",
            "detail": "all source needles found" if not missing_needles else ";".join(missing_needles),
            "valid_for_claim": no_claim(),
        }
    )

    theorem = theorem_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_02_action_grammar_present",
            "status": "PASS" if any("S_matter=sum_A" in row["statement"] and "e_obs(q(Phi))" in row["statement"] for row in theorem) else "FAIL",
            "detail": "observed-frame quotient matter action grammar is present",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_03_variation_decomposition_present",
            "status": "PASS" if any("G_direct" in row["statement"] and "G_nonHilbert" in row["statement"] for row in theorem) else "FAIL",
            "detail": "vertical matter variation is decomposed into leak channels",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_04_no_direct_coupling_guard_present",
            "status": "PASS" if any("A(X)J_H" in row["statement"] and "source-only prefactors" in row["statement"] for row in theorem) else "FAIL",
            "detail": "direct coupling/source-prefactor guard is present",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_05_matter_Qv_zero_present",
            "status": "PASS" if any("Q_v^matter=0" in row["statement"] for row in theorem) else "FAIL",
            "detail": "conditional matter/source Qv zero statement is present",
            "valid_for_claim": no_claim(),
        }
    )

    certificates = certificate_rows()
    required_statuses = {
        "MISSING_EXPLICIT_LM_DENSITY",
        "MISSING_Q_EOBS_CONNECTION_DESCENT",
        "MISSING_MATTER_LIFT_NO_MARKER_PROOF",
        "MISSING_NO_DIRECT_SLOT_GRAMMAR",
        "MISSING_SUPPORT_OR_TAIL_THEOREM",
        "MISSING_POSITIVE_MHREF",
    }
    present_statuses = {row["status"] for row in certificates}
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_06_required_gaps_explicit",
            "status": "PASS" if required_statuses <= present_statuses else "FAIL",
            "detail": "Lm, q/eobs, lift, no-direct-slot, support, and M_H_ref gaps explicit",
            "valid_for_claim": no_claim(),
        }
    )

    source_rows = source_charge_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_07_source_charge_rows_nonready",
            "status": "PASS" if all(row["valid_for_claim"] == "false" for row in source_rows) else "FAIL",
            "detail": "matter/source charge rows remain nonclaim/nonready",
            "valid_for_claim": no_claim(),
        }
    )

    gates = claim_gate_rows()
    gate_ok = all(row["gate_status"] in {"BLOCKED", "CONDITIONAL_BLOCKED"} for row in gates)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_08_global_claims_blocked",
            "status": "PASS" if gate_ok else "FAIL",
            "detail": "matter/source, coupling, total Qv, and GR/Newton gates not promoted",
            "valid_for_claim": no_claim(),
        }
    )

    csv_failures: list[str] = []
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            csv_failures.append(f"{name}:missing")
            continue
        try:
            parsed = csv_rows(path)
        except Exception as exc:
            csv_failures.append(f"{name}:{exc}")
            continue
        if not parsed:
            csv_failures.append(f"{name}:empty")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_09_csv_parse",
            "status": "PASS" if not csv_failures else "FAIL",
            "detail": "generated CSVs parse and have rows" if not csv_failures else ";".join(csv_failures),
            "valid_for_claim": no_claim(),
        }
    )

    true_claims: list[str] = []
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            continue
        for row in csv_rows(path):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                true_claims.append(f"{name}:{row}")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_10_no_claim_flags",
            "status": "PASS" if not true_claims else "FAIL",
            "detail": "no generated row has valid_for_claim=true" if not true_claims else ";".join(true_claims),
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_11_formalization_untouched_by_script",
            "status": "PASS",
            "detail": "script writes only post-checkpoint-work outputs",
            "valid_for_claim": no_claim(),
        }
    )

    next_selected = any(row["row_id"] == "NEXT2396_0_selected" for row in next_rows())
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_12_next_selected",
            "status": "PASS" if next_selected else "FAIL",
            "detail": "no-direct matter coupling grammar selected next",
            "valid_for_claim": no_claim(),
        }
    )

    overall_status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2396_OVERALL",
            "status": overall_status,
            "detail": "2396 states the exact matter/source vertical-zero theorem, isolates the no-direct coupling slot as root bottleneck, refuses promotion, and selects coupling grammar next",
            "valid_for_claim": no_claim(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    theorem = theorem_rows()
    certificates = certificate_rows()
    source_rows = source_charge_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()
    validation = validation_rows()

    body = f"""# 2396 — Matter Source Lift And No Direct Slot Proof Or Source Charge Row

## Result

2396 turns the matter/source problem into a clean sufficient theorem plus a sharp coupling obstruction.

The safe matter action shape is

`S_matter = sum_A int L_A(e_obs(q(Phi)), psi_A, D_omega[e_obs(q)] psi_A; theta_A) + dB_A`.

For a pure vertical `v in ker(Dq)`,

`delta_v S_matter = G_e[v] + G_psi[v] + G_theta[v] + G_direct[v] + G_W[v] + G_B[v] + G_nonHilbert[v]`.

If `e_obs` and `omega_obs` descend through `q`, matter fields and constants have a fixed lift, the worldtube is the
Hilbert support selected before readout, and the parent grammar forbids direct residual matter/source slots, then all
terms vanish or reduce to ordinary constraints.  In that case

`Theta_matter(v)-mu_matter[v]` carries no physical vertical kernel charge, so conditionally `Q_v^matter=0`.

The catch is the important bit: current MTS does not yet forbid the dangerous coupling forms

`V_m[X,rho_A,W_source,C_top]`, `A_A(X)L_A`, `A(X)J_H`, source-only prefactors, species-frame factors, or material
markers outside `q/Obs_e`.

So the matter/source theorem is exact as a route, but not claim-grade yet.  The coupling/no-direct-slot grammar is now
the root bottleneck.

## Source Register

{markdown_table(SOURCES, ["source_id", "path", "needed_for", "needles", "valid_for_claim"])}

## Matter Source Lift Theorem

{markdown_table(theorem, ["row_id", "claim", "statement", "derivation_status", "consequence", "missing_for_current_claim", "valid_for_claim"])}

## Matter Zero Certificate

{markdown_table(certificates, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## Source Charge Rows

{markdown_table(source_rows, ["quantity_id", "definition", "units", "formula_or_bound", "current_value_status", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_targets, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is where the theory is now most honestly exposed.  EH can be made silent by quotient geometry.  Matter can also
be made silent, but only if the coupling grammar is strict enough.  If the parent action allows even one source-only
prefactor or residual matter vertex, local GR does not follow; it becomes a finite coupling/source-charge residual
that must be bounded.  The next move is therefore exactly the coupling hunt.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2396_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2396_VALIDATION.csv'}")


if __name__ == "__main__":
    main()

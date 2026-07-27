from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_HCORE_QR_COUPLING_SOURCE_EQUATION_2576"
CHECKPOINT_ID = "2576"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QR_RAW = ROOT / "source-intake" / "qr-hat" / "raw"

RAW_QRHAT = QR_RAW / "QRHAT1255_CASSINI_GAMMA_PHENOMENOLOGICAL_BOUND_NONCLAIM.csv"
DOC = ROOT / "2576-Y5-R2FR-parent-Hcore-QR-source-equation-coupling-owner-or-boundary-charge-owner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_SOURCE_REGISTER.csv",
    "hcore_audit": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_HCORE_QR_SOURCE_EQUATION_AUDIT.csv",
    "uv_spine": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_UV_REDUCTION_SPINE.csv",
    "coupling_owner": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_COUPLING_OWNER_EXTENSION.csv",
    "coefficient_law": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv",
    "epsilonm_ledger": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_EPSILONM_SOURCE_CLOSURE_LEDGER.csv",
    "qr_binding": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_QR_DELTA_P_BINDING_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2576_VALIDATION.csv",
}

COPY_TARGETS = {
    "hcore_audit": LOCAL_BOUNDS / "Hcore_QR_coupling_source_equation_audit_2576_NONCLAIM.csv",
    "uv_spine": LOCAL_BOUNDS / "UV_reduction_spine_coupling_2576_NONCLAIM.csv",
    "coefficient_law": BETA_SOURCE / "V_Newton_PPN_coupling_coefficient_law_2576_NONCLAIM.csv",
    "epsilonm_ledger": QUEUE / "JR2576_EPSILONM_COUPLING_SOURCE_CLOSURE_LEDGER_NONCLAIM.csv",
    "next_target": QUEUE / "JR2576_WORLDTUBE_HILBERT_SOURCE_SELECTOR_COUPLING_OR_REQ_FILL_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2576_00_2575_handoff",
        "source_path": ROOT / "2575-Y5-R2FR-QR-parent-zero-signature-or-live-delta-p-coupling-input-row.md",
        "needles": ["NEXT2575_0_selected", "QRZ2575_6_verdict", "LIVE2575_0_QRHAT1255_Cassini_ceiling"],
        "role": "active handoff selecting parent H_core QR source equation with coupling owner",
    },
    {
        "source_id": "SRC2576_01_2502_precedent",
        "source_path": ROOT / "2502-Y5-R2FR-parent-Hcore-QR-source-equation-or-boundary-charge-owner.md",
        "needles": ["HQR2502_5_current_verdict", "UV2502_5_status", "VAL2502_OVERALL"],
        "role": "precedent H_core/u-v route and QR source-equation blocker",
    },
    {
        "source_id": "SRC2576_02_1884_zero_flux",
        "source_path": ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
        "needles": ["NBC1884_1_exact_zero_flux_lemma", "NBC1884_4_no_boundary_charge_parent_signature", "VAL1884_OVERALL"],
        "role": "exact zero-flux conditional and boundary/source descent blocker",
    },
    {
        "source_id": "SRC2576_03_2174_hcore",
        "source_path": ROOT / "2174-Y5-R2FR-Hcore-canonical-bracket-closure-or-auxiliary-route-demotion.md",
        "needles": ["CUS2174_3_core_expansion", "DF2174_4_second_class", "VAL2174_OVERALL"],
        "role": "H_core skeleton and conditional second-class u-sector route",
    },
    {
        "source_id": "SRC2576_04_2177_v_readout",
        "source_path": ROOT / "2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md",
        "needles": ["VOR2177_2_constraint_surface", "PPN2177_5_verdict", "VAL2177_OVERALL"],
        "role": "u=0 coframe reconstruction and conditional v-only readout",
    },
    {
        "source_id": "SRC2576_05_2178_v_source",
        "source_path": ROOT / "2178-Y5-R2FR-constraint-before-readout-ordering-and-v-PPN-source-convention-or-readout-lock.md",
        "needles": ["VS2178_2_required_solution", "PPN2178_2_beta_law", "VAL2178_OVERALL"],
        "role": "v=-2U/c^2 source convention and beta drift law",
    },
    {
        "source_id": "SRC2576_06_2179_v_coefficients",
        "source_path": ROOT / "2179-Y5-R2FR-parent-v-field-action-normalization-and-beta-quadratic-zero-or-finite-row.md",
        "needles": ["VAC2179_5_current_verdict", "BKA2179_2_pure_linear_branch", "VAL2179_OVERALL"],
        "role": "v action coefficient normalization and kappa_v route",
    },
    {
        "source_id": "SRC2576_07_2180_mass_glue",
        "source_path": ROOT / "2180-Y5-R2FR-PiM-JH-mass-current-to-v-source-coefficient-glue-or-delta-kappa-fill.md",
        "needles": ["NGL2180_2_observable_newton_residual", "KGL2180_1_kappa_decomposition", "VAL2180_OVERALL"],
        "role": "Newton residual and kappa_v decomposition",
    },
    {
        "source_id": "SRC2576_08_2181_commutator",
        "source_path": ROOT / "2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md",
        "needles": ["PCA2181_0_product_rule", "EMD2181_4_total_envelope", "VAL2181_OVERALL"],
        "role": "Pi_M current commutator and epsilon_M no-cancellation envelope",
    },
    {
        "source_id": "SRC2576_09_2182_topological_hilbert",
        "source_path": ROOT / "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
        "needles": ["TEA2182_0_identity_target", "CG2182_5_Newton_local_GR", "VAL2182_OVERALL"],
        "role": "topological-Hilbert source equality route and local-GR blocker",
    },
    {
        "source_id": "SRC2576_10_1253_Hcore",
        "source_path": OUT / "P8_Y5_R10_1253_RECIPROCAL_HCORE_SOURCE_EQUATION_ATTEMPT.csv",
        "needles": ["HCE1253_0_reciprocal_euler_source", "SOURCE_EQUATION_NOT_DERIVED", "HCE1253_1_boundary_flux_definition"],
        "role": "earlier formal reciprocal H_core source equation and boundary flux attempt",
    },
    {
        "source_id": "SRC2576_11_2575_validation",
        "source_path": OUT / "P8_Y5_BRR545_2575_VALIDATION.csv",
        "needles": ["VAL2575_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def hcore_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "HQR2576_0_cell_current_equation",
            "object": "exterior reciprocal cell current",
            "equation_or_clause": "W(r) partial_r C_R(r)=Q_R in the exterior, with C_R(infinity)=0",
            "derivation_status": "EXACT_CONDITIONAL_EXISTING_BRANCH",
            "missing_parent_input": "does not by itself set Q_R=0 or fix finite Q_R from parent dynamics",
            "coupling_requirement": "Q_R must be normalized against parent-owned kappa_MTS and ell_J before any source/readout comparison",
            "claim_effect": "identifies the charge channel but does not close local GR",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2576_1_Hcore_source_equation_shape",
            "object": "parent reciprocal Euler/source equation",
            "equation_or_clause": "E_R := delta H_core/delta C_R = rho_R + div(B_R), with Q_R as the asymptotic boundary flux",
            "derivation_status": "FORMAL_SHAPE_ONLY",
            "missing_parent_input": "explicit H_core density, variational boundary term, reciprocal source current rho_R, and charge class",
            "coupling_requirement": "the same parent block must own the EH coefficient, source-current scale ell_J, and no fitted-GM shortcut",
            "claim_effect": "would decide whether Q_R is zero, finite, or a no-go residual",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2576_2_u_second_class_route",
            "object": "radial reciprocal sum mode u=C_R/2",
            "equation_or_clause": "if H_core contains a parent-owned second-class pair u≈0, p_u≈0 with I_u=J_u=0, then C_R=0 before readout",
            "derivation_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_parent_input": "invariance, I_u=0, J_u=0, boundary differentiability, source silence, and matter/readout descent",
            "coupling_requirement": "I_u and J_u must not secretly re-enter through kappa_MTS, ell_J, endpoint, or source normalization",
            "claim_effect": "best route to Q_R=0, but still a theorem target",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2576_3_v_readout_route",
            "object": "visible quotient branch after u=0",
            "equation_or_clause": "u=0 -> T=exp(v/2), sqrt(S)=exp(-v/2), A=exp(v), B=exp(-v)",
            "derivation_status": "EXACT_CONDITIONAL_RECONSTRUCTION",
            "missing_parent_input": "source equation v=-2U/c^2, action coefficient normalization, epsilon_M=0, kappa_v=0",
            "coupling_requirement": "readout and source convention must fix kappa_MTS and ell_J before comparing to measured GM",
            "claim_effect": "narrows local branch from raw metric freedom to one v field",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2576_4_boundary_owner",
            "object": "boundary charge and compact source class",
            "equation_or_clause": "Q_R=0 requires zero reciprocal boundary charge for the allowed local source class",
            "derivation_status": "UNSIGNED",
            "missing_parent_input": "differentiable boundary action, source compactness class, no reciprocal matter charge, and projection silence",
            "coupling_requirement": "boundary charge cannot shift under hidden source-current or gravitational coupling rescaling",
            "claim_effect": "bulk u=0 alone is insufficient if boundary hair remains",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2576_5_coupling_owner",
            "object": "source/coupling normalization",
            "equation_or_clause": "kappa_MTS and ell_J must descend as parent-owned constants or fixed-before-readout conventions",
            "derivation_status": "UNSIGNED_HARD_BLOCKER",
            "missing_parent_input": "parent ownership of EH coefficient, source-current scale, same-frame mass measure, and no fitted-baseline absorption",
            "coupling_requirement": "carry delta_kappa and delta_ellJ as explicit residuals until signed",
            "claim_effect": "blocks Newton, PPN beta, and local-GR scoring even if a gamma-like branch is small",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2576_6_current_verdict",
            "object": "parent H_core QR source equation plus coupling owner",
            "equation_or_clause": "current corpus does not derive E_R, Q_R boundary owner, source descent, and kappa/ell_J ownership in one parent package",
            "derivation_status": "PARENT_HCORE_QR_COUPLING_EQUATION_NOT_DERIVED_CURRENT_CORPUS",
            "missing_parent_input": "explicit parent action block tying reciprocal charge, worldtube Hilbert source, boundary flux, and coupling scales together",
            "coupling_requirement": "coupling is not metadata; it is part of the theorem statement",
            "claim_effect": "local GR/Newton remains blocked, but the missing object is now sharply specified",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def uv_spine_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "spine_id": "UV2576_0_definitions",
            "object": "radial coframe variables",
            "law": "u=a+b=C_R/2; v=a-b=ln(T/sqrt(S))",
            "status": "DEFINITION_FROM_PRIOR_BRANCH",
            "coupling_slot": "none yet, but source normalization enters when solving v",
            "needed_for_claim": "same definitions must be parent-owned before readout",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2576_1_constraint_surface",
            "object": "u=0 branch",
            "law": "T=exp(v/2), sqrt(S)=exp(-v/2), A=T^2=exp(v), B=S=exp(-v)",
            "status": "EXACT_CONDITIONAL",
            "coupling_slot": "readout rods/clocks must not reintroduce u or source-scale tails",
            "needed_for_claim": "parent theorem forcing u=0 before readout",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2576_2_Newton_target",
            "object": "first-order source solution",
            "law": "for U=GM/r>0, Newton requires v=-2U/c^2+O(U^2/c^4)",
            "status": "REQUIRED_SOURCE_NORMALIZATION",
            "coupling_slot": "G, M, kappa_MTS, and ell_J must be fixed in the same frame",
            "needed_for_claim": "derive C_v/K_v and mass-current identity rather than fitting GM after the fact",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2576_3_gamma_shape",
            "object": "first PPN shape",
            "law": "if v=-2U/c^2+O(U^2/c^4) and u=0, then gamma=1 at first order",
            "status": "EXACT_CONDITIONAL",
            "coupling_slot": "gamma shape is not enough if source coupling or readout tails remain",
            "needed_for_claim": "full PPN vector with source/coupling ownership",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2576_4_beta_shape",
            "object": "second-order v coefficient",
            "law": "for v=-2x+kappa_v x^2+..., x=U/c^2, beta-1=kappa_v/2",
            "status": "EXACT_CONDITIONAL",
            "coupling_slot": "kappa_v can receive source, boundary, readout, operator, kappa_MTS, and ell_J pieces",
            "needed_for_claim": "derive kappa_v=0 or a finite bounded vector",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2576_5_status",
            "object": "local route",
            "law": "route is now u-zero -> v-source -> coupling-owned Newton residual -> beta residual",
            "status": "ROUTE_NARROWED_NOT_CLAIMABLE",
            "coupling_slot": "delta_kappa and delta_ellJ are explicit residuals, not hidden knobs",
            "needed_for_claim": "worldtube-Hilbert source selector plus zero boundary flux and fixed coupling baseline",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def coupling_owner_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "coupling_id": "COUP2576_0_kappa_owner",
            "quantity": "kappa_MTS / G-sector normalization",
            "required_parent_signature": "EH/local kinetic coefficient descends from parent action and is fixed before readout",
            "current_status": "MISSING_PARENT_OWNER",
            "residual_symbol": "delta_kappa := Dln_kappa_MTS",
            "where_it_enters": "Newton amplitude, beta/source normalization, PPN comparator conversion",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "COUP2576_1_ellJ_owner",
            "quantity": "ell_J / source-current scale",
            "required_parent_signature": "matter Hilbert/source current normalization descends in the same frame as v",
            "current_status": "MISSING_PARENT_OWNER",
            "residual_symbol": "delta_ellJ := Dln_ell_J",
            "where_it_enters": "epsilon_M, measured GM bridge, compact-source selector",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "COUP2576_2_fixed_baseline",
            "quantity": "measured GM/H0/source baseline",
            "required_parent_signature": "baseline is fixed before readout and not fitted to hide local residuals",
            "current_status": "FIXED_BEFORE_READOUT_CONTRACT_NOT_DERIVED",
            "residual_symbol": "delta_baseline",
            "where_it_enters": "prevents comparator-only local passes",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "COUP2576_3_source_coupling",
            "quantity": "H_core source terms",
            "required_parent_signature": "rho_R, Pi_M J_H, and B_R carry explicit kappa/ell_J slots or prove independence",
            "current_status": "SOURCE_COUPLING_SLOTS_UNSIGNED",
            "residual_symbol": "e_source_coupling",
            "where_it_enters": "Q_R, epsilon_M, boundary flux, beta source coefficient",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "COUP2576_4_verdict",
            "quantity": "coupling owner package",
            "required_parent_signature": "parent action owns gravitational coefficient, source-current scale, readout frame, and baseline together",
            "current_status": "COUPLING_OWNER_NOT_DERIVED_CURRENT_CORPUS",
            "residual_symbol": "delta_kappa + delta_ellJ + delta_baseline + e_source_coupling",
            "where_it_enters": "hard blocker for Newton/local-GR claim",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def coefficient_law_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "law_id": "LAW2576_0_delta_KC",
            "quantity": "v action/source coefficient residual",
            "definition": "delta_KC := C_v c^4/(16*pi*G_ref*K_v)-1",
            "status": "EXACT_LEDGER_DEFINITION",
            "must_derive_or_bound": "delta_KC=0 or finite sourced bound",
            "coupling_dependency": "G_ref cannot be a fitted absorption of kappa_MTS",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2576_1_epsilon_M",
            "quantity": "mass-current glue residual",
            "definition": "epsilon_M := M_source[v]/M_eff[Pi_M J_H]-1",
            "status": "EXACT_LEDGER_DEFINITION",
            "must_derive_or_bound": "epsilon_M=0 via worldtube-Hilbert source selector or finite bound",
            "coupling_dependency": "ell_J and source measure must be same-frame and parent-owned",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2576_2_delta_kappa",
            "quantity": "gravitational coupling residual",
            "definition": "delta_kappa := Dln_kappa_MTS relative to fixed local comparator normalization",
            "status": "NEW_EXPLICIT_COUPLING_SLOT",
            "must_derive_or_bound": "prove parent constant/fixed-before-readout or carry into local tests",
            "coupling_dependency": "direct coupling term",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2576_3_delta_ellJ",
            "quantity": "source-current scale residual",
            "definition": "delta_ellJ := Dln_ell_J relative to the compact-source Hilbert current",
            "status": "NEW_EXPLICIT_COUPLING_SLOT",
            "must_derive_or_bound": "prove parent source-current scale or carry into local tests",
            "coupling_dependency": "direct source normalization term",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2576_4_Delta_Newton_v_coupled",
            "quantity": "coupled Newton residual",
            "definition": "Delta_Newton_v_coupled := (1+delta_KC)(1+epsilon_M)(1+delta_kappa)(1+delta_ellJ)-1",
            "status": "NO_CANCELLATION_LEDGER",
            "must_derive_or_bound": "all four factors must be zero/owned or finite-bounded before Newton/local-GR claim",
            "coupling_dependency": "prevents hiding coupling failure inside measured GM",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2576_5_kappa_v",
            "quantity": "second-order beta residual",
            "definition": "kappa_v = -eta_v + kappa_source_quad + kappa_PiM + kappa_boundary + kappa_readout + kappa_operator + kappa_coupling",
            "status": "EXTENDED_LEDGER_DEFINITION",
            "must_derive_or_bound": "kappa_v=0 or finite bounded full vector",
            "coupling_dependency": "kappa_coupling collects delta_kappa, delta_ellJ, and baseline effects at second order",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2576_6_beta",
            "quantity": "PPN beta drift",
            "definition": "beta-1=kappa_v/2 in the constrained v-readout branch",
            "status": "EXACT_CONDITIONAL",
            "must_derive_or_bound": "beta pass requires kappa_v, not just gamma shape",
            "coupling_dependency": "coupled kappa_v must be included",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def epsilonm_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "ledger_id": "EM2576_0_topological_Hilbert_identity",
            "term": "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "current_status": "EXACT_IDENTITY_TARGET_NOT_ZERO_PROOF",
            "missing_input": "derive R_eq=0 and identify B_zero boundary representative",
            "coupling_owner_needed": "Hilbert source and topological current must use same ell_J normalization",
            "claim_effect": "epsilon_M remains open",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "EM2576_1_commutator",
            "term": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "current_status": "EXACT_OBSTRUCTION_TERM",
            "missing_input": "prove I_commutator=0 for local compact sources or bound it",
            "coupling_owner_needed": "projection Pi_M cannot depend on hidden coupling/readout frame",
            "claim_effect": "source conservation alone is insufficient",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "EM2576_2_boundary_flux",
            "term": "B_zero_flux",
            "current_status": "UNSIGNED",
            "missing_input": "zero compact boundary flux for worldtube selector",
            "coupling_owner_needed": "boundary representative must be invariant under source-current rescaling",
            "claim_effect": "epsilon_M and Q_R boundary owner remain blocked",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "EM2576_3_worldtube_selector",
            "term": "compact Hilbert source worldtube",
            "current_status": "UNSIGNED",
            "missing_input": "same-frame source measure, admissible local source class, and no reciprocal matter charge",
            "coupling_owner_needed": "ell_J fixed before selecting the worldtube mass current",
            "claim_effect": "M_source[v] cannot yet be equated to measured mass",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "EM2576_4_coupling_baseline",
            "term": "delta_kappa, delta_ellJ",
            "current_status": "NEW_HARD_RESIDUALS",
            "missing_input": "parent action ownership or finite local bounds",
            "coupling_owner_needed": "this is the coupling owner gate itself",
            "claim_effect": "prevents a hidden coupling win masquerading as Newton recovery",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "EM2576_5_verdict",
            "term": "epsilon_M coupled source closure",
            "current_status": "SOURCE_CLOSURE_WITH_COUPLING_NOT_DERIVED",
            "missing_input": "R_eq=0, B_zero_flux=0, I_commutator=0, worldtube selector, kappa/ellJ owner",
            "coupling_owner_needed": "full source/coupling package",
            "claim_effect": "Newton/local GR remains blocked",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def qr_binding_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "binding_id": "QRB2576_0_zero_flux_conditional",
            "statement": "If Q_R=0, W>0, J_R=0 exterior, and C_R(infinity)=0, then C_R=0 and delta_p=0 after readout descent.",
            "current_status": "EXACT_CONDITIONAL",
            "coupling_status": "must also prove no coupling/source readout tail reopens delta_p",
            "claim_effect": "not claimable until Q_R=0 is parent-signed",
            "valid_for_claim": False,
        },
        {
            "binding_id": "QRB2576_1_QRHAT_ceiling",
            "statement": "QRHAT1255 gives abs(q_R_hat)<=4.6e-5 and abs(delta_p)<=2.3e-5 as a comparator-derived ceiling.",
            "current_status": "LIVE_NONCLAIM_GUARDRAIL",
            "coupling_status": "not an MTS prediction and not coupling-owned",
            "claim_effect": "useful smoke guard only",
            "valid_for_claim": False,
        },
        {
            "binding_id": "QRB2576_2_uv_branch_relation",
            "statement": "u=0 removes C_R and leaves v to carry Newton/PPN recovery.",
            "current_status": "EXACT_CONDITIONAL_REDUCTION",
            "coupling_status": "v source amplitude still depends on delta_KC, epsilon_M, delta_kappa, delta_ellJ",
            "claim_effect": "route narrowed but not closed",
            "valid_for_claim": False,
        },
        {
            "binding_id": "QRB2576_3_full_vector",
            "statement": "full local vector requires Q_R/u, v amplitude, beta, source, boundary, readout, and coupling residuals together.",
            "current_status": "FULL_VECTOR_NOT_SCORE_READY",
            "coupling_status": "coupling owner missing",
            "claim_effect": "no R10, PPN, WEP, clock, orbital, Newton, or local-GR claim",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2576_0_internal_progress",
            "claim": "2576 identifies the exact missing parent package for Q_R/u/v/source/coupling closure.",
            "gate_status": "PASS_INTERNAL_PROGRESS",
            "reason": "the route is sharper and fewer loopholes are left unnamed",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2576_1_QR_zero",
            "claim": "Q_R=0 is derived.",
            "gate_status": "BLOCKED",
            "reason": "boundary charge/source descent/matter descent/projection silence/coupling owner are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2576_2_Hcore_source_equation",
            "claim": "parent H_core supplies reciprocal source equation.",
            "gate_status": "BLOCKED",
            "reason": "E_R, rho_R, B_R, explicit H_core, and charge class remain formal shape only",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2576_3_coupling_owner",
            "claim": "kappa_MTS and ell_J are parent-owned.",
            "gate_status": "BLOCKED",
            "reason": "coupling/source baseline ownership is not derived",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2576_4_Newton",
            "claim": "Newton limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "Delta_Newton_v_coupled requires delta_KC=epsilon_M=delta_kappa=delta_ellJ=0 or finite bounds",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2576_5_beta",
            "claim": "PPN beta=1 is derived.",
            "gate_status": "BLOCKED",
            "reason": "kappa_v with coupling/source/readout terms is not zeroed",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2576_6_local_GR",
            "claim": "local GR recovery is derived.",
            "gate_status": "BLOCKED",
            "reason": "gamma-shape branch is insufficient without full source, beta, boundary, readout, and coupling vector",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2576_7_no_shortcuts",
            "claim": "closure-only zero, gamma-only pass, fitted-GM absorption, or comparator ceiling can be used as evidence.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "all such routes are explicitly demoted to nonclaim unless parent signed",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2576_0_zero_proof_failed_current_corpus",
            "decision": "PARENT_HCORE_QR_COUPLING_ZERO_PROOF_NOT_AVAILABLE",
            "reason": "H_core source equation, boundary charge, source descent, and coupling owner are not signed in one package",
            "effect": "do not claim Q_R=0 or local GR",
        },
        {
            "decision_id": "DEC2576_1_route_narrowed",
            "decision": "LOCAL_ROUTE_REDUCED_TO_UV_SOURCE_COUPLING_SPINE",
            "reason": "if u=0 is parent-signed, the coframe is v-only and the remaining Newton/PPN problem is a source/coupling coefficient problem",
            "effect": "focus next work on source selector and coupling normalization rather than repeating gamma-only tests",
        },
        {
            "decision_id": "DEC2576_2_Newton_requirements",
            "decision": "NEWTON_REQUIRES_DELTA_KC_EPSILONM_DELTAKAPPA_DELTAELLJ",
            "reason": "measured GM can otherwise hide action/source/coupling mismatches",
            "effect": "carry coupled Newton residual explicitly",
        },
        {
            "decision_id": "DEC2576_3_beta_requirements",
            "decision": "BETA_REDUCED_TO_KAPPA_V_WITH_COUPLING",
            "reason": "v second-order coefficient is the cleanest beta gate after u=0",
            "effect": "derive pure linear exterior v branch or fill finite kappa_v residuals",
        },
        {
            "decision_id": "DEC2576_4_next",
            "decision": "WORLDTUBE_HILBERT_SOURCE_SELECTOR_WITH_COUPLING_SELECTED_NEXT",
            "reason": "epsilon_M and coupling owner are now the choke point for Newton and local GR",
            "effect": "2577 should try to prove source selector, zero boundary flux, and fixed coupling baseline or fill R_eq/B_zero/I_commutator/delta_kappa/delta_ellJ rows",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2576_0_selected",
            "selection_status": "selected",
            "target_file": "2577-Y5-R2FR-worldtube-Hilbert-source-selector-coupling-and-zero-boundary-flux-or-R-eq-fill.md",
            "target_script": "scripts/Y5_R2FR_worldtube_Hilbert_source_selector_coupling_and_zero_boundary_flux_or_R_eq_fill_2577.py",
            "task": "derive parent-owned compact Hilbert source worldtube, same-frame source measure, topological representative, zero boundary flux, and fixed coupling/source-current baseline for the constrained v branch; otherwise fill R_eq, B_zero_flux, I_commutator, delta_kappa, and delta_ellJ finite residual rows",
            "acceptance_target": "epsilon_M=0 and coupling owner theorem, or explicit finite residual ledger blocking local-GR claim",
            "guardrails": "no GitHub; no formalization-workbench edits; no QRHAT ceiling as prediction; no gamma-only pass; no fitted GM/H0 shortcut",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "hcore_audit": OUTPUTS["hcore_audit"],
        "uv_spine": OUTPUTS["uv_spine"],
        "coefficient_law": OUTPUTS["coefficient_law"],
        "epsilonm_ledger": OUTPUTS["epsilonm_ledger"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2576_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2576_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2576_01_Hcore_verdict_blocked",
        any(row["audit_id"] == "HQR2576_6_current_verdict" and row["derivation_status"] == "PARENT_HCORE_QR_COUPLING_EQUATION_NOT_DERIVED_CURRENT_CORPUS" for row in data["hcore_audit"]),
        "parent H_core QR coupling equation remains blocked",
    )
    add(
        "VAL2576_02_uv_spine_written",
        any(row["spine_id"] == "UV2576_5_status" and row["status"] == "ROUTE_NARROWED_NOT_CLAIMABLE" for row in data["uv_spine"]),
        "u/v local route is narrowed but nonclaim",
    )
    add(
        "VAL2576_03_coupling_owner_rows",
        any(row["coupling_id"] == "COUP2576_4_verdict" and row["current_status"] == "COUPLING_OWNER_NOT_DERIVED_CURRENT_CORPUS" for row in data["coupling_owner"]),
        "coupling owner verdict row blocks hidden kappa/ell_J shortcuts",
    )
    add(
        "VAL2576_04_coupled_Newton_law",
        any(row["law_id"] == "LAW2576_4_Delta_Newton_v_coupled" and "delta_kappa" in row["definition"] and "delta_ellJ" in row["definition"] for row in data["coefficient_law"]),
        "coupled Newton residual explicitly includes delta_kappa and delta_ellJ",
    )
    add(
        "VAL2576_05_epsilonM_blocked",
        any(row["ledger_id"] == "EM2576_5_verdict" and row["current_status"] == "SOURCE_CLOSURE_WITH_COUPLING_NOT_DERIVED" for row in data["epsilonm_ledger"]),
        "epsilon_M source closure with coupling remains blocked",
    )
    add(
        "VAL2576_06_QR_binding_nonclaim",
        any(row["binding_id"] == "QRB2576_3_full_vector" and row["current_status"] == "FULL_VECTOR_NOT_SCORE_READY" for row in data["qr_binding"]),
        "QR/delta_p/full local vector remains nonclaim",
    )
    add(
        "VAL2576_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows R10, PPN, WEP, clock, orbital, Newton or local-GR claim",
    )
    add(
        "VAL2576_08_next_target_written",
        any(row["route_id"] == "NEXT2576_0_selected" for row in data["next"]),
        "2577 worldtube-Hilbert source selector with coupling target selected",
    )
    add(
        "VAL2576_09_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2576*", "*P8_Y5_HCORE_QR_COUPLING_2576*", "*JR2576*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2576_10_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2576 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2576_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2576_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2576_OVERALL",
        overall,
        "2576 blocks parent Hcore QR/coupling closure, narrows local recovery to u/v/source/coupling spine, and selects worldtube-Hilbert source selector with coupling next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2576 Y5 R2FR Parent Hcore QR Source Equation Coupling Owner Or Boundary Charge Owner",
        "",
        "**Status:** private nonclaim derivation checkpoint. The parent `H_core` source equation plus boundary-charge owner plus coupling/source-scale owner is not derived in the current corpus.",
        "",
        "**Main result:** the best local-GR route is now sharply narrowed: first derive a parent-owned `u=0` / `Q_R=0` mechanism, then solve the constrained `v` branch with `v=-2U/c^2`, `delta_KC=0`, `epsilon_M=0`, `delta_kappa=0`, `delta_ellJ=0`, and `kappa_v=0`. The new no-shortcut rule is that `kappa_MTS` and `ell_J` are part of the theorem, not calibration metadata. QRHAT1255 remains a nonclaim ceiling only.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Hcore QR Source Equation Audit",
        markdown_table(data["hcore_audit"], ["audit_id", "object", "equation_or_clause", "derivation_status", "missing_parent_input", "coupling_requirement", "claim_effect", "valid_for_claim"]),
        "",
        "## UV Reduction Spine",
        markdown_table(data["uv_spine"], ["spine_id", "object", "law", "status", "coupling_slot", "needed_for_claim", "valid_for_claim"]),
        "",
        "## Coupling Owner Extension",
        markdown_table(data["coupling_owner"], ["coupling_id", "quantity", "required_parent_signature", "current_status", "residual_symbol", "where_it_enters", "valid_for_claim"]),
        "",
        "## Newton / PPN Coefficient Law",
        markdown_table(data["coefficient_law"], ["law_id", "quantity", "definition", "status", "must_derive_or_bound", "coupling_dependency", "valid_for_claim"]),
        "",
        "## EpsilonM Source Closure Ledger",
        markdown_table(data["epsilonm_ledger"], ["ledger_id", "term", "current_status", "missing_input", "coupling_owner_needed", "claim_effect", "valid_for_claim"]),
        "",
        "## QR / Delta_p Binding Status",
        markdown_table(data["qr_binding"], ["binding_id", "statement", "current_status", "coupling_status", "claim_effect", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    BETA_SOURCE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "hcore_audit": hcore_audit_rows(),
        "uv_spine": uv_spine_rows(),
        "coupling_owner": coupling_owner_rows(),
        "coefficient_law": coefficient_law_rows(),
        "epsilonm_ledger": epsilonm_ledger_rows(),
        "qr_binding": qr_binding_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["hcore_audit"], data["hcore_audit"])
    write_csv(OUTPUTS["uv_spine"], data["uv_spine"])
    write_csv(OUTPUTS["coupling_owner"], data["coupling_owner"])
    write_csv(OUTPUTS["coefficient_law"], data["coefficient_law"])
    write_csv(OUTPUTS["epsilonm_ledger"], data["epsilonm_ledger"])
    write_csv(OUTPUTS["qr_binding"], data["qr_binding"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2576_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

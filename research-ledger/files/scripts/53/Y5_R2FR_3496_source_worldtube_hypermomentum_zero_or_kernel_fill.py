from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3496-Y5-R2FR-source-worldtube-hypermomentum-zero-or-kernel-fill.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3496": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3495": {
        "path": ROOT / "3495-Y5-R2FR-source-readout-boundary-gamma-current-zero-or-P4-tail-priority.md",
        "role": "3495 handoff and priority decision",
    },
    "priority_3495": {
        "path": OUT / "P8_Y5_R2FR_3495_P4_TAIL_PRIORITY_QUEUE.csv",
        "role": "P4 tail priority queue",
    },
    "decomposition_3495": {
        "path": OUT / "P8_Y5_R2FR_3495_GAMMA_CURRENT_DECOMPOSITION.csv",
        "role": "Gamma-current source/readout decomposition",
    },
    "gates_3495": {
        "path": OUT / "P8_Y5_R2FR_3495_GATES.csv",
        "role": "3495 theorem gates",
    },
    "p4_lock_3493": {
        "path": OUT / "P8_Y5_R2FR_3493_OFFICIAL_P4_LOCAL_GEOMETRY_INTERFACE.csv",
        "role": "official P4 local-geometry interface",
    },
    "hilbert_3423": {
        "path": OUT / "P8_Y5_R2FR_3423_HILBERT_WORLDTUBE_CLOSURE_THEOREM.csv",
        "role": "Hilbert worldtube closure theorem",
    },
    "selector_3375": {
        "path": OUT / "P8_Y5_R2FR_3375_WORLDTUBE_SOURCE_MEASURE_SELECTOR_THEOREM.csv",
        "role": "worldtube/source measure selector theorem",
    },
    "poynting_3375": {
        "path": OUT / "P8_Y5_R2FR_3375_POYNTING_SOURCE_WORLD_TUBE_PLACEMENT.csv",
        "role": "Poynting placement in source measure",
    },
    "rworldtube_3375": {
        "path": OUT / "P8_Y5_R2FR_3375_RWORLDTUBE_BOUND_ROWS_NONCLAIM.csv",
        "role": "worldtube residual bound rows",
    },
    "poynting_bound_3249": {
        "path": OUT / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv",
        "role": "source-worldtube Poynting bound row",
    },
    "flux_norm_3250": {
        "path": OUT / "P8_Y5_R2FR_3250_SOURCE_WORLDTUBE_FLUX_NORM_ROW.csv",
        "role": "source-worldtube flux norm row",
    },
    "matter_descent_2611": {
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
        "role": "matter/worldtube descent theorem attempt",
    },
    "support_2388": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv",
        "role": "worldtube support certificate",
    },
    "selector_2183": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2183_WORLDTUBE_HILBERT_SELECTOR_THEOREM.csv",
        "role": "worldtube Hilbert selector theorem",
    },
    "owner_2122": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv",
        "role": "source/readout owner lemma",
    },
    "zero_2118": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv",
        "role": "source/readout zero theorem attempt",
    },
    "commutator_1898": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
        "role": "readout/projector commutator obstruction",
    },
    "wep_3492": {
        "path": OUT / "P8_Y5_R2FR_3492_WEP_PRODUCT_BOUNDS.csv",
        "role": "WEP inherited product bounds",
    },
    "ppn_3492": {
        "path": OUT / "P8_Y5_R2FR_3492_PPN_PRODUCT_BOUNDS.csv",
        "role": "PPN inherited product bounds",
    },
}


def generated_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": str(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def hypermomentum_zero_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "DER3496_0_define_source_hypermomentum",
            "claim_piece": "source hypermomentum target",
            "statement": "The source tail is the independent-connection response Delta_source := delta S_source / delta Gamma_ind, equivalently the source piece of Delta_lambda^{mu nu}.",
            "derivation": "If Gamma_ind is not an argument of the ordinary source functional, the Frechet derivative with respect to Gamma_ind is identically zero; the only possible survival is through pre-variation support, projector, boundary, calibration or readout maps.",
            "status": "EXACT_IDENTITY_AND_TARGET",
            "missing_to_promote": "single parent branch must say whether support/projector/source normalization are pre-variation arguments or post-variation readouts",
            "source_path": str(SOURCES["decomposition_3495"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "step_id": "DER3496_1_bulk_matter_no_independent_gamma",
            "claim_piece": "bulk ordinary matter",
            "statement": "For S_matter = Sbar_m[psi, e_obs(q(Phi)), omega_LC(e_obs), theta(q(Phi))], partial S_matter / partial Gamma_ind = 0.",
            "derivation": "The chain rule gives delta_v S_matter = (delta Sbar/de_obs)D_v e_obs + (delta Sbar/dtheta)D_v theta + spin terms through D_v omega_LC[e_obs]; all vanish for vertical v in ker(Dq) if e_obs and theta descend through q.",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "missing_to_promote": "explicit parent matter Lagrangian and all-sector no-Gamma ordinary source signature",
            "source_path": str(SOURCES["matter_descent_2611"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "step_id": "DER3496_2_worldtube_support_stability",
            "claim_piece": "support selector",
            "statement": "If J_H[tau] descends through e_obs/q and has compact regular support, then W_source := closure(supp J_H[tau]) is vertically silent.",
            "derivation": "D_v J_H = 0 distributionally implies the support current does not move under Gamma_ind variation; for regular support branches, D_v W_source = 0. If support is singular or chosen by readout masks, the support drift becomes a finite residual.",
            "status": "DERIVED_REGULAR_SUPPORT_LEMMA_CONDITIONAL",
            "missing_to_promote": "compact regular Hilbert support, no readout mask, same tau/e_obs frame and no-crossing certificate",
            "source_path": str(SOURCES["support_2388"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "step_id": "DER3496_3_hamiltonian_charge_descent",
            "claim_piece": "source mass and GM normalization",
            "statement": "If M_H[W] is the Hamiltonian/Noether charge of the same W_source with fixed tau, reference and normalization, then delta_Gamma_ind M_H = 0.",
            "derivation": "M_H = H_tau[S] - H_ref is a surface/current functional of the same descended fields. With fixed linked surfaces and reference, Gamma_ind variation cannot change the dressed source charge; without this lock, Delta_GM_transfer and reference drift remain finite.",
            "status": "DERIVED_CONDITIONAL_CHARGE_DESCENT",
            "missing_to_promote": "H_tau integrability, positive M_H_ref, boundary/reference lock, same object Pi_M J_H = J_M_top",
            "source_path": str(SOURCES["hilbert_3423"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "step_id": "DER3496_4_poynting_not_optional",
            "claim_piece": "EM/Poynting energy in source measure",
            "statement": "If EM uses the public e_obs Hodge star, Poynting flux and Maxwell stress are part of the Hilbert current and not a separate Gamma-source tail.",
            "derivation": "The source charge is dressed: M_source = M_matter + M_EM + M_binding + M_boundary plus retained residuals. Public-Hodge EM contributes through T_EM[e_obs,A], not through Gamma_ind. Hidden-frame EM or unowned boundary flux reopens R_Poynting_worldtube.",
            "status": "DERIVED_PLACEMENT_CONDITIONAL",
            "missing_to_promote": "public-Hodge EM signature, boundary/collar flux norms or zero theorem",
            "source_path": str(SOURCES["poynting_3375"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "step_id": "DER3496_5_projector_commutator_boundary",
            "claim_piece": "projector and boundary current",
            "statement": "Even when bulk matter descends, a field-dependent projector obeys delta(Pi J)=Pi delta J + (delta Pi)J, so source hypermomentum can re-enter through delta Pi.",
            "derivation": "This is the surviving counterroute. It is killed only if Pi, boundary transport, domain selector, support weights and source collars are fixed downstream q/e_obs functors before variation.",
            "status": "COUNTERMODEL_ROUTE_ACTIVE",
            "missing_to_promote": "projector/domain/boundary descent certificate or finite K_boundary_projector bound",
            "source_path": str(SOURCES["commutator_1898"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "step_id": "DER3496_6_verdict",
            "claim_piece": "epsilon_hypermomentum_source",
            "statement": "The source-hypermomentum zero proof is real as a local theorem, but current MTS has not signed every source-worldtube selector clause in one parent action.",
            "derivation": "Under the owned matter, regular support, Hamiltonian charge, public EM and fixed projector clauses, epsilon_hypermomentum_source = 0. If any clause fails, the tail is not mysterious; it is bounded by the explicit kernel vector in this checkpoint.",
            "status": "CONDITIONAL_THEOREM_SHARPENED_KERNEL_RETAINED",
            "missing_to_promote": "minimal parent source-action signature or first numeric/source-backed kernel row",
            "source_path": str(SOURCES["priority_3495"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def worldtube_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "CLAUSE3496_0_parent_Lm",
            "clause": "explicit parent ordinary matter Lagrangian",
            "required_signature": "L_m[psi,e_obs(q),omega_LC(e_obs),theta(q)] with no Gamma_ind or source-marker slot",
            "evidence_status": "UNSIGNED_CONTRACT_EXISTS",
            "if_unsigned_residual": "epsilon_JH_owner",
            "source_path": str(SOURCES["support_2388"]["path"]),
            "zero_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_1_same_frame_tau",
            "clause": "same e_obs/tau frame for matter, clocks, rods, source and orbit",
            "required_signature": "tau and e_obs are parent-selected before readout and are shared by Hilbert current and empirical readout",
            "evidence_status": "UNSIGNED",
            "if_unsigned_residual": "epsilon_frame_tau_selector",
            "source_path": str(SOURCES["support_2388"]["path"]),
            "zero_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_2_regular_support",
            "clause": "compact regular W_source support",
            "required_signature": "W_source = closure(supp J_H[tau]) has compact regular support or a sourced exterior tail bound",
            "evidence_status": "UNSIGNED_OR_BOUND_REQUIRED",
            "if_unsigned_residual": "epsilon_support_tail",
            "source_path": str(SOURCES["support_2388"]["path"]),
            "zero_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_3_no_marker_mask",
            "clause": "no material marker or readout mask selects the source after variation",
            "required_signature": "source profile and worldtube are determined by J_H only, not fitted radius, galaxy mask, material label or residual-tuned boundary",
            "evidence_status": "UNSIGNED",
            "if_unsigned_residual": "epsilon_marker_selector",
            "source_path": str(SOURCES["support_2388"]["path"]),
            "zero_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_4_hamiltonian_reference",
            "clause": "positive same-frame Hamiltonian mass denominator",
            "required_signature": "M_H_ref > 0 and H_ref/tau/reference are fixed in the same q/e_obs branch",
            "evidence_status": "UNSIGNED_DENOMINATOR",
            "if_unsigned_residual": "epsilon_MHref",
            "source_path": str(SOURCES["hilbert_3423"]["path"]),
            "zero_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_5_poynting_public_hodge",
            "clause": "Poynting and EM stress are included in the Hilbert source",
            "required_signature": "EM action uses the public e_obs Hodge star; any boundary/collar flux is zero or bounded",
            "evidence_status": "CONDITIONAL_PLACEMENT_OK_INPUT_NORMS_MISSING",
            "if_unsigned_residual": "epsilon_Poynting_worldtube",
            "source_path": str(SOURCES["poynting_3375"]["path"]),
            "zero_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_6_projector_boundary",
            "clause": "projector/domain/boundary transport is downstream and fixed",
            "required_signature": "Pi, boundary transport, support weights and collar maps descend through q/e_obs before variation",
            "evidence_status": "COUNTERMODEL_ACTIVE",
            "if_unsigned_residual": "epsilon_projector_comm",
            "source_path": str(SOURCES["commutator_1898"]["path"]),
            "zero_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_7_GM_transfer",
            "clause": "measured GM is the same parent Hilbert/Noether source charge",
            "required_signature": "GM_obs = G_ref M_H with G_ref parent fixed and no fitted-G absorption after readout",
            "evidence_status": "UNSIGNED_TRANSFER",
            "if_unsigned_residual": "epsilon_GM_transfer",
            "source_path": str(SOURCES["selector_3375"]["path"]),
            "zero_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def source_hypermomentum_kernel_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "KHS3496_0_master_envelope",
            "residual_symbol": "epsilon_hypermomentum_source",
            "definition": "total independent-Gamma source-worldtube tail after owned-coframe spin removal",
            "bound_formula": "abs(epsilon_hypermomentum_source) <= sum_i abs(K_i * epsilon_i)",
            "required_inputs": "K_i values plus zero-proof or source-backed values for every epsilon_i row below",
            "source_clause": "DER3496_6_verdict",
            "current_status": "EXECUTABLE_SYMBOLIC_ENVELOPE_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KHS3496_1_JH_owner",
            "residual_symbol": "epsilon_JH_owner",
            "definition": "bulk Hilbert current changes under Gamma_ind variation",
            "bound_formula": "||delta_Gamma J_H|| / max(||J_H||, M_H_ref)",
            "required_inputs": "explicit L_m, e_obs(q), omega_LC(e_obs), theta(q), no Gamma_ind slot",
            "source_clause": "CLAUSE3496_0_parent_Lm",
            "current_status": "ZERO_IF_PARENT_LM_SIGNED_ELSE_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KHS3496_2_support_tail",
            "residual_symbol": "epsilon_support_tail",
            "definition": "support drift or exterior source tail of W_source",
            "bound_formula": "dist_support(W_var,W_parent)/L_source + ||J_H||_tail/M_H_ref",
            "required_inputs": "support topology, regularity certificate, exterior tail norm, same tau/e_obs frame",
            "source_clause": "CLAUSE3496_2_regular_support",
            "current_status": "REGULAR_SUPPORT_ZERO_OR_TAIL_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KHS3496_3_marker_selector",
            "residual_symbol": "epsilon_marker_selector",
            "definition": "source mask/material marker/readout-selected support leakage",
            "bound_formula": "||D_marker W_source|| + ||D_readout J_H||/||J_H||",
            "required_inputs": "no-marker grammar or explicit derivative of support/profile mask",
            "source_clause": "CLAUSE3496_3_no_marker_mask",
            "current_status": "NO_MARKER_ZERO_OR_SELECTOR_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KHS3496_4_MHref_reference",
            "residual_symbol": "epsilon_MHref",
            "definition": "Hamiltonian denominator/reference drift",
            "bound_formula": "abs(delta_Gamma(H_tau-H_ref))/abs(M_H_ref)",
            "required_inputs": "H_tau, H_ref, N_G, tau, e_obs, positivity, integrability and reference lock",
            "source_clause": "CLAUSE3496_4_hamiltonian_reference",
            "current_status": "REFERENCE_LOCK_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KHS3496_5_Poynting_worldtube",
            "residual_symbol": "epsilon_Poynting_worldtube",
            "definition": "EM/Poynting flux not already included in Hilbert charge",
            "bound_formula": "mu0^-1 ||E_T||_L2(B)||B_T||_L2(B)/abs(M_H_ref) + collar_flux/abs(M_H_ref)",
            "required_inputs": "unit system, E/B norms, boundary measure, collar normal, public-Hodge certificate",
            "source_clause": "CLAUSE3496_5_poynting_public_hodge",
            "current_status": "PLACED_BUT_INPUT_NORMS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KHS3496_6_projector_comm",
            "residual_symbol": "epsilon_projector_comm",
            "definition": "delta Pi source/boundary/projector commutator",
            "bound_formula": "||delta_Gamma Pi|| * ||J_H|| / abs(M_H_ref)",
            "required_inputs": "projector/domain/boundary descent certificate or operator norm for delta Pi",
            "source_clause": "CLAUSE3496_6_projector_boundary",
            "current_status": "COUNTERMODEL_ACTIVE_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KHS3496_7_GM_transfer",
            "residual_symbol": "epsilon_GM_transfer",
            "definition": "measured GM transfer and fitted-G absorption leakage",
            "bound_formula": "abs(delta_Gamma(G_ref M_H) + delta_cal GM_obs)/abs(G_ref M_H)",
            "required_inputs": "G_ref branch constant, Poisson/Gauss calibration theorem, orbit/GM no-fitted-G guard",
            "source_clause": "CLAUSE3496_7_GM_transfer",
            "current_status": "GM_TRANSFER_UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def product_bound_inheritance_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_row in read_csv(SOURCES["wep_3492"]["path"]):
        if source_row.get("coefficient_symbol") == "epsilon_hypermomentum_source":
            rows.append(
                {
                    "inherit_id": f"HSB3496_WEP_{source_row.get('bound_id')}",
                    "bound_family": "WEP_product",
                    "observable": source_row.get("arena", ""),
                    "source_bound_id": source_row.get("bound_id", ""),
                    "inherited_product_bound": source_row.get("product_symbol", ""),
                    "bound_value": source_row.get("bound_value", ""),
                    "bound_units": source_row.get("bound_units", ""),
                    "kernel_requirement": "source-worldtube kernel vector KHS3496_0..7 plus material/source projection factors",
                    "source_reference": source_row.get("source_path", ""),
                    "score_status": "PRODUCT_BOUND_INHERITED_KERNEL_REQUIRED",
                    "valid_for_claim": "False",
                }
            )
    for source_row in read_csv(SOURCES["ppn_3492"]["path"]):
        if source_row.get("coefficient_symbol") == "epsilon_hypermomentum_source":
            rows.append(
                {
                    "inherit_id": f"HSB3496_PPN_{source_row.get('bound_id')}",
                    "bound_family": "PPN_product",
                    "observable": source_row.get("observable", ""),
                    "source_bound_id": source_row.get("bound_id", ""),
                    "inherited_product_bound": source_row.get("product_symbol", ""),
                    "bound_value": source_row.get("bound_value", ""),
                    "bound_units": source_row.get("bound_units", ""),
                    "kernel_requirement": source_row.get("missing_for_score", ""),
                    "source_reference": source_row.get("source_reference", ""),
                    "score_status": "PRODUCT_BOUND_INHERITED_KERNEL_REQUIRED",
                    "valid_for_claim": "False",
                }
            )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3496_0_theorem_not_rejected",
            "decision": "Keep the source-worldtube zero route alive.",
            "rationale": "The chain-rule, support-stability, Hamiltonian-charge and public-Hodge pieces form a real conditional theorem; it is not just a vague missing ledger.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3496_1_no_claim_yet",
            "decision": "Do not claim epsilon_hypermomentum_source = 0 yet.",
            "rationale": "The current corpus still lacks one signed parent source-action branch covering L_m, tau/e_obs, compact support, H_ref/M_H_ref, Poynting and projector descent together.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3496_2_next_best_move",
            "decision": "Write the minimal parent source-action signature next before collecting more loose bounds.",
            "rationale": "A single parent action signature can close several clauses at once; if it fails, KHS3496 is ready for the first numeric/source-backed hsrc bound row.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3497-Y5-R2FR-minimal-parent-source-action-signature-or-first-hsrc-bound-row.md",
            "next_script": "scripts/Y5_R2FR_3497_minimal_parent_source_action_signature_or_first_hsrc_bound_row.py",
            "objective": "Try to sign the smallest parent source-action branch that makes L_m, tau/e_obs, W_source, H_tau/H_ref, G_ref, public EM and projector descent one object; if it fails, fill the first source-hypermomentum bound row from KHS3496.",
            "success_gate": "all CLAUSE3496 rows signed in one parent branch, or first KHS3496 arena row has real numeric/source-backed coefficients and remains nonclaim until validated",
            "forbidden_shortcuts": "using point-source GR as proof; hiding Poynting flux; fitting G after readout; treating readout masks as source selectors; promoting product bounds without K_i kernels",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_files = [
        OUT / "P8_Y5_R2FR_3496_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3496_HYPERMOMENTUM_ZERO_DERIVATION.csv",
        OUT / "P8_Y5_R2FR_3496_WORLDTUBE_CLAUSE_AUDIT.csv",
        OUT / "P8_Y5_R2FR_3496_SOURCE_HYPERMOMENTUM_KERNEL_VECTOR.csv",
        OUT / "P8_Y5_R2FR_3496_PRODUCT_BOUND_INHERITANCE.csv",
        OUT / "P8_Y5_R2FR_3496_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3496_NEXT_TARGET.csv",
    ]
    parsed_counts: list[str] = []
    for output_file in output_files:
        parsed_counts.append(f"{output_file.name}:{len(read_csv(output_file))}")

    all_rows = [*sources, *derivation, *clauses, *kernels, *bounds, *decisions, *next_rows]
    unsigned_clause_count = sum(1 for clause_row in clauses if clause_row.get("zero_ready") != "True")
    inherited_wep_count = sum(1 for bound_row in bounds if bound_row.get("bound_family") == "WEP_product")
    inherited_ppn_count = sum(1 for bound_row in bounds if bound_row.get("bound_family") == "PPN_product")

    checks = [
        {
            "check_id": "VAL3496_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local sources exist",
        },
        {
            "check_id": "VAL3496_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3496_2_derivation_chain",
            "passed": len(derivation) >= 7 and any(row["status"] == "DERIVED_REGULAR_SUPPORT_LEMMA_CONDITIONAL" for row in derivation),
            "detail": f"derivation_steps={len(derivation)}; support lemma present",
        },
        {
            "check_id": "VAL3496_3_unsigned_clauses_block_claim",
            "passed": unsigned_clause_count > 0,
            "detail": f"unsigned_or_unready_clauses={unsigned_clause_count}",
        },
        {
            "check_id": "VAL3496_4_kernel_vector_complete",
            "passed": len(kernels) >= 8 and kernels[0]["residual_symbol"] == "epsilon_hypermomentum_source",
            "detail": f"kernel_rows={len(kernels)}; master={kernels[0]['residual_symbol']}",
        },
        {
            "check_id": "VAL3496_5_product_bounds_inherited",
            "passed": inherited_wep_count == 2 and inherited_ppn_count == 3,
            "detail": f"WEP={inherited_wep_count}; PPN={inherited_ppn_count}",
        },
        {
            "check_id": "VAL3496_6_no_claim",
            "passed": all(str(output_row.get("valid_for_claim", "False")) == "False" for output_row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3496_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
        },
        {
            "check_id": "VAL3496_8_next_target",
            "passed": len(next_rows) == 1 and "3497" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3496_SUMMARY",
            "passed": all(bool(check["passed"]) for check in checks),
            "detail": "PASS" if all(bool(check["passed"]) for check in checks) else "FAIL",
        }
    )
    return [
        {
            "check_id": check["check_id"],
            "passed": str(bool(check["passed"])),
            "detail": check["detail"],
            "valid_for_claim": "False",
        }
        for check in checks
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    derivation: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3496 - Source-Worldtube Hypermomentum Zero or Kernel Fill",
                "",
                "## Current Verdict",
                "- **Derivation advanced:** `epsilon_hypermomentum_source = 0` follows as an exact conditional theorem if source matter, support, Hamiltonian charge, public EM and projectors are all downstream `q/e_obs` objects.",
                "- **No claim yet:** the parent corpus has not signed those clauses in one minimal source-action branch.",
                "- **Real progress:** the gap is no longer just `source missing`; it is split into a finite kernel vector with inherited WEP/PPN product bounds.",
                "- **Best next attack:** write the minimal parent source-action signature and see if it signs the clauses together.",
                "",
                "## Hypermomentum Zero Derivation",
                markdown_table(
                    derivation,
                    ["step_id", "claim_piece", "statement", "status", "missing_to_promote", "valid_for_claim"],
                ),
                "",
                "## Worldtube Clause Audit",
                markdown_table(
                    clauses,
                    [
                        "clause_id",
                        "clause",
                        "required_signature",
                        "evidence_status",
                        "if_unsigned_residual",
                        "zero_ready",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Source-Hypermomentum Kernel Vector",
                markdown_table(
                    kernels,
                    [
                        "kernel_id",
                        "residual_symbol",
                        "definition",
                        "bound_formula",
                        "current_status",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Product-Bound Inheritance",
                markdown_table(
                    bounds,
                    [
                        "inherit_id",
                        "bound_family",
                        "observable",
                        "inherited_product_bound",
                        "bound_value",
                        "bound_units",
                        "score_status",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    [
                        "next_doc",
                        "next_script",
                        "objective",
                        "success_gate",
                        "forbidden_shortcuts",
                        "claim_allowed",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Validation",
                markdown_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {generated_timestamp()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    derivation_rows = hypermomentum_zero_derivation_rows()
    clause_rows = worldtube_clause_audit_rows()
    kernel_rows = source_hypermomentum_kernel_rows()
    bound_rows = product_bound_inheritance_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    write_csv(
        OUT / "P8_Y5_R2FR_3496_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3496_HYPERMOMENTUM_ZERO_DERIVATION.csv",
        derivation_rows,
        ["step_id", "claim_piece", "statement", "derivation", "status", "missing_to_promote", "source_path", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3496_WORLDTUBE_CLAUSE_AUDIT.csv",
        clause_rows,
        [
            "clause_id",
            "clause",
            "required_signature",
            "evidence_status",
            "if_unsigned_residual",
            "source_path",
            "zero_ready",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3496_SOURCE_HYPERMOMENTUM_KERNEL_VECTOR.csv",
        kernel_rows,
        [
            "kernel_id",
            "residual_symbol",
            "definition",
            "bound_formula",
            "required_inputs",
            "source_clause",
            "current_status",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3496_PRODUCT_BOUND_INHERITANCE.csv",
        bound_rows,
        [
            "inherit_id",
            "bound_family",
            "observable",
            "source_bound_id",
            "inherited_product_bound",
            "bound_value",
            "bound_units",
            "kernel_requirement",
            "source_reference",
            "score_status",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3496_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3496_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation = validation_rows(
        source_rows,
        derivation_rows,
        clause_rows,
        kernel_rows,
        bound_rows,
        decision_ledger_rows,
        next_rows,
    )
    write_csv(
        OUT / "P8_Y5_BRR545_3496_VALIDATION.csv",
        validation,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(derivation_rows, clause_rows, kernel_rows, bound_rows, decision_ledger_rows, next_rows, validation)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3523-Y5-R2FR-source-label-forgetting-functor-and-EM-Hodge-owner-or-marker-kernel-bound.md"
CANONICAL_STATUS = OUT / "P8_EM_source_label_forgetting_EM_Hodge_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3523": {"path": Path(__file__).resolve(), "role": "3523 generator"},
    "doc_3522": {
        "path": ROOT / "3522-Y5-R2FR-representative-identity-vs-global-symmetry-or-active-marker-bound.md",
        "role": "representative identity vs symmetry handoff",
    },
    "next_3522": {
        "path": OUT / "P8_Y5_R2FR_3522_NEXT_TARGET.csv",
        "role": "3522-selected source-label/EM-Hodge target",
    },
    "status_3522": {
        "path": OUT / "P8_EM_representative_identity_status.csv",
        "role": "canonical representative identity status",
    },
    "matter_2587": {
        "path": ROOT / "2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
        "role": "minimal parent matter action, single observed stack, no-source-slot contract",
    },
    "matter_contract_2587": {
        "path": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
        "role": "2587 matter action contract rows",
    },
    "sort_constructor_2688": {
        "path": ROOT / "2688-Y5-R2FR-parent-sort-constructor-from-MTS-primitives-or-delta-w-component-values.md",
        "role": "source-label forgetting and Delta_w constructor blocker",
    },
    "vertical_poynting_3115": {
        "path": ROOT / "3115-Y5-R2FR-local-vertical-Noether-generator-certificate-under-AX1090.md",
        "role": "EM/Hodge/Poynting readout and Hilbert-stress route",
    },
    "em_owner_1099": {
        "path": ROOT / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
        "role": "no-extra-F2/gauge-normalization owner and alpha residual guard",
    },
    "em_theorem_1099": {
        "path": OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
        "role": "1099 EM kinetic owner theorem attempt",
    },
    "alpha_rows_1099": {
        "path": OUT / "P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv",
        "role": "1099 alpha coefficient source rows",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def toy_kernel_rows() -> list[dict[str, Any]]:
    state = [1.0, 2.0, 5.0]
    relabelled = [5.0, 2.0, 1.0]
    common_weights = [1.0, 1.0, 1.0]
    source_weights = [1.0, 1.0, 1.1]
    common_state = sum(weight * value * value for weight, value in zip(common_weights, state))
    common_relabelled = sum(weight * value * value for weight, value in zip(common_weights, relabelled))
    weighted_state = sum(weight * value * value for weight, value in zip(source_weights, state))
    weighted_relabelled = sum(weight * value * value for weight, value in zip(source_weights, relabelled))
    beta = 0.02
    delta_x = 0.3
    z_em_leak = beta * delta_x
    rows = [
        {
            "test_id": "TK3523_0_common_source_weight",
            "channel": "matter_source_weight",
            "toy_quantity": "sum_A w_common h_A^2",
            "state_value": f"{common_state:.8g}",
            "relabelled_value": f"{common_relabelled:.8g}",
            "residual": f"{abs(common_state - common_relabelled):.8g}",
            "expected_result": "zero_if_common_mode",
            "meaning": "common source normalization forgets labels in the toy model",
            "valid_for_claim": "False",
        },
        {
            "test_id": "TK3523_1_source_label_weight",
            "channel": "matter_source_weight",
            "toy_quantity": "sum_A w_A h_A^2 with fixed source weights",
            "state_value": f"{weighted_state:.8g}",
            "relabelled_value": f"{weighted_relabelled:.8g}",
            "residual": f"{abs(weighted_state - weighted_relabelled):.8g}",
            "expected_result": "nonzero_if_fixed_source_label_survives",
            "meaning": "source-label coefficients reopen representative dependence",
            "valid_for_claim": "False",
        },
        {
            "test_id": "TK3523_2_EM_gauge_norm_marker",
            "channel": "EM_gauge_normalization",
            "toy_quantity": "delta log Z_EM = beta deltaX",
            "state_value": "0",
            "relabelled_value": f"{z_em_leak:.8g}",
            "residual": f"{abs(z_em_leak):.8g}",
            "expected_result": "nonzero_if_hidden_EM_marker_survives",
            "meaning": "a hidden marker in Z_EM creates alpha/Hodge/Poynting residual pressure",
            "valid_for_claim": "False",
        },
        {
            "test_id": "TK3523_3_public_Poynting_Hilbert_route",
            "channel": "EM_Hilbert_stress",
            "toy_quantity": "S^a=-h^a_mu T_EM^{mu nu} u_nu",
            "state_value": "defined_from_T_EM",
            "relabelled_value": "same_if_T_EM_q_owned",
            "residual": "0_if_Hodge_ZEM_q_owned_else_epsilon_EM",
            "expected_result": "Poynting_is_not_extra_source",
            "meaning": "Poynting belongs to public Maxwell Hilbert stress when Hodge and Z_EM descend through q",
            "valid_for_claim": "False",
        },
    ]
    return rows


def functor_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "FC3523_0_parent_observed_stack",
            "object": "Q_pub=q(Phi)",
            "required_statement": "The observed stack used by matter and EM is Q_pub=(g_pub/e_obs,D_obs,A_obs,tau,ell_J,Hodge) and is parent-owned before readout/fitting.",
            "derivation_if_signed": "All ordinary matter and EM actions can be written on public quotient objects rather than representative labels.",
            "current_status": "CONTRACT_AVAILABLE_NOT_PARENT_SIGNED",
            "blocks_if_missing": "q_stack, tau/ell_J, Hodge and current normalization residuals",
            "source_path": str(SOURCES["matter_2587"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "FC3523_1_source_label_forgetting_functor",
            "object": "F_src: Matter_parent -> Matter_public",
            "required_statement": "F_src maps labelled source/matter bundles to public matter fields plus fixed representation constants theta_A; no spacetime/source-dependent label weight survives.",
            "derivation_if_signed": "S_matter=sum_A S_A[psi_A;Q_pub,theta_A] has one Hilbert variation and J_H=q^*Jbar_H.",
            "current_status": "FUNCTOR_OWNER_NOT_DERIVED",
            "blocks_if_missing": "Delta_w_label, c_A current rescale, shadow source frame",
            "source_path": str(SOURCES["sort_constructor_2688"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "FC3523_2_no_source_only_slot",
            "object": "forbidden morphisms",
            "required_statement": "Hom_parent(SourceLabel/Marker/Readout, Coeff_active_source)=empty_or_common_mode before variation.",
            "derivation_if_signed": "w_A(X), c_A(X), source masks and shadow frames are not legal bulk parent terms.",
            "current_status": "NOHOM_EXACT_CONDITIONAL_ONLY",
            "blocks_if_missing": "source-dependent Newton/WEP/PPN/clock/orbital residuals",
            "source_path": str(SOURCES["matter_2587"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "FC3523_3_EM_Hodge_owner_functor",
            "object": "F_EM: Q_pub -> (*_q,Z_EM,T_Q)",
            "required_statement": "The Hodge star, gauge norm Z_EM, charge generator/lattice and current normalization are functions of q(Phi) or fixed representation data, not hidden/private labels.",
            "derivation_if_signed": "S_EM=-1/4 int mu_g Z_EM F^2 gives Maxwell Hilbert stress and no standalone alpha/Hodge/Poynting marker.",
            "current_status": "EM_OWNER_NOT_SIGNED",
            "blocks_if_missing": "b_alpha, delta_Hodge, constitutive tensor, Poynting/source residual",
            "source_path": str(SOURCES["em_owner_1099"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "FC3523_4_variation_before_readout",
            "object": "Hilbert/Maxwell variation order",
            "required_statement": "Functional derivatives are taken on the parent/public quotient action before support fitting, local calibration, arena projection or material readout.",
            "derivation_if_signed": "prevents fitted GM, post-readout current changes and external Poynting masks from manufacturing source coupling.",
            "current_status": "WORKFLOW_CONTRACT_NOT_PARENT_THEOREM",
            "blocks_if_missing": "domain-motion, support, boundary and calibration residuals",
            "source_path": str(SOURCES["matter_2587"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "DER3523_0_matter_source_descent",
            "statement": "If FC3523_0 through FC3523_2 and FC3523_4 hold, then source labels are forgotten before Hilbert variation.",
            "derivation": "With S_matter=sum_A S_A[psi_A;Q_pub,theta_A], variation gives T_H=sum_A delta S_A/delta Q_pub. Because label A appears only as fixed representation data theta_A and not as w_A(X), c_A(X) or a shadow frame, no vertical representative/source-label derivative contributes except common-mode normalization.",
            "consequence": "J_H=q^*Jbar_H conditionally; Delta_w_label and epsilon_source_slot theorem-zero if the parent functor is signed.",
            "current_status": "EXACT_CONDITIONAL_NOT_LIVE_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "DER3523_1_source_label_counterterm",
            "statement": "If a fixed source weight survives, representative identity fails in the source sector.",
            "derivation": "A term sum_A w_A(X)S_A is invariant only under simultaneous transformation of the physical source weights. With fixed labelled weights, relabelling the representative changes the source action by Delta S=sum_A w_A(S_A(pi.h)-S_A(h)), as TK3523_1 demonstrates.",
            "consequence": "Delta_w_label must be zero by theorem or carried into WEP/R10/PPN/clock/orbital kernels.",
            "current_status": "COUNTERTERM_RETAINED_AS_NONCLAIM_BOUND",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "DER3523_2_public_Maxwell_Poynting_lock",
            "statement": "If FC3523_3 holds, Poynting flux is part of public Maxwell Hilbert stress, not an extra source coupling.",
            "derivation": "For S_EM=-1/4 int mu_g Z_EM F_{mu nu}F^{mu nu}, metric variation gives T_EM^{mu nu}=Z_EM(F^mu_alpha F^{nu alpha}-1/4 g_pub^{mu nu}F^2). An observer Poynting vector is S^a=-h^a_mu T_EM^{mu nu}u_nu. Thus Poynting is already in the Hilbert source when g_pub, Hodge star and Z_EM are q-owned.",
            "consequence": "EM source coupling can reduce to GR Hilbert stress if Hodge/Z_EM/current normalization are quotient-owned.",
            "current_status": "EXACT_PUBLIC_ROUTE_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "DER3523_3_EM_hidden_marker_counterterm",
            "statement": "Gauge invariance alone does not kill hidden EM markers.",
            "derivation": "A term f_X(X_private)F^2 is covariant and U(1)-gauge invariant. Unless f_X is constant, sequestered, or q-owned, L_v log Z_EM produces alpha/clock/WEP/R10 and Poynting/source residuals.",
            "consequence": "No-extra-F2 or parent T_Q/gauge-norm owner must be signed; otherwise b_alpha and epsilon_EM remain finite.",
            "current_status": "COUNTERTERM_RETAINED_AS_NONCLAIM_BOUND",
            "valid_for_claim": "False",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3523_0_Qpub_owner",
            "gate": "single observed stack owner",
            "pass_condition": "q(Phi), e_obs/g_pub, D_obs, A_obs, tau, ell_J and Hodge are parent-owned before readout",
            "current_evidence": "2587 writes the contract; parent signature remains missing",
            "passed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3523_1_Fsrc_owner",
            "gate": "source-label forgetting functor",
            "pass_condition": "F_src exists and excludes source-only weights/current rescalings/shadow frames",
            "current_evidence": "2688 identifies this as missing hinge",
            "passed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3523_2_EM_owner",
            "gate": "EM Hodge/gauge norm owner",
            "pass_condition": "Hodge star, Z_EM, T_Q/charge lattice and current normalization are q-owned or fixed representation data",
            "current_evidence": "1099 no-extra-F2 theorem is conditional; 3115 Poynting route is conditional",
            "passed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3523_3_variation_order",
            "gate": "variation before readout/calibration",
            "pass_condition": "Hilbert and Maxwell variation occur before support fitting, arena kernels, local GM calibration or Poynting readout",
            "current_evidence": "workflow contract exists in 2587 but is not parent theorem",
            "passed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3523_4_total",
            "gate": "coupling owner closes",
            "pass_condition": "G3523_0 through G3523_3 pass together",
            "current_evidence": "no source signs all matter and EM owner clauses",
            "passed": "False",
            "valid_for_claim": "False",
        },
    ]


def kernel_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "KB3523_0_Delta_w_label",
            "channel": "matter/source-label",
            "symbol": "Delta_w_label",
            "formula": "Delta_w_label = P_perp w_source or 0 from signed F_src",
            "needed_inputs": "source composition vector, common-mode projector, parent source-label forgetting theorem, arena kernels",
            "units": "dimensionless",
            "source_path": str(SOURCES["sort_constructor_2688"]["path"]),
            "current_status": "MISSING_Fsrc_OR_NUMERIC_VALUES",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KB3523_1_epsilon_J",
            "channel": "Hilbert current normalization",
            "symbol": "epsilon_J",
            "formula": "epsilon_J <= ||c_A-c_common|| ||J_A|| + support/boundary/jump terms",
            "needed_inputs": "ell_J owner, current normalization theorem, support/jump ledger, source map",
            "units": "source_current_norm",
            "source_path": str(SOURCES["matter_2587"]["path"]),
            "current_status": "MISSING_CURRENT_OWNER_OR_BOUND",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KB3523_2_b_alpha",
            "channel": "EM gauge normalization",
            "symbol": "b_alpha",
            "formula": "b_alpha = L_v log Z_EM or 0 from no-extra-F2/T_Q owner",
            "needed_inputs": "T_Q owner, charge lattice, gauge norm, radiative/readout alpha map",
            "units": "dimensionless vertical derivative",
            "source_path": str(SOURCES["alpha_rows_1099"]["path"]),
            "current_status": "MISSING_EM_OWNER_OR_STANDALONE_BOUND",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KB3523_3_delta_Hodge_constitutive",
            "channel": "EM Hodge/constitutive readout",
            "symbol": "delta_star_chi",
            "formula": "||L_v *g|| + ||L_v chi_constitutive||",
            "needed_inputs": "public metric/Hodge owner, constitutive tensor owner, clock/spectral projection",
            "units": "operator_norm",
            "source_path": str(SOURCES["vertical_poynting_3115"]["path"]),
            "current_status": "MISSING_HODGE_CONSTITUTIVE_OWNER",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KB3523_4_Poynting_source_projection",
            "channel": "Poynting/Hilbert source projection",
            "symbol": "epsilon_Poynting",
            "formula": "epsilon_Poynting = ||D[-h T_EM u][v]|| with T_EM from q-owned Maxwell action, else finite kernel",
            "needed_inputs": "observer field, source support, EM stress map, Hodge/Z_EM owner, arena projection",
            "units": "stress_flux_norm",
            "source_path": str(SOURCES["vertical_poynting_3115"]["path"]),
            "current_status": "MISSING_POYNTING_PROJECTION_KERNEL",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3523_0_matter_functor_route",
            "quantity": "source_label_forgetting_functor",
            "value": "exact_conditional_contract",
            "meaning": "a signed F_src would remove source labels before Hilbert variation and conditionally produce universal source current",
            "claim_effect": "route to GR/Newton source coupling sharpened",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3523_1_EM_Poynting_route",
            "quantity": "Poynting_as_Maxwell_Hilbert_stress",
            "value": "exact_conditional_derivation",
            "meaning": "Poynting is not an extra source if Hodge/Z_EM/current normalization are q-owned",
            "claim_effect": "Maxwell/EM route tied to GR source stress",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3523_2_live_coupling_owner",
            "quantity": "coupling_owner_parent_signed_by_current_MTS",
            "value": "False",
            "meaning": "Q_pub owner, F_src, EM Hodge/gauge owner and variation-order theorem are not signed together",
            "claim_effect": "no local-GR/Newton/Maxwell/source-coupling claim",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3523_3_next_best",
            "quantity": "next_best_attack",
            "value": "observed_stack_and_charge_lattice_owner",
            "meaning": "the next smallest parent object is the shared observed stack plus EM charge/gauge norm owner",
            "claim_effect": "try to turn conditional matter/EM contract into a parent theorem",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3523_0_coupling_route",
            "decision": "keep F_src as exact theorem target",
            "rationale": "source-label forgetting before Hilbert variation is the cleanest way to avoid fitted source coupling",
            "effect": "local GR/Newton source universality has a concrete owner to derive",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3523_1_Poynting_route",
            "decision": "fold Poynting into Maxwell Hilbert stress when EM owner closes",
            "rationale": "Poynting flux is derived from T_EM, so it belongs in public source stress if Hodge/Z_EM descend through q",
            "effect": "your Poynting intuition is useful, but it becomes a quotient-ownership test",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3523_2_no_promotion",
            "decision": "do not promote live coupling owner",
            "rationale": "the current corpus has contracts and conditional derivations, not a signed shared owner",
            "effect": "retain marker kernels and attack observed-stack/charge-lattice ownership next",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3524-Y5-R2FR-observed-stack-and-charge-lattice-parent-owner-or-local-source-kernel-values.md",
            "next_script": "scripts/Y5_R2FR_3524_observed_stack_and_charge_lattice_parent_owner_or_local_source_kernel_values.py",
            "objective": "Try to parent-sign the shared observed stack q(Phi)->g/e/tau/ell_J/Hodge and the EM charge-lattice/gauge-norm owner; if it fails, fill local source-kernel value requirements for Delta_w, epsilon_J, b_alpha, delta_Hodge and Poynting projection.",
            "success_gate": "Either the shared observed stack plus charge/gauge owner is derived from MTS primitives, or each coupling residual has explicit source/unit/projection requirements and remains nonclaim.",
            "why_next": "3523 reduces the coupling problem to a shared parent owner rather than another broad audit.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    toys: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    derivations: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    toy_by_id = {row["test_id"]: row for row in toys}
    checks.append({"check_id": "VAL3523_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append(
        {
            "check_id": "VAL3523_1_toy_kernels_execute",
            "passed": bool_text(
                toy_by_id["TK3523_0_common_source_weight"]["residual"] == "0"
                and float(toy_by_id["TK3523_1_source_label_weight"]["residual"]) > 0
                and float(toy_by_id["TK3523_2_EM_gauge_norm_marker"]["residual"]) > 0
                and "T_EM" in toy_by_id["TK3523_3_public_Poynting_Hilbert_route"]["state_value"]
            ),
            "detail": "common source mode is silent; source-label and EM markers leak; Poynting routes through T_EM",
            "valid_for_claim": "False",
        }
    )
    checks.append({"check_id": "VAL3523_2_functor_contract_covers_matter_and_EM", "passed": bool_text(any(row["clause_id"] == "FC3523_1_source_label_forgetting_functor" for row in contracts) and any(row["clause_id"] == "FC3523_3_EM_Hodge_owner_functor" for row in contracts)), "detail": "F_src and F_EM clauses written", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3523_3_derives_Poynting_Hilbert_route", "passed": bool_text(any(row["derivation_id"] == "DER3523_2_public_Maxwell_Poynting_lock" and "Hilbert stress" in row["statement"] for row in derivations)), "detail": "Poynting is derived as Maxwell Hilbert-stress route conditionally", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3523_4_live_coupling_not_promoted", "passed": bool_text(any(row["gate_id"] == "G3523_4_total" and row["passed"] == "False" for row in gates) and any(row["status_id"] == "STAT3523_2_live_coupling_owner" and row["value"] == "False" for row in status)), "detail": "current MTS coupling owner remains unclaimed", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3523_5_kernel_bounds_nonclaim", "passed": bool_text(all(row["valid_for_claim"] == "False" and "MISSING" in row["current_status"] for row in kernels)), "detail": "source-label, current, alpha, Hodge and Poynting kernels remain nonclaim", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3523_6_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + toys + contracts + derivations + gates + kernels + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no local-GR/Newton/Maxwell/source-coupling claim is promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3523_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3524-Y5-R2FR-observed-stack-and-charge-lattice")), "detail": "3524 observed stack and charge lattice owner target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3523_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3523_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3523_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3523_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    toys: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    derivations: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3523 - Source Label Forgetting Functor And EM Hodge Owner Or Marker Kernel Bound

## Summary
- **Coupling result:** the clean route is now explicit. MTS gets universal source coupling only if a parent functor forgets source/representative labels before Hilbert variation.
- **Matter theorem target:** `F_src` must map labelled matter/source bundles to public matter fields plus fixed representation constants, with no `w_A(X)`, `c_A(X)`, source masks or shadow frames.
- **EM theorem target:** `F_EM` must own Hodge star, gauge normalization `Z_EM`, charge generator/lattice and current normalization through `q(Phi)` or fixed representation data.
- **Poynting placement:** Poynting is not an extra hidden force in the local branch; when `F_EM` closes it is the flux of Maxwell Hilbert stress. If Hodge or `Z_EM` leaks, Poynting becomes a residual channel.
- **Current verdict:** exact conditional route, not live claim. The missing object is now shared observed-stack plus charge/gauge owner, not another broad mystery.

## Core Contract
The parent action must have the local quotient-coupled form

`S_parent = S_geom[Phi] + sum_A S_A[psi_A; Q_pub(Phi), theta_A] - 1/4 int mu_g(Q_pub) Z_EM(Q_pub,theta_Q) F^2 + S_boundary[Q_pub]`

where `Q_pub=q(Phi)` owns the metric/coframe, derivative, clock, source scale, Hodge star and EM normalization before readout. Source labels may appear only as fixed representation constants `theta_A`, not as source-dependent bulk weights or current rescalings.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Toy Kernel Runner
{markdown_table(toys, ["test_id", "channel", "toy_quantity", "state_value", "relabelled_value", "residual", "expected_result", "meaning", "valid_for_claim"])}

## Functor Contract
{markdown_table(contracts, ["clause_id", "object", "required_statement", "derivation_if_signed", "current_status", "blocks_if_missing", "source_path", "valid_for_claim"])}

## Derivations And Counterterms
{markdown_table(derivations, ["derivation_id", "statement", "derivation", "consequence", "current_status", "valid_for_claim"])}

## Promotion Gates
{markdown_table(gates, ["gate_id", "gate", "pass_condition", "current_evidence", "passed", "valid_for_claim"])}

## Marker Kernel Bounds
{markdown_table(kernels, ["kernel_id", "channel", "symbol", "formula", "needed_inputs", "units", "source_path", "current_status", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    toys = toy_kernel_rows()
    contracts = functor_contract_rows()
    derivations = derivation_rows()
    gates = promotion_gate_rows()
    kernels = kernel_bound_rows()
    status = status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3523_SOURCE_REGISTER.csv",
        "toy_kernels": OUT / "P8_Y5_R2FR_3523_TOY_KERNEL_RUNNER.csv",
        "functor_contract": OUT / "P8_Y5_R2FR_3523_FUNCTOR_CONTRACT.csv",
        "derivations": OUT / "P8_Y5_R2FR_3523_DERIVATIONS_AND_COUNTERTERMS.csv",
        "promotion_gates": OUT / "P8_Y5_R2FR_3523_PROMOTION_GATES.csv",
        "kernel_bounds": OUT / "P8_Y5_R2FR_3523_MARKER_KERNEL_BOUNDS.csv",
        "status": OUT / "P8_Y5_R2FR_3523_SOURCE_LABEL_FORGETTING_EM_HODGE_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "decision_ledger": OUT / "P8_Y5_R2FR_3523_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3523_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3523_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["toy_kernels"], toys, ["test_id", "channel", "toy_quantity", "state_value", "relabelled_value", "residual", "expected_result", "meaning", "valid_for_claim"])
    write_csv(outputs["functor_contract"], contracts, ["clause_id", "object", "required_statement", "derivation_if_signed", "current_status", "blocks_if_missing", "source_path", "valid_for_claim"])
    write_csv(outputs["derivations"], derivations, ["derivation_id", "statement", "derivation", "consequence", "current_status", "valid_for_claim"])
    write_csv(outputs["promotion_gates"], gates, ["gate_id", "gate", "pass_condition", "current_evidence", "passed", "valid_for_claim"])
    write_csv(outputs["kernel_bounds"], kernels, ["kernel_id", "channel", "symbol", "formula", "needed_inputs", "units", "source_path", "current_status", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, toys, contracts, derivations, gates, kernels, status, decisions, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, toys, contracts, derivations, gates, kernels, status, decisions, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3524-Y5-R2FR-observed-stack-and-charge-lattice-parent-owner-or-local-source-kernel-values.md"
CANONICAL_STATUS = OUT / "P8_EM_observed_stack_charge_lattice_owner_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3524": {"path": Path(__file__).resolve(), "role": "3524 generator"},
    "doc_3523": {
        "path": ROOT / "3523-Y5-R2FR-source-label-forgetting-functor-and-EM-Hodge-owner-or-marker-kernel-bound.md",
        "role": "source-label forgetting and EM-Hodge handoff",
    },
    "next_3523": {
        "path": OUT / "P8_Y5_R2FR_3523_NEXT_TARGET.csv",
        "role": "3523-selected observed-stack/charge owner target",
    },
    "observed_stack_2588": {
        "path": ROOT / "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md",
        "role": "q/e_obs/tau/ell_J observed-stack conditional descent",
    },
    "observed_stack_cert_2588": {
        "path": OUT / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv",
        "role": "2588 owner certificate gates",
    },
    "observed_stack_audit_2588": {
        "path": OUT / "P8_Y5_OBS_STACK_2588_Q_OBSE_TAU_DESCENT_AUDIT.csv",
        "role": "2588 q/e_obs/tau descent audit",
    },
    "charge_owner_1100": {
        "path": ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
        "role": "T_Q fixed charge-lattice/gauge-norm signature",
    },
    "charge_signature_1100": {
        "path": OUT / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
        "role": "1100 T_Q/gauge-norm signature clauses",
    },
    "charge_theorem_1100": {
        "path": OUT / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
        "role": "1100 conditional T_Q theorem and countermodels",
    },
    "hodge_owner_3503": {
        "path": ROOT / "3503-Y5-R2FR-observed-Hodge-Maxwell-owner-and-total-Hilbert-current-closure-or-EM-bound.md",
        "role": "observed Hodge/Maxwell/Hilbert current owner chain",
    },
    "hodge_rule_3504": {
        "path": ROOT / "3504-Y5-R2FR-observed-Hodge-flow-rule-from-q-eobs-or-DeltaHodge-bound.md",
        "role": "Hodge uniqueness and q/e_obs chain rule",
    },
    "em_domain_3505": {
        "path": ROOT / "3505-Y5-R2FR-visible-EM-action-domain-exhaustion-no-chiEM-no-hidden-Hodge-or-bound.md",
        "role": "visible EM action-domain exhaustion target",
    },
    "em_owner_3465": {
        "path": ROOT / "3465-Y5-R2FR-EM-alpha-Hodge-charge-owner-or-WEP-raw-to-effective-map.md",
        "role": "EM owner audit plus alpha-only WEP bound",
    },
    "em_owner_audit_3465": {
        "path": OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
        "role": "3465 EM owner package audit",
    },
    "alpha_bound_3465": {
        "path": OUT / "P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv",
        "role": "3465 alpha-only effective WEP ceiling",
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


def owner_synthesis_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "OWN3524_0_Qpub",
            "parent_object": "Q_pub=q(Phi)",
            "required_components": "regular q map; parent-null kernel; basic e_obs; same-frame readout; tau identity; ell_J source scale; no shadow frame",
            "conditional_gain": "matter, clocks, rods, photons, orbital support and source current use one observed geometry/time/scale stack",
            "current_evidence": "2588 writes exact conditional descent and all certificate gates",
            "current_status": "CONTRACT_EXACT_BUT_OWNER_NOT_SIGNED",
            "source_path": str(SOURCES["observed_stack_2588"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN3524_1_Hodge",
            "parent_object": "*_obs[e_obs(q)]",
            "required_components": "e_obs q-basic; orientation fixed; EM action uses *_obs; no independent chi_EM/f_H/readout Hodge map",
            "conditional_gain": "Maxwell stress, light cone and Poynting flow use the same observed geometry as local source coupling",
            "current_evidence": "3504 proves Hodge uniqueness and q/e_obs chain rule conditionally",
            "current_status": "CONDITIONAL_ZERO_ROUTE_ACTION_DOMAIN_OPEN",
            "source_path": str(SOURCES["hodge_rule_3504"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN3524_2_TQ",
            "parent_object": "T_Q, charge lattice and gauge norm",
            "required_components": "parent T_Q object; fixed compact charge lattice/base unit; nonrescalable norm; unique F_Q^2; same current owner; readout/radiative closure",
            "conditional_gain": "b_alpha=0, Maxwell normalization fixed, Lorentz force/current and EM source stress share one owner",
            "current_evidence": "1100 gives exact conditional theorem but keeps norm/no-extra-F2/current/readout unsigned",
            "current_status": "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED",
            "source_path": str(SOURCES["charge_owner_1100"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN3524_3_total_Hilbert_current",
            "parent_object": "J_H_total = J_H_matter + J_H_EM + permitted boundary/radiative pieces",
            "required_components": "same Q_pub variation; same EM owner; matter-EM exchange cancellation; stationary exterior flux bound; natural Pi_M projector",
            "conditional_gain": "Poynting is source bookkeeping inside total Hilbert stress, while external flux becomes an explicit boundary kernel",
            "current_evidence": "3503 writes the exact total-current chain and bound vector",
            "current_status": "CONDITIONAL_TOTAL_CURRENT_CLOSURE_NOT_SIGNED",
            "source_path": str(SOURCES["hodge_owner_3503"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN3524_4_composite_owner",
            "parent_object": "Omega_local = (Q_pub,*_obs,T_Q,J_H_total)",
            "required_components": "OWN3524_0 through OWN3524_3 close together before readout/calibration",
            "conditional_gain": "local GR/Newton/Maxwell source coupling can be derived as one parent Hilbert-source branch rather than fitted sector weights",
            "current_evidence": "no inspected source signs all components together",
            "current_status": "COMPOSITE_OWNER_NOT_PARENT_DERIVED",
            "source_path": str(SOURCES["doc_3523"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def composite_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "COT3524_0_shared_owner_theorem",
            "claim": "Shared observed-stack plus charge/gauge owner derives universal local source coupling.",
            "formal_statement": "If Omega_local=(Q_pub,*_obs,T_Q,J_H_total) is parent-owned, all matter and EM actions factor through it before readout, and independent source/EM marker slots are absent, then the local source is the total Hilbert stress on the observed geometry.",
            "derivation": "Variation of S_matter[psi;Q_pub,theta] and S_EM[A_Q,*_obs(Q_pub),Z_EM(T_Q)] with respect to Q_pub gives T_total. Matter-EM Lorentz exchange cancels inside nabla_mu T_total^{mu nu}; Poynting is T_EM^{0i}; source labels and EM normalizations cannot vary independently because they are fixed representation/parent data.",
            "current_status": "EXACT_CONDITIONAL_COMPOSITE_THEOREM",
            "effect_if_signed": "J_H=q^*Jbar_H, Delta_w_label=0, epsilon_J=0, b_alpha=0, Delta_Hodge=0 and Poynting source projection becomes ordinary Hilbert stress modulo external flux bounds.",
            "fires_for_live_mts": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "COT3524_1_hodge_not_scale_owner",
            "claim": "Hodge uniqueness alone does not fix Newton/source normalization.",
            "formal_statement": "In 4D, Maxwell two-form Hodge agreement can preserve light cones while leaving conformal/source/charge-current scale open.",
            "derivation": "3504's conformal caveat: g->Omega^2 g leaves * on 2-forms invariant, so e_obs/Hodge success must be paired with tau, ell_J, T_Q and current normalization owners.",
            "current_status": "NO_OVERCLAIM_GUARD_ACTIVE",
            "effect_if_signed": "prevents claiming local GR/Newton from EM light-cone/Hodge matching alone",
            "fires_for_live_mts": "True",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "COT3524_2_charge_norm_countermodel",
            "claim": "Compact U(1) labels alone do not fix alpha/source coupling.",
            "formal_statement": "Integer charge labels do not determine the absolute base charge/gauge norm unless T_Q's norm and unique F_Q^2 owner are parent-fixed.",
            "derivation": "1100 retains T_Q->sT_Q and independent lambda_A F_Q^2 countermodels; both leave formal gauge structure intact while changing physical normalization.",
            "current_status": "COUNTERMODEL_RETAINED",
            "effect_if_signed": "forces charge/gauge norm ownership rather than unit-rescaling alpha away",
            "fires_for_live_mts": "True",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "COT3524_3_value_backstop",
            "claim": "If the composite owner does not close, local tests require kernel values not broad prose.",
            "formal_statement": "Retained channels must be represented by Delta_w_label, epsilon_J, b_alpha, Delta_Hodge, epsilon_Poynting and their arena kernels with units, source paths and no-cancellation policy.",
            "derivation": "Each missing owner component has a measurable transfer: WEP/R10/PPN/clock/orbital/source-normalization/Maxwell light-cone/Poynting flux.",
            "current_status": "FINITE_VALUE_REQUIREMENTS_STAGED",
            "effect_if_signed": "turns the failure branch into empirical plumbing rather than another closure paragraph",
            "fires_for_live_mts": "True",
            "valid_for_claim": "False",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3524_0_q_stack_owner",
            "gate": "Q_pub owner",
            "pass_condition": "q map, kernel, e_obs, tau, ell_J and no-shadow frame close together",
            "current_status": "False",
            "blocking_source": "2588: OSA2588_7 / OSC2588_0..7",
            "if_failed": "epsilon_q_owner, epsilon_DObs_e, epsilon_tau_selector, epsilon_ellJ_scale, shadow/readout residuals",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3524_1_hodge_owner",
            "gate": "observed Hodge owner",
            "pass_condition": "e_obs q-basic plus fixed orientation plus EM action-domain excludes independent chi_EM/hidden Hodge/readout Hodge",
            "current_status": "False",
            "blocking_source": "3504: HFR3504_6 / HSG3504 gates",
            "if_failed": "Delta_Hodge_EM, Delta_chi, hidden/disformal Hodge, readout Hodge",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3524_2_charge_gauge_owner",
            "gate": "T_Q/charge/gauge norm owner",
            "pass_condition": "T_Q object, fixed lattice/base unit, fixed norm, unique F2, same current owner and readout/radiative guard close",
            "current_status": "False",
            "blocking_source": "1100: TQS1100_6",
            "if_failed": "b_alpha, w_EM, C_XF2, C_JQ, current rescale",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3524_3_total_hilbert_current",
            "gate": "total Hilbert source current",
            "pass_condition": "matter plus EM total current closes; Pi_M natural; no external/radiative Poynting leakage or it is bounded",
            "current_status": "False",
            "blocking_source": "3503: THC3503_4..6",
            "if_failed": "Delta_J_total, Delta_PiM_metric, Phi_EM_rad",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3524_4_total",
            "gate": "composite local source owner",
            "pass_condition": "G3524_0 through G3524_3 pass together before readout/calibration",
            "current_status": "False",
            "blocking_source": "3524 synthesis",
            "if_failed": "no derived local-GR/Newton/Maxwell/source-coupling claim; use kernel values",
            "valid_for_claim": "False",
        },
    ]


def kernel_value_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "KV3524_0_Delta_w_label",
            "channel": "source-label/material weight",
            "required_value": "Delta_w_label or theorem-zero",
            "formula": "Delta_w_label=P_perp w_source; use sum_abs envelope until covariance source exists",
            "units": "dimensionless",
            "source_or_owner_needed": "F_src / source-label forgetting theorem or material/source weight prior",
            "projection_needed": "WEP/R10/PPN/clock/orbital arena kernels",
            "current_status": "MISSING_VALUE_OR_THEOREM_ZERO",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KV3524_1_epsilon_J",
            "channel": "Hilbert current/source normalization",
            "required_value": "epsilon_J or theorem-zero",
            "formula": "epsilon_J <= ||c_A-c_common|| ||J_A|| + support/boundary/jump/source-current scale terms",
            "units": "source_current_norm_or_dimensionless_after_MHref",
            "source_or_owner_needed": "ell_J owner, same-frame M_H_ref, source-current owner and support ledger",
            "projection_needed": "Newton/PPN/orbital/source-normalization map",
            "current_status": "MISSING_CURRENT_OWNER_OR_NUMERIC_BOUND",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KV3524_2_b_alpha",
            "channel": "EM gauge normalization",
            "required_value": "b_alpha standalone or theorem-zero",
            "formula": "b_alpha=L_v log Z_EM; zero if T_Q/gauge norm/no-extra-F2/readout guard closes",
            "units": "dimensionless_vertical_derivative",
            "source_or_owner_needed": "T_Q owner, fixed norm, unique F2, current owner, radiative/readout closure",
            "projection_needed": "clock/WEP/R10/spectroscopy tau and material maps",
            "current_status": "MISSING_STANDALONE_VALUE;ALPHA_ONLY_WEP_EFFECTIVE_BOUND_EXISTS_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KV3524_3_Delta_Hodge_EM",
            "channel": "EM Hodge/constitutive",
            "required_value": "Delta_Hodge_EM components or theorem-zero",
            "formula": "*_EM-*_obs[e_obs(q)] plus chi_principal/skewon/axion/hidden/readout/conformal/orientation components",
            "units": "tensor_dimensionless_or_component_declared",
            "source_or_owner_needed": "visible EM action-domain exhaustion and no independent constitutive/Hodge/background/readout map",
            "projection_needed": "Maxwell limit, light-cone, birefringence, Poynting, clock, PPN",
            "current_status": "CONDITIONAL_ZERO_ROUTE_NOT_CLAIMED;COMPONENT_BOUNDS_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KV3524_4_epsilon_Poynting",
            "channel": "Poynting/source projection",
            "required_value": "epsilon_Poynting or theorem-zero",
            "formula": "epsilon_Poynting=||D[-h^a_mu T_EM^{mu nu}u_nu][v]|| plus boundary flux Phi_EM_rad/(G_ref M_H)",
            "units": "stress_flux_norm_or_dimensionless_after_MHref",
            "source_or_owner_needed": "observed Hodge owner, charge/current owner, stationary exterior/source support, boundary flux convention",
            "projection_needed": "Gdot/clock/local source drift/orbital source normalization",
            "current_status": "MISSING_POYNTING_PROJECTION_AND_FLUX_VALUE",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KV3524_5_alpha_only_WEP_bound_import",
            "channel": "existing nonclaim numeric bound",
            "required_value": "|D_e_eff| <= 1.407170315973e-12",
            "formula": "D_e_eff_abs_bound = eta_TiPt_bound / Delta_Q_alpha_Coulomb_abs",
            "units": "dimensionless",
            "source_or_owner_needed": str(SOURCES["alpha_bound_3465"]["path"]),
            "projection_needed": "alpha-only isolated WEP source-leg assumption; full material tensor still deferred",
            "current_status": "NUMERIC_NONCLAIM_BOUND_AVAILABLE_NOT_MTS_PREDICTION",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3524_0_composite_theorem",
            "quantity": "shared_owner_derives_local_source_coupling",
            "value": "exact_conditional",
            "meaning": "if Q_pub, observed Hodge, T_Q/gauge norm and total Hilbert current are one parent owner, matter+EM source coupling reduces to total Hilbert stress",
            "claim_effect": "strongest current derivation route to local GR/Newton/Maxwell source coupling",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3524_1_live_owner",
            "quantity": "composite_owner_parent_signed_by_current_MTS",
            "value": "False",
            "meaning": "2588, 1100, 3503 and 3504 each provide conditional clauses, but no source signs all together",
            "claim_effect": "no derived local-GR/Newton/Maxwell/source-coupling claim",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3524_2_value_branch",
            "quantity": "local_kernel_value_requirements",
            "value": "staged",
            "meaning": "Delta_w, epsilon_J, b_alpha, Delta_Hodge and Poynting kernels now have explicit value/source/unit/projection requirements",
            "claim_effect": "failure branch is test-plumbed rather than left as broad missing prose",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3524_3_next_best",
            "quantity": "next_best_attack",
            "value": "visible_EM_action_domain_or_q_stack_owner_first",
            "meaning": "the tightest derivation fork is either forbid independent EM constitutive/F2 slots or prove q/e_obs/tau/ell_J parent ownership",
            "claim_effect": "continue by trying one parent owner clause rather than recircling the full ladder",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3524_0_synthesis",
            "decision": "promote the composite owner as the next theorem target, not as a claim",
            "rationale": "2588/1100/3503/3504 fit together into one parent-object throat",
            "effect": "the route to GR/Newton/Maxwell source coupling is now one shared owner problem",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3524_1_guard",
            "decision": "do not infer source normalization from Hodge/light-cone or compact charge labels alone",
            "rationale": "3504 conformal caveat and 1100 rescaling countermodel both block that shortcut",
            "effect": "prevents fake victory from mathematically pretty but under-owned pieces",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3524_2_backstop",
            "decision": "stage kernel value rows if the owner remains unsigned",
            "rationale": "the empirical route needs values/projections, not another missing paragraph",
            "effect": "sets up future R10/WEP/PPN/clock/orbital/Maxwell tests without claim leakage",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3525-Y5-R2FR-visible-EM-action-domain-exhaustion-or-q-stack-owner-first-branch.md",
            "next_script": "scripts/Y5_R2FR_3525_visible_EM_action_domain_exhaustion_or_q_stack_owner_first_branch.py",
            "objective": "Choose and execute the tighter first owner proof: either visible EM action-domain exhaustion forbids independent chi_EM/f_H/lambda F2/readout Hodge slots, or q/e_obs/tau/ell_J parent ownership closes the observed stack first.",
            "success_gate": "One owner clause is parent-signed or the corresponding residual component row gains explicit numeric/source/unit/projection requirements.",
            "why_next": "3524 shows the whole branch cannot close at once; the least circular next step is to close one owner clause cleanly.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3524_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3524_1_composite_owner_written", "passed": bool_text(any(row["owner_id"] == "OWN3524_4_composite_owner" for row in owners) and any(row["theorem_id"] == "COT3524_0_shared_owner_theorem" for row in theorems)), "detail": "composite owner and conditional theorem are present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3524_2_uses_2588_1100_3504_chain", "passed": bool_text(any("2588" in row["source_path"] for row in owners) and any("1100" in row["source_path"] for row in owners) and any("3504" in row["source_path"] for row in owners)), "detail": "observed stack, charge/gauge owner and Hodge chain-rule sources are all used", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3524_3_live_owner_not_promoted", "passed": bool_text(any(row["gate_id"] == "G3524_4_total" and row["current_status"] == "False" for row in gates) and any(row["status_id"] == "STAT3524_1_live_owner" and row["value"] == "False" for row in status)), "detail": "composite owner remains nonclaim", "valid_for_claim": "False"})
    required_kernel_ids = {"KV3524_0_Delta_w_label", "KV3524_1_epsilon_J", "KV3524_2_b_alpha", "KV3524_3_Delta_Hodge_EM", "KV3524_4_epsilon_Poynting"}
    checks.append({"check_id": "VAL3524_4_kernel_requirements_complete", "passed": bool_text({row["kernel_id"] for row in kernels} >= required_kernel_ids), "detail": "Delta_w, epsilon_J, b_alpha, Delta_Hodge and Poynting kernel requirements present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3524_5_numeric_nonclaim_bound_imported", "passed": bool_text(any(row["kernel_id"] == "KV3524_5_alpha_only_WEP_bound_import" and "1.407170315973e-12" in row["required_value"] for row in kernels)), "detail": "existing alpha-only WEP nonclaim bound imported as value evidence", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3524_6_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + owners + theorems + gates + kernels + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no local-GR/Newton/Maxwell/source-coupling claim is promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3524_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3525-Y5-R2FR-visible-EM-action-domain")), "detail": "3525 owner-clause-first branch selected", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3524_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3524_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3524_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3524_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3524 - Observed Stack And Charge Lattice Parent Owner Or Local Source Kernel Values

## Summary
- **Composite theorem target:** the local GR/Newton/Maxwell source route now reduces to one shared parent owner: `Omega_local=(Q_pub,*_obs,T_Q,J_H_total)`.
- **Derived conditional:** if this owner is signed before readout/calibration, matter plus EM source coupling is the total Hilbert stress on the observed geometry; Poynting is included as Maxwell stress flux.
- **No shortcut:** Hodge/light-cone matching does not fix source normalization, and compact charge labels do not fix alpha/gauge norm without a parent norm/no-extra-`F²` owner.
- **Current verdict:** the composite theorem is exact conditionally but not live-claimable; the current corpus has all pieces as conditional clauses, not one parent-signed object.
- **Backstop progress:** the failure branch now has explicit kernel value requirements, including the existing nonclaim alpha-only WEP ceiling.

## Composite Owner Equation
`Omega_local = (Q_pub=q(Phi), *_obs[e_obs(q)], T_Q/N_Q/Z_EM, J_H_total)`

`S_local = S_geom[Q_pub] + S_matter[psi;Q_pub,theta] - 1/4 int mu(Q_pub) Z_EM(T_Q,N_Q) F_Q^2 + S_boundary[Q_pub]`

If every term factors through `Omega_local` before readout, then the local source is `T_total = T_matter + T_EM`, with `T_EM` carrying the Poynting flux. If any component is independently labelled, it becomes a kernel rather than a derivation.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Owner Synthesis
{markdown_table(owners, ["owner_id", "parent_object", "required_components", "conditional_gain", "current_evidence", "current_status", "source_path", "valid_for_claim"])}

## Composite Theorems
{markdown_table(theorems, ["theorem_id", "claim", "formal_statement", "derivation", "current_status", "effect_if_signed", "fires_for_live_mts", "valid_for_claim"])}

## Promotion Gates
{markdown_table(gates, ["gate_id", "gate", "pass_condition", "current_status", "blocking_source", "if_failed", "valid_for_claim"])}

## Kernel Value Requirements
{markdown_table(kernels, ["kernel_id", "channel", "required_value", "formula", "units", "source_or_owner_needed", "projection_needed", "current_status", "valid_for_claim"])}

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
    owners = owner_synthesis_rows()
    theorems = composite_theorem_rows()
    gates = gate_rows()
    kernels = kernel_value_rows()
    status = status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3524_SOURCE_REGISTER.csv",
        "owner_synthesis": OUT / "P8_Y5_R2FR_3524_OWNER_SYNTHESIS.csv",
        "composite_theorems": OUT / "P8_Y5_R2FR_3524_COMPOSITE_THEOREMS.csv",
        "promotion_gates": OUT / "P8_Y5_R2FR_3524_PROMOTION_GATES.csv",
        "kernel_value_requirements": OUT / "P8_Y5_R2FR_3524_KERNEL_VALUE_REQUIREMENTS.csv",
        "status": OUT / "P8_Y5_R2FR_3524_OBSERVED_STACK_CHARGE_OWNER_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "decision_ledger": OUT / "P8_Y5_R2FR_3524_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3524_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3524_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["owner_synthesis"], owners, ["owner_id", "parent_object", "required_components", "conditional_gain", "current_evidence", "current_status", "source_path", "valid_for_claim"])
    write_csv(outputs["composite_theorems"], theorems, ["theorem_id", "claim", "formal_statement", "derivation", "current_status", "effect_if_signed", "fires_for_live_mts", "valid_for_claim"])
    write_csv(outputs["promotion_gates"], gates, ["gate_id", "gate", "pass_condition", "current_status", "blocking_source", "if_failed", "valid_for_claim"])
    write_csv(outputs["kernel_value_requirements"], kernels, ["kernel_id", "channel", "required_value", "formula", "units", "source_or_owner_needed", "projection_needed", "current_status", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, owners, theorems, gates, kernels, status, decisions, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, owners, theorems, gates, kernels, status, decisions, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()

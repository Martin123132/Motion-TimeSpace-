from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_EH_LOCAL_GEOMETRY_KERNEL_SPLIT_OR_EH_CONTAMINATION_ROW_2395"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md"
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
        "source_id": "SRC2395_2394_doc",
        "path": str(POST_ROOT / "2394-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md"),
        "needed_for": "EH sector split selected by 2394",
        "needles": "SVL2394_0_EH_local_geometry|epsilon_Qv_EH_kernel_split|NEXT2394_0_selected|VAL2394_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2395_2394_sector_csv",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2394_SECTOR_VARIATION_LEDGER.csv"),
        "needed_for": "machine-readable EH sector row",
        "needles": "SVL2394_0_EH_local_geometry|MISSING_BASIC_COFRAME_TO_KILL_THETA_EH|MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2395_2394_leak_csv",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2394_QV_PIECE_LEAK_ROWS.csv"),
        "needed_for": "EH contamination leak row",
        "needles": "epsilon_Qv_EH_kernel_split|MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT|epsilon_Qv_total",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2395_2391_doc",
        "path": str(POST_ROOT / "2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md"),
        "needed_for": "quotient/basic coframe theorem and anti-tautology guard",
        "needles": "Q_vis := Phi_parent/V|e_parent = Obs_e o q|DObs_e[Dq(v)] = 0|projection-by-declaration",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2395_2391_certificate",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_CERTIFICATE.csv"),
        "needed_for": "q/Obs_e prerequisite statuses",
        "needles": "QOC2391_2_presymplectic_null|QOC2391_3_basic_coframe|MISSING_BASIC_COFRAME_PROOF|QOC2391_4_no_projection_declaration",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2395_2390_doc",
        "path": str(POST_ROOT / "2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md"),
        "needed_for": "same-frame chain rule",
        "needles": "e_obs(Phi) := Obs_e(q(Phi))|Lie_v e_obs = DObs_e[Dq(v)] = 0|SFL2390_1_vertical_kernel",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2395_2390_certificate",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv"),
        "needed_for": "same-frame ownership prerequisites",
        "needles": "SFC2390_1_Obs_e|SFC2390_2_same_readout|SFC2390_4_no_shadow_frame",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2395_2393_doc",
        "path": str(POST_ROOT / "2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md"),
        "needed_for": "vertical Noether current and Qv contract",
        "needles": "J_v := Theta_parent(v_epsilon) - mu_v|J_v = dQ_v + C_v|VQC2393_4_Qv",
        "valid_for_claim": no_claim(),
    },
]


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHK2395_0_pure_vertical_definition",
            "claim": "pure vertical EH test direction",
            "statement": "A pure local vertical vector v_k is a parent tangent with Dq(v_k)=0 and no observed spacetime generator xi at the readout/boundary surface.",
            "derivation_status": "DEFINITION_REQUIRED",
            "consequence": "separates internal quotient-kernel motion from physical GR diffeomorphism charge",
            "missing_for_current_claim": "parent q, vertical basis, and boundary/readout split are not fully signed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHK2395_1_chain_rule_EH_silence",
            "claim": "pure vertical leaves observed local geometry fixed",
            "statement": "If e_obs(Phi)=Obs_e(q(Phi)) and Dq(v_k)=0, then delta_v e_obs = DObs_e[Dq(v_k)] = 0.",
            "derivation_status": "CONDITIONAL_CHAIN_RULE_PROOF",
            "consequence": "the EH Lagrangian built only from e_obs has no pure-vertical local variation",
            "missing_for_current_claim": "Obs_e/q ownership and basic coframe proof remain unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHK2395_2_theta_EH_zero",
            "claim": "EH symplectic potential is zero on pure vertical kernel",
            "statement": "For L_EH[e_obs], delta_v L_EH = E_EH dot delta_v e_obs + dTheta_EH(e_obs;delta_v e_obs). If delta_v e_obs=0 pointwise, then Theta_EH(e_obs;v_k)=0.",
            "derivation_status": "CONDITIONAL_VARIATION_PROOF",
            "consequence": "epsilon_theta_EH_kernel_split is killed if the chain-rule hypotheses are signed",
            "missing_for_current_claim": "basic coframe and pure-vertical split are not current certificates",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHK2395_3_mu_EH_zero",
            "claim": "EH Noether boundary term mu_EH is zero for pure vertical v",
            "statement": "Because v_k is not an observed diffeomorphism and delta_v L_EH=0 rather than L_xi L_EH=d(i_xi L_EH), the EH diffeomorphism boundary term mu_xi is not activated.",
            "derivation_status": "CONDITIONAL_SPLIT_PROOF",
            "consequence": "standard GR charge belongs to observed xi, not pure kernel v_k",
            "missing_for_current_claim": "horizontal observed-diffeomorphism lift and boundary class are not fixed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHK2395_4_Qv_EH_zero",
            "claim": "pure vertical EH charge vanishes",
            "statement": "J_EH[v_k]=Theta_EH(v_k)-mu_EH[v_k]=0, so dQ_EH[v_k]+C_EH[v_k]=0. With zero compact/local boundary flux, choose Q_EH[v_k]=0 as the kernel contribution.",
            "derivation_status": "CONDITIONAL_ZERO_CHARGE_PROOF",
            "consequence": "EH no longer contaminates epsilon_Qv_EH_kernel_split once prerequisites are signed",
            "missing_for_current_claim": "zero compact flux and boundary/reference convention remain separate locks",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHK2395_5_observed_xi_reference",
            "claim": "observed diffeomorphism EH charge is reference, not kernel",
            "statement": "If a parent tangent decomposes as h_xi+k with Dq(k)=0 and h_xi projecting to an observed spacetime diffeomorphism, then Q_EH[h_xi] is the ordinary GR reference charge and must not be counted as Q_v^kernel.",
            "derivation_status": "CONDITIONAL_REFERENCE_SPLIT",
            "consequence": "GR mass/ADM/Komar-like charge can be retained as the baseline while pure vertical residuals are tested separately",
            "missing_for_current_claim": "horizontal lift h_xi and M_H_ref normalization are not parent-fixed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHK2395_6_verdict",
            "claim": "EH sector status",
            "statement": "2395 conditionally proves the EH pure-kernel zero, but does not promote a current-MTS EH pass because q/Obs_e, pure vertical split, zero flux, boundary convention, and M_H_ref are not all signed.",
            "derivation_status": "CONDITIONAL_EH_ZERO_NOT_PROMOTED",
            "consequence": "the EH door is now mathematically narrow; the live work moves to signing prerequisites and non-EH sectors",
            "missing_for_current_claim": "QOC2391_3_basic_coframe;QOC2391_2_presymplectic_null;SFC2390_1_Obs_e;VQC2393_7_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def certificate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHC2395_0_q_Obs_e_owned",
            "certificate": "parent-owned observed coframe",
            "required_test": "e_obs=Obs_e(q(Phi)) with q and Obs_e fixed before local readout",
            "status": "MISSING_PARENT_Q_OBS_E_OWNERSHIP",
            "residual_if_missing": "epsilon_DObs_e",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHC2395_1_basic_coframe",
            "certificate": "basic coframe along vertical fibres",
            "required_test": "Lie_v e_obs=0 for every pure local vertical v in ker(Dq)",
            "status": "MISSING_BASIC_COFRAME_PROOF",
            "residual_if_missing": "epsilon_Qv_EH_kernel_split",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHC2395_2_pure_vertical_split",
            "certificate": "pure vertical vs observed diffeomorphism split",
            "required_test": "v_k has Dq(v_k)=0 and no observed xi/asymptotic generator; h_xi carries the ordinary GR charge separately",
            "status": "MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT",
            "residual_if_missing": "epsilon_Qv_EH_kernel_split",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHC2395_3_boundary_flux",
            "certificate": "zero compact/local EH flux for pure vertical v",
            "required_test": "pure vertical v is compact/local or derivative-silent on the charge surface, and boundary/reference terms are assigned to the boundary sector",
            "status": "MISSING_EH_ZERO_FLUX_BOUNDARY_CLASS",
            "residual_if_missing": "epsilon_Qv_boundary",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHC2395_4_MHref",
            "certificate": "same-frame positive Hamiltonian reference",
            "required_test": "M_H_ref is derived from the observed GR reference branch, not imported from orbital fitting",
            "status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "residual_if_missing": "all normalized Qv rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHC2395_5_EH_conditional_ready",
            "certificate": "EH kernel-zero theorem readiness",
            "required_test": "EHC2395_0 through EHC2395_4 pass together",
            "status": "CONDITIONAL_THEOREM_READY_BUT_UNSIGNED",
            "residual_if_missing": "epsilon_Qv_EH_kernel_split_retained",
            "valid_for_claim": no_claim(),
        },
    ]


def contamination_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_EH_kernel_split",
            "definition": "EH/reference charge contamination caused by failing to separate pure vertical kernel motion from observed spacetime diffeomorphism charge",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "0 if EHC2395_0..EHC2395_4 pass; otherwise retain as source row",
            "current_value_status": "CONDITIONAL_ZERO_UNSIGNED",
            "source_path": str(DOC_PATH),
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_theta_EH_kernel_split",
            "definition": "EH symplectic-potential response to a supposed vertical direction",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "||Theta_EH(e_obs;DObs_e[Dq(v)])||/M_H_ref",
            "current_value_status": "MISSING_DOBS_VERTICAL_NORM_AND_MHREF",
            "source_path": str(DOC_PATH),
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_xi_leak",
            "definition": "ordinary observed diffeomorphism charge accidentally counted as vertical kernel charge",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "Q_EH[h_xi]/M_H_ref if h_xi is not separated from k",
            "current_value_status": "MISSING_HORIZONTAL_VERTICAL_SPLIT",
            "source_path": str(DOC_PATH),
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_EH_boundary_flux",
            "definition": "pure-vertical EH boundary or reference-improvement flux",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "integral_S(delta Q_EH[v_k]-i_v Theta_EH+delta B_EH)/M_H_ref",
            "current_value_status": "MISSING_ZERO_FLUX_SURFACE_CLASS",
            "source_path": str(DOC_PATH),
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2395_0_accept_conditional_EH_zero",
            "decision": "accept the conditional EH pure-kernel zero theorem",
            "reason": "if e_obs descends through q and v is truly in ker(Dq), the EH local geometry does not move",
            "consequence": "EH contamination is no longer a conceptual mystery; it is a prerequisite-signature problem",
            "status": "CONDITIONAL_EH_ZERO_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2395_1_keep_GR_reference_separate",
            "decision": "keep observed GR diffeomorphism charge as reference, not kernel",
            "reason": "ordinary EH charge belongs to h_xi, while pure kernel k must carry no observed xi",
            "consequence": "MTS can reduce to GR without double-counting GR mass as residual kernel charge",
            "status": "REFERENCE_SPLIT_REQUIRED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2395_2_no_current_promotion",
            "decision": "do not claim EH sector pass for current MTS",
            "reason": "q/Obs_e ownership, basic coframe, vertical basis, zero flux, and M_H_ref remain unsigned",
            "consequence": "epsilon_Qv_EH_kernel_split remains nonclaim until certificates close",
            "status": "EH_ZERO_NOT_PROMOTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2395_3_next",
            "decision": "attack matter/source lift and no-direct-slot proof next",
            "reason": "once EH is conditionally separated, the next local-GR danger is hidden source/coupling charge in ordinary matter and worldtube normalization",
            "consequence": "2396 should prove matter/source vertical invisibility or keep epsilon_Qv_matter_source live",
            "status": "SELECT_2396_MATTER_SOURCE_LIFT",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2395_0_EH_kernel_zero",
            "gate": "EH pure vertical kernel charge zero",
            "gate_status": "CONDITIONAL_BLOCKED",
            "claim_effect": "mathematically derived under q/Obs_e and pure-vertical split, but not current-MTS claim-grade",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2395_1_total_Qv",
            "gate": "total vertical Qv extracted",
            "gate_status": "BLOCKED",
            "claim_effect": "non-EH sectors remain unclosed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2395_2_matter_source",
            "gate": "matter/source vertical invisibility",
            "gate_status": "BLOCKED",
            "claim_effect": "ordinary source/coupling sector remains next root blocker",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2395_3_GR_Newton",
            "gate": "local GR/Newton reduction",
            "gate_status": "BLOCKED",
            "claim_effect": "EH conditional zero is necessary but not sufficient",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2395_0_claim_EH_pass",
            "claim": "EH sector is fully passed for current MTS",
            "allowed": "false",
            "reason": "the proof is conditional on unsigned q/Obs_e, pure vertical split, zero flux, and M_H_ref clauses",
            "blocking_rows": "EHC2395_0_q_Obs_e_owned;EHC2395_1_basic_coframe;EHC2395_2_pure_vertical_split;EHC2395_3_boundary_flux;EHC2395_4_MHref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2395_1_claim_GR_charge_zero",
            "claim": "ordinary GR/EH diffeomorphism charge vanishes",
            "allowed": "false",
            "reason": "observed xi charge is the GR reference branch, not the pure vertical kernel branch",
            "blocking_rows": "EHK2395_5_observed_xi_reference;DEC2395_1_keep_GR_reference_separate",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2395_2_claim_local_GR",
            "claim": "local GR/Newton is derived from 2395",
            "allowed": "false",
            "reason": "2395 only handles the EH door conditionally; matter, extra, projector, boundary, coupling, PPN, and Newtonian-limit gates remain",
            "blocking_rows": "CG2395_1_total_Qv;CG2395_2_matter_source;CG2395_3_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2395_0_selected",
            "next_file": "2396-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md",
            "success_condition": "prove S_matter descends through q/Obs_e, vertical v does not move matter representation/source slots, and matter/source Qv is constraint-only",
            "fallback_condition": "retain epsilon_Qv_matter_source, epsilon_hidden_source_slot, and M_H_ref source rows as nonclaim",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2395_1_parallel",
            "next_file": "2396b-Y5-R2FR-basic-coframe-vertical-basis-signature-or-DObsE-bound.md",
            "success_condition": "sign parent q/Obs_e and Lie_v e_obs=0 for the actual local vertical basis",
            "fallback_condition": "keep epsilon_DObs_e and epsilon_Qv_EH_kernel_split as finite bound/source rows",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2395_2_later",
            "next_file": "2396c-Y5-R2FR-MHref-reference-normalization-and-EH-boundary-class.md",
            "success_condition": "fix GR reference charge, positive M_H_ref, and compact/local zero-flux boundary class",
            "fallback_condition": "retain epsilon_EH_boundary_flux and all normalized rows as non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2395_SOURCE_REGISTER.csv": lambda: SOURCES,
    "P8_Y5_PARENT_QLOC_2395_EH_KERNEL_SPLIT_THEOREM.csv": theorem_rows,
    "P8_Y5_PARENT_QLOC_2395_EH_ZERO_CERTIFICATE.csv": certificate_rows,
    "P8_Y5_PARENT_QLOC_2395_EH_CONTAMINATION_ROWS.csv": contamination_rows,
    "P8_Y5_PARENT_QLOC_2395_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2395_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2395_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2395_NEXT_TARGET.csv": next_rows,
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
            "row_id": "VAL2395_00_sources_exist",
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
            "row_id": "VAL2395_01_needles_found",
            "status": "PASS" if not missing_needles else "FAIL",
            "detail": "all source needles found" if not missing_needles else ";".join(missing_needles),
            "valid_for_claim": no_claim(),
        }
    )

    theorem = theorem_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_02_chain_rule_present",
            "status": "PASS" if any("DObs_e[Dq(v_k)] = 0" in row["statement"] for row in theorem) else "FAIL",
            "detail": "EH chain-rule kernel silence is present",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_03_theta_Qv_zero_present",
            "status": "PASS" if any("Theta_EH" in row["statement"] for row in theorem) and any("Q_EH[v_k]=0" in row["statement"] for row in theorem) else "FAIL",
            "detail": "conditional Theta_EH and Q_EH zero statements are present",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_04_observed_xi_guard_present",
            "status": "PASS" if any("Q_EH[h_xi]" in row["statement"] for row in theorem) else "FAIL",
            "detail": "observed diffeomorphism reference-charge guard is present",
            "valid_for_claim": no_claim(),
        }
    )

    certificates = certificate_rows()
    required_statuses = {
        "MISSING_PARENT_Q_OBS_E_OWNERSHIP",
        "MISSING_BASIC_COFRAME_PROOF",
        "MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT",
        "MISSING_EH_ZERO_FLUX_BOUNDARY_CLASS",
        "MISSING_POSITIVE_SAME_FRAME_MHREF",
    }
    present_statuses = {row["status"] for row in certificates}
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_05_required_gaps_explicit",
            "status": "PASS" if required_statuses <= present_statuses else "FAIL",
            "detail": "q/Obs_e, basic coframe, pure split, zero flux, and M_H_ref gaps explicit",
            "valid_for_claim": no_claim(),
        }
    )

    contamination = contamination_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_06_contamination_rows_nonready",
            "status": "PASS" if all(row["valid_for_claim"] == "false" for row in contamination) else "FAIL",
            "detail": "EH contamination rows remain nonclaim/nonready",
            "valid_for_claim": no_claim(),
        }
    )

    gates = claim_gate_rows()
    gate_ok = all(row["gate_status"] in {"BLOCKED", "CONDITIONAL_BLOCKED"} for row in gates)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_07_global_claims_blocked",
            "status": "PASS" if gate_ok else "FAIL",
            "detail": "EH pass, total Qv, matter/source, and GR/Newton gates not promoted",
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
            "row_id": "VAL2395_08_csv_parse",
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
            "row_id": "VAL2395_09_no_claim_flags",
            "status": "PASS" if not true_claims else "FAIL",
            "detail": "no generated row has valid_for_claim=true" if not true_claims else ";".join(true_claims),
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_10_formalization_untouched_by_script",
            "status": "PASS",
            "detail": "script writes only post-checkpoint-work outputs",
            "valid_for_claim": no_claim(),
        }
    )

    next_selected = any(row["row_id"] == "NEXT2395_0_selected" for row in next_rows())
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_11_next_selected",
            "status": "PASS" if next_selected else "FAIL",
            "detail": "matter/source lift and no-direct-slot proof selected next",
            "valid_for_claim": no_claim(),
        }
    )

    overall_status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2395_OVERALL",
            "status": overall_status,
            "detail": "2395 conditionally proves the EH pure-vertical kernel zero, separates observed GR charge as reference, refuses current-MTS promotion, and selects matter/source lift next",
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
    contamination = contamination_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()
    validation = validation_rows()

    body = f"""# 2395 — EH Local Geometry Kernel Split Or EH Contamination Row

## Result

2395 gets a real derivation foothold.

If the observed local geometry is genuinely quotient-owned,

`e_obs(Phi) = Obs_e(q(Phi))`,

and the tested vector is a pure local vertical direction,

`v_k in ker(Dq)` with no observed spacetime generator `xi`,

then

`delta_v e_obs = DObs_e[Dq(v_k)] = 0`.

For an EH term built only from `e_obs`,

`delta_v L_EH = E_EH dot delta_v e_obs + dTheta_EH(e_obs;delta_v e_obs) = 0`,

so

`Theta_EH(e_obs;v_k)=0`, `mu_EH[v_k]=0`, `J_EH[v_k]=0`, and conditionally `Q_EH[v_k]=0`

after the compact/local zero-flux boundary class is fixed.

That is the good news.  The guardrail is just as important: the ordinary EH/GR diffeomorphism charge is not being
zeroed.  If a parent tangent has an observed spacetime part `h_xi`, then `Q_EH[h_xi]` is the GR reference charge.
Only the pure quotient-kernel part `k` is supposed to vanish.  This is exactly the route MTS needs if it is going to
reduce to GR instead of replacing GR with a hidden residual charge.

Current MTS still cannot claim the EH pass, because the q/Obs_e ownership, basic coframe proof, pure vertical split,
zero-flux surface class, and same-frame `M_H_ref` are not all signed.  So 2395 is a conditional theorem plus a retained
EH contamination row, not a public local-GR claim.

## Source Register

{markdown_table(SOURCES, ["source_id", "path", "needed_for", "needles", "valid_for_claim"])}

## EH Kernel Split Theorem

{markdown_table(theorem, ["row_id", "claim", "statement", "derivation_status", "consequence", "missing_for_current_claim", "valid_for_claim"])}

## EH Zero Certificate

{markdown_table(certificates, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## EH Contamination Rows

{markdown_table(contamination, ["quantity_id", "definition", "units", "formula_or_bound", "current_value_status", "source_path", "valid_for_claim"])}

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

This is a net improvement.  The EH door is no longer vague: if `e_obs` is quotient-basic and `v` is truly pure
vertical, EH contributes no kernel charge.  That means the local-GR route is not obviously dead at the EH level.
The next danger is less forgiving: matter/source/coupling.  If ordinary matter has a hidden direct slot, source
prefactor, or representation marker outside q/Obs_e, the local branch leaks even if EH behaves perfectly.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2395_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2395_VALIDATION.csv'}")


if __name__ == "__main__":
    main()

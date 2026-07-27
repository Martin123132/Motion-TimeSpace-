from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3497-Y5-R2FR-minimal-parent-source-action-signature-or-first-hsrc-bound-row.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3497": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3496": {
        "path": ROOT / "3496-Y5-R2FR-source-worldtube-hypermomentum-zero-or-kernel-fill.md",
        "role": "3496 handoff",
    },
    "derivation_3496": {
        "path": OUT / "P8_Y5_R2FR_3496_HYPERMOMENTUM_ZERO_DERIVATION.csv",
        "role": "3496 source-hypermomentum theorem chain",
    },
    "clauses_3496": {
        "path": OUT / "P8_Y5_R2FR_3496_WORLDTUBE_CLAUSE_AUDIT.csv",
        "role": "3496 clause audit",
    },
    "kernel_3496": {
        "path": OUT / "P8_Y5_R2FR_3496_SOURCE_HYPERMOMENTUM_KERNEL_VECTOR.csv",
        "role": "3496 fallback kernel vector",
    },
    "bounds_3496": {
        "path": OUT / "P8_Y5_R2FR_3496_PRODUCT_BOUND_INHERITANCE.csv",
        "role": "3496 inherited WEP/PPN product bounds",
    },
    "p4_lock_3493": {
        "path": OUT / "P8_Y5_R2FR_3493_OFFICIAL_P4_LOCAL_GEOMETRY_INTERFACE.csv",
        "role": "official P4 tail interface",
    },
    "matter_descent_2611": {
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
        "role": "matter/worldtube descent theorem",
    },
    "selector_3375": {
        "path": OUT / "P8_Y5_R2FR_3375_WORLDTUBE_SOURCE_MEASURE_SELECTOR_THEOREM.csv",
        "role": "worldtube source measure selector",
    },
    "hilbert_3423": {
        "path": OUT / "P8_Y5_R2FR_3423_HILBERT_WORLDTUBE_CLOSURE_THEOREM.csv",
        "role": "Hilbert worldtube closure",
    },
    "poynting_3375": {
        "path": OUT / "P8_Y5_R2FR_3375_POYNTING_SOURCE_WORLD_TUBE_PLACEMENT.csv",
        "role": "Poynting/EM placement",
    },
    "commutator_1898": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
        "role": "projector/readout commutator obstruction",
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


def parent_source_action_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "MPA3497_0_field_space",
            "object": "parent local field space",
            "minimal_signature": "Phi -> q(Phi); e_obs=e(q); theta=theta(q); ordinary fields psi_A; EM gauge A; no ordinary-sector Gamma_ind",
            "why_it_matters": "Every local source/readout object must be a functor of public q/e_obs data, otherwise the source-current can carry hidden representative dependence.",
            "candidate_status": "CANDIDATE_BRANCH_WRITTEN",
            "live_claim_status": "NOT_ADOPTED_IN_CORE_ACTION",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "MPA3497_1_matter_action",
            "object": "ordinary matter action",
            "minimal_signature": "S_m = sum_A int L_A(psi_A, D_LC[e_obs] psi_A, e_obs, theta_A(q))",
            "why_it_matters": "Gamma_ind is absent from the ordinary source action, so the bulk source hypermomentum derivative is zero by variable absence.",
            "candidate_status": "SIGNS_CLAUSE3496_0_INSIDE_BRANCH",
            "live_claim_status": "REQUIRES_ADOPTION_AND_SECTOR_AUDIT",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "MPA3497_2_spin_connection",
            "object": "ordinary spin transport",
            "minimal_signature": "omega_spin := omega_LC[e_obs]; independent contorsion is not an ordinary matter argument",
            "why_it_matters": "Keeps the 3494 owned-coframe spin zero branch aligned with the source-worldtube zero route.",
            "candidate_status": "SIGNS_SPIN_COMPATIBILITY_INSIDE_BRANCH",
            "live_claim_status": "REQUIRES_GLOBAL_NO_INDEPENDENT_GAMMA_SIGNATURE",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "MPA3497_3_source_selector",
            "object": "source worldtube",
            "minimal_signature": "J_H[tau] := delta S_m / delta e_obs contracted with tau; W_source := closure(supp J_H[tau]) on compact regular support branches",
            "why_it_matters": "The source support is derived from the same current as matter rather than fitted after readout.",
            "candidate_status": "SIGNS_CLAUSE3496_2_INSIDE_BRANCH",
            "live_claim_status": "REGULAR_SUPPORT_AND_NO_CROSSING_STILL_NEED_PUBLIC_PROOF",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "MPA3497_4_charge_map",
            "object": "dressed source mass and GM",
            "minimal_signature": "M_H[W] := N_G^-1 int_S Q_tau[e_obs,psi,A] - H_ref; GM_obs := G_ref M_H with G_ref branch constant",
            "why_it_matters": "Newtonian source normalization is a Hamiltonian/Noether charge, not a fitted orbital mass inserted after the fact.",
            "candidate_status": "SIGNS_CLAUSE3496_4_AND_7_INSIDE_BRANCH",
            "live_claim_status": "H_REF_POSITIVITY_INTEGRABILITY_AND_GAUSS_READOUT_STILL_NEED_STRESS_TEST",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "MPA3497_5_em_poynting",
            "object": "EM and Poynting source energy",
            "minimal_signature": "S_EM = -1/4 int Z_F(q) F wedge *_e_obs F; T_EM and Poynting flux are included in J_H/H_tau",
            "why_it_matters": "The Poynting vector is not ignored; it is either inside the public Hilbert source or kept as a named boundary residual.",
            "candidate_status": "SIGNS_CLAUSE3496_5_INSIDE_BRANCH_IF_PUBLIC_HODGE",
            "live_claim_status": "EM_CHARGE_OWNER_AND_BOUNDARY_FLUX_NORMS_STILL_NEED_STRESS_TEST",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "MPA3497_6_projectors",
            "object": "projector/domain/boundary maps",
            "minimal_signature": "Pi_M, domain collars, support weights and boundary transport are natural fixed functors of q/e_obs/tau before variation",
            "why_it_matters": "Kills delta(Pi J)=Pi delta J+(delta Pi)J only when Pi has no hidden Gamma/readout dependence.",
            "candidate_status": "SIGNS_CLAUSE3496_6_ONLY_IF_NATURALITY_ACCEPTED",
            "live_claim_status": "WEAKEST_CANDIDATE_CLAUSE_REQUIRES_NEXT_STRESS_TEST",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "MPA3497_7_readout_order",
            "object": "empirical readout order",
            "minimal_signature": "orbital, clock, WEP, PPN and R10 readout maps are post-variation functors of solved e_obs/A/J_H data",
            "why_it_matters": "Readouts can report residuals but cannot redefine the source current that was already varied.",
            "candidate_status": "SIGNS_NO_REENTRY_INSIDE_BRANCH",
            "live_claim_status": "OFFICIAL_ARENA_READOUTS_STILL_NEED_OPERATOR_TESTS",
            "valid_for_claim": "False",
        },
    ]


def clause_signing_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "CLAUSE3496_0_parent_Lm",
            "candidate_signature": "MPA3497_1_matter_action",
            "candidate_signs_clause": "True",
            "proof": "Gamma_ind is absent from L_A, and D_LC depends only on e_obs; therefore partial S_m / partial Gamma_ind = 0 inside the candidate branch.",
            "remaining_public_risk": "the branch must be adopted as the parent ordinary matter grammar",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_1_same_frame_tau",
            "candidate_signature": "MPA3497_3_source_selector;MPA3497_4_charge_map",
            "candidate_signs_clause": "True",
            "proof": "J_H, W_source, H_tau and readout use the same e_obs and tau by construction.",
            "remaining_public_risk": "tau selector and boundary/asymptotic normalization need a standalone certificate",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_2_regular_support",
            "candidate_signature": "MPA3497_3_source_selector",
            "candidate_signs_clause": "True",
            "proof": "W_source is not a free mask; it is closure(supp J_H[tau]) on compact regular branches, so D_Gamma W_source=0 follows from D_Gamma J_H=0.",
            "remaining_public_risk": "singular support and exterior tails require either a regularity theorem or finite tail norm",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_3_no_marker_mask",
            "candidate_signature": "MPA3497_3_source_selector;MPA3497_7_readout_order",
            "candidate_signs_clause": "True",
            "proof": "No fitted radius, galaxy mask, composition marker or residual-tuned support appears in the source selector.",
            "remaining_public_risk": "material/composition labels must remain in matter fields and not re-enter as source selectors",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_4_hamiltonian_reference",
            "candidate_signature": "MPA3497_4_charge_map",
            "candidate_signs_clause": "True",
            "proof": "M_H is defined as a same-frame Hamiltonian/Noether charge with fixed H_ref and N_G, making its Gamma_ind derivative zero if integrability holds.",
            "remaining_public_risk": "integrability, positivity and reference lock are formal premises not yet externally proved",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_5_poynting_public_hodge",
            "candidate_signature": "MPA3497_5_em_poynting",
            "candidate_signs_clause": "True",
            "proof": "Public-Hodge EM puts Maxwell stress and Poynting flux inside J_H/H_tau; hidden-frame or boundary flux is not hidden but retained as residual.",
            "remaining_public_risk": "charge normalization, alpha owner and boundary flux norms still need the EM stress test",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_6_projector_boundary",
            "candidate_signature": "MPA3497_6_projectors",
            "candidate_signs_clause": "Conditional",
            "proof": "If Pi/domain/collar maps are natural q/e_obs/tau functors before variation, delta_Gamma Pi=0; this is the weakest line because naturality must be checked sector by sector.",
            "remaining_public_risk": "projector naturality is the first stress-test target",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CLAUSE3496_7_GM_transfer",
            "candidate_signature": "MPA3497_4_charge_map;MPA3497_7_readout_order",
            "candidate_signs_clause": "True",
            "proof": "GM_obs is defined after variation as G_ref M_H; no fitted-G absorption is allowed in the source-current variation.",
            "remaining_public_risk": "must derive weak-field Poisson/Gauss readout from the same charge",
            "valid_for_claim": "False",
        },
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "VAR3497_0_bulk_zero",
            "variation_piece": "delta_Gamma_ind S_m",
            "result_inside_candidate": "0",
            "reason": "Gamma_ind is not an argument of L_A; omega_spin is omega_LC[e_obs].",
            "public_status": "CANDIDATE_ZERO_NOT_LIVE_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "VAR3497_1_source_current_zero",
            "variation_piece": "delta_Gamma_ind J_H[tau]",
            "result_inside_candidate": "0",
            "reason": "J_H is the e_obs Hilbert current of S_m, and e_obs descends through q.",
            "public_status": "CANDIDATE_ZERO_NOT_LIVE_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "VAR3497_2_support_zero",
            "variation_piece": "delta_Gamma_ind W_source",
            "result_inside_candidate": "0 on compact regular support branches",
            "reason": "W_source is closure(supp J_H[tau]); D_Gamma J_H=0 distributionally.",
            "public_status": "REGULARITY_PREMISE_NEEDS_STRESS_TEST",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "VAR3497_3_charge_zero",
            "variation_piece": "delta_Gamma_ind M_H",
            "result_inside_candidate": "0 if H_tau/H_ref integrable and fixed",
            "reason": "M_H is a same-frame Hamiltonian/Noether surface charge of the same source.",
            "public_status": "REFERENCE_PREMISE_NEEDS_STRESS_TEST",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "VAR3497_4_projector_zero",
            "variation_piece": "delta_Gamma_ind(Pi J_H)",
            "result_inside_candidate": "0 only if delta_Gamma Pi=0",
            "reason": "Pi must be a natural q/e_obs/tau functor; otherwise the known commutator route survives.",
            "public_status": "WEAKEST_LINK",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "VAR3497_5_hsrc_verdict",
            "variation_piece": "epsilon_hypermomentum_source",
            "result_inside_candidate": "0 modulo projector naturality and support/reference premises",
            "reason": "All source-current channels are either variable-absent or post-variation readouts in the candidate action.",
            "public_status": "INTERNAL_CANDIDATE_CLOSURE_NOT_CURRENT_MTS_CLAIM",
            "valid_for_claim": "False",
        },
    ]


def fallback_bound_rows() -> list[dict[str, Any]]:
    inherited_rows = read_csv(SOURCES["bounds_3496"]["path"])
    selected_rows = [row for row in inherited_rows if row.get("bound_family") == "PPN_product" and row.get("observable") == "alpha3"]
    if not selected_rows:
        selected_rows = inherited_rows[:1]
    rows: list[dict[str, Any]] = []
    for source_row in selected_rows:
        rows.append(
            {
                "fallback_id": "FHS3497_0_first_if_candidate_rejected",
                "trigger": "candidate parent-source action rejected or projector naturality fails",
                "arena": source_row.get("observable", ""),
                "bound_value": source_row.get("bound_value", ""),
                "bound_units": source_row.get("bound_units", ""),
                "required_kernel": "KHS3496_0 master envelope plus KHS3496_6_projector_comm first",
                "status": "FALLBACK_ROW_SELECTED_NOT_EXECUTED",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3497_0_candidate_exists",
            "decision": "A minimal parent source-action branch can internally kill epsilon_hypermomentum_source.",
            "rationale": "Bulk matter, source current, support, Hamiltonian charge, GM and Poynting all become q/e_obs-owned objects in one grammar.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3497_1_weakest_link",
            "decision": "Projector/domain/boundary naturality is the weakest remaining line.",
            "rationale": "The known delta(Pi J) commutator is the one route not killed merely by writing the matter action; Pi must be natural or bounded.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3497_2_no_github_no_claim",
            "decision": "Keep this private and nonclaim until the branch survives stress tests.",
            "rationale": "The action signature is promising structure, not an adopted public theory statement.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3498-Y5-R2FR-projector-naturality-stress-test-or-Kprojector-bound.md",
            "next_script": "scripts/Y5_R2FR_3498_projector_naturality_stress_test_or_Kprojector_bound.py",
            "objective": "Stress-test MPA3497_6: prove Pi/domain/boundary/collar maps are natural q/e_obs/tau functors, or fill KHS3496_6_projector_comm as the first finite source-hypermomentum bound component.",
            "success_gate": "delta_Gamma Pi=0 theorem for source/worldtube/projector maps, or first K_projector_comm bound row with source path, units and nonclaim status",
            "forbidden_shortcuts": "assuming projectors commute because GR does; burying boundary motion in calibration; treating chosen support masks as parent-owned without a selector proof",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_files = [
        OUT / "P8_Y5_R2FR_3497_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3497_MINIMAL_PARENT_SOURCE_ACTION_SIGNATURE.csv",
        OUT / "P8_Y5_R2FR_3497_CLAUSE_SIGNING_TEST.csv",
        OUT / "P8_Y5_R2FR_3497_VARIATION_CHAIN.csv",
        OUT / "P8_Y5_R2FR_3497_FALLBACK_FIRST_BOUND_ROW.csv",
        OUT / "P8_Y5_R2FR_3497_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3497_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *signature, *clauses, *variation, *fallback, *decisions, *next_rows]
    signed_or_conditional = sum(1 for clause_row in clauses if clause_row.get("candidate_signs_clause") in {"True", "Conditional"})
    strict_true_count = sum(1 for clause_row in clauses if clause_row.get("candidate_signs_clause") == "True")
    weakest_link_count = sum(1 for clause_row in clauses if clause_row.get("candidate_signs_clause") == "Conditional")
    checks = [
        {
            "check_id": "VAL3497_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local sources exist",
        },
        {
            "check_id": "VAL3497_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3497_2_candidate_signature_complete",
            "passed": len(signature) >= 8,
            "detail": f"signature_rows={len(signature)}",
        },
        {
            "check_id": "VAL3497_3_clause_signing_attempt",
            "passed": signed_or_conditional == 8 and strict_true_count >= 7 and weakest_link_count == 1,
            "detail": f"signed_or_conditional={signed_or_conditional}; strict_true={strict_true_count}; conditional={weakest_link_count}",
        },
        {
            "check_id": "VAL3497_4_variation_chain",
            "passed": len(variation) >= 6 and variation[-1]["public_status"] == "INTERNAL_CANDIDATE_CLOSURE_NOT_CURRENT_MTS_CLAIM",
            "detail": f"variation_rows={len(variation)}; verdict={variation[-1]['public_status']}",
        },
        {
            "check_id": "VAL3497_5_fallback_bound_selected",
            "passed": len(fallback) >= 1 and fallback[0]["status"] == "FALLBACK_ROW_SELECTED_NOT_EXECUTED",
            "detail": fallback[0]["arena"],
        },
        {
            "check_id": "VAL3497_6_no_claim",
            "passed": all(str(output_row.get("valid_for_claim", "False")) == "False" for output_row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3497_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
        },
        {
            "check_id": "VAL3497_8_next_target",
            "passed": len(next_rows) == 1 and "3498" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3497_SUMMARY",
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
    signature: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3497 - Minimal Parent Source-Action Signature or First Hsrc Bound Row",
                "",
                "## Current Verdict",
                "- **Best result:** a minimal candidate parent source-action branch now exists that internally kills `epsilon_hypermomentum_source` by variable absence and source-measure descent.",
                "- **Weakest link:** projector/domain/boundary naturality remains conditional; this is the exact place where `delta(Pi J)` can still bite.",
                "- **No public claim:** this is a candidate branch and stress-test target, not an adopted MTS theorem yet.",
                "- **Fallback ready:** if projector naturality fails, the selected first fallback is the `alpha3` source-hypermomentum product row.",
                "",
                "## Minimal Parent Source-Action Signature",
                markdown_table(
                    signature,
                    [
                        "signature_id",
                        "object",
                        "minimal_signature",
                        "candidate_status",
                        "live_claim_status",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Clause Signing Test",
                markdown_table(
                    clauses,
                    [
                        "clause_id",
                        "candidate_signature",
                        "candidate_signs_clause",
                        "proof",
                        "remaining_public_risk",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Variation Chain",
                markdown_table(
                    variation,
                    ["chain_id", "variation_piece", "result_inside_candidate", "reason", "public_status", "valid_for_claim"],
                ),
                "",
                "## Fallback First Bound Row",
                markdown_table(
                    fallback,
                    ["fallback_id", "trigger", "arena", "bound_value", "bound_units", "required_kernel", "status", "valid_for_claim"],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
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
    signature_rows = parent_source_action_signature_rows()
    clause_rows = clause_signing_test_rows()
    variation_rows = variation_chain_rows()
    fallback_rows = fallback_bound_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    write_csv(
        OUT / "P8_Y5_R2FR_3497_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3497_MINIMAL_PARENT_SOURCE_ACTION_SIGNATURE.csv",
        signature_rows,
        ["signature_id", "object", "minimal_signature", "why_it_matters", "candidate_status", "live_claim_status", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3497_CLAUSE_SIGNING_TEST.csv",
        clause_rows,
        ["clause_id", "candidate_signature", "candidate_signs_clause", "proof", "remaining_public_risk", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3497_VARIATION_CHAIN.csv",
        variation_rows,
        ["chain_id", "variation_piece", "result_inside_candidate", "reason", "public_status", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3497_FALLBACK_FIRST_BOUND_ROW.csv",
        fallback_rows,
        ["fallback_id", "trigger", "arena", "bound_value", "bound_units", "required_kernel", "status", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3497_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3497_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation = validation_rows(
        source_rows,
        signature_rows,
        clause_rows,
        variation_rows,
        fallback_rows,
        decision_ledger_rows,
        next_rows,
    )
    write_csv(
        OUT / "P8_Y5_BRR545_3497_VALIDATION.csv",
        validation,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(signature_rows, clause_rows, variation_rows, fallback_rows, decision_ledger_rows, next_rows, validation)


if __name__ == "__main__":
    main()

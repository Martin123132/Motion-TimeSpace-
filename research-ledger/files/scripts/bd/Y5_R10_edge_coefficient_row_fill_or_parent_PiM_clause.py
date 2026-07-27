from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_edge_coefficient_row_fill_pack_written_parent_PiM_clause_unsigned_nonclaim"
CLAIM_CEILING = "edge_coefficient_row_fill_and_parent_PiM_clause_audit_only_no_Qbar_edge_zero_no_R10_no_R11_no_PPN_no_local_GR_claim"
NEXT_TARGET = "675-Y5-R10-source-backed-edge-row-scout-or-Qedge-null-action-clause.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_PATH = ROOT / "674-Y5-R10-edge-coefficient-row-fill-or-parent-PiM-clause.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "510_doc": ROOT / "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
    "539_validation": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_VALIDATION.csv",
    "541_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "544_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "544_validation": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_544_VALIDATION.csv",
    "621_doc": ROOT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
    "622_doc": ROOT / "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
    "629_doc": ROOT / "629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md",
    "629_validation": RESIDUALS / "P8_Y5_BRR545_629_VALIDATION.csv",
    "629_source_search": RESIDUALS / "P8_Y5_R10_629_SOURCE_SEARCH_STATUS.csv",
    "629_curve_audit": RESIDUALS / "P8_Y5_R10_629_R10_CURVE_PROMOTION_AUDIT.csv",
    "bound_live_placeholder": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
    "bound_review_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
    "667_doc": ROOT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
    "667_validation": RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv",
    "667_ansatz": RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
    "667_variation": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "668_doc": ROOT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
    "668_validation": RESIDUALS / "P8_Y5_BRR545_668_VALIDATION.csv",
    "668_sector_audit": RESIDUALS / "P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
    "668_boundary_lock": RESIDUALS / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
    "669_doc": ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
    "669_validation": RESIDUALS / "P8_Y5_BRR545_669_VALIDATION.csv",
    "669_lx_gates": RESIDUALS / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
    "669_residual_vector": RESIDUALS / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
    "670_doc": ROOT / "670-Y5-R10-no-pole-quotient-LX-route-or-positive-sourcefree-operator-proof.md",
    "670_validation": RESIDUALS / "P8_Y5_BRR545_670_VALIDATION.csv",
    "670_no_pole": RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
    "670_zero_effect": RESIDUALS / "P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv",
    "671_doc": ROOT / "671-Y5-R10-parent-Omega-DCX-boundary-charge-owner-or-edge-residual-vector.md",
    "671_validation": RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv",
    "671_edge": RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
    "672_doc": ROOT / "672-Y5-R10-boundary-exactness-projector-orthogonality-or-edge-coefficient-source-plan.md",
    "672_validation": RESIDUALS / "P8_Y5_BRR545_672_VALIDATION.csv",
    "672_source_plan": RESIDUALS / "P8_Y5_R10_672_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
    "673_doc": ROOT / "673-Y5-R10-edge-coefficient-source-acquisition-or-Hamiltonian-PiM-orthogonality-proof.md",
    "673_validation": RESIDUALS / "P8_Y5_BRR545_673_VALIDATION.csv",
    "673_pim_audit": RESIDUALS / "P8_Y5_R10_673_HAMILTONIAN_PIM_ORTHOGONALITY_PROOF_AUDIT.csv",
    "673_glue_audit": RESIDUALS / "P8_Y5_R10_673_SOURCE_MEASURE_GLUE_AUDIT.csv",
    "673_acquisition": RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
    "673_decision": RESIDUALS / "P8_Y5_R10_673_ZERO_OR_SOURCE_DECISION.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_PATHS[source_id]) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def numeric_rows(path: Path, required_columns: tuple[str, ...]) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    rows = read_csv(path)
    numeric_count = 0
    claim_count = 0
    for row in rows:
        if row.get("valid_for_claim", "").lower() == "true":
            claim_count += 1
        try:
            values = [float(row[column]) for column in required_columns]
        except (KeyError, TypeError, ValueError):
            continue
        if all(value > 0 for value in values):
            numeric_count += 1
    return numeric_count, claim_count


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "510_doc": "worldtube source-measure reference theorem and residual runner",
        "539_doc": "Hamiltonian Pi_M candidate definition",
        "539_validation": "539 validation gate",
        "541_contract": "Hamiltonian source-measure contract",
        "544_status": "boundary/reference first-row status",
        "544_validation": "544 validation gate",
        "621_doc": "matter coupling normal-form theorem context",
        "622_doc": "parent matter sector contract context",
        "629_doc": "R10 bound curve digitization/c_g projection smoke runner",
        "629_validation": "629 validation gate",
        "629_source_search": "R10 source search status",
        "629_curve_audit": "R10 curve promotion audit",
        "bound_live_placeholder": "live digitized R10 bound curve file",
        "bound_review_candidate": "private vector review candidate curve",
        "667_doc": "explicit parent boundary action ansatz",
        "667_validation": "667 validation gate",
        "667_ansatz": "parent boundary action ansatz rows",
        "667_variation": "variation ledger rows",
        "668_doc": "sector Lagrangian owner and boundary-condition lock",
        "668_validation": "668 validation gate",
        "668_sector_audit": "sector owner audit rows",
        "668_boundary_lock": "boundary condition lock rows",
        "669_doc": "minimal L_X operator owner attempt",
        "669_validation": "669 validation gate",
        "669_lx_gates": "L_X owner gate tests",
        "669_residual_vector": "R10/R11 residual vector from missing L_X owner",
        "670_doc": "no-pole quotient or positive source-free proof",
        "670_validation": "670 validation gate",
        "670_no_pole": "no-pole quotient proof chain",
        "670_zero_effect": "R10/R11 zero-or-residual effect rows",
        "671_doc": "boundary charge owner / edge residual vector",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector",
        "672_doc": "boundary exactness and source plan",
        "672_validation": "672 validation gate",
        "672_source_plan": "edge coefficient source plan",
        "673_doc": "Hamiltonian Pi_M orthogonality proof audit",
        "673_validation": "673 validation gate",
        "673_pim_audit": "673 Pi_M orthogonality audit",
        "673_glue_audit": "673 source-measure glue audit",
        "673_acquisition": "673 edge coefficient acquisition ledger",
        "673_decision": "673 zero-or-source decisions",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def parent_pim_clause_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "PPC674_0_null_edge_action_clause",
            "candidate_clause": "edge sector is variationally exact/topological and not in the physical quotient",
            "mathematical_form": "S_parent=S_red[q(Phi)]+int_boundary dB_edge, Dq[v_edge]=0, delta S_edge=dC_edge",
            "acceptance_test": "same parent action owns q, B_edge, allowed boundary class, and shows Pi_M^H[Q_edge]=0",
            "current_result": "not_parent_signed",
            "why_not_enough": "667/668 give an ansatz and boundary-condition lock, but no unique edge action and boundary class are fixed",
            "if_passes": "Qbar_edge_XH(lambda)=0 without coefficient sourcing",
            "fallback": "fill edge coefficient row pack",
            "valid_for_claim": "false",
            "source_paths": source_list("667_ansatz", "667_variation", "668_boundary_lock", "672_source_plan", "673_pim_audit"),
            "generated_utc": now,
        },
        {
            "clause_id": "PPC674_1_mass_cohomology_orthogonality",
            "candidate_clause": "edge charge lives in a mass-cohomology complement",
            "mathematical_form": "Omega_H(T_M,T_edge)=0 and omega_M^H(Q_edge)=0",
            "acceptance_test": "parent symplectic form fixes the mass representative and edge representative before readout",
            "current_result": "not_derived",
            "why_not_enough": "Pi_M^H is candidate-defined, but the mass/edge orthogonal decomposition is not parent-owned",
            "if_passes": "Pi_M^H[Q_edge^H(lambda)] vanishes by cohomology",
            "fallback": "source Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("539_doc", "673_pim_audit", "671_edge"),
            "generated_utc": now,
        },
        {
            "clause_id": "PPC674_2_fixed_reference_integrability",
            "candidate_clause": "reference subtraction and Hamiltonian variation are fixed before edge readout",
            "mathematical_form": "delta H_tau=int_S(delta Q_tau-i_tau theta), delta_ref H_tau=0, B_zero_flux=Delta_symp=0",
            "acceptance_test": "B_ref, theta, Q_tau, tau, and M_H_ref are parent-owned with no source/range dependence",
            "current_result": "not_closed",
            "why_not_enough": "544 still reports no claim-valid B_zero_flux, Delta_symp, or M_H_ref row",
            "if_passes": "edge projection denominator/reference becomes stable",
            "fallback": "retain M_H_ref and boundary/reference fill slots",
            "valid_for_claim": "false",
            "source_paths": source_list("541_contract", "544_status", "667_variation", "668_boundary_lock"),
            "generated_utc": now,
        },
        {
            "clause_id": "PPC674_3_same_frame_matter_quotient",
            "candidate_clause": "matter reads only quotient variables and carries no edge/test-body marker",
            "mathematical_form": "S_matter=Sbar[q(Phi),psi,theta_obs], partial S_matter/partial edge=0, qbar_XT=0",
            "acceptance_test": "parent matter functor is common, same-frame, and blind to edge before empirical fitting",
            "current_result": "not_closed",
            "why_not_enough": "matter-coupling normal form remains a contract/route, not a signed theorem for qbar_XT",
            "if_passes": "test-body response factor qbar_XT vanishes",
            "fallback": "source qbar_XT or keep it as a nonclaim coefficient",
            "valid_for_claim": "false",
            "source_paths": source_list("621_doc", "622_doc", "673_acquisition"),
            "generated_utc": now,
        },
        {
            "clause_id": "PPC674_4_no_pole_vertical_first_class",
            "candidate_clause": "edge/X direction is first-class vertical with zero boundary charge",
            "mathematical_form": "v_edge in ker(Dq), Omega(v_edge,.)=0, Q_edge=0 on allowed local boundary",
            "acceptance_test": "quotient verticality, Omega/DCX owner, bracket closure, and boundary zero all pass together",
            "current_result": "conditional_but_unsigned",
            "why_not_enough": "670-672 preserve useful conditional zeros, but not the full measured edge charge zero",
            "if_passes": "K_edge and Qbar_edge_XH are inactive",
            "fallback": "retain K_edge, B_X, and Qbar_edge source slots",
            "valid_for_claim": "false",
            "source_paths": source_list("670_no_pole", "670_zero_effect", "671_edge", "672_source_plan"),
            "generated_utc": now,
        },
        {
            "clause_id": "PPC674_5_verdict",
            "candidate_clause": "parent PiM clause closes edge branch",
            "mathematical_form": "PPC674_0 through PPC674_4 jointly imply alpha_edge(lambda)=0",
            "acceptance_test": "all parent clauses pass without MISSING, conditional-only, or source-backed residual placeholders",
            "current_result": "failed_for_current_claim",
            "why_not_enough": "every viable route still has at least one unsigned parent ownership or source-measure clause",
            "if_passes": "R10 edge row can become theorem-zero candidate",
            "fallback": "edge coefficient row fill pack stays nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("673_decision", "673_validation", "672_validation", "671_validation"),
            "generated_utc": now,
        },
    ]


def coefficient_requirement_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "requirement_id": "CFR674_0_lambda_edge",
            "column_or_factor": "lambda_edge",
            "role": "select R10/local bound scale",
            "claim_promotable_if": "positive numeric length with source path and active-support derivation, or parent no-edge theorem",
            "current_fill": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "units": "m",
            "source_path_needed": "parent edge support/range derivation or source-backed envelope",
            "valid_for_claim": "false",
            "source_paths": source_list("673_acquisition", "671_edge", "672_source_plan"),
            "generated_utc": now,
        },
        {
            "requirement_id": "CFR674_1_K_edge",
            "column_or_factor": "K_edge",
            "role": "edge Green/boundary kernel normalization",
            "claim_promotable_if": "numeric normalized kernel or theorem-zero edge kernel inactivity",
            "current_fill": "MISSING_SOURCE_BACKED_K_EDGE",
            "units": "dimensionless_or_declared",
            "source_path_needed": "parent boundary Green kernel and unit map",
            "valid_for_claim": "false",
            "source_paths": source_list("673_acquisition", "669_residual_vector", "670_zero_effect"),
            "generated_utc": now,
        },
        {
            "requirement_id": "CFR674_2_Qbar_edge_XH",
            "column_or_factor": "Qbar_edge_XH",
            "role": "Hamiltonian mass projection of edge charge",
            "claim_promotable_if": "Pi_M^H[Q_edge]/M_H numeric, or parent proof of exact zero",
            "current_fill": "MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "units": "dimensionless_or_declared",
            "source_path_needed": "Hamiltonian projection with numerator, denominator, frame, reference",
            "valid_for_claim": "false",
            "source_paths": source_list("673_pim_audit", "673_glue_audit", "541_contract", "544_status"),
            "generated_utc": now,
        },
        {
            "requirement_id": "CFR674_3_qbar_XT",
            "column_or_factor": "qbar_XT",
            "role": "test-body edge response",
            "claim_promotable_if": "same-frame matter quotient theorem zero or composition-specific source-backed response",
            "current_fill": "MISSING_SOURCE_BACKED_QBAR_XT_OR_THEOREM_ZERO",
            "units": "dimensionless_or_declared",
            "source_path_needed": "matter coupling normal-form theorem or response coefficient",
            "valid_for_claim": "false",
            "source_paths": source_list("621_doc", "622_doc", "673_acquisition"),
            "generated_utc": now,
        },
        {
            "requirement_id": "CFR674_4_BX_boundary_momentum",
            "column_or_factor": "B_X_boundary_momentum",
            "role": "boundary primitive/current entering Q_edge",
            "claim_promotable_if": "parent boundary action fixes B_X and counterterm, or exact/proper zero",
            "current_fill": "MISSING_BOUNDARY_OWNER",
            "units": "boundary_current_units",
            "source_path_needed": "variation ledger and boundary representative",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_boundary_lock", "671_edge", "672_source_plan"),
            "generated_utc": now,
        },
        {
            "requirement_id": "CFR674_5_M_H_ref",
            "column_or_factor": "M_H_ref",
            "role": "positive Hamiltonian source mass denominator",
            "claim_promotable_if": "positive same-frame Hamiltonian mass with fixed reference and observed calibration",
            "current_fill": "MISSING_SOURCE_BACKED_M_H_REF_FOR_CURRENT_BRANCH",
            "units": "mass_or_geometrized_mass",
            "source_path_needed": "source-measure and Poisson/Gauss calibration branch",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "541_contract", "544_status"),
            "generated_utc": now,
        },
        {
            "requirement_id": "CFR674_6_alpha_bound_lambda",
            "column_or_factor": "alpha_bound(lambda)",
            "role": "empirical R10 bound curve comparator",
            "claim_promotable_if": "live bound file has promoted source-backed digitized rows with no placeholders",
            "current_fill": "LIVE_FILE_PLACEHOLDER_REVIEW_CANDIDATE_NONCLAIM",
            "units": "lambda_m_alpha_dimensionless",
            "source_path_needed": "machine-readable/digitized source-backed R10 curve",
            "valid_for_claim": "false",
            "source_paths": source_list("629_source_search", "629_curve_audit", "bound_live_placeholder", "bound_review_candidate"),
            "generated_utc": now,
        },
        {
            "requirement_id": "CFR674_7_alpha_edge_formula",
            "column_or_factor": "alpha_edge(lambda)",
            "role": "executable product/envelope compared against R10",
            "claim_promotable_if": "all active factors source-backed or theorem-zero, and force-law mapping declared",
            "current_fill": "FORMULA_READY_INPUTS_MISSING",
            "units": "dimensionless",
            "source_path_needed": "alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT with declared convention",
            "valid_for_claim": "false",
            "source_paths": source_list("673_acquisition", "672_source_plan", "629_validation"),
            "generated_utc": now,
        },
    ]


def row_fill_pack_rows() -> list[dict[str, str]]:
    now = generated_utc()
    alpha_formula = "alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT"
    return [
        {
            "row_id": "EFR674_0_current_edge_branch_template",
            "branch_id": "MTS_R10_edge_branch_current",
            "lambda_value": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "lambda_units": "m",
            "K_edge": "MISSING_SOURCE_BACKED_K_EDGE",
            "Qbar_edge_XH": "MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "qbar_XT": "MISSING_SOURCE_BACKED_QBAR_XT_OR_THEOREM_ZERO",
            "B_X_boundary_momentum": "MISSING_BOUNDARY_OWNER",
            "M_H_ref": "MISSING_SOURCE_BACKED_M_H_REF_FOR_CURRENT_BRANCH",
            "alpha_edge_formula": alpha_formula,
            "alpha_predicted": "",
            "alpha_bound_source": str(SOURCE_PATHS["bound_live_placeholder"]),
            "derivation_status": "unfilled_template_nonclaim",
            "promotion_gate": "fail_until_every_factor_numeric_or_theorem_zero_and_bound_curve_promoted",
            "valid_for_claim": "false",
            "source_paths": source_list("673_acquisition", "671_edge", "672_source_plan"),
            "generated_utc": now,
        },
        {
            "row_id": "EFR674_1_parent_clause_theorem_zero_candidate",
            "branch_id": "MTS_R10_edge_branch_parent_zero_if_signed",
            "lambda_value": "inactive_if_Qedge_null_clause_signed",
            "lambda_units": "m",
            "K_edge": "0_if_parent_no_edge_kernel",
            "Qbar_edge_XH": "0_if_PiM_orthogonality_signed",
            "qbar_XT": "0_if_matter_quotient_blindness_signed",
            "B_X_boundary_momentum": "0_or_exact_if_boundary_clause_signed",
            "M_H_ref": "MISSING_SOURCE_BACKED_M_H_REF_FOR_CURRENT_BRANCH",
            "alpha_edge_formula": alpha_formula,
            "alpha_predicted": "0_only_if_parent_clause_passes",
            "alpha_bound_source": "not_needed_for_theorem_zero_but_needed_for_nonzero_scoring",
            "derivation_status": "candidate_zero_clause_unsigned",
            "promotion_gate": "fail_parent_clause_unsigned",
            "valid_for_claim": "false",
            "source_paths": source_list("667_ansatz", "668_boundary_lock", "670_no_pole", "673_pim_audit"),
            "generated_utc": now,
        },
        {
            "row_id": "EFR674_2_review_curve_pressure_only",
            "branch_id": "MTS_R10_edge_branch_pressure_wall",
            "lambda_value": "available_only_from_private_review_candidate_grid",
            "lambda_units": "m",
            "K_edge": "MISSING_SOURCE_BACKED_K_EDGE",
            "Qbar_edge_XH": "MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "qbar_XT": "MISSING_SOURCE_BACKED_QBAR_XT_OR_THEOREM_ZERO",
            "B_X_boundary_momentum": "MISSING_BOUNDARY_OWNER",
            "M_H_ref": "MISSING_SOURCE_BACKED_M_H_REF_FOR_CURRENT_BRANCH",
            "alpha_edge_formula": alpha_formula,
            "alpha_predicted": "",
            "alpha_bound_source": str(SOURCE_PATHS["bound_review_candidate"]),
            "derivation_status": "private_pressure_only_nonclaim",
            "promotion_gate": "fail_MTS_coefficients_missing_and_curve_review_candidate_nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("629_curve_audit", "bound_review_candidate", "673_acquisition"),
            "generated_utc": now,
        },
    ]


def bound_curve_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    live_numeric, live_claim = numeric_rows(SOURCE_PATHS["bound_live_placeholder"], ("lambda_value", "alpha_bound"))
    review_numeric, review_claim = numeric_rows(SOURCE_PATHS["bound_review_candidate"], ("lambda_value", "alpha_bound"))
    return [
        {
            "gate_id": "BCG674_0_live_digitized_file",
            "artifact": str(SOURCE_PATHS["bound_live_placeholder"]),
            "numeric_rows": str(live_numeric),
            "claim_rows": str(live_claim),
            "current_status": "placeholder_or_unpromoted" if live_claim == 0 else "has_claim_rows_review_required",
            "claim_effect": "cannot score R10 claim from live file",
            "valid_for_claim": "false",
            "source_paths": source_list("bound_live_placeholder", "629_curve_audit"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG674_1_review_candidate_curve",
            "artifact": str(SOURCE_PATHS["bound_review_candidate"]),
            "numeric_rows": str(review_numeric),
            "claim_rows": str(review_claim),
            "current_status": "private_pressure_wall_only",
            "claim_effect": "can guide coefficient pressure, not public/live claim",
            "valid_for_claim": "false",
            "source_paths": source_list("bound_review_candidate", "629_source_search", "629_curve_audit"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG674_2_MTS_edge_row",
            "artifact": "P8_Y5_R10_674_EDGE_ROW_FILL_PACK.csv",
            "numeric_rows": "0",
            "claim_rows": "0",
            "current_status": "MTS_coefficients_missing_or_theorem_unsigned",
            "claim_effect": "R10 comparator must remain blocked",
            "valid_for_claim": "false",
            "source_paths": source_list("673_acquisition", "673_decision"),
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    parent_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    row_pack: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    parent_claim_rows = sum(1 for row in parent_rows if row["valid_for_claim"] == "true")
    requirement_claim_rows = sum(1 for row in requirement_rows if row["valid_for_claim"] == "true")
    row_pack_claim_rows = sum(1 for row in row_pack if row["valid_for_claim"] == "true")
    bound_claim_rows = sum(1 for row in bound_rows if row["valid_for_claim"] == "true")
    return [
        {
            "evaluator_id": "EV674_0_parent_clause",
            "target": "derive edge theorem-zero from parent PiM clause",
            "status": "fail_nonclaim",
            "reason": "parent action, mass cohomology, fixed reference, matter quotient, and no-pole clauses do not all pass",
            "claim_effect": "Qbar_edge_XH remains live",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV674_1_row_fill_pack",
            "target": "stage executable R10 edge row schema",
            "status": "pass_nonclaim",
            "reason": f"parent_claim_rows={parent_claim_rows};requirement_claim_rows={requirement_claim_rows};row_pack_claim_rows={row_pack_claim_rows}",
            "claim_effect": "future fill rows ready, no evidence promoted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV674_2_bound_curve",
            "target": "R10 bound curve readiness",
            "status": "blocked_nonclaim",
            "reason": f"bound_claim_rows={bound_claim_rows};live file remains unpromoted and review candidate is pressure-only",
            "claim_effect": "R10 claim remains blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV674_3_next",
            "target": "select next target",
            "status": "source_backed_edge_row_scout_or_Qedge_null_action_clause",
            "reason": "either source the actual row inputs or write a genuinely sharper null-edge action clause",
            "claim_effect": "next private checkpoint only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D674_0_parent_clause",
            "target": "Qedge null / PiM orthogonality clause",
            "result": "not_signed",
            "reason": "candidate parent clauses exist, but none jointly owns edge exactness, mass orthogonality, source measure, matter blindness, and boundary/reference lock",
            "next_action": "try sharper Qedge null action clause only if it supplies a parent-owned boundary representative",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D674_1_edge_row_fill",
            "target": "R10 edge coefficient row",
            "result": "fill_pack_written_nonclaim",
            "reason": "the coefficient slots are now concrete enough to source or leave blocked without ambiguity",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D674_2_no_promotion",
            "target": "R10/R11/PPN/local-GR claims",
            "result": "blocked",
            "reason": "no parent theorem-zero and no source-backed numeric edge row exist",
            "next_action": "continue private derivation/source-backed scouting only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS674_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "parent PiM clause did not close; edge coefficient row fill pack staged",
            "blocked_claims": "Qbar_edge_zero;R10;R11;PPN;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def contains_missing_or_blocker(rows: list[dict[str, str]]) -> bool:
    text = " ".join(str(value) for row in rows for value in row.values()).upper()
    markers = ["MISSING", "UNSIGNED", "NOT_SIGNED", "NOT_DERIVED", "NOT_CLOSED", "CONDITIONAL", "PLACEHOLDER", "NONCLAIM"]
    return any(marker in text for marker in markers)


def validation_rows(
    source_rows: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    row_pack: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    rows.append(
        {
            "check_id": "V674_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
            "generated_utc": now,
        }
    )

    validation_ids = [
        "539_validation",
        "544_validation",
        "629_validation",
        "667_validation",
        "668_validation",
        "669_validation",
        "670_validation",
        "671_validation",
        "672_validation",
        "673_validation",
    ]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append(
        {
            "check_id": "V674_1_prior_validations_clean",
            "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail",
            "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()),
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V674_2_parent_clause_attempt_coverage",
            "result": "pass" if len(parent_rows) >= 6 else "fail",
            "detail": f"parent_clause_rows={len(parent_rows)}",
            "generated_utc": now,
        }
    )

    parent_promoted = [row for row in parent_rows if row["valid_for_claim"] == "true"]
    rows.append(
        {
            "check_id": "V674_3_parent_clause_not_promoted",
            "result": "pass" if not parent_promoted and any(row["current_result"] == "failed_for_current_claim" for row in parent_rows) else "fail",
            "detail": "parent clause remains unsigned and nonclaim",
            "generated_utc": now,
        }
    )

    required_factors = {
        "lambda_edge",
        "K_edge",
        "Qbar_edge_XH",
        "qbar_XT",
        "B_X_boundary_momentum",
        "M_H_ref",
        "alpha_bound(lambda)",
        "alpha_edge(lambda)",
    }
    actual_factors = {row["column_or_factor"] for row in requirement_rows}
    rows.append(
        {
            "check_id": "V674_4_coefficient_requirements_complete",
            "result": "pass" if required_factors.issubset(actual_factors) else "fail",
            "detail": "missing=" + ";".join(sorted(required_factors - actual_factors)),
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V674_5_row_fill_pack_blocked",
            "result": "pass" if row_pack and contains_missing_or_blocker(row_pack) and all(row["valid_for_claim"] == "false" for row in row_pack) else "fail",
            "detail": f"row_pack_rows={len(row_pack)};all_nonclaim={all(row['valid_for_claim']=='false' for row in row_pack)}",
            "generated_utc": now,
        }
    )

    live_rows = [row for row in bound_rows if row["gate_id"] == "BCG674_0_live_digitized_file"]
    review_rows = [row for row in bound_rows if row["gate_id"] == "BCG674_1_review_candidate_curve"]
    live_claim_rows = int(live_rows[0]["claim_rows"]) if live_rows else -1
    review_numeric_rows = int(review_rows[0]["numeric_rows"]) if review_rows else 0
    rows.append(
        {
            "check_id": "V674_6_bound_curve_nonclaim_status",
            "result": "pass" if live_claim_rows == 0 and review_numeric_rows > 0 else "fail",
            "detail": f"live_claim_rows={live_claim_rows};review_numeric_rows={review_numeric_rows}",
            "generated_utc": now,
        }
    )

    generated = parent_rows + requirement_rows + row_pack + bound_rows + evaluator + decision
    claim_rows = [row for row in generated if row.get("valid_for_claim") == "true"]
    rows.append(
        {
            "check_id": "V674_7_no_claim_rows_promoted",
            "result": "pass" if not claim_rows else "fail",
            "detail": "all generated rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}",
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V674_8_next_target_selected",
            "result": "pass" if any(row["next_action"] == NEXT_TARGET for row in decision) else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": now,
        }
    )

    output_paths = [
        RESIDUALS / "P8_Y5_R10_674_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_674_PARENT_PIM_CLAUSE_TEST.csv",
        RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
        RESIDUALS / "P8_Y5_R10_674_EDGE_ROW_FILL_PACK.csv",
        RESIDUALS / "P8_Y5_R10_674_BOUND_CURVE_STATUS_GATE.csv",
        RESIDUALS / "P8_Y5_R10_674_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_674_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_674_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append(
        {
            "check_id": "V674_9_generated_outputs_scoped",
            "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail",
            "detail": "all 674 outputs target post-checkpoint-work",
            "generated_utc": now,
        }
    )

    changed_count = formalization_changed_count()
    rows.append(
        {
            "check_id": "V674_10_formalization_workbench_untouched",
            "result": "pass" if changed_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed_count}",
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V674_11_status_nonclaim",
            "result": "pass" if "no_R10" in CLAIM_CEILING and "no_Qbar_edge_zero" in CLAIM_CEILING else "fail",
            "detail": CLAIM_CEILING,
            "generated_utc": now,
        }
    )

    evaluator_statuses = [row["status"] for row in evaluator]
    rows.append(
        {
            "check_id": "V674_12_evaluator_nonclaim_passes",
            "result": "pass" if all("claim" in status or status == "source_backed_edge_row_scout_or_Qedge_null_action_clause" for status in evaluator_statuses) else "fail",
            "detail": ";".join(evaluator_statuses),
            "generated_utc": now,
        }
    )

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    row_pack: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 674 - Y5 R10 Edge Coefficient Row Fill Or Parent PiM Clause

## Verdict

674 tried the only derivation route still worth trying at this fork: a sharper parent `Pi_M`/null-edge clause.

Result: not signed.

The clean kill-shot would be:

```text
S_parent = S_red[q(Phi)] + int_boundary dB_edge
Dq[v_edge] = 0
Pi_M^H[Q_edge^H(lambda)] = 0
```

but the present corpus still lacks the jointly owned parent boundary representative, mass-cohomology orthogonality, fixed Hamiltonian reference, same-frame matter quotient, and no-pole boundary-zero certificate.

So 674 does not claim R10. It writes the edge coefficient row-fill pack and keeps every row invalid for claim until theorem-zero or source-backed values exist.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Parent PiM Clause Test

{markdown_table(parent_rows, ["clause_id", "candidate_clause", "mathematical_form", "acceptance_test", "current_result", "why_not_enough", "if_passes", "fallback", "valid_for_claim"])}

## Coefficient Requirements

{markdown_table(requirement_rows, ["requirement_id", "column_or_factor", "role", "claim_promotable_if", "current_fill", "units", "source_path_needed", "valid_for_claim"])}

## Edge Row Fill Pack

{markdown_table(row_pack, ["row_id", "branch_id", "lambda_value", "K_edge", "Qbar_edge_XH", "qbar_XT", "B_X_boundary_momentum", "M_H_ref", "alpha_predicted", "derivation_status", "promotion_gate", "valid_for_claim"])}

## Bound Curve Status Gate

{markdown_table(bound_rows, ["gate_id", "artifact", "numeric_rows", "claim_rows", "current_status", "claim_effect", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default route: either source the actual edge row inputs from parent-local files, or write a genuinely new null-edge action clause. Do not promote R10 from the private review curve or template rows.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    parent_rows = parent_pim_clause_rows()
    requirement_rows = coefficient_requirement_rows()
    row_pack = row_fill_pack_rows()
    bound_rows = bound_curve_gate_rows()
    evaluator = evaluator_rows(parent_rows, requirement_rows, row_pack, bound_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, parent_rows, requirement_rows, row_pack, bound_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_674_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_674_PARENT_PIM_CLAUSE_TEST.csv",
        parent_rows,
        ["clause_id", "candidate_clause", "mathematical_form", "acceptance_test", "current_result", "why_not_enough", "if_passes", "fallback", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
        requirement_rows,
        ["requirement_id", "column_or_factor", "role", "claim_promotable_if", "current_fill", "units", "source_path_needed", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_674_EDGE_ROW_FILL_PACK.csv",
        row_pack,
        ["row_id", "branch_id", "lambda_value", "lambda_units", "K_edge", "Qbar_edge_XH", "qbar_XT", "B_X_boundary_momentum", "M_H_ref", "alpha_edge_formula", "alpha_predicted", "alpha_bound_source", "derivation_status", "promotion_gate", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_674_BOUND_CURVE_STATUS_GATE.csv",
        bound_rows,
        ["gate_id", "artifact", "numeric_rows", "claim_rows", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_674_EVALUATOR.csv",
        evaluator,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_674_DECISION.csv",
        decision,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_674_NONCLAIM_SUMMARY.csv",
        summary,
        ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, parent_rows, requirement_rows, row_pack, bound_rows, evaluator, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"parent_clause_rows={len(parent_rows)}")
    print(f"coefficient_requirement_rows={len(requirement_rows)}")
    print(f"row_fill_pack_rows={len(row_pack)}")
    print(f"bound_curve_gate_rows={len(bound_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

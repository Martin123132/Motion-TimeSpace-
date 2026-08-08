from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3551-Y5-R2FR-MHref-qbasic-descent-or-Htau-Href-bound-pack.md"
CANONICAL_STATUS = OUT / "P8_Y5_MHref_qbasic_descent_Htau_Href_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3551": {"path": Path(__file__).resolve(), "role": "3551 generator"},
    "doc_3550": {
        "path": ROOT / "3550-Y5-R2FR-mass-flat-source-connection-PiM-chainmap-or-CM-Cshape-bound.md",
        "role": "mass-flat source connection handoff",
    },
    "next_3550": {
        "path": OUT / "P8_Y5_R2FR_3550_NEXT_TARGET.csv",
        "role": "3550 selected M_H_ref q-basic target",
    },
    "zero_proof_3550": {
        "path": OUT / "P8_Y5_R2FR_3550_MASS_FLAT_ZERO_PROOF_ATTEMPT.csv",
        "role": "M_H_ref q-basic clause from 3550",
    },
    "source_flatness_3515": {
        "path": OUT / "P8_EM_source_branch_mass_connection_flatness_law.csv",
        "role": "A_X^M source-connection identity",
    },
    "quotient_descent_3516": {
        "path": OUT / "P8_EM_quotient_source_coordinate_descent_certificate.csv",
        "role": "M_H_ref quotient-source descent clause",
    },
    "qmap_3517": {
        "path": OUT / "P8_EM_actual_q_map_vertical_basis_candidate.csv",
        "role": "candidate q-map and anti-tautology guard",
    },
    "field_quotient_2570": {
        "path": OUT / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv",
        "role": "vertical residual ledger",
    },
    "tau_source_rows_2597": {
        "path": OUT / "P8_Y5_TAU_IDENTITY_2597_MHREF_SOURCE_ACQUISITION_ROWS.csv",
        "role": "same tau / H_tau / H_ref / M_H_ref source acquisition rows",
    },
    "boundary_clock_owner_2599": {
        "path": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_OWNER_ATTEMPT.csv",
        "role": "boundary-clock tau owner attempt",
    },
    "htau_integrability_2667": {
        "path": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "role": "H_tau integrability curl gate",
    },
    "mhref_reference_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
        "role": "M_H_ref and H_ref reference lock",
    },
    "tau_generator_contract_685": {
        "path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "role": "tau generator contract",
    },
    "tau_generator_audit_684": {
        "path": OUT / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        "role": "tau generator audit",
    },
    "charge_decomposition_1008": {
        "path": OUT / "P8_Y5_R10_1008_CHARGE_DECOMPOSITION_SCHEMA.csv",
        "role": "parent Q_tau/H_tau charge decomposition schema",
    },
    "theta_qtau_doc_1008": {
        "path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "role": "parent theta/Q_tau extraction checkpoint",
    },
    "parent_frame_mhref_1519": {
        "path": OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
        "role": "parent frame M_H_ref first-row schema",
    },
    "denominator_ledger_1519": {
        "path": OUT / "P8_Y5_PARENT_FRAME_1519_DENOMINATOR_ACQUISITION_LEDGER.csv",
        "role": "denominator acquisition ledger",
    },
    "mhref_rows_2596": {
        "path": OUT / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
        "role": "M_H_ref denominator rows",
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


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


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


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "MHD3551_0_definition",
            "claim_piece": "mass coordinate",
            "statement": "M_H_ref(Phi) := H_tau[S_outer;Phi] - H_ref[Phi]",
            "proof_step": "This defines the source mass coordinate used by the source-branch connection A_X^M.",
            "condition_needed": "H_tau and H_ref must use the same tau, coframe, surface branch and units.",
            "current_status": "DEFINITION_ONLY_NONCLAIM",
            "source_path": str(SOURCES["mhref_reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "MHD3551_1_sum_difference_descent",
            "claim_piece": "q-basic difference theorem",
            "statement": "If H_tau=Hbar_tau(q(Phi)) and H_ref=Hbar_ref(q(Phi)), then M_H_ref=Mbar_H_ref(q(Phi)).",
            "proof_step": "Mbar_H_ref(q):=Hbar_tau(q)-Hbar_ref(q), so a difference of two q-basic scalars is q-basic.",
            "condition_needed": "same q branch, same tau/coframe/surface branch, no fitted reference subtraction.",
            "current_status": "EXACT_THEOREM_CONDITIONAL",
            "source_path": str(SOURCES["quotient_descent_3516"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "MHD3551_2_vertical_zero",
            "claim_piece": "A_X^M zero",
            "statement": "If M_H_ref=Mbar_H_ref(q(Phi)) and Dq(v_X)=0, then A_X^M=D_X M_H_ref=0.",
            "proof_step": "D_X M_H_ref=dMbar_H_ref(Dq(v_X))=0.",
            "condition_needed": "actual vertical residual vector v_X and actual parent q map.",
            "current_status": "EXACT_THEOREM_CONDITIONAL",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "MHD3551_3_mass_flat_corollary",
            "claim_piece": "C_M zero",
            "statement": "If A_X^M vanishes identically on the source branch, then partial_M A_X^M=0 and C_M=0.",
            "proof_step": "C_M = -(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau), so the first factor is zero.",
            "condition_needed": "no readout-defined source mass and positive normalization denominator.",
            "current_status": "EXACT_COROLLARY_NOT_PROMOTED",
            "source_path": str(SOURCES["source_flatness_3515"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "MHD3551_4_no_cancellation_rule",
            "claim_piece": "leakage discipline",
            "statement": "Without signed q-basicness, D_X M_H_ref must be bounded as D_X H_tau - D_X H_ref without relying on cancellation.",
            "proof_step": "|D_X M_H_ref| <= |D_X H_tau| + |D_X H_ref| by the triangle inequality.",
            "condition_needed": "independent H_tau and H_ref source rows, units and arena projections.",
            "current_status": "BOUND_ROUTE_REQUIRED_IF_THEOREM_UNSIGNED",
            "source_path": str(SOURCES["htau_integrability_2667"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def descent_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "HHD3551_0_actual_q_branch",
            "object": "q branch",
            "required_signature": "single visible q/e_obs/tau branch used by H_tau, H_ref, clocks, R10 and orbital readout",
            "current_evidence": "3517 proposes q components and marks source coordinates as non-primitive to avoid tautology",
            "status": "CANDIDATE_UNSIGNED",
            "failure_residual": "E_Dq",
            "source_path": str(SOURCES["qmap_3517"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "HHD3551_1_vertical_basis",
            "object": "v_X",
            "required_signature": "Dq(v_X)=0 for the actual residual direction used in source coupling",
            "current_evidence": "2570 supplies the chain-rule template but no live q matrix/kernel proof",
            "status": "UNSIGNED",
            "failure_residual": "E_vertical",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "HHD3551_2_Htau_qbasic",
            "object": "H_tau",
            "required_signature": "integrable parent Hamiltonian charge for tau_obs, built from theta/Q_tau with every retained sector extracted, zeroed or bounded",
            "current_evidence": "2597 lists H_tau, theta_MTS and Q_tau_MTS as missing; 2667 says H_tau curl is not claim-ready",
            "status": "UNSIGNED",
            "failure_residual": "E_Htau",
            "source_path": str(SOURCES["tau_source_rows_2597"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "HHD3551_3_Href_qbasic",
            "object": "H_ref",
            "required_signature": "source-blind reference/counterterm selected by boundary/topology/stationarity/asymptotic coframe before source readout",
            "current_evidence": "2938 installs the contract; 2597 still marks H_ref missing",
            "status": "UNSIGNED",
            "failure_residual": "E_Href",
            "source_path": str(SOURCES["mhref_reference_2938"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "HHD3551_4_same_tau_surface_frame",
            "object": "same branch",
            "required_signature": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary and the same surface/coframe branch is used",
            "current_evidence": "2599 says same tau normalization theorem and boundary-clock owner are missing",
            "status": "UNSIGNED",
            "failure_residual": "E_frame_tau",
            "source_path": str(SOURCES["boundary_clock_owner_2599"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "HHD3551_5_positive_denominator",
            "object": "M_H_ref",
            "required_signature": "finite positive same-frame M_H_ref with units, not imported from orbital GM",
            "current_evidence": "2597 and 2938 both keep positive M_H_ref as missing/nonclaim",
            "status": "UNSIGNED",
            "failure_residual": "E_denominator",
            "source_path": str(SOURCES["mhref_rows_2596"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def leakage_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "LB3551_0_A_M_identity",
            "quantity": "A_X^M",
            "formula": "A_X^M = D_X M_H_ref = D_X H_tau - D_X H_ref",
            "non_cancellation_bound": "|A_X^M| <= |D_X H_tau| + |D_X H_ref|",
            "needed_inputs": "D_X H_tau; D_X H_ref; common units; same branch; source path for each derivative",
            "current_value": "MISSING_DX_HTAU_AND_DX_HREF",
            "units": "mass/energy derivative along X or dimensionless after division by M_H_ref",
            "arena": "Gdot; Newton source mass; PPN source normalization; R10 denominator",
            "status": "EXACT_IDENTITY_BOUND_INPUTS_MISSING",
            "source_path": str(SOURCES["quotient_descent_3516"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "LB3551_1_Htau_leak",
            "quantity": "D_X H_tau",
            "formula": "D_X H_tau = E_theta + E_Qtau + E_curl + E_surface + E_sector + E_boundary",
            "non_cancellation_bound": "|D_X H_tau| <= |E_theta| + |E_Qtau| + |E_curl| + |E_surface| + |E_sector| + |E_boundary|",
            "needed_inputs": "parent theta/Q_tau owner; integrability curl bound; sector charge extraction; surface lock",
            "current_value": "MISSING_PARENT_HTAU_DERIVATIVE",
            "units": "mass/energy derivative or normalized residual",
            "arena": "source charge; clock; Newton/Poisson; PPN",
            "status": "NONCLAIM_BOUND_ROW",
            "source_path": str(SOURCES["charge_decomposition_1008"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "LB3551_2_Href_leak",
            "quantity": "D_X H_ref",
            "formula": "D_X H_ref = E_ref_selector + E_ref_boundary + E_ref_frame + E_ref_readout",
            "non_cancellation_bound": "|D_X H_ref| <= |E_ref_selector| + |E_ref_boundary| + |E_ref_frame| + |E_ref_readout|",
            "needed_inputs": "source-blind reference selector; boundary/topology/coframe data; no fitted counterterm certificate",
            "current_value": "MISSING_SOURCE_BLIND_HREF_DERIVATIVE",
            "units": "mass/energy derivative or normalized residual",
            "arena": "R10 denominator; Gdot; local boundary terms",
            "status": "NONCLAIM_BOUND_ROW",
            "source_path": str(SOURCES["mhref_reference_2938"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "LB3551_3_normalized_mass_leak",
            "quantity": "epsilon_MHref",
            "formula": "epsilon_MHref := |D_X M_H_ref|/|M_H_ref|",
            "non_cancellation_bound": "epsilon_MHref <= (|D_X H_tau|+|D_X H_ref|)/|M_H_ref|",
            "needed_inputs": "positive M_H_ref; D_X H_tau; D_X H_ref; uncertainty and units",
            "current_value": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "units": "dimensionless",
            "arena": "source-normalized Newton branch; local GR denominator; R10",
            "status": "NONCLAIM_DENOMINATOR_GUARD",
            "source_path": str(SOURCES["mhref_rows_2596"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "LB3551_4_C_M_derivative",
            "quantity": "partial_M A_X^M",
            "formula": "partial_M A_X^M = partial_M(D_X H_tau - D_X H_ref)",
            "non_cancellation_bound": "|partial_M A_X^M| <= |partial_M D_X H_tau| + |partial_M D_X H_ref|",
            "needed_inputs": "mass derivative of H_tau leak; mass derivative of H_ref leak; Pi_M H_tau denominator",
            "current_value": "MISSING_PARTIAL_M_DX_HTAU_AND_HREF",
            "units": "inverse mass/energy times residual derivative",
            "arena": "C_M in Pi_M/H_tau denominator square",
            "status": "NONCLAIM_CM_INPUT_ROW",
            "source_path": str(SOURCES["source_flatness_3515"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3551_0_theorem_verdict",
            "question": "Does 3551 prove live M_H_ref q-basic descent?",
            "decision": "No live claim. The theorem is exact, but H_tau and H_ref are not parent-signed q-basic scalars yet.",
            "basis": "2597 marks H_tau/H_ref/M_H_ref missing; 2667 keeps H_tau integrability blocked; 2938 keeps H_ref a contract only.",
            "consequence": "A_X^M and C_M remain nonclaim, but their leakage is now an explicit two-owner bound problem.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3551_1_no_cancellation",
            "question": "Can H_tau and H_ref leakage cancel?",
            "decision": "No. Treat them as independently zeroed or independently bounded.",
            "basis": "A source-blind reference cannot be tuned against the physical H_tau charge without laundering the mass denominator.",
            "consequence": "Use |D_X H_tau|+|D_X H_ref| and never a signed difference as evidence.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3551_2_next_target",
            "question": "Which owner should be attacked next?",
            "decision": "Attack H_tau q-basic charge extraction before H_ref polish.",
            "basis": "H_tau carries theta/Q_tau/integrability/source-charge content; without it M_H_ref cannot become a derived source mass.",
            "consequence": "Move to 3552: H_tau q-basic charge extraction or D_X H_tau bound pack.",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3551_0",
            "checkpoint": "3551 M_H_ref q-basic descent or H_tau/H_ref bound pack",
            "claim_allowed": "False",
            "M_H_ref_descent_status": "EXACT_IF_HTAU_AND_HREF_QBASIC_SAME_BRANCH; CURRENTLY_UNSIGNED",
            "A_XM_status": "A_X^M=D_X H_tau-D_X H_ref; ZERO_CONDITIONAL; BOUND_ROWS_NONCLAIM",
            "C_M_status": "C_M zero follows if A_X^M vanishes identically; otherwise partial_M leakage inputs missing",
            "strongest_result": "mass-coordinate obstruction reduced to two independent owners: H_tau charge extraction and H_ref source-blind selector",
            "next_target": "3552-Y5-R2FR-Htau-qbasic-charge-extraction-or-DXHtau-bound-pack.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3551_0",
            "target_doc": "3552-Y5-R2FR-Htau-qbasic-charge-extraction-or-DXHtau-bound-pack.md",
            "target_script": "scripts/Y5_R2FR_3552_Htau_qbasic_charge_extraction_or_DXHtau_bound_pack.py",
            "objective": "derive H_tau q-basicness by extracting the parent theta/Q_tau Hamiltonian charge on the visible q/e_obs/tau branch; if not, produce explicit nonclaim D_X H_tau and partial_M D_X H_tau bound rows",
            "success_gate": "either H_tau is parent-owned q-basic/integrable on the selected branch, or every H_tau leakage component has a source path, units, arena projection and valid_for_claim=false",
            "reason": "H_tau is the larger missing owner inside M_H_ref; H_ref cannot rescue the source mass by cancellation",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_csvs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    leaks: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_sources_exist = all(row["exists"] == "True" for row in sources)
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    exact_theorem_present = any(row["theorem_id"] == "MHD3551_1_sum_difference_descent" for row in theorem)
    required_clauses = {"HHD3551_2_Htau_qbasic", "HHD3551_3_Href_qbasic", "HHD3551_5_positive_denominator"}
    covered_clauses = {row["clause_id"] for row in clauses}
    descent_clauses_covered = required_clauses.issubset(covered_clauses)
    all_nonclaim = (
        all(row["valid_for_claim"] == "False" for row in theorem)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in clauses)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in leaks)
        and all(row["valid_for_claim"] == "False" for row in decisions)
    )
    no_cancellation_bound = all("+" in row["non_cancellation_bound"] or row["bound_id"] == "LB3551_0_A_M_identity" for row in leaks)
    missing_markers_present = all("MISSING_" in row["current_value"] for row in leaks)
    no_formalization_outputs = all(not path.resolve().is_relative_to(FORMALIZATION.resolve()) for path in generated_csvs)

    return [
        {
            "validation_id": "VAL3551_0_sources_exist",
            "passes": bool_text(all_sources_exist),
            "status": "PASS" if all_sources_exist else "FAIL",
            "detail": f"{sum(row['exists'] == 'True' for row in sources)}/{len(sources)} cited source paths exist",
        },
        {
            "validation_id": "VAL3551_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3551_2_exact_descent_theorem_present",
            "passes": bool_text(exact_theorem_present),
            "status": "PASS" if exact_theorem_present else "FAIL",
            "detail": "difference-of-q-basic-scalars theorem is present",
        },
        {
            "validation_id": "VAL3551_3_required_descent_clauses_covered",
            "passes": bool_text(descent_clauses_covered),
            "status": "PASS" if descent_clauses_covered else "FAIL",
            "detail": "H_tau, H_ref and positive M_H_ref denominator clauses are present",
        },
        {
            "validation_id": "VAL3551_4_all_rows_nonclaim",
            "passes": bool_text(all_nonclaim),
            "status": "PASS" if all_nonclaim else "FAIL",
            "detail": "theorem, clause, leakage and decision rows do not promote a claim",
        },
        {
            "validation_id": "VAL3551_5_no_cancellation_bound_pack",
            "passes": bool_text(no_cancellation_bound and missing_markers_present),
            "status": "PASS" if no_cancellation_bound and missing_markers_present else "FAIL",
            "detail": "leakage rows use triangle-bound discipline and expose missing parent inputs",
        },
        {
            "validation_id": "VAL3551_6_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3551 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3551 - M_H_ref q-basic descent or H_tau/H_ref bound pack",
        "",
        "## Verdict",
        "",
        "- **The derivation attempt succeeds conditionally:** `M_H_ref = H_tau - H_ref` is q-basic if `H_tau` and `H_ref` are q-basic on the same `q/e_obs/tau/surface` branch.",
        "- **The local zero mechanism is exact:** for vertical `v_X`, `D_X M_H_ref = dMbar_H_ref(Dq(v_X)) = 0`; then `A_X^M=0`, `partial_M A_X^M=0`, and `C_M=0`.",
        "- **It is not live yet:** current source rows still mark `H_tau`, `H_ref`, positive `M_H_ref`, theta/Q_tau ownership, H_tau curl, and same-tau normalization as unsigned.",
        "- **No cancellation is allowed:** if the theorem does not fire, use `|D_X M_H_ref| <= |D_X H_tau| + |D_X H_ref|`; do not tune the reference against the physical charge.",
        "",
        "## Descent Theorem",
        "",
        markdown_table(
            rows_by_name["theorem"],
            ["theorem_id", "claim_piece", "statement", "proof_step", "current_status"],
        ),
        "",
        "## Required Signatures",
        "",
        markdown_table(
            rows_by_name["clauses"],
            ["clause_id", "object", "required_signature", "status", "failure_residual"],
        ),
        "",
        "## Leakage Bound Pack",
        "",
        markdown_table(
            rows_by_name["leaks"],
            ["bound_id", "quantity", "formula", "non_cancellation_bound", "current_value", "status"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decisions"],
            ["decision_id", "question", "decision", "consequence"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3552-Y5-R2FR-Htau-qbasic-charge-extraction-or-DXHtau-bound-pack.md`: extract or bound `H_tau` itself, because it is the larger missing owner inside the mass coordinate.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    theorem = theorem_rows()
    clauses = descent_clause_rows()
    leaks = leakage_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3551_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv": (
            theorem,
            [
                "theorem_id",
                "claim_piece",
                "statement",
                "proof_step",
                "condition_needed",
                "current_status",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3551_HTAU_HREF_DESCENT_CLAUSE_AUDIT.csv": (
            clauses,
            [
                "clause_id",
                "object",
                "required_signature",
                "current_evidence",
                "status",
                "failure_residual",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3551_MHREF_LEAKAGE_BOUND_PACK.csv": (
            leaks,
            [
                "bound_id",
                "quantity",
                "formula",
                "non_cancellation_bound",
                "needed_inputs",
                "current_value",
                "units",
                "arena",
                "status",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3551_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "consequence", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3551_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "M_H_ref_descent_status",
                "A_XM_status",
                "C_M_status",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3551_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "M_H_ref_descent_status",
                "A_XM_status",
                "C_M_status",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, theorem, clauses, leaks, decisions)
    validation_path = OUT / "P8_Y5_BRR545_3551_VALIDATION.csv"
    write_csv(validation_path, validation, ["validation_id", "passes", "status", "detail"])
    generated_paths.append(validation_path)

    write_doc(
        {
            "theorem": theorem,
            "clauses": clauses,
            "leaks": leaks,
            "decisions": decisions,
            "status": status,
            "next_target": next_target,
            "validation": validation,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()

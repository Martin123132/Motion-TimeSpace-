from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3399-Y5-R2FR-source-normalization-component-extractor-under-AX1090.md"


SOURCES = {
    "3398_doc": ROOT / "3398-Y5-R2FR-parent-line-finite-source-normalization-bound-pack-under-AX1090.md",
    "3398_defs": OUT / "P8_Y5_R2FR_3398_RESIDUAL_BOUND_DEFINITIONS.csv",
    "3398_inputs": OUT / "P8_Y5_R2FR_3398_COMPONENT_INPUTS_NONCLAIM.csv",
    "3395_residuals": OUT / "P8_Y5_R2FR_3395_COUPLING_RESIDUAL_CONTRACT_NONCLAIM.csv",
    "3395_parent_line": OUT / "P8_Y5_R2FR_3395_MINIMAL_PARENT_ACTION_LINE_CANDIDATE.csv",
    "3396_adoption": OUT / "P8_Y5_R2FR_3396_PARENT_ADOPTION_PACKET_NONCLAIM.csv",
    "3377_theorem": OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv",
    "2576_law": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv",
    "2576_epsilonM": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_EPSILONM_SOURCE_CLOSURE_LEDGER.csv",
    "2576_owner": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_COUPLING_OWNER_EXTENSION.csv",
    "2576_gates": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_CLAIM_GATES.csv",
    "2577_theorem": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv",
    "2577_residuals": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_RESIDUAL_INPUT_LEDGER.csv",
    "2577_epsilonM": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_EPSILONM_CLOSURE_STATUS.csv",
    "2577_implications": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_NEWTON_GR_IMPLICATIONS.csv",
    "constant_kappa_theorem": OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
    "constant_kappa_gates": OUT / "P8_CONSTANT_KAPPA_GATE_TESTS.csv",
    "global_coupling_contract": OUT / "P8_global_coupling_superselection_CONTRACT.csv",
    "universal_kappa_contract": OUT / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
    "source_ward_contract": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "ward_owner_contract": OUT / "P8_Ward_source_owner_identity_CONTRACT.csv",
    "source_current_2642_proof": OUT / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv",
    "source_current_2642_bounds": OUT / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv",
    "hamiltonian_charge_contract": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
    "source_measure_flux_theorem": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "source_measure_flux_map": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "source_norm_2583_coeffs": OUT / "P8_Y5_SOURCE_NORM_2583_R11_COEFFICIENT_VECTOR.csv",
    "source_norm_2583_gm": OUT / "P8_Y5_SOURCE_NORM_2583_CONSTANT_GM_RESIDUAL_ROWS.csv",
}


OUTPUT_PATHS = {
    "source_register": OUT / "P8_Y5_R2FR_3399_SOURCE_REGISTER.csv",
    "component_extraction": OUT / "P8_Y5_R2FR_3399_COMPONENT_EXTRACTION_MATRIX.csv",
    "numeric_source_scan": OUT / "P8_Y5_R2FR_3399_NUMERIC_SOURCE_SCAN.csv",
    "first_order_theorem": OUT / "P8_Y5_R2FR_3399_FIRST_ORDER_NEWTON_ZERO_THEOREM.csv",
    "closure_chain": OUT / "P8_Y5_R2FR_3399_NEWTON_CLOSURE_CHAIN.csv",
    "kappav_targets": OUT / "P8_Y5_R2FR_3399_KAPPAV_SECOND_ORDER_TARGETS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3399_PROMOTION_GATES.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3399_RUNNER_NONCLAIM.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3399_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3399_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3399_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def text_contains(path: Path, *needles: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    return all(needle.lower() in text for needle in needles)


def rows_containing(path: Path, *needles: str) -> list[dict[str, str]]:
    if not path.exists():
        return []
    result: list[dict[str, str]] = []
    for row in read_csv(path):
        blob = " ".join(str(value) for value in row.values()).lower()
        if all(needle.lower() in blob for needle in needles):
            result.append(row)
    return result


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": f"SRC3399_{idx:02d}_{name}",
            "path": str(path),
            "exists": path.exists(),
            "role": "component_extraction_source",
            "valid_for_claim": False,
        }
        for idx, (name, path) in enumerate(SOURCES.items())
    ]


def source_status(path: Path, *needles: str) -> str:
    hits = rows_containing(path, *needles)
    if not hits:
        return "NO_MATCH_FOUND"
    blob = " ".join(" ".join(row.values()) for row in hits).lower()
    if "missing_numeric" in blob or "values_missing" in blob or "not_parent_derived" in blob or "not_derived" in blob or "unsigned" in blob:
        return "MATCHED_CONDITIONAL_OR_MISSING_NUMERIC"
    if "exact" in blob or "conditional" in blob:
        return "MATCHED_EXACT_CONDITIONAL"
    return "MATCHED_RELEVANT_ROW"


def component_extraction() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "CX3399_0_B_delta_kappa",
            "bound_symbol": "B_delta_kappa",
            "residual_closed_if": "global/superselection or topological-zero-form kappa clause is parent-signed and carries no source/species/range labels",
            "strongest_extracted_evidence": "T508_0/T508_1 and CU1/GS1 define a sufficient constant-kappa route; 2576 says current owner missing",
            "source_files": ";".join(str(SOURCES[key]) for key in ["constant_kappa_theorem", "constant_kappa_gates", "global_coupling_contract", "universal_kappa_contract", "2576_owner"]),
            "extraction_status": "CONDITIONAL_ZERO_ROUTE_EXTRACTED_NOT_PARENT_SIGNED",
            "numeric_bound_value": "MISSING_NUMERIC_VALUE",
            "numeric_bound_units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CX3399_1_B_delta_ellJ",
            "bound_symbol": "B_delta_ellJ",
            "residual_closed_if": "same observed coframe matter variation defines Hilbert stress, J_H, compact mass, and PPN source density with ell_J=1",
            "strongest_extracted_evidence": "SC1/SC2 define Hilbert/Ward route; SCI2642_1 gives clean descent lemma; current parent signature remains unsigned",
            "source_files": ";".join(str(SOURCES[key]) for key in ["source_ward_contract", "source_current_2642_proof", "source_current_2642_bounds", "2576_owner"]),
            "extraction_status": "CONDITIONAL_ZERO_ROUTE_EXTRACTED_NOT_PARENT_SIGNED",
            "numeric_bound_value": "MISSING_NUMERIC_VALUE",
            "numeric_bound_units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CX3399_2_B_GH",
            "bound_symbol": "B_GH",
            "residual_closed_if": "Hamiltonian boundary charge H_tau equals the same Pi_M-projected Hilbert mass current normalized by G_ref",
            "strongest_extracted_evidence": "HC4/HC8 and WSC2577_2 specify the needed H_tau/Pi_M identity; both are not parent-derived",
            "source_files": ";".join(str(SOURCES[key]) for key in ["hamiltonian_charge_contract", "source_measure_flux_theorem", "2577_theorem"]),
            "extraction_status": "CONDITIONAL_ZERO_ROUTE_EXTRACTED_PIM_HAMILTONIAN_UNSIGNED",
            "numeric_bound_value": "MISSING_NUMERIC_VALUE",
            "numeric_bound_units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CX3399_3_B_GPPN",
            "bound_symbol": "B_GPPN",
            "residual_closed_if": "PPN potential U uses the same G_ref and same M_H/Pi_M J_H source as Poisson and H_tau",
            "strongest_extracted_evidence": "3397/3398 require same U; 2577 implications say local GR would follow if epsilon_M, delta_KC, delta_kappa, delta_ellJ, kappa_v and vector silence close",
            "source_files": ";".join(str(SOURCES[key]) for key in ["3398_defs", "2577_implications", "2576_law"]),
            "extraction_status": "CONDITIONAL_ZERO_ROUTE_EXTRACTED_PPN_SOURCE_UNSIGNED",
            "numeric_bound_value": "MISSING_NUMERIC_VALUE",
            "numeric_bound_units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CX3399_4_B_delta_KC",
            "bound_symbol": "B_delta_KC",
            "residual_closed_if": "parent v-reduction gives L_v=-c^4/(32*pi*G_ref)|grad v|^2-rho_H*c^2*v/2",
            "strongest_extracted_evidence": "3377 and 3398 derive the coefficient-ratio target; 2576 defines delta_KC exactly",
            "source_files": ";".join(str(SOURCES[key]) for key in ["3377_theorem", "2576_law", "3398_defs"]),
            "extraction_status": "DERIVED_RATIO_TARGET_EXTRACTED_PARENT_COEFFICIENTS_UNSIGNED",
            "numeric_bound_value": "MISSING_PARENT_Av_Bv_NUMERIC_VALUE",
            "numeric_bound_units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CX3399_5_B_epsilon_M",
            "bound_symbol": "B_epsilon_M",
            "residual_closed_if": "worldtube selector, PiM/Hamiltonian identity, R_eq zero, B_zero flux zero, Pi_M chain map, fixed kappa/ellJ, and extra-channel silence all hold in one branch",
            "strongest_extracted_evidence": "EPS2577_1 gives exact conditional zero theorem; EPS2577_2 gives exact absolute no-cancellation envelope; residual ledger has missing numeric inputs",
            "source_files": ";".join(str(SOURCES[key]) for key in ["2577_epsilonM", "2577_residuals", "2577_theorem", "source_measure_flux_map"]),
            "extraction_status": "EXACT_ENVELOPE_EXTRACTED_COMPONENT_NUMERICS_MISSING",
            "numeric_bound_value": "MISSING_NUMERIC_VALUE",
            "numeric_bound_units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CX3399_6_B_kappa_v",
            "bound_symbol": "B_kappa_v",
            "residual_closed_if": "second-order beta-source, PiM, boundary, readout, operator, and coupling terms vanish or are independently bounded",
            "strongest_extracted_evidence": "2576 gives kappa_v=-eta_v+kappa_source_quad+kappa_PiM+kappa_boundary+kappa_readout+kappa_operator+kappa_coupling; 2642/2583 identify source and boundary component ledgers",
            "source_files": ";".join(str(SOURCES[key]) for key in ["2576_law", "source_current_2642_bounds", "source_norm_2583_coeffs", "source_norm_2583_gm"]),
            "extraction_status": "SECOND_ORDER_LEDGER_EXTRACTED_COMPONENT_NUMERICS_MISSING",
            "numeric_bound_value": "MISSING_NUMERIC_VALUE",
            "numeric_bound_units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["evidence_files_exist"] = all(Path(path).exists() for path in row["source_files"].split(";"))
    return rows


def numeric_source_scan() -> list[dict[str, Any]]:
    files = {
        "B_epsilon_M_components": SOURCES["2577_residuals"],
        "B_kappa_v_component_bounds": SOURCES["source_current_2642_bounds"],
        "R11_source_coefficients": SOURCES["source_norm_2583_coeffs"],
        "constant_GM_rows": SOURCES["source_norm_2583_gm"],
    }
    rows: list[dict[str, Any]] = []
    for scan_id, path in files.items():
        table = read_csv(path) if path.exists() else []
        missing_numeric = 0
        score_ready_true = 0
        claim_true = 0
        for row in table:
            blob = " ".join(str(value) for value in row.values())
            if "MISSING_NUMERIC" in blob or "MISSING_" in blob or "VALUES_MISSING" in blob:
                missing_numeric += 1
            if str(row.get("score_ready", "")).lower() == "true":
                score_ready_true += 1
            if str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true += 1
        rows.append(
            {
                "scan_id": f"NS3399_{scan_id}",
                "path": str(path),
                "rows_scanned": len(table),
                "rows_with_missing_numeric_markers": missing_numeric,
                "score_ready_true_rows": score_ready_true,
                "claim_true_rows": claim_true,
                "scan_verdict": "NO_NUMERIC_SOURCE_ROWS_READY" if score_ready_true == 0 and claim_true == 0 else "REVIEW_READY_ROWS",
                "valid_for_claim": False,
            }
        )
    return rows


def first_order_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_row": "T3399_P0_parent_branch",
            "premise_or_step": "premise",
            "statement": "Use one parent branch with observed metric/coframe g_obs/e_obs, universal kappa_MTS, matter action S_matter[e_obs(q(Phi)),Psi], H_tau/Q_tau/B_ref/Pi_M, and ell_J fixed before readout.",
            "evidence": "MPL3395 candidate and 3396 adoption packet",
            "status": "STAGED_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_row": "T3399_P1_constant_kappa",
            "premise_or_step": "premise",
            "statement": "kappa_MTS is a global/superselection or topological integration constant with kappa_MTS=8*pi*G_ref/c^4 in the local branch.",
            "evidence": "T508/CU/GS contracts give sufficient route",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
        },
        {
            "theorem_row": "T3399_P2_hilbert_source",
            "premise_or_step": "premise",
            "statement": "The same S_matter variation defines T_mu_nu, J_H, M_H, and PPN source density, so ell_J=1 and delta_ellJ=0.",
            "evidence": "SC Ward contract plus SCI2642_1 descent lemma",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
        },
        {
            "theorem_row": "T3399_P3_pim_charge",
            "premise_or_step": "premise",
            "statement": "Pi_M is a fixed chain map and H_tau boundary charge equals the Pi_M-projected Hilbert mass current with the same G_ref.",
            "evidence": "HC4/HC8/WSC2577_2",
            "status": "CONDITIONAL_ZERO_ROUTE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_row": "T3399_P4_no_boundary_or_extra_mass",
            "premise_or_step": "premise",
            "statement": "R_eq=0, B_zero_flux=0, I_commutator=0, extra source channels vanish, and calibration is fixed before readout.",
            "evidence": "EPS2577 zero theorem and source-measure residual map",
            "status": "CONDITIONAL_ZERO_ROUTE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_row": "T3399_P5_v_ratio",
            "premise_or_step": "premise",
            "statement": "The parent v reduction has B_v/A_v=16*pi*G_ref/c^4, equivalently A_v=c^4/(32*pi*G_ref) and B_v=1/2.",
            "evidence": "3377/3398 v-action ratio derivation",
            "status": "RATIO_DERIVED_PARENT_COEFFICIENTS_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_row": "T3399_D1_residual_zeroes",
            "premise_or_step": "derivation",
            "statement": "P1-P5 imply delta_kappa=0, delta_ellJ=0, epsilon_Gref_match=0, delta_KC=0, and epsilon_M=0 in the same branch.",
            "evidence": "Definitions in 3398 and extracted component zero routes",
            "status": "EXACT_CONDITIONAL_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "theorem_row": "T3399_D2_newton_zero",
            "premise_or_step": "derivation",
            "statement": "Substituting those zeroes into Delta_Newton_v_coupled=(1+delta_KC)(1+epsilon_M)(1+delta_kappa)(1+delta_ellJ)-1 gives Delta_Newton_v_coupled=0.",
            "evidence": "3398 product law",
            "status": "EXACT_CONDITIONAL_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "theorem_row": "T3399_D3_ppn_not_closed",
            "premise_or_step": "guardrail",
            "statement": "This closes only the first-order Newton/source-amplitude branch; beta/full PPN still needs kappa_v and preferred-frame/conservation/location residuals.",
            "evidence": "3397 PPN vector gate and 2576 beta law",
            "status": "LOCAL_GR_NOT_CLAIMED",
            "valid_for_claim": False,
        },
    ]


def closure_chain() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "NC3399_0_delta_kappa",
            "input": "P1 constant kappa",
            "derived_residual": "delta_kappa=0",
            "current_status": "conditional route extracted, parent signature missing",
            "blocks_now": True,
            "valid_for_claim": False,
        },
        {
            "chain_id": "NC3399_1_delta_ellJ",
            "input": "P2 same Hilbert source",
            "derived_residual": "delta_ellJ=0",
            "current_status": "conditional route extracted, matter descent/source-scale signature missing",
            "blocks_now": True,
            "valid_for_claim": False,
        },
        {
            "chain_id": "NC3399_2_epsilon_Gref_match",
            "input": "P1+P3 same G_ref in EH/H_tau/PPN",
            "derived_residual": "epsilon_Gref_match=0",
            "current_status": "conditional route extracted, H_tau/Pi_M/PPN source identity missing",
            "blocks_now": True,
            "valid_for_claim": False,
        },
        {
            "chain_id": "NC3399_3_delta_KC",
            "input": "P5 v coefficient ratio",
            "derived_residual": "delta_KC=0",
            "current_status": "ratio target derived, parent A_v/B_v extraction missing",
            "blocks_now": True,
            "valid_for_claim": False,
        },
        {
            "chain_id": "NC3399_4_epsilon_M",
            "input": "P2+P3+P4 worldtube/Hilbert selector",
            "derived_residual": "epsilon_M=0",
            "current_status": "exact zero theorem extracted, components unsigned/numeric missing",
            "blocks_now": True,
            "valid_for_claim": False,
        },
        {
            "chain_id": "NC3399_5_Delta_Newton",
            "input": "NC3399_0..NC3399_4",
            "derived_residual": "Delta_Newton_v_coupled=0",
            "current_status": "exact first-order Newton closure theorem assembled but not parent-signed",
            "blocks_now": True,
            "valid_for_claim": False,
        },
    ]


def kappav_targets() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "KV3399_0_eta_v",
            "component": "eta_v",
            "meaning": "intrinsic second-order v nonlinearity",
            "needed_for": "beta-1=kappa_v/2",
            "current_status": "MISSING_SECOND_ORDER_V_SOLUTION",
            "valid_for_claim": False,
        },
        {
            "target_id": "KV3399_1_source_quad",
            "component": "kappa_source_quad",
            "meaning": "quadratic matter/source normalization correction",
            "needed_for": "beta source stability",
            "current_status": "MISSING_SECOND_ORDER_SOURCE_EXPANSION",
            "valid_for_claim": False,
        },
        {
            "target_id": "KV3399_2_PiM",
            "component": "kappa_PiM",
            "meaning": "second-order Pi_M/projector mass correction",
            "needed_for": "beta and zeta source conservation",
            "current_status": "MISSING_PIM_VARIATION_BOUND",
            "valid_for_claim": False,
        },
        {
            "target_id": "KV3399_3_boundary",
            "component": "kappa_boundary",
            "meaning": "second-order boundary/reference/source-worldtube term",
            "needed_for": "beta, zeta3, alpha3",
            "current_status": "MISSING_BOUNDARY_SECOND_ORDER_BOUND",
            "valid_for_claim": False,
        },
        {
            "target_id": "KV3399_4_readout_operator",
            "component": "kappa_readout+kappa_operator",
            "meaning": "readout and non-EH/operator correction at beta order",
            "needed_for": "beta and full PPN vector",
            "current_status": "MISSING_READOUT_OPERATOR_SECOND_ORDER_BOUND",
            "valid_for_claim": False,
        },
        {
            "target_id": "KV3399_5_coupling",
            "component": "kappa_coupling",
            "meaning": "second-order propagation of delta_kappa/delta_ellJ/source baseline",
            "needed_for": "beta after first-order Newton closure",
            "current_status": "PARTIALLY_REDUCED_IF_FIRST_ORDER_CHAIN_SIGNS",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3399_0_component_sources",
            "claim": "component zero/bound routes are extracted from existing corpus",
            "gate_pass": True,
            "reason": "all seven headline bound symbols have source files and extracted status rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3399_1_first_order_theorem",
            "claim": "first-order Newton/source-amplitude zero theorem is assembled",
            "gate_pass": True,
            "reason": "premises imply delta_kappa=delta_ellJ=epsilon_Gref_match=delta_KC=epsilon_M=0 and hence Delta_Newton=0",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3399_2_parent_signed",
            "claim": "the first-order theorem is active in the current parent theory",
            "gate_pass": False,
            "reason": "constant-kappa, same-source, PiM/Hamiltonian, boundary, and v-coefficient clauses are not parent-signed together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3399_3_numeric_fallback",
            "claim": "numeric component fallback rows are ready for scoring",
            "gate_pass": False,
            "reason": "source scans found missing numeric markers and no score-ready rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3399_4_local_GR",
            "claim": "local GR/PPN is derived",
            "gate_pass": False,
            "reason": "first-order Newton route is conditional; kappa_v and full PPN vector remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3399_0_scan",
            "test": "source component extraction",
            "status": "PASS_COMPONENT_ROUTES_EXTRACTED_NONCLAIM",
            "detail": "seven component rows produced from existing coupling/ward/source-selector corpus",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3399_1_newton_theorem",
            "test": "first-order Newton closure chain",
            "status": "PASS_EXACT_CONDITIONAL_THEOREM_ASSEMBLED",
            "detail": "Delta_Newton=0 follows if named parent clauses are signed in one branch",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3399_2_numeric",
            "test": "numeric source rows",
            "status": "BLOCK_NUMERIC_ROWS_NOT_READY",
            "detail": "fallback remains nonclaim because numeric rows are absent",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3399_3_beta",
            "test": "kappa_v beta branch",
            "status": "BLOCK_SECOND_ORDER_COMPONENTS_OPEN",
            "detail": "kappa_v component targets listed for next attack",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3399_0_actual_progress",
            "finding": "the first-order Newton/source-amplitude route is no longer just a missing list",
            "reason": "existing constant-kappa, Ward/source-current, Hamiltonian/PiM, and worldtube selector pieces assemble into an exact conditional zero theorem",
            "next_action": "write the parent-signature clause pack that would make P0-P5 active, or choose numeric fallback rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3399_1_best_route",
            "finding": "least-scrutiny path is parent-signing the first-order theorem, not fitting numeric fallback constants",
            "reason": "numeric fallback rows are absent; the algebraic zero theorem is cleaner and closer to GR-style reduction",
            "next_action": "3400 should be a parent-clause adoption/signature audit for P0-P5, not another broad scan",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3399_2_remaining_hard_part",
            "finding": "even if first-order Newton closes, beta/local PPN still lives in kappa_v",
            "reason": "2576 makes beta-1=kappa_v/2; 3399 only reduces first-order source-amplitude coupling",
            "next_action": "after parent clause pack, attack kappa_v second-order targets",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3400-Y5-R2FR-first-order-source-coupling-parent-signature-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3400_first_order_source_coupling_parent_signature_pack.py",
            "objective": "turn T3399 P0-P5 into a precise parent-signature clause pack and audit whether the current core can adopt it without contradiction",
            "why_next": "3399 found that the clean route is an exact conditional first-order Newton zero theorem; the next leap is to try to sign it rather than keep scanning",
            "valid_for_claim": False,
        },
        {
            "target_id": "3401-Y5-R2FR-kappav-second-order-beta-ledger-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3401_kappav_second_order_beta_ledger.py",
            "objective": "derive or bound eta_v, source_quad, PiM, boundary, readout/operator, and coupling terms in kappa_v",
            "why_next": "local GR still requires beta/full PPN after first-order Newton source coupling is conditionally closed",
            "valid_for_claim": False,
        },
    ]


def validate(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": passed, "detail": detail})

    add("VAL3399_0_sources_exist", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3399_1_components", "all expected bound components extracted", len(outputs["component_extraction"]) == 7 and all(row["evidence_files_exist"] for row in outputs["component_extraction"]), "")
    add("VAL3399_2_numeric_scan", "numeric scan blocks fallback scoring", all(row["scan_verdict"] == "NO_NUMERIC_SOURCE_ROWS_READY" for row in outputs["numeric_source_scan"]), "")
    theorem_rows = outputs["first_order_theorem"]
    add("VAL3399_3_theorem_premises", "first-order theorem has premises and derivation rows", sum(1 for row in theorem_rows if row["premise_or_step"] == "premise") >= 6 and sum(1 for row in theorem_rows if row["premise_or_step"] == "derivation") >= 2, "")
    add("VAL3399_4_newton_zero_step", "Delta_Newton zero derivation is explicit", any("Delta_Newton_v_coupled=0" in row["statement"] for row in theorem_rows), "")
    add("VAL3399_5_kappav_targets", "kappa_v second-order targets listed", len(outputs["kappav_targets"]) >= 6, "")
    add("VAL3399_6_no_overclaim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim", False)).lower() == "false" for group in outputs.values() for row in group), "")
    add("VAL3399_7_scope", "no 3399 output path targets formalization-workbench", "formalization-workbench" not in str(DOC).lower() and all("formalization-workbench" not in str(path).lower() for path in OUTPUT_PATHS.values()), "")
    add("VAL3399_8_next_target", "next target is parent-signature pack", any("parent-signature" in row["objective"] for row in outputs["next_target"]), "")
    add("VAL3399_9_overall", "3399 validation overall", all(row["passed"] is True for row in rows), "all required checks passed")
    return rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    sections = [
        "# 3399 - Y5/R2FR source-normalization component extractor under AX1090",
        "",
        "## Summary",
        "- 3399 mines the existing coupling corpus rather than starting over.",
        "- It extracts conditional zero routes for `B_delta_kappa`, `B_delta_ellJ`, `B_GH`, `B_GPPN`, `B_delta_KC`, `B_epsilon_M`, and `B_kappa_v`.",
        "- The main advance is an assembled first-order Newton/source-amplitude zero theorem: if the named parent clauses P0-P5 are signed in one branch, then `Delta_Newton_v_coupled=0` follows algebraically.",
        "- This is not a local-GR claim: the parent signature is not yet adopted, numeric fallback rows are not score-ready, and `kappa_v`/full PPN remain open.",
        f"- Generated UTC: `{timestamp}`.",
        "",
        "## Source Register",
        md_table(outputs["source_register"]),
        "",
        "## Component Extraction Matrix",
        md_table(outputs["component_extraction"]),
        "",
        "## Numeric Source Scan",
        md_table(outputs["numeric_source_scan"]),
        "",
        "## First-Order Newton Zero Theorem",
        md_table(outputs["first_order_theorem"]),
        "",
        "## Newton Closure Chain",
        md_table(outputs["closure_chain"]),
        "",
        "## Kappa_v Second-Order Targets",
        md_table(outputs["kappav_targets"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Nonclaim Runner",
        md_table(outputs["runner_nonclaim"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    outputs = {
        "source_register": source_register(),
        "component_extraction": component_extraction(),
        "numeric_source_scan": numeric_source_scan(),
        "first_order_theorem": first_order_theorem(),
        "closure_chain": closure_chain(),
        "kappav_targets": kappav_targets(),
        "promotion_gates": promotion_gates(),
        "runner_nonclaim": runner_nonclaim(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    outputs["validation"] = validate(outputs)
    for name, rows in outputs.items():
        write_csv(OUTPUT_PATHS[name], rows)
    parsed = [(path.name, len(read_csv(path))) for path in OUTPUT_PATHS.values()]
    if not all(row["passed"].lower() == "true" for row in read_csv(OUTPUT_PATHS["validation"])):
        raise RuntimeError("3399 validation failed")
    write_doc(outputs)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUT_PATHS)} CSV outputs under {OUT}")
    print("Parsed outputs: " + "; ".join(f"{name}={count}" for name, count in parsed))


if __name__ == "__main__":
    main()

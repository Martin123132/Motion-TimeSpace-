from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1910"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1910-Y5-R2FR-parent-material-response-functional-or-exact-mass-defect-tensor-contract.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1909_doc": ROOT / "1909-Y5-R2FR-TiPt-alloy-material-binding-projection-or-blocker-ledger.md",
    "1909_validation": OUT / "P8_Y5_BRR545_1909_VALIDATION.csv",
    "1909_proxy": OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_PROXY_VECTOR_NONCLAIM.csv",
    "1909_blockers": OUT / "P8_Y5_PARENT_QLOC_1909_MATERIAL_BINDING_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv",
    "1909_projection_status": OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_MATERIAL_BINDING_PROJECTION_STATUS_NONCLAIM.csv",
    "1895_basis": OUT / "P8_Y5_PARENT_QLOC_1895_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv",
    "1607_schema": MICROSCOPE_RESIDUALS / "R2FR_material_tensor_import_schema_nonclaim_1607.csv",
    "1053_charge_matrix": OUT / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv",
    "1080_cparent_contract": OUT / "P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv",
    "1466_em_decision": MICROSCOPE_COEFFS / "C_parent_WEP_EM_edge_signing_decision_1466.csv",
    "1466_em_attempt": MICROSCOPE_COEFFS / "EM_current_edge_owner_proof_attempt_1466.csv",
    "1837_response_contract": MICROSCOPE_RESIDUALS / "P8_Y5_PARENT_QLOC_1837_PWEP_RESPONSE_CONTRACT.csv",
    "1897_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv",
    "1899_wep_input_pack": OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
    "1899_action_owner": OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv",
    "1900_official_data": OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
}


SOURCE_NEEDLES = {
    "1909_doc": ["NEXT1909_0_primary", "1910-Y5-R2FR-parent-material-response-functional-or-exact-mass-defect-tensor-contract.md"],
    "1909_validation": ["VAL1909_OVERALL,PASS"],
    "1909_proxy": ["AP1909_TA6V_minus_PtRh10", "DIFFERENTIAL_ALLOY_PROXY_CONTEXT_ONLY"],
    "1909_blockers": ["BB1909_5_source_readout_kernel", "MISSING_SOURCE_READOUT_TAU_KERNEL"],
    "1909_projection_status": ["MP1909_3_verdict", "ALLOY_PROXY_GAINED_MATERIAL_BINDING_PROJECTION_STILL_BLOCKED"],
    "1895_basis": ["PMTB1895_3_tensor_formula", "FORMULA_STUB_PARENT_BASIS_MISSING"],
    "1607_schema": ["MTS1607_2_component", "MTS1607_12_no_double_counting_rule"],
    "1053_charge_matrix": ["WCM1053_6", "MISSING_FULL_MATERIAL_TENSOR"],
    "1080_cparent_contract": ["CP1080_0_definition", "MISSING_PARENT_COEFFICIENT"],
    "1466_em_decision": ["SIGN1466_0_EM_edge", "KEEP_EM_EDGE_AS_EXACT_CONDITIONAL"],
    "1466_em_attempt": ["EME1466_5_verdict", "EXACT_CONDITIONAL_EDGE_THEOREM_NOT_PARENT_SIGNED"],
    "1837_response_contract": ["PWC1837_2_material_source", "MISSING_MATERIAL_SOURCE_PRODUCT"],
    "1897_projection_requirements": ["DPR1897_1_arena_tau_K", "MISSING_ARENA_PROJECTION_KERNELS"],
    "1899_wep_input_pack": ["WIP1899_3_material_tensor", "MISSING_FULL_MATERIAL_TENSOR"],
    "1899_action_owner": ["ACO1899_6_verdict", "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED"],
    "1900_official_data": ["OFFICIAL_DATA_TARGET_NOT_ACQUIRED_NONCLAIM", "SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1910_SOURCE_REGISTER.csv",
    "response_functional": OUT / "P8_Y5_PARENT_QLOC_1910_PARENT_MATERIAL_RESPONSE_FUNCTIONAL_ATTEMPT.csv",
    "common_mode_zero": OUT / "P8_Y5_PARENT_QLOC_1910_COMMON_MODE_ZERO_THEOREM_CONDITIONAL.csv",
    "tensor_contract": OUT / "P8_Y5_PARENT_QLOC_1910_EXACT_MASS_DEFECT_TENSOR_CONTRACT_NONCLAIM.csv",
    "proxy_refusal": OUT / "P8_Y5_PARENT_QLOC_1910_PROXY_IMPORT_REFUSAL_MATRIX_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1910_RESPONSE_FUNCTIONAL_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1910_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1910_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1910_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1910_VALIDATION.csv",
}


BRANCH_COPIES = {
    "response_functional": SOURCE_WEIGHT_DOCS / "PARENT_MATERIAL_RESPONSE_FUNCTIONAL_1910_NONCLAIM.csv",
    "tensor_contract": MICROSCOPE_RESIDUALS / OUTPUTS["tensor_contract"].name,
    "proxy_refusal": QUEUE / "JR1910_PROXY_IMPORT_REFUSAL_MATRIX_NONCLAIM.csv",
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, MICROSCOPE_COEFFS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in SOURCE_NEEDLES[source_id] if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(SOURCE_NEEDLES[source_id]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def proxy_values() -> dict[str, str]:
    for row in csv_rows(INPUTS["1909_proxy"]):
        if row["proxy_id"] == "AP1909_TA6V_minus_PtRh10":
            return row
    raise RuntimeError("AP1909_TA6V_minus_PtRh10 not found")


def response_functional_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "MRF1910_0_target",
            "claim_piece": "parent material response functional",
            "formal_statement": "Construct R_A^X := V_X ln M_A[q, matter, theta] and DeltaR_AB^X := R_A^X - R_B^X in a parent-owned basis before WEP readout.",
            "result": "TARGET_SHARP",
            "what_is_derived": "the exact object that must replace ad-hoc Z/A or DD charge shortcuts",
            "what_is_not_derived": "the parent-owned list of V_X, coefficient C_X, and source/readout/tau contraction",
            "source_anchor": "PMTB1895_3_tensor_formula; PWC1837_2_material_source",
            "parent_signed": False,
            "projection_ready": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MRF1910_1_mass_functional_definition",
            "claim_piece": "test-body mass functional",
            "formal_statement": "Let M_A = c^-2 integral_A rho_A(e_obs, psi_A, A_Q, q, theta) dV in one declared observed coframe; component splits are admissible only after a no-double-count partition is signed.",
            "result": "DEFINITION_CONTRACT_STATED",
            "what_is_derived": "all material response rows must be derivatives of one mass functional, not separate fitted source charges",
            "what_is_not_derived": "the current corpus does not yet provide the signed partition of rho_A into independent parent components",
            "source_anchor": "MTS1607_12_no_double_counting_rule; BB1909_1_atomic_nuclear_mass_convention",
            "parent_signed": False,
            "projection_ready": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MRF1910_2_common_mode_zero",
            "claim_piece": "universal mass-energy response cancels in WEP",
            "formal_statement": "If V_U M_A = sigma_U M_A for every ordinary test body A in the same observed coframe, then DeltaR_AB^U = V_U ln M_A - V_U ln M_B = 0 exactly.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "what_is_derived": "common-mode universal metric response cannot create a Ti/Pt differential WEP signal",
            "what_is_not_derived": "MTS has not yet proven all nonuniversal V_X are absent or parent-zero",
            "source_anchor": "ACO1899_1_conditional_lemma; PMTB1895_3_tensor_formula",
            "parent_signed": False,
            "projection_ready": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MRF1910_3_sector_response_law",
            "claim_piece": "finite component response law",
            "formal_statement": "If M_A = sum_c E_Ac/c^2 and V_X E_Ac = gamma_cX E_Ac with independent components c, then DeltaR_AB^X = sum_c (f_Ac - f_Bc) gamma_cX, f_Ac := E_Ac/sum_d E_Ad.",
            "result": "EXACT_CONDITIONAL_ALGEBRA",
            "what_is_derived": "alloy proxies become tensor inputs only through component fractions f_Ac and parent generator weights gamma_cX",
            "what_is_not_derived": "gamma_cX, the independent component partition, and the source/readout product are missing",
            "source_anchor": "AP1909_TA6V_minus_PtRh10; MTS1607_2_component; CP1080_0_definition",
            "parent_signed": False,
            "projection_ready": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MRF1910_4_proxy_nonpromotion",
            "claim_piece": "proxy-to-tensor refusal",
            "formal_statement": "A material proxy P_AB is not a prediction unless P_AB = DeltaR_AB^X in a declared parent basis, with C_X, R_source^X, K_X and tau_X either derived, sourced, or theorem-zero.",
            "result": "ANTI_SHORTCUT_RULE_DERIVED_FROM_RESPONSE_LAW",
            "what_is_derived": "why 1909 alloy rows are useful but cannot score WEP/local-GR",
            "what_is_not_derived": "the values needed for a score-ready WEP product",
            "source_anchor": "DPR1897_1_arena_tau_K; WIP1899_3_material_tensor; BB1909_5_source_readout_kernel",
            "parent_signed": False,
            "projection_ready": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MRF1910_5_verdict",
            "claim_piece": "1910 parent material response functional verdict",
            "formal_statement": "Current MTS work has an exact conditional response functional and common-mode zero theorem, but not a parent-signed nonuniversal coefficient-zero theorem or exact mass-defect tensor.",
            "result": "CONDITIONAL_RESPONSE_FUNCTIONAL_DERIVED_PARENT_PROMOTION_BLOCKED",
            "what_is_derived": "the correct algebraic shape of the local material response branch",
            "what_is_not_derived": "the parent zero/signature that would reduce MTS to GR locally for material WEP channels",
            "source_anchor": "MRF1910_0_target through MRF1910_4_proxy_nonpromotion",
            "parent_signed": False,
            "projection_ready": False,
            "valid_for_claim": False,
        },
    ]


def common_mode_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CMZ1910_0_domain",
            "statement": "All ordinary test bodies share one observed coframe, one parent matter action, one Hilbert source, and one universal mass-energy coupling branch V_U.",
            "status": "ANTECEDENT_NOT_PARENT_SIGNED",
            "proof_note": "this is exactly the GR/Newton-style local branch: universal source response is geometry, not material label",
            "missing_for_promotion": "single parent matter action/current owner and no species-source prefactor theorem",
            "source_anchor": "ACO1899_6_verdict",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CMZ1910_1_calculation",
            "statement": "V_U ln M_A = sigma_U and V_U ln M_B = sigma_U imply DeltaR_AB^U = 0.",
            "status": "EXACT_ALGEBRA",
            "proof_note": "the logarithmic derivative removes the common rescaling; no cancellation tuning is used",
            "missing_for_promotion": "prove all retained WEP-sensitive directions are common-mode or coefficient-zero",
            "source_anchor": "MRF1910_2_common_mode_zero",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CMZ1910_2_nonuniversal_residual",
            "statement": "Any nonuniversal V_X with gamma_cX not equal across independent material components produces DeltaR_AB^X = sum_c Deltaf_c gamma_cX and therefore needs a zero theorem or a bound row.",
            "status": "EXACT_CONDITIONAL_RESIDUAL_LAW",
            "proof_note": "the 1909 alloy vector shows Deltaf_c proxies are not identically zero for Ti/Pt materials",
            "missing_for_promotion": "C_X=0 theorem or finite source-backed C_X with material/source/readout contraction",
            "source_anchor": "AP1909_TA6V_minus_PtRh10; CP1080_0_definition",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CMZ1910_3_verdict",
            "statement": "The local GR-compatible route is now precise: prove nonuniversal material coefficients vanish before readout, or keep a finite tensor product as empirical nonclaim input.",
            "status": "LOCAL_GR_ROUTE_SHARP_BUT_UNSIGNED",
            "proof_note": "this is progress because the missing coupling is no longer vague",
            "missing_for_promotion": "parent nonuniversal coefficient-zero theorem",
            "source_anchor": "CMZ1910_0_domain through CMZ1910_2_nonuniversal_residual",
            "valid_for_claim": False,
        },
    ]


def tensor_contract_rows() -> list[dict[str, Any]]:
    proxy = proxy_values()
    return [
        {
            "tensor_id": "MDT1910_0_common_mode",
            "component": "universal_common_mode_mass_energy",
            "required_formula": "DeltaR_AB^U = 0 if V_U M_A = sigma_U M_A for all ordinary A",
            "current_proxy": "not needed if theorem signed",
            "required_source_or_proof": "parent-signed universal minimal-coupling/common-mode theorem",
            "parent_owner_requirement": "one matter action/current/source owner; no source-only species prefactor",
            "no_double_count_rule": "common-mode component projected out before nonuniversal tensor rows",
            "units": "dimensionless logarithmic response",
            "current_status": "DERIVED_CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "tensor_id": "MDT1910_1_electron_rest",
            "component": "electron",
            "required_formula": "DeltaR_AB^e = f_Ae - f_Be if V_e rescales electron rest energy only",
            "current_proxy": proxy["electron_rest_mass_fraction"],
            "required_source_or_proof": "CODATA/NIST electron fraction plus parent owner for electron rest-mass generator",
            "parent_owner_requirement": "V_e and C_e derived or theorem-zero in parent action",
            "no_double_count_rule": "electron rest energy excluded from nuclear/atomic residual mass rows",
            "units": "dimensionless mass fraction contrast",
            "current_status": "NUMERIC_PROXY_PARENT_OWNER_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "tensor_id": "MDT1910_2_nucleon_or_light_quark_rest",
            "component": "light_quark_or_nucleon_rest",
            "required_formula": "DeltaR_AB^q = sum_isotopes Deltaf_isotope partial ln M_isotope/partial ln m_q in the declared parent basis",
            "current_proxy": f"Z_over_A={proxy['Z_over_A_proxy']}; N_over_A={proxy['N_over_A_proxy']}",
            "required_source_or_proof": "AME/nuclear mass source plus parent light-quark/nucleon response convention",
            "parent_owner_requirement": "V_q and C_q derived or theorem-zero; proton/neutron rest rows separated from binding rows",
            "no_double_count_rule": "rest nucleon response cannot double-count QCD residual or nuclear binding energy",
            "units": "dimensionless logarithmic response",
            "current_status": "PROXY_ONLY_EXACT_MASS_DEFECT_TENSOR_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "tensor_id": "MDT1910_3_EM_Coulomb_binding",
            "component": "EM_Coulomb",
            "required_formula": "DeltaR_AB^alpha = partial_alpha ln M_A - partial_alpha ln M_B with EM binding owned by the parent EM generator",
            "current_proxy": "WCM1053_4 DD alpha/Coulomb smoke; AP1909 coulomb_formula_proxy=" + proxy["coulomb_formula_proxy"],
            "required_source_or_proof": "parent EM edge owner plus bounded map from external DD/liquid-drop proxy to MTS basis",
            "parent_owner_requirement": "unique A_Q/F_Q^2 owner and no hidden representative EM kinetic branch",
            "no_double_count_rule": "EM binding removed from nuclear surface/QCD residual rows",
            "units": "dimensionless logarithmic response",
            "current_status": "EXTERNAL_PROXY_PARENT_EM_OWNER_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "tensor_id": "MDT1910_4_nuclear_binding",
            "component": "nuclear_binding",
            "required_formula": "DeltaR_AB^bind = partial_X ln M_A^bind - partial_X ln M_B^bind for each retained binding generator X",
            "current_proxy": "WCM1053_5 DD surface/binding smoke",
            "required_source_or_proof": "exact mass-defect/binding tensor or parent theorem reducing retained nuclear channels",
            "parent_owner_requirement": "nuclear/QCD binding generator list and C_X owner",
            "no_double_count_rule": "binding rows must sum with rest and EM rows to the declared total mass functional",
            "units": "dimensionless logarithmic response",
            "current_status": "MISSING_NUCLEAR_BINDING_TENSOR",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "tensor_id": "MDT1910_5_QCD_gluon_residual",
            "component": "QCD_gluon",
            "required_formula": "DeltaR_AB^LambdaQCD = partial ln M_A/partial ln Lambda_QCD - partial ln M_B/partial ln Lambda_QCD after rest/binding components are separated",
            "current_proxy": "MISSING",
            "required_source_or_proof": "PDG/AME-compatible QCD residual convention or parent theorem-zero",
            "parent_owner_requirement": "V_LambdaQCD and C_LambdaQCD derived or theorem-zero",
            "no_double_count_rule": "QCD residual is the closure row after all explicit rest/binding terms are assigned",
            "units": "dimensionless logarithmic response",
            "current_status": "MISSING_QCD_RESIDUAL_CONVENTION",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "tensor_id": "MDT1910_6_lattice_impurity_coating",
            "component": "lattice_impurity_coating",
            "required_formula": "DeltaR_AB^lat = response of flight material processing, lattice/chemical binding, impurity and coating sectors, or a parent zero theorem",
            "current_proxy": "bulk alloy mass fractions only",
            "required_source_or_proof": "official material systematics or theorem that these sectors are common-mode/negligible for retained parent generators",
            "parent_owner_requirement": "parent decides whether chemical/lattice/coating energy is visible to V_X",
            "no_double_count_rule": "chemical/lattice energy not hidden inside atomic/nuclear mass rows without a convention",
            "units": "dimensionless logarithmic response or theorem tag",
            "current_status": "MISSING_FLIGHT_MATERIAL_SYSTEMATICS_OR_ZERO_THEOREM",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "tensor_id": "MDT1910_7_source_readout_product",
            "component": "source_readout_tau_product",
            "required_formula": "eta_AB = sum_X C_X R_source^X K_WEP^X tau_WEP^X DeltaR_AB^X, with no cancellation unless parent identity proves it",
            "current_proxy": "MISSING official source/readout/tau kernel",
            "required_source_or_proof": "official CMSM/source-worldtube arrays or parent point-source/common-mode theorem plus tau convention",
            "parent_owner_requirement": "variation before readout and no readout re-entry",
            "no_double_count_rule": "readout/source normalization cannot be absorbed into material tensor or empirical bound",
            "units": "dimensionless eta product after normalization",
            "current_status": "MISSING_SOURCE_READOUT_TAU_KERNEL",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def proxy_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "PIR1910_0_natural_element_stub",
            "candidate": "1908 natural Ti/Pt element Z/A and N/A stub",
            "refusal_reason": "not MICROSCOPE alloy composition and not a parent material response tensor",
            "allowed_use": "sanity/debug only",
            "promotion_requirement": "alloy/material/binding tensor in parent basis",
            "accepted_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "PIR1910_1_alloy_proxy",
            "candidate": "1909 TA6V_minus_PtRh10 alloy proxy vector",
            "refusal_reason": "numeric alloy contrasts lack gamma_cX, C_X, no-double-count mass functional and source/readout/tau contraction",
            "allowed_use": "nonclaim scaffold and regression test input",
            "promotion_requirement": "MDT1910 tensor rows source-filled or theorem-zero",
            "accepted_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "PIR1910_2_DD_smoke",
            "candidate": "Damour-Donoghue alpha/surface smoke components",
            "refusal_reason": "external phenomenological basis cannot be imported as MTS without basis map and parent operator owner",
            "allowed_use": "cross-check/stress-test only",
            "promotion_requirement": "MTS-to-DD basis map plus parent EM/nuclear owner",
            "accepted_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "PIR1910_3_bound_inversion",
            "candidate": "choose C_X from MICROSCOPE eta bound",
            "refusal_reason": "empirical bound can test a coefficient but cannot define the parent coefficient",
            "allowed_use": "upper-bound fallback after forward model exists",
            "promotion_requirement": "derive/source C_X before comparison",
            "accepted_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "PIR1910_4_unity_tau",
            "candidate": "set tau_WEP or source/readout kernel to 1",
            "refusal_reason": "shortcuts hide source-worldtube/readout normalization and can fake a local pass",
            "allowed_use": "none for claim-grade scoring",
            "promotion_requirement": "derive/source tau and K_WEP or theorem-reduce them",
            "accepted_for_claim": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1910_0_functional_shape",
            "condition": "parent material response functional shape is exact",
            "current_status": "PASS_CONDITIONAL_ALGEBRA_ONLY",
            "source_anchor": "MRF1910_2_common_mode_zero; MRF1910_3_sector_response_law",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1910_1_parent_zero",
            "condition": "all nonuniversal material coefficients are parent-zero or absent before readout",
            "current_status": "FAIL_NONUNIVERSAL_COEFFICIENT_ZERO_THEOREM_MISSING",
            "source_anchor": "CMZ1910_2_nonuniversal_residual; CP1080_0_definition",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1910_2_tensor_contract",
            "condition": "exact mass-defect/material tensor rows are filled or theorem-zero",
            "current_status": "FAIL_EXACT_TENSOR_CONTRACT_UNFILLED",
            "source_anchor": OUTPUTS["tensor_contract"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1910_3_source_readout",
            "condition": "source-worldtube/readout/tau product is sourced or theorem-reduced",
            "current_status": "FAIL_SOURCE_READOUT_TAU_KERNEL_MISSING",
            "source_anchor": "MDT1910_7_source_readout_product",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1910_4_claim",
            "condition": "1910 supports WEP/local-GR claim-grade reduction",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1910_0_functional_shape through CG1910_3_source_readout",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1910_0_keep",
            "decision": "keep conditional response functional",
            "reason": "it gives the exact algebraic map from parent material generators to Ti/Pt WEP response",
            "status": "DERIVATION_PROGRESS_CONDITIONAL",
            "next_dependency": "nonuniversal coefficient-zero theorem or finite C_X contract",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1910_1_block",
            "decision": "do not promote proxy material tensor",
            "reason": "1909 proxies are component contrasts but not parent response derivatives with coefficients/source/readout",
            "status": "PROXY_PROMOTION_REFUSED",
            "next_dependency": "exact mass-defect tensor rows or theorem-zero",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1910_2_next",
            "decision": "attack nonuniversal coefficient-zero theorem",
            "reason": "for a GR-reduction route, the cleanest win is to prove parent action kills nonuniversal material couplings before readout",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1911 nonuniversal material coefficient zero theorem or finite C_X contract",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1910_0_primary",
            "selection_status": "selected",
            "target_doc": "1911-Y5-R2FR-nonuniversal-material-coefficient-zero-theorem-or-finite-CX-contract.md",
            "target_script": "scripts/Y5_R2FR_nonuniversal_material_coefficient_zero_theorem_or_finite_CX_contract_1911.py",
            "objective": "try to prove C_X=0 for all nonuniversal material response channels from parent action/common-mode descent; if it fails, emit finite coefficient acquisition contract",
            "success_condition": "parent-signed nonuniversal material coefficient zero theorem, or exact finite C_X contract with no proxy/bound inversion",
            "do_not": "do not use alloy proxies, DD smoke rows, or MICROSCOPE bounds as parent coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1910_0_gain",
            "area": "derivation",
            "summary": "the parent material-response law is now explicit: common-mode directions cancel; nonuniversal directions require component fractions times parent generator weights",
            "risk_level": "REAL_THEORY_PROGRESS_CONDITIONAL",
            "project_meaning": "the local branch has an exact algebraic spine rather than only data proxies",
            "next_action": "prove nonuniversal coefficients vanish or source them honestly",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1910_1_gr_route",
            "area": "GR reduction",
            "summary": "a GR-compatible local pass would follow if parent action permits only universal/common-mode material coupling before readout",
            "risk_level": "PROMISING_BUT_UNSIGNED",
            "project_meaning": "this directly targets the user priority: reduce to GR/Newton locally by derivation, not fit",
            "next_action": "1911 coefficient-zero theorem",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1910_2_claim",
            "area": "WEP/local testing",
            "summary": "claim remains blocked because exact tensor rows and source/readout product are not filled",
            "risk_level": "SAFE_NONCLAIM",
            "project_meaning": "we strengthened the framework without pretending the data scaffold is a prediction",
            "next_action": "keep proxies as smoke/debug only",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "response_functional": response_functional_rows(),
        "common_mode_zero": common_mode_zero_rows(),
        "tensor_contract": tensor_contract_rows(),
        "proxy_refusal": proxy_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in [
                "valid_for_claim",
                "claim_allowed",
                "valid_prediction_row",
                "projection_ready",
                "score_ready",
                "gate_pass",
                "accepted_for_claim",
                "parent_signed",
            ]:
                if field in row and bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all claim/projection/parent-signed flags remain false"


def response_rows_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    required = {
        "MRF1910_2_common_mode_zero": "EXACT_CONDITIONAL_THEOREM",
        "MRF1910_3_sector_response_law": "EXACT_CONDITIONAL_ALGEBRA",
        "MRF1910_5_verdict": "CONDITIONAL_RESPONSE_FUNCTIONAL_DERIVED_PARENT_PROMOTION_BLOCKED",
    }
    bad = []
    row_by_id = {row["attempt_id"]: row for row in rows}
    for row_id, result in required.items():
        if row_id not in row_by_id:
            bad.append(f"{row_id}:missing")
        elif row_by_id[row_id]["result"] != result:
            bad.append(f"{row_id}:{row_by_id[row_id]['result']}")
    return not bad, "; ".join(bad) if bad else "conditional response functional and verdict present"


def tensor_contract_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    required_components = {
        "universal_common_mode_mass_energy",
        "electron",
        "light_quark_or_nucleon_rest",
        "EM_Coulomb",
        "nuclear_binding",
        "QCD_gluon",
        "lattice_impurity_coating",
        "source_readout_tau_product",
    }
    present = {row["component"] for row in rows}
    bad = []
    missing = required_components - present
    if missing:
        bad.append(f"missing_components={sorted(missing)}")
    for row in rows:
        if bool_string(row["score_ready"]) == "true" or bool_string(row["valid_for_claim"]) == "true":
            bad.append(f"{row['tensor_id']}:claim_flag_true")
        if not row["no_double_count_rule"]:
            bad.append(f"{row['tensor_id']}:missing_no_double_count_rule")
    return not bad, "; ".join(bad) if bad else "exact tensor contract components present and nonclaim"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1910_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
        }
    )
    response_ok, response_detail = response_rows_valid(csv_rows(OUTPUTS["response_functional"]))
    checks.append({"validation_id": "VAL1910_01_response_functional", "status": "PASS" if response_ok else "FAIL", "detail": response_detail, "valid_for_claim": False})
    common_rows = csv_rows(OUTPUTS["common_mode_zero"])
    checks.append(
        {
            "validation_id": "VAL1910_02_common_mode_zero",
            "status": "PASS" if any(row["theorem_id"] == "CMZ1910_3_verdict" and row["status"] == "LOCAL_GR_ROUTE_SHARP_BUT_UNSIGNED" for row in common_rows) else "FAIL",
            "detail": "common-mode zero route sharp but unsigned",
            "valid_for_claim": False,
        }
    )
    tensor_ok, tensor_detail = tensor_contract_valid(csv_rows(OUTPUTS["tensor_contract"]))
    checks.append({"validation_id": "VAL1910_03_tensor_contract", "status": "PASS" if tensor_ok else "FAIL", "detail": tensor_detail, "valid_for_claim": False})
    refusal_rows = csv_rows(OUTPUTS["proxy_refusal"])
    checks.append(
        {
            "validation_id": "VAL1910_04_proxy_refusal",
            "status": "PASS" if len(refusal_rows) >= 5 and all(bool_string(row["accepted_for_claim"]) == "false" for row in refusal_rows) else "FAIL",
            "detail": "proxy, smoke, bound-inversion and unity-tau shortcuts refused",
            "valid_for_claim": False,
        }
    )
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1910_05_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1910_4_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
        }
    )
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1910_06_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1910_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1911 nonuniversal coefficient-zero route selected",
            "valid_for_claim": False,
        }
    )
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append({"validation_id": "VAL1910_07_claim_flags_safe", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1910_08_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1910_09_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1910_10_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1910-Y5-R2FR-parent-material-response",
            "P8_Y5_PARENT_QLOC_1910",
            "Y5_R2FR_parent_material_response_functional_or_exact_mass_defect_tensor_contract_1910",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1910_11_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1910_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1910_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1910 parent material response functional or exact mass-defect tensor contract", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1910 - Parent Material Response Functional Or Exact Mass-Defect Tensor Contract

## Purpose

This checkpoint attacks the real coupling gap exposed by 1909. It tries to derive the parent material-response functional needed for the local WEP/GR branch. The result is meaningful but still nonclaim: the response law is now exact conditionally, the universal/common-mode branch cancels exactly, and every nonuniversal material channel is forced into either a parent-zero theorem or an exact tensor contract.

## Result

- Derived the conditional response law `DeltaR_AB^X = sum_c (f_Ac - f_Bc) gamma_cX`.
- Derived the conditional common-mode zero theorem: universal mass-energy rescaling gives `DeltaR_AB = 0`.
- Refused promotion of natural element stubs, alloy proxies, DD smoke rows, bound inversion, and unity-tau shortcuts.
- Wrote the exact mass-defect/material tensor contract needed before WEP/local-GR scoring.
- Claim remains blocked because the parent nonuniversal coefficient-zero theorem and source/readout/tau product are still missing.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent Material Response Functional Attempt

{markdown_table(rows_by_name["response_functional"])}

## Common-Mode Zero Theorem

{markdown_table(rows_by_name["common_mode_zero"])}

## Exact Mass-Defect Tensor Contract

{markdown_table(rows_by_name["tensor_contract"])}

## Proxy Import Refusal Matrix

{markdown_table(rows_by_name["proxy_refusal"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

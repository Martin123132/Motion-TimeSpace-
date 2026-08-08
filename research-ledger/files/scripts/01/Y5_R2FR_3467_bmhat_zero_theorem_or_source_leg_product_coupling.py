from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3467-Y5-R2FR-bmhat-zero-theorem-or-source-leg-product-coupling.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

ETA_TIPT_BOUND = 2.8e-15

SOURCES: dict[str, dict[str, Any]] = {
    "script_3467": {"type": "local", "path": Path(__file__).resolve(), "role": "generator for this checkpoint"},
    "doc_3466": {
        "type": "local",
        "path": ROOT / "3466-Y5-R2FR-unique-F2-Hodge-owner-or-WEP-nuclear-mass-component-row.md",
        "role": "3466 handoff: mass/nuclear material row and finite D_mhat ceiling",
    },
    "mass_row_3466": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv",
        "role": "mass/nuclear WEP component row",
    },
    "mass_search_3466": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3466_NUCLEAR_MASS_COMPONENT_SEARCH.csv",
        "role": "mass material charge and missing b_mhat/source-leg search",
    },
    "envelope_3466": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3466_NO_CANCELLATION_ENVELOPE_UPDATE.csv",
        "role": "no-cancellation envelope with mass and alpha pieces",
    },
    "action_1937": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_1937_MINIMAL_PARENT_MATTER_ACTION_SIGNATURE.csv",
        "role": "minimal quotient-descended matter action signature",
    },
    "hilbert_1937": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv",
        "role": "Hilbert source theorem and common renormalization guard",
    },
    "direct_matter_2612": {
        "type": "local",
        "path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
        "role": "no direct matter X-vertex grammar attempt",
    },
    "prefactor_2612": {
        "type": "local",
        "path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv",
        "role": "source prefactor and alpha/mass vertex classification",
    },
    "hilbert_owner_2615": {
        "type": "local",
        "path": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
        "role": "total Hilbert source owner audit",
    },
    "exchange_2615": {
        "type": "local",
        "path": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
        "role": "Noether exchange collapse and common calibration theorem",
    },
    "label_forgetting_2648": {
        "type": "local",
        "path": OUT / "P8_Y5_SOURCE_FUNCTOR_LABEL_FORGETTING_2648_LABEL_FORGETTING_ATTEMPT.csv",
        "role": "source functor label-forgetting attempt",
    },
    "object_language_2650": {
        "type": "local",
        "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv",
        "role": "object-language no source-prefactor theorem attempt",
    },
    "typing_2650": {
        "type": "local",
        "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_SOURCE_PREFACTOR_TYPING_GATE.csv",
        "role": "parent typing gate for source-only coefficients",
    },
    "material_tensor_2650": {
        "type": "local",
        "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv",
        "role": "parent material tensor basis gap",
    },
    "source_ward_contract": {
        "type": "local",
        "path": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
        "role": "source-current Ward/universality contract",
    },
    "source_owner_contract": {
        "type": "local",
        "path": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "parent source-owner action term contract",
    },
    "no_species_contract": {
        "type": "local",
        "path": OUT / "P8_no_species_source_charge_CONTRACT.csv",
        "role": "no species/material source-charge contract",
    },
    "dd_map_2441": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2441_MTS_TO_DD_CHARGE_MAP.csv",
        "role": "MTS-to-Damour-Donoghue map including b_mhat",
    },
    "mass_gap_2441": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2441_MASS_SECTOR_GAP_LEDGER.csv",
        "role": "mass-sector gap ledger",
    },
    "reduced_formula_2441": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2441_WEP_REDUCED_FORMULA_NONCLAIM.csv",
        "role": "reduced WEP formula with D_mhat and D_e",
    },
    "dd_charges_3265": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3265_DD_MATERIAL_CHARGES_NONCLAIM.csv",
        "role": "alloy-aware Damour-Donoghue material charge rows",
    },
    "damour_donoghue_arxiv": {
        "type": "external",
        "url": "https://arxiv.org/abs/1007.2792",
        "role": "Damour-Donoghue mass/EM charge framework",
    },
    "microscope_final": {
        "type": "external",
        "url": "https://arxiv.org/abs/2209.15487",
        "role": "MICROSCOPE final Ti/Pt WEP bound",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        values = [
            str(row.get(field, ""))
            .replace("\n", "<br>")
            .replace("|", "/")
            for field in fields
        ]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"n/a", "missing", "not_applicable"} or "MISSING" in text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    rows: list[dict[str, Any]] = []
    for source_id, meta in SOURCES.items():
        path = meta.get("path")
        url = meta.get("url", "")
        source_type = meta["type"]
        rows.append(
            {
                "timestamp_utc": stamp,
                "source_id": source_id,
                "source_type": source_type,
                "source_path": str(path) if path else "",
                "source_url": url,
                "exists_or_url_present": bool(path.exists()) if isinstance(path, Path) else bool(url),
                "role": meta["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def get_delta_qhatm_and_bound() -> tuple[float, float]:
    mass_rows = read_csv(SOURCES["mass_row_3466"]["path"])
    delta_row = next(row for row in mass_rows if row["component_id"] == "MASS3466_1_alloy_material_charge")
    bound_row = next(row for row in mass_rows if row["component_id"] == "MASS3466_2_alloy_single_channel_bound")
    delta_qhatm = parse_float(delta_row["bound_or_value"])
    bound = parse_float(bound_row["bound_or_value"])
    if delta_qhatm is None or bound is None:
        raise ValueError("3466 mass rows are not numeric")
    return delta_qhatm, bound


def bmhat_zero_theorem_attempt() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "BMZ3467_0_definition",
            "claim_piece": "mass/nuclear coefficient definition",
            "statement": "b_mhat := L_v ln(mhat/Lambda_QCD) or, more generally, the vertical derivative of the dimensionless nuclear mass/binding constants entering the ordinary matter action.",
            "derivation_status": "DEFINITION_FIXED",
            "proof_or_obstruction": "This isolates the dangerous piece: a common mass scale is not b_mhat; only dimensionless mass-ratio/binding drift produces differential WEP charge.",
            "required_parent_clause": "none for definition",
            "source_path": str(SOURCES["dd_map_2441"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BMZ3467_1_common_scale_cancellation",
            "claim_piece": "common Lambda_QCD or mass-unit scaling",
            "statement": "If every material mass has M_A(q)=C(q) M_A^0 with the same C(q), then L_v ln M_A-L_v ln M_B=0 and the effect is a measured-G/unit calibration, not a WEP residual.",
            "derivation_status": "EXACT_WEP_CANCELLATION",
            "proof_or_obstruction": "eta_AB depends on differential acceleration; a universal multiplicative source factor cancels from the numerator and can only affect the common Newtonian calibration.",
            "required_parent_clause": "Hilbert source/common-mode calibration separation",
            "source_path": str(SOURCES["hilbert_1937"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BMZ3467_2_dimensionless_constant_silence",
            "claim_piece": "b_mhat theorem-zero route",
            "statement": "If theta_SM={alpha_EM,mhat/Lambda_QCD,m_e/Lambda_QCD,nuclear binding coefficients,...} is q-basic or superselected parent data, L_v theta_SM=0; hence b_mhat=0 and all mass-ratio WEP charges vanish before readout.",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "Chain rule: D(q^*theta_bar)[v]=Dtheta_bar[Dq(v)]=0 for v in ker(Dq). The theorem is clean if MTS proves ordinary constants descend through q or are fixed representation data.",
            "required_parent_clause": "constant-sector universality; no hidden-to-SM-coefficient morphism; readout/radiative preservation",
            "source_path": str(SOURCES["no_species_contract"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BMZ3467_3_no_direct_mass_vertex",
            "claim_piece": "exclude m_A(X), Yukawa/Higgs/QCD gauge-kinetic marker slots",
            "statement": "A parent grammar that admits no direct matter X vertex forbids hidden scalar dependence in mass ratios and nuclear binding coefficients.",
            "derivation_status": "CONDITIONAL_GRAMMAR_ROUTE_NOT_SIGNED",
            "proof_or_obstruction": "2612 classifies alpha/mass vertices as forbidden by policy, not yet by parent theorem; 2650 likewise keeps the typed object-language proof unsigned.",
            "required_parent_clause": "parent object-language derivation of no direct mass/constant coefficient slot",
            "source_path": str(SOURCES["direct_matter_2612"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BMZ3467_4_countermodel",
            "claim_piece": "why covariance/minimal coupling alone is insufficient",
            "statement": "S_matter may contain y_q(X) H psi psi, Z_G(X) Tr G^2, or B_nuc(X) O_bind while remaining local and covariant; these generate b_mhat unless the parent grammar forbids them.",
            "derivation_status": "EXACT_COUNTERMODEL_CLASS",
            "proof_or_obstruction": "Ordinary covariance chooses tensor shape but not constancy of dimensionless couplings; a direct mass/constant slot is the mass-sector analogue of the hidden F2 slot.",
            "required_parent_clause": "no coefficient morphism HiddenInvariant -> {Yukawa,Higgs,QCD,binding} plus radiative/readout closure",
            "source_path": str(SOURCES["prefactor_2612"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BMZ3467_5_verdict",
            "claim_piece": "promote b_mhat=0 from current corpus",
            "statement": "The b_mhat zero theorem is exact conditionally, but current MTS has not parent-signed constant-sector universality or no mass-vertex grammar.",
            "derivation_status": "NOT_PARENT_DERIVED_CURRENT_CORPUS",
            "proof_or_obstruction": "Proceed with a source-product coupling row rather than claiming local WEP/GR closure.",
            "required_parent_clause": "BMZ3467_2 and BMZ3467_3 closed together",
            "source_path": str(SOURCES["object_language_2650"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def mass_variation_chain_rule(delta_qhatm: float) -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "MVC3467_0_material_mass_function",
            "object": "material mass response",
            "formula": "M_A(q)=C_mass(q) * Mbar_A(theta_SM(q), alpha_EM(q), binding(q), isotope/alloy data)",
            "derived_result": "L_v ln M_A = L_v ln C_mass + sum_i Q_i^A b_i",
            "status": "CHAIN_RULE_DERIVED",
            "source_path": str(SOURCES["material_tensor_2650"]["path"]),
            "valid_for_claim": False,
        },
        {
            "chain_id": "MVC3467_1_common_mode",
            "object": "universal mass/source scale",
            "formula": "Delta_AB[L_v ln C_mass]=0",
            "derived_result": "common scaling calibrates measured G or units and cannot by itself make eta_AB",
            "status": "EXACT_COMMON_MODE_REMOVAL",
            "source_path": str(SOURCES["exchange_2615"]["path"]),
            "valid_for_claim": False,
        },
        {
            "chain_id": "MVC3467_2_mhat_channel",
            "object": "Damour-Donoghue mass-ratio channel",
            "formula": "Delta_AB[L_v ln M] contains Delta_Qhatm_AB * b_mhat",
            "derived_result": f"MICROSCOPE alloy Delta_Qhatm_abs={delta_qhatm:.12e}",
            "status": "DIFFERENTIAL_CHANNEL_NUMERIC_MATERIAL_FACTOR_READY",
            "source_path": str(SOURCES["mass_row_3466"]["path"]),
            "valid_for_claim": False,
        },
        {
            "chain_id": "MVC3467_3_zero_condition",
            "object": "b_mhat zero",
            "formula": "L_v theta_SM=0 -> b_mhat=0 -> Delta_Qhatm_AB*b_mhat=0",
            "derived_result": "exact if quotient/superselection constant-sector theorem is parent-signed",
            "status": "EXACT_CONDITIONAL_ZERO",
            "source_path": str(SOURCES["no_species_contract"]["path"]),
            "valid_for_claim": False,
        },
        {
            "chain_id": "MVC3467_4_finite_condition",
            "object": "retained mass-sector coupling",
            "formula": "D_mhat_eff := tau_WEP(lambda) * S_E^q * b_mhat",
            "derived_result": "if b_mhat is not zero-derived, WEP constrains the product, not b_mhat alone",
            "status": "SOURCE_PRODUCT_OBJECT_DEFINED",
            "source_path": str(SOURCES["reduced_formula_2441"]["path"]),
            "valid_for_claim": False,
        },
    ]


def source_product_rows(delta_qhatm: float, single_channel_bound: float) -> list[dict[str, Any]]:
    recomputed = ETA_TIPT_BOUND / delta_qhatm
    return [
        {
            "product_id": "SPC3467_0_product_definition",
            "object": "D_mhat_eff",
            "formula": "D_mhat_eff := tau_WEP(lambda) * S_E^q * b_mhat",
            "known_inputs": "Delta_Qhatm material contrast; eta_TiPt bound",
            "missing_inputs": "tau_WEP(lambda); source leg S_E^q; parent coefficient b_mhat",
            "numeric_bound": "not_individually_numeric",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_map_2441"]["path"]),
            "status": "PRODUCT_DEFINED_FACTORS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "product_id": "SPC3467_1_product_bound",
            "object": "abs(tau_WEP*S_E^q*b_mhat)",
            "formula": "abs(D_mhat_eff) <= eta_TiPt_bound / Delta_Qhatm_abs under isolated mass-channel premise",
            "known_inputs": f"eta_TiPt_bound={ETA_TIPT_BOUND:.12e}; Delta_Qhatm_abs={delta_qhatm:.12e}",
            "missing_inputs": "single-channel/no-cancellation premise; live alpha/direct/shadow/readout terms",
            "numeric_bound": f"{recomputed:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["mass_row_3466"]["path"]),
            "status": "FINITE_NONCLAIM_PRODUCT_CEILING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "product_id": "SPC3467_2_factor_split_refusal",
            "object": "S_E^q versus b_mhat",
            "formula": "D_mhat_eff bound does not separately bound S_E^q or b_mhat without an independent normalization or theorem.",
            "known_inputs": f"recomputed_bound={recomputed:.12e}; imported_bound_3466={single_channel_bound:.12e}",
            "missing_inputs": "q normalization; Earth/source composition leg; parent mass coefficient",
            "numeric_bound": "factor_split_blocked",
            "units": "dimensionless",
            "source_path": str(SOURCES["mass_gap_2441"]["path"]),
            "status": "NO_FACTOR_SPLIT_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "product_id": "SPC3467_3_if_tau_not_one",
            "object": "range/readout tau correction",
            "formula": "if tau_WEP(lambda) is external to D_mhat_eff, then abs(S_E^q*b_mhat) <= eta/(tau_WEP*Delta_Qhatm)",
            "known_inputs": "formal dependence only",
            "missing_inputs": "tau_WEP(lambda) from source-worldtube/orbit/readout branch",
            "numeric_bound": "MISSING_TAU_WEP_LAMBDA",
            "units": "dimensionless",
            "source_path": str(SOURCES["source_ward_contract"]["path"]),
            "status": "TAU_FACTORIZATION_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def newton_g_guard() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "G3467_0_GR_constant",
            "point": "GR uses Newton's constant as a calibrated coupling; it does not derive its numerical value from Einstein-Hilbert structure alone.",
            "MTS_rule": "MTS may likewise retain one universal local coupling calibration, but cannot hide time/range/species/material dependence in that calibration.",
            "status": "COMMON_MODE_ALLOWED_DIFFERENTIAL_FORBIDDEN",
            "source_path": str(SOURCES["hilbert_1937"]["path"]),
            "valid_for_claim": False,
        },
        {
            "guard_id": "G3467_1_common_mass_scale",
            "point": "A universal shift in all rest masses or all source strengths is a common mode.",
            "MTS_rule": "common mode belongs to measured-G/source normalization; it drops out of eta_TiPt.",
            "status": "SAFE_CALIBRATION_CHANNEL",
            "source_path": str(SOURCES["exchange_2615"]["path"]),
            "valid_for_claim": False,
        },
        {
            "guard_id": "G3467_2_dimensionless_ratio",
            "point": "A drift in mhat/Lambda_QCD or binding coefficients is not a Newton-G calibration.",
            "MTS_rule": "dimensionless mass-ratio drift remains a real WEP/local-source residual unless b_mhat=0 or D_mhat_eff is bounded.",
            "status": "DANGEROUS_DIFFERENTIAL_CHANNEL",
            "source_path": str(SOURCES["dd_map_2441"]["path"]),
            "valid_for_claim": False,
        },
    ]


def claim_gates(theorem_rows: list[dict[str, Any]], product_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    zero_not_derived = any(row["theorem_id"] == "BMZ3467_5_verdict" and "NOT_PARENT_DERIVED" in row["derivation_status"] for row in theorem_rows)
    product_bound = any(row["product_id"] == "SPC3467_1_product_bound" and parse_float(row["numeric_bound"]) for row in product_rows)
    return [
        {
            "gate_id": "CG3467_0_bmhat_zero",
            "gate": "b_mhat=0 parent theorem",
            "pass": not zero_not_derived,
            "detail": "constant-sector q-basic/superselection theorem not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3467_1_product_bound",
            "gate": "D_mhat_eff product ceiling exists",
            "pass": product_bound,
            "detail": "finite nonclaim ceiling written for tau_WEP*S_E^q*b_mhat",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3467_2_factor_split",
            "gate": "S_E^q and b_mhat separately known",
            "pass": False,
            "detail": "only the product is bounded; no separate source leg or mass coefficient owner yet",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3467_3_newton_calibration",
            "gate": "Newton/G common mode separated from WEP source charge",
            "pass": True,
            "detail": "common calibration allowed, but differential mass-ratio drift remains live",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3467_4_local_GR_WEP_claim",
            "gate": "local GR/WEP source coupling derived",
            "pass": False,
            "detail": "blocked by b_mhat/source product, alpha/direct/shadow/readout/projector terms, and second-order source gates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger(single_channel_bound: float) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3467_0_zero_theorem",
            "decision": "Do not claim b_mhat=0 from the current corpus.",
            "reason": "The theorem is exact if dimensionless SM/mass constants are q-basic or superselected, but current parent grammar does not yet prove that.",
            "next_action": "Target the constant-sector universality/no-hidden-coefficient-morphism proof directly.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3467_1_product_progress",
            "decision": "Carry D_mhat_eff as the actual coupling product.",
            "reason": f"The WEP mass channel now constrains abs(tau_WEP*S_E^q*b_mhat) <= {single_channel_bound:.12e} under the isolated-channel ceiling.",
            "next_action": "Either prove b_mhat=0, prove S_E^q=0/silent in local vacuum, or source tau_WEP and the source leg.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3467_2_next_route",
            "decision": "Best next step is constant-sector universality before more data plumbing.",
            "reason": "Material factors are now usable; the remaining gap is a parent theorem saying mass ratios cannot be vertical response variables.",
            "next_action": "3468 should attempt the no hidden-to-SM coefficient morphism theorem for {F2, Yukawa/Higgs, QCD scale, nuclear binding}.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3468-Y5-R2FR-constant-sector-universality-or-hidden-SM-coefficient-morphism.md",
            "next_script": "scripts/Y5_R2FR_3468_constant_sector_universality_or_hidden_SM_coefficient_morphism.py",
            "objective": "Try to prove that visible dimensionless constants and mass-ratio coefficients are q-basic/superselected parent data, covering alpha/F2, Yukawa/Higgs, QCD scale ratios, and nuclear binding; if it fails, output the finite coefficient vector that WEP/clocks/R10 must bound.",
            "success_gate": "Either b_alpha and b_mhat-like coefficients are theorem-zero under one parent constant-sector owner, or each retained coefficient has a source-product row and no-cancellation envelope.",
            "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; treating common G calibration as proof of dimensionless-constant silence.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validate(
    outputs: dict[str, Path],
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    chain_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    g_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    delta_qhatm: float,
    single_channel_bound: float,
) -> list[dict[str, Any]]:
    stamp = now()
    local_sources_ok = all(row["exists_or_url_present"] for row in source_rows if row["source_type"] == "local")
    zero_not_claimed = any(row["theorem_id"] == "BMZ3467_5_verdict" and row["derivation_status"] == "NOT_PARENT_DERIVED_CURRENT_CORPUS" for row in theorem_rows)
    conditional_theorem_present = any(row["theorem_id"] == "BMZ3467_2_dimensionless_constant_silence" and row["derivation_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows)
    chain_rule_present = any(row["chain_id"] == "MVC3467_0_material_mass_function" and row["status"] == "CHAIN_RULE_DERIVED" for row in chain_rows)
    recomputed = ETA_TIPT_BOUND / delta_qhatm
    product_bound_ok = abs(recomputed - single_channel_bound) < 1e-25 and any(
        row["product_id"] == "SPC3467_1_product_bound"
        and abs((parse_float(row["numeric_bound"]) or 0.0) - recomputed) < 1e-25
        for row in product_rows
    )
    g_guard_present = any(row["guard_id"] == "G3467_2_dimensionless_ratio" for row in g_rows)
    local_gr_blocked = any(row["gate_id"] == "CG3467_4_local_GR_WEP_claim" and row["pass"] is False for row in gate_rows)
    no_claim_rows = not any(
        str(value).lower() == "true"
        for rows in (theorem_rows, chain_rows, product_rows, g_rows, gate_rows)
        for row in rows
        for key, value in row.items()
        if key in {"claim_allowed", "valid_for_claim"}
    )
    parse_counts: list[str] = []
    csv_parse_ok = True
    for label, path in outputs.items():
        if label == "validation":
            continue
        try:
            parse_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:  # pragma: no cover
            parse_counts.append(f"{path.name}:ERROR:{exc}")
            csv_parse_ok = False
    formalization_ok = True
    formalization_detail = "formalization_exists=False"
    if FORMALIZATION.exists():
        matches = list(FORMALIZATION.rglob("*3467*"))
        formalization_ok = not matches
        formalization_detail = f"formalization_exists=True; 3467_outputs_in_formalization={len(matches)}"

    rows = [
        {"validation_id": "VAL3467_0_local_sources_exist", "pass": local_sources_ok, "detail": "all local sources exist", "timestamp_utc": stamp},
        {"validation_id": "VAL3467_1_zero_theorem_not_overclaimed", "pass": zero_not_claimed and conditional_theorem_present, "detail": "exact conditional b_mhat theorem retained but not promoted", "timestamp_utc": stamp},
        {"validation_id": "VAL3467_2_mass_chain_rule_present", "pass": chain_rule_present, "detail": "common mode plus differential mass-ratio chain rule written", "timestamp_utc": stamp},
        {"validation_id": "VAL3467_3_product_bound_recomputed", "pass": product_bound_ok, "detail": f"eta/delta_qhatm={recomputed:.12e}", "timestamp_utc": stamp},
        {"validation_id": "VAL3467_4_newton_G_guard_present", "pass": g_guard_present, "detail": "common G calibration separated from dimensionless ratio drift", "timestamp_utc": stamp},
        {"validation_id": "VAL3467_5_local_GR_claim_blocked", "pass": local_gr_blocked, "detail": "local GR/WEP pass remains false", "timestamp_utc": stamp},
        {"validation_id": "VAL3467_6_no_claim_rows", "pass": no_claim_rows, "detail": "all claim_allowed and valid_for_claim flags remain false", "timestamp_utc": stamp},
        {"validation_id": "VAL3467_7_csv_parse", "pass": csv_parse_ok, "detail": ";".join(parse_counts), "timestamp_utc": stamp},
        {"validation_id": "VAL3467_8_formalization_untouched_by_3467", "pass": formalization_ok, "detail": formalization_detail, "timestamp_utc": stamp},
    ]
    rows.append(
        {
            "validation_id": "VAL3467_SUMMARY",
            "pass": all(str(row["pass"]).lower() == "true" for row in rows),
            "detail": "PASS" if all(str(row["pass"]).lower() == "true" for row in rows) else "FAIL",
            "timestamp_utc": stamp,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    chain_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    g_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    delta_qhatm: float,
    single_channel_bound: float,
) -> None:
    doc = f"""# 3467 - b_mhat Zero Theorem Or Source-Leg Product Coupling

**Current verdict:** the mass-sector zero route is now precise. A common mass/source scale can be absorbed into the local Newton/G calibration and cancels from WEP, but dimensionless mass-ratio drift does not. Therefore `b_mhat=0` follows exactly if the visible constant sector is `q`-basic/superselected; the current corpus has not parent-signed that theorem.

**Concrete progress:** the live coupling is no longer vague. The retained product is `D_mhat_eff := tau_WEP(lambda) S_E^q b_mhat`, and the MICROSCOPE mass-channel ceiling is `|D_mhat_eff| <= {single_channel_bound:.12e}` using `Delta_Qhatm_abs={delta_qhatm:.12e}`. This is still nonclaim because `tau_WEP`, `S_E^q`, and `b_mhat` are not separately owned.

## Source Register
{md_table(source_rows)}

## b_mhat Zero Theorem Attempt
{md_table(theorem_rows)}

## Mass Variation Chain Rule
{md_table(chain_rows)}

## Source-Product Coupling Rows
{md_table(product_rows)}

## Newton-G Calibration Guard
{md_table(g_rows)}

## Claim Gates
{md_table(gate_rows)}

## Decision Ledger
{md_table(decision_rows)}

## Validation
{md_table(validation_rows)}

## Next Target
{md_table(next_rows)}

## Short Readout
- Exact win: common mass/source scale is separated from real WEP source charge.
- Conditional theorem: `L_v theta_SM=0` implies `b_mhat=0`.
- Concrete bound: `|tau_WEP S_E^q b_mhat| <= {single_channel_bound:.12e}` under the isolated mass-channel ceiling.
- Still missing: parent proof that dimensionless SM/mass constants are `q`-basic, or a sourced split for `tau_WEP`, `S_E^q`, and `b_mhat`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register()
    delta_qhatm, single_channel_bound = get_delta_qhatm_and_bound()
    theorem_rows = bmhat_zero_theorem_attempt()
    chain_rows = mass_variation_chain_rule(delta_qhatm)
    product_rows = source_product_rows(delta_qhatm, single_channel_bound)
    g_rows = newton_g_guard()
    gate_rows = claim_gates(theorem_rows, product_rows)
    decision_rows = decision_ledger(single_channel_bound)
    next_rows = next_target()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3467_SOURCE_REGISTER.csv",
        "bmhat_zero": OUT / "P8_Y5_R2FR_3467_BMHAT_ZERO_THEOREM_ATTEMPT.csv",
        "mass_chain": OUT / "P8_Y5_R2FR_3467_MASS_VARIATION_CHAIN_RULE.csv",
        "source_product": OUT / "P8_Y5_R2FR_3467_SOURCE_PRODUCT_COUPLING_ROWS.csv",
        "g_guard": OUT / "P8_Y5_R2FR_3467_NEWTON_G_CALIBRATION_GUARD.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3467_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3467_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3467_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3467_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["bmhat_zero"], theorem_rows)
    write_csv(outputs["mass_chain"], chain_rows)
    write_csv(outputs["source_product"], product_rows)
    write_csv(outputs["g_guard"], g_rows)
    write_csv(outputs["claim_gates"], gate_rows)
    write_csv(outputs["decision"], decision_rows)
    write_csv(outputs["next"], next_rows)
    validation_rows = validate(outputs, source_rows, theorem_rows, chain_rows, product_rows, g_rows, gate_rows, delta_qhatm, single_channel_bound)
    write_csv(outputs["validation"], validation_rows)
    write_doc(source_rows, theorem_rows, chain_rows, product_rows, g_rows, gate_rows, decision_rows, validation_rows, next_rows, delta_qhatm, single_channel_bound)

    summary = next(row for row in validation_rows if row["validation_id"] == "VAL3467_SUMMARY")
    print(summary["detail"])
    print(DOC)


if __name__ == "__main__":
    main()

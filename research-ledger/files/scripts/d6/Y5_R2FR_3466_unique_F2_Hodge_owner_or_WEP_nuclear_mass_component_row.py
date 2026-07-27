from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3466-Y5-R2FR-unique-F2-Hodge-owner-or-WEP-nuclear-mass-component-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

ETA_TIPT_BOUND_3465 = 2.8e-15
DELTA_Q_ALPHA_ABS_3465 = 0.001989808886825

SOURCES: dict[str, dict[str, Any]] = {
    "script_3466": {"type": "local", "path": Path(__file__).resolve(), "role": "generator for this checkpoint"},
    "doc_3465": {
        "type": "local",
        "path": ROOT / "3465-Y5-R2FR-EM-alpha-Hodge-charge-owner-or-WEP-raw-to-effective-map.md",
        "role": "3465 handoff: EM owner not closed; alpha WEP bound present; mass/nuclear row missing",
    },
    "raw_3465": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3465_RAW_TO_EFFECTIVE_COMPONENT_ROWS.csv",
        "role": "raw-to-effective WEP component rows from 3465",
    },
    "alpha_bound_3465": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv",
        "role": "alpha-only effective WEP source-leg ceiling from 3465",
    },
    "em_owner_3464": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv",
        "role": "EM owner localization predecessor",
    },
    "f2_1805": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_1805_NO_EXTRA_F2_THEOREM_ATTEMPT.csv",
        "role": "no-extra-F2 theorem attempt",
    },
    "alpha_level_1812": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
        "role": "alpha/fibre-level owner audit",
    },
    "unique_f2_1922": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_1922_UNIQUE_EM_F2_PROOF_AUDIT.csv",
        "role": "unique EM F2 proof audit and counterterm obstruction",
    },
    "f2_gates_3212": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3212_NO_EXTRA_F2_THEOREM_GATES.csv",
        "role": "no-extra-F2 gate list",
    },
    "hidden_f2_3282": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3282_HIDDEN_F2_SLOT_THEOREM_ATTEMPT.csv",
        "role": "hidden F2 slot zero routes and exact countermodel",
    },
    "hodge_3286": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3286_HODGE_POYNTING_OWNER_THEOREM.csv",
        "role": "Hodge/Poynting owner theorem and derivative identity",
    },
    "chi_3287": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3287_CHI_TO_HODGE_RECONSTRUCTION_THEOREM.csv",
        "role": "constitutive chi to Hodge reconstruction theorem",
    },
    "material_2440": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
        "role": "Damour-Donoghue Ti/Pt material sensitivity basis",
    },
    "source_register_2440": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_SOURCE_REGISTER.csv",
        "role": "source register for Damour/ONERA/MICROSCOPE material anchors",
    },
    "projection_2440": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv",
        "role": "WEP material/source projection formula",
    },
    "smoke_bounds_2440": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_SINGLE_COMPONENT_SMOKE_BOUNDS_NONCLAIM.csv",
        "role": "one-component D_mhat and D_e smoke bounds",
    },
    "dd_map_2441": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2441_MTS_TO_DD_CHARGE_MAP.csv",
        "role": "MTS-to-Damour-Donoghue charge map",
    },
    "mass_gap_2441": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2441_MASS_SECTOR_GAP_LEDGER.csv",
        "role": "mass-sector missing component ledger",
    },
    "reduced_formula_2441": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2441_WEP_REDUCED_FORMULA_NONCLAIM.csv",
        "role": "reduced WEP formula with D_mhat and D_e source legs",
    },
    "dd_charges_3265": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3265_DD_MATERIAL_CHARGES_NONCLAIM.csv",
        "role": "alloy-aware nonclaim Damour-Donoghue material charge rows",
    },
    "source_register_3265": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3265_SOURCE_REGISTER.csv",
        "role": "source register for DD tex, Eot-Wash tex, and 3264 handoff",
    },
    "delta_3264": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3264_TIPT_DD_DELTA_VECTOR_NONCLAIM.csv",
        "role": "TA6V minus PtRh10 DD delta vector from 3264",
    },
    "bounds_3264": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3264_MULTICHANNEL_WEP_BOUNDS_NONCLAIM.csv",
        "role": "two-channel MICROSCOPE strip bound from 3264",
    },
    "upgraded_material_3312": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3312_UPGRADED_MATERIAL_CHARGES.csv",
        "role": "upgraded material charge categories",
    },
    "local_bounds": {
        "type": "local",
        "path": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
        "role": "local empirical WEP bound ledger used by 3465",
    },
    "damour_donoghue_arxiv": {
        "type": "external",
        "url": "https://arxiv.org/abs/1007.2792",
        "role": "Damour-Donoghue two-charge dilaton-charge framework",
    },
    "damour_onera_pdf": {
        "type": "external",
        "url": "https://www.ihes.fr/~damour/Conferences/ONERA29Jan2013.pdf",
        "role": "ONERA table used by 2440 for Ti/Pt charge contrast",
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
    body = []
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
        source_type = meta["type"]
        path = meta.get("path")
        url = meta.get("url", "")
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


def unique_f2_hodge_owner_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "F2H3466_0_variation_identity",
            "clause": "vertical EM action variation",
            "derivation": "For S_EM=-1/4 int F_AB chi^{ABCD}F_CD, L_v S_EM contains -1/4 int F(L_v chi)F plus current/boundary/readout terms; if chi, F, current normalization, and observer coframe are q-basic then the vertical EM source vanishes.",
            "result": "EXACT_CONDITIONAL_IDENTITY",
            "gap": "q-basic chi/F/current/coframe are not parent-signed together.",
            "source_path": str(SOURCES["hodge_3286"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "F2H3466_1_hodge_reconstruction",
            "clause": "Hodge shape from constitutive chi",
            "derivation": "Local reciprocal nonbirefringent EM chi reconstructs a conformal EM metric and chi=lambda *_g plus axion/skewon residuals; this makes the Hodge branch derivable conditionally, not arbitrary.",
            "result": "DERIVED_CONDITIONAL_SHAPE",
            "gap": "scalar impedance lambda=Z_Q, axion/readout drift, and same-metric identification with matter/clock metric remain unsigned.",
            "source_path": str(SOURCES["chi_3287"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "F2H3466_2_hidden_F2_counterterm",
            "clause": "no hidden scalar gauge-kinetic slot",
            "derivation": "A term f_X(I_hid)F_Q^2 is visible-U(1) and covariance compatible unless a stronger q-basic, shift, or trivial-invariant-algebra gate forbids it.",
            "result": "EXACT_COUNTERMODEL_RETAINED",
            "gap": "current corpus has exact zero routes, but none is parent-owned across action, radiative corrections, and readout.",
            "source_path": str(SOURCES["hidden_f2_3282"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "F2H3466_3_unique_norm",
            "clause": "unique parent Maxwell F2 normalization",
            "derivation": "Fixed T_Q, charge lattice, parent gauge norm, and no independent lambda(X)F^2 would force b_alpha=0.",
            "result": "NOT_PARENT_SIGNED",
            "gap": "T_Q/gauge norm owner, coefficient-domain exhaustion, current owner, Hodge descent, and radiative/readout closure do not all pass.",
            "source_path": str(SOURCES["f2_gates_3212"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "F2H3466_4_verdict",
            "clause": "unique F2/Hodge owner theorem-zero",
            "derivation": "F2H3466_0 and F2H3466_1 give the right theorem skeleton; F2H3466_2 blocks unconditional promotion.",
            "result": "NOT_PROMOTED_USE_MASS_COMPONENT_ROW",
            "gap": "EM/Hodge route is mathematically sharp but still conditional; move concrete WEP map forward by filling mass/nuclear material contrast.",
            "source_path": str(SOURCES["unique_f2_1922"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def load_material_inputs() -> dict[str, Any]:
    material_2440 = read_csv(SOURCES["material_2440"]["path"])
    material_3265 = read_csv(SOURCES["dd_charges_3265"]["path"])

    pt_minus_ti = next(row for row in material_2440 if row.get("row_id") == "WMS2440_2_Pt_minus_Ti")
    onera_delta_q_mhat = abs(parse_float(pt_minus_ti.get("Q_mhat")) or 0.0)
    onera_delta_q_e = abs(parse_float(pt_minus_ti.get("Q_e")) or 0.0)

    ptrh10 = next(row for row in material_3265 if row.get("material_id") == "PtRh10")
    ta6v = next(row for row in material_3265 if row.get("material_id") == "TA6V")
    alloy_delta_q_mhat = abs(
        (parse_float(ptrh10.get("Qhatm_prime")) or 0.0)
        - (parse_float(ta6v.get("Qhatm_prime")) or 0.0)
    )
    alloy_delta_q_e = abs(
        (parse_float(ptrh10.get("Qe_prime")) or 0.0)
        - (parse_float(ta6v.get("Qe_prime")) or 0.0)
    )

    return {
        "onera_delta_q_mhat": onera_delta_q_mhat,
        "onera_delta_q_e": onera_delta_q_e,
        "alloy_delta_q_mhat": alloy_delta_q_mhat,
        "alloy_delta_q_e": alloy_delta_q_e,
        "ptrh10_row": ptrh10,
        "ta6v_row": ta6v,
        "pt_minus_ti_row": pt_minus_ti,
    }


def nuclear_mass_component_search(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "search_id": "NMS3466_0_DD_ONERA_TiPt",
            "target": "Delta_Q_mhat_TiPt",
            "found": True,
            "value": f"{inputs['onera_delta_q_mhat']:.12e}",
            "companion_Delta_Qe": f"{inputs['onera_delta_q_e']:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["material_2440"]["path"]),
            "source_row": "WMS2440_2_Pt_minus_Ti",
            "status": "SOURCE_BACKED_APPROXIMATE_ONERA_CONTRAST",
            "valid_for_claim": False,
        },
        {
            "search_id": "NMS3466_1_DD_alloy_TA6V_PtRh10",
            "target": "Delta_Qhatm_prime_abs_MICROSCOPE_alloys",
            "found": True,
            "value": f"{inputs['alloy_delta_q_mhat']:.12e}",
            "companion_Delta_Qe": f"{inputs['alloy_delta_q_e']:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_charges_3265"]["path"]),
            "source_row": "MAT3265_from3264_PtRh10; MAT3265_from3264_TA6V",
            "status": "ALLOY_AWARE_NONCLAIM_DD_CONTRAST_FILLED",
            "valid_for_claim": False,
        },
        {
            "search_id": "NMS3466_2_b_mhat_owner",
            "target": "b_mhat or b_nuclear",
            "found": False,
            "value": "MISSING_PARENT_COEFFICIENT",
            "companion_Delta_Qe": "",
            "units": "dimensionless",
            "source_path": str(SOURCES["mass_gap_2441"]["path"]),
            "source_row": "MSG2441_0_b_mhat; MSG2441_1_b_bind",
            "status": "MATERIAL_CHARGE_FOUND_COMPONENT_OWNER_MISSING",
            "valid_for_claim": False,
        },
        {
            "search_id": "NMS3466_3_source_leg",
            "target": "S_E^q",
            "found": False,
            "value": "MISSING_SOURCE_OWNER",
            "companion_Delta_Qe": "",
            "units": "dimensionless",
            "source_path": str(SOURCES["mass_gap_2441"]["path"]),
            "source_row": "MSG2441_3_source_leg",
            "status": "SOURCE_LEG_STILL_BLOCKS_MTS_PREDICTION",
            "valid_for_claim": False,
        },
    ]


def wep_mass_component_rows(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    alloy_bound = ETA_TIPT_BOUND_3465 / inputs["alloy_delta_q_mhat"]
    onera_bound = ETA_TIPT_BOUND_3465 / inputs["onera_delta_q_mhat"]
    return [
        {
            "component_id": "MASS3466_0_definition",
            "component": "D_mhat_eff",
            "formula": "D_mhat_eff := S_E^q * b_mhat",
            "known_inputs": "definition from Damour-Donoghue map",
            "missing_inputs": "S_E^q;b_mhat parent owner",
            "bound_or_value": "not_numeric_without_product_owner",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_map_2441"]["path"]),
            "source_row": "DDMAP2441_1_missing_b_mhat",
            "status": "PRODUCT_DEFINED_PARENT_OWNER_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "MASS3466_1_alloy_material_charge",
            "component": "Delta_Qhatm_prime_abs_MICROSCOPE_alloys",
            "formula": "abs(Qhatm_prime(PtRh10)-Qhatm_prime(TA6V))",
            "known_inputs": "PtRh10 and TA6V DD material rows",
            "missing_inputs": "exact isotope assay; source leg; b_mhat",
            "bound_or_value": f"{inputs['alloy_delta_q_mhat']:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_charges_3265"]["path"]),
            "source_row": "MAT3265_from3264_PtRh10; MAT3265_from3264_TA6V",
            "status": "MASS_MATERIAL_CHARGE_FILLED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "MASS3466_2_alloy_single_channel_bound",
            "component": "abs(D_mhat_eff)_single_channel",
            "formula": "abs(D_mhat_eff) <= eta_TiPt_bound/Delta_Qhatm_prime_abs if alpha/direct/shadow/readout channels are zero",
            "known_inputs": f"eta_TiPt_bound={ETA_TIPT_BOUND_3465:.12e}; Delta_Qhatm_prime_abs={inputs['alloy_delta_q_mhat']:.12e}",
            "missing_inputs": "single-channel premise; S_E^q;b_mhat parent owner",
            "bound_or_value": f"{alloy_bound:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_charges_3265"]["path"]),
            "source_row": "computed from 3265 alloy rows and 3465 eta bound",
            "status": "FINITE_NONCLAIM_MASS_CHANNEL_CEILING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "MASS3466_3_ONERA_crosscheck_bound",
            "component": "abs(D_mhat_eff)_ONERA_single_channel",
            "formula": "abs(D_mhat_eff) <= eta_TiPt_bound/Delta_Q_mhat_ONERA",
            "known_inputs": f"eta_TiPt_bound={ETA_TIPT_BOUND_3465:.12e}; Delta_Q_mhat_ONERA={inputs['onera_delta_q_mhat']:.12e}",
            "missing_inputs": "single-channel premise; S_E^q;b_mhat parent owner",
            "bound_or_value": f"{onera_bound:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["material_2440"]["path"]),
            "source_row": "WMS2440_2_Pt_minus_Ti",
            "status": "CONSISTENT_ONERA_CROSSCHECK_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def no_cancellation_envelope(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    alpha_bound = ETA_TIPT_BOUND_3465 / DELTA_Q_ALPHA_ABS_3465
    mass_bound = ETA_TIPT_BOUND_3465 / inputs["alloy_delta_q_mhat"]
    return [
        {
            "envelope_id": "NCE3466_0_full_formula",
            "formula": "abs(Delta_Qhatm*D_mhat_eff)+abs(Delta_Qe*D_e_eff)+abs(direct_delta_w)+abs(shadow_source)+abs(readout_frame)+abs(projector_tail) <= eta_TiPt_bound",
            "numeric_piece": f"eta_TiPt_bound={ETA_TIPT_BOUND_3465:.12e}",
            "status": "ENVELOPE_FORMULA_READY_COMPONENTS_INCOMPLETE",
            "source_path": str(SOURCES["reduced_formula_2441"]["path"]),
            "valid_for_claim": False,
        },
        {
            "envelope_id": "NCE3466_1_alpha_piece",
            "formula": "abs(Delta_Qe*D_e_eff) <= eta_TiPt_bound",
            "numeric_piece": f"Delta_Q_alpha_abs={DELTA_Q_ALPHA_ABS_3465:.12e}; abs(D_e_eff)<={alpha_bound:.12e}",
            "status": "ALPHA_SINGLE_CHANNEL_CEILING_FROM_3465",
            "source_path": str(SOURCES["alpha_bound_3465"]["path"]),
            "valid_for_claim": False,
        },
        {
            "envelope_id": "NCE3466_2_mass_piece",
            "formula": "abs(Delta_Qhatm*D_mhat_eff) <= eta_TiPt_bound",
            "numeric_piece": f"Delta_Qhatm_alloy_abs={inputs['alloy_delta_q_mhat']:.12e}; abs(D_mhat_eff)<={mass_bound:.12e}",
            "status": "MASS_SINGLE_CHANNEL_CEILING_ADDED",
            "source_path": str(SOURCES["dd_charges_3265"]["path"]),
            "valid_for_claim": False,
        },
        {
            "envelope_id": "NCE3466_3_no_cancellation_guard",
            "formula": "single-channel ceilings cannot be added as a pass; final score requires the absolute sum over every live channel",
            "numeric_piece": "direct/shadow/readout/projector and S_E^q*b_i product owners still missing",
            "status": "NO_CANCELLATION_GUARD_STILL_BLOCKS_CLAIM",
            "source_path": str(SOURCES["projection_2440"]["path"]),
            "valid_for_claim": False,
        },
    ]


def claim_gates(
    f2_rows: list[dict[str, Any]],
    search_rows: list[dict[str, Any]],
    mass_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    f2_not_promoted = any(row["result"] == "NOT_PROMOTED_USE_MASS_COMPONENT_ROW" for row in f2_rows)
    material_found = any(row["search_id"] == "NMS3466_1_DD_alloy_TA6V_PtRh10" and row["found"] for row in search_rows)
    component_missing = any(row["search_id"] == "NMS3466_2_b_mhat_owner" and not row["found"] for row in search_rows)
    source_missing = any(row["search_id"] == "NMS3466_3_source_leg" and not row["found"] for row in search_rows)
    finite_mass_bound = any(row["component_id"] == "MASS3466_2_alloy_single_channel_bound" for row in mass_rows)
    return [
        {
            "gate_id": "CG3466_0_unique_F2_Hodge_zero",
            "gate": "unique F2/Hodge owner proves b_alpha and EM source zero",
            "pass": False,
            "detail": "conditional identities exist but hidden F2/counterterm and readout gates are not parent-signed" if f2_not_promoted else "unexpected",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3466_1_mass_material_charge",
            "gate": "mass/nuclear material contrast is no longer missing",
            "pass": material_found,
            "detail": "alloy-aware nonclaim Delta_Qhatm row found and propagated",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3466_2_mass_source_product",
            "gate": "D_mhat_eff=S_E^q*b_mhat is parent-owned or bounded",
            "pass": not component_missing and not source_missing,
            "detail": "b_mhat and source leg S_E^q remain missing, so no MTS prediction is claimed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3466_3_finite_mass_ceiling",
            "gate": "single-channel mass ceiling is computed for future coupling tests",
            "pass": finite_mass_bound,
            "detail": "nonclaim ceiling exists only under isolated mass-channel/no-cancellation premise",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3466_4_local_GR_WEP_pass",
            "gate": "local GR/WEP source coupling passes",
            "pass": False,
            "detail": "claim remains blocked until direct/shadow/readout/projector terms and D_i source products are theorem-zero or sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    mass_bound = ETA_TIPT_BOUND_3465 / inputs["alloy_delta_q_mhat"]
    return [
        {
            "decision_id": "DEC3466_0_F2_Hodge",
            "decision": "Do not promote unique F2/Hodge owner theorem.",
            "reason": "The chain-rule/Hodge reconstruction is real, but hidden F2 and readout/radiative counterterms remain admissible without a stronger parent gate.",
            "next_action": "Keep EM/Hodge route as an exact conditional theorem, not a claim.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3466_1_mass_progress",
            "decision": "Promote the mass/nuclear WEP row from missing-material to finite nonclaim component.",
            "reason": f"Delta_Qhatm_alloy_abs={inputs['alloy_delta_q_mhat']:.12e} gives abs(D_mhat_eff)<={mass_bound:.12e} under a one-channel ceiling.",
            "next_action": "Attack the actual coupling: derive or bound D_mhat_eff=S_E^q*b_mhat.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3466_2_next_route",
            "decision": "Next best target is b_mhat/source-leg ownership, not another material sweep.",
            "reason": "The material side now has usable mass and alpha contrasts; the missing physics is the MTS product coupling into Earth/source matter.",
            "next_action": "3467 should try a mass-sector q-basic/superselection theorem for b_mhat=0; if that fails, derive a source-leg product row for S_E^q*b_mhat.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3467-Y5-R2FR-bmhat-zero-theorem-or-source-leg-product-coupling.md",
            "next_script": "scripts/Y5_R2FR_3467_bmhat_zero_theorem_or_source_leg_product_coupling.py",
            "objective": "Try to prove the mass/nuclear coefficient b_mhat is q-basic/superselected and therefore zero; if not, derive or bound the source product D_mhat_eff=S_E^q*b_mhat using the 3466 material row.",
            "success_gate": "Either b_mhat=0 is parent-signed, or a nonclaim source-product row exists with S_E^q, b_mhat, units, source path, and no-cancellation envelope.",
            "exclude": "GitHub action; formalization-workbench edits; local-GR/WEP pass claim; hiding D_mhat in G_N calibration; signed cancellation.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validate(
    outputs: dict[str, Path],
    source_rows: list[dict[str, Any]],
    f2_rows: list[dict[str, Any]],
    search_rows: list[dict[str, Any]],
    mass_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    stamp = now()
    local_sources_ok = all(
        row["exists_or_url_present"]
        for row in source_rows
        if row["source_type"] == "local"
    )
    f2_not_overclaimed = any(row["result"] == "EXACT_COUNTERMODEL_RETAINED" for row in f2_rows) and any(
        row["result"] == "NOT_PROMOTED_USE_MASS_COMPONENT_ROW" for row in f2_rows
    )
    material_filled = any(
        row["search_id"] == "NMS3466_1_DD_alloy_TA6V_PtRh10"
        and row["found"]
        and parse_float(row["value"])
        and parse_float(row["value"]) > 0
        for row in search_rows
    )
    owner_missing_recorded = any(
        row["search_id"] == "NMS3466_2_b_mhat_owner" and row["found"] is False
        for row in search_rows
    )
    mass_bound_finite = any(
        row["component_id"] == "MASS3466_2_alloy_single_channel_bound"
        and parse_float(row["bound_or_value"])
        and parse_float(row["bound_or_value"]) > 0
        for row in mass_rows
    )
    no_cancellation_blocks = any(
        row["envelope_id"] == "NCE3466_3_no_cancellation_guard"
        and row["status"] == "NO_CANCELLATION_GUARD_STILL_BLOCKS_CLAIM"
        for row in envelope_rows
    )
    no_claim_rows = not any(
        str(value).lower() == "true"
        for rows in (f2_rows, search_rows, mass_rows, envelope_rows, gate_rows)
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
        except Exception as exc:  # pragma: no cover - validation output
            parse_counts.append(f"{path.name}:ERROR:{exc}")
            csv_parse_ok = False
    formalization_ok = True
    formalization_detail = "formalization_exists=False"
    if FORMALIZATION.exists():
        matches = list(FORMALIZATION.rglob("*3466*"))
        formalization_ok = not matches
        formalization_detail = f"formalization_exists=True; 3466_outputs_in_formalization={len(matches)}"

    rows = [
        {
            "validation_id": "VAL3466_0_local_sources_exist",
            "pass": local_sources_ok,
            "detail": ";".join(row["source_id"] for row in source_rows if row["source_type"] == "local" and not row["exists_or_url_present"]) or "all local sources exist",
            "timestamp_utc": stamp,
        },
        {
            "validation_id": "VAL3466_1_F2_Hodge_not_overclaimed",
            "pass": f2_not_overclaimed,
            "detail": "conditional theorem plus exact hidden-F2 countermodel retained",
            "timestamp_utc": stamp,
        },
        {
            "validation_id": "VAL3466_2_mass_material_charge_filled",
            "pass": material_filled,
            "detail": "Delta_Qhatm alloy material row is positive and numeric",
            "timestamp_utc": stamp,
        },
        {
            "validation_id": "VAL3466_3_bmhat_owner_still_blocked",
            "pass": owner_missing_recorded,
            "detail": "b_mhat and S_E^q missing rows explicitly retained",
            "timestamp_utc": stamp,
        },
        {
            "validation_id": "VAL3466_4_mass_bound_finite_nonclaim",
            "pass": mass_bound_finite,
            "detail": "single-channel D_mhat_eff ceiling computed",
            "timestamp_utc": stamp,
        },
        {
            "validation_id": "VAL3466_5_no_cancellation_guard_blocks_claim",
            "pass": no_cancellation_blocks,
            "detail": "absolute envelope still requires all live channels",
            "timestamp_utc": stamp,
        },
        {
            "validation_id": "VAL3466_6_no_claim_rows",
            "pass": no_claim_rows,
            "detail": "all claim_allowed and valid_for_claim flags remain false",
            "timestamp_utc": stamp,
        },
        {
            "validation_id": "VAL3466_7_csv_parse",
            "pass": csv_parse_ok,
            "detail": ";".join(parse_counts),
            "timestamp_utc": stamp,
        },
        {
            "validation_id": "VAL3466_8_formalization_untouched_by_3466",
            "pass": formalization_ok,
            "detail": formalization_detail,
            "timestamp_utc": stamp,
        },
    ]
    rows.append(
        {
            "validation_id": "VAL3466_SUMMARY",
            "pass": all(str(row["pass"]).lower() == "true" for row in rows),
            "detail": "PASS" if all(str(row["pass"]).lower() == "true" for row in rows) else "FAIL",
            "timestamp_utc": stamp,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    f2_rows: list[dict[str, Any]],
    search_rows: list[dict[str, Any]],
    mass_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    mass_bound = next(row for row in mass_rows if row["component_id"] == "MASS3466_2_alloy_single_channel_bound")["bound_or_value"]
    delta_q = next(row for row in mass_rows if row["component_id"] == "MASS3466_1_alloy_material_charge")["bound_or_value"]
    doc = f"""# 3466 - Unique F2/Hodge Owner Or WEP Nuclear-Mass Component Row

**Current verdict:** the unique `F^2`/Hodge route is mathematically sharpened but still not parent-promoted. The exact vertical-zero identity exists if `chi`, `F`, current normalization, and the observer coframe are all `q`-basic, but hidden `f_X(I_hid)F^2` and readout/radiative slots remain live countermodels.

**Concrete progress:** the mass/nuclear WEP row is no longer merely missing. The alloy-aware Damour-Donoghue contrast gives `Delta_Qhatm_abs={delta_q}`, so the isolated one-channel ceiling is `|D_mhat_eff| <= {mass_bound}` with `D_mhat_eff := S_E^q b_mhat`; this is a finite nonclaim coupling target, not a WEP/local-GR pass.

## Source Register
{md_table(source_rows)}

## Unique F2/Hodge Owner Audit
{md_table(f2_rows)}

## Nuclear/Mass Component Search
{md_table(search_rows)}

## WEP Mass Component Rows
{md_table(mass_rows)}

## No-Cancellation Envelope Update
{md_table(envelope_rows)}

## Claim Gates
{md_table(gate_rows)}

## Decision Ledger
{md_table(decision_rows)}

## Validation
{md_table(validation_rows)}

## Next Target
{md_table(next_rows)}

## Short Readout
- EM/Hodge theorem-zero: not claimed; exact conditional identity and exact countermodel are both retained.
- New finite progress: `Delta_Qhatm_abs={delta_q}` and `|D_mhat_eff| <= {mass_bound}` in the isolated mass-channel ceiling.
- Still missing: parent ownership or bound for `D_mhat_eff=S_E^q b_mhat`, plus direct/shadow/readout/projector terms.
- Best next move: try the `b_mhat=0` mass-superselection theorem; if it fails, derive a source-product row for `S_E^q b_mhat`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register()
    f2_rows = unique_f2_hodge_owner_audit()
    inputs = load_material_inputs()
    search_rows = nuclear_mass_component_search(inputs)
    mass_rows = wep_mass_component_rows(inputs)
    envelope_rows = no_cancellation_envelope(inputs)
    gate_rows = claim_gates(f2_rows, search_rows, mass_rows)
    decision_rows = decision_ledger(inputs)
    next_rows = next_target()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3466_SOURCE_REGISTER.csv",
        "f2_hodge_audit": OUT / "P8_Y5_R2FR_3466_UNIQUE_F2_HODGE_OWNER_AUDIT.csv",
        "mass_search": OUT / "P8_Y5_R2FR_3466_NUCLEAR_MASS_COMPONENT_SEARCH.csv",
        "mass_rows": OUT / "P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv",
        "envelope": OUT / "P8_Y5_R2FR_3466_NO_CANCELLATION_ENVELOPE_UPDATE.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3466_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3466_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3466_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3466_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["f2_hodge_audit"], f2_rows)
    write_csv(outputs["mass_search"], search_rows)
    write_csv(outputs["mass_rows"], mass_rows)
    write_csv(outputs["envelope"], envelope_rows)
    write_csv(outputs["claim_gates"], gate_rows)
    write_csv(outputs["decision"], decision_rows)
    write_csv(outputs["next"], next_rows)
    validation_rows = validate(outputs, source_rows, f2_rows, search_rows, mass_rows, envelope_rows, gate_rows)
    write_csv(outputs["validation"], validation_rows)
    write_doc(source_rows, f2_rows, search_rows, mass_rows, envelope_rows, gate_rows, decision_rows, validation_rows, next_rows)

    summary = next(row for row in validation_rows if row["validation_id"] == "VAL3466_SUMMARY")
    print(summary["detail"])
    print(DOC)


if __name__ == "__main__":
    main()

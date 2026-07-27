from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3468-Y5-R2FR-constant-sector-universality-or-hidden-SM-coefficient-morphism.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

ETA_TIPT_BOUND = 2.8e-15

SOURCES: dict[str, dict[str, Any]] = {
    "script_3468": {"type": "local", "path": Path(__file__).resolve(), "role": "generator for this checkpoint"},
    "doc_3467": {
        "type": "local",
        "path": ROOT / "3467-Y5-R2FR-bmhat-zero-theorem-or-source-leg-product-coupling.md",
        "role": "3467 handoff: b_mhat zero theorem and product bound",
    },
    "next_3467": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3467_NEXT_TARGET.csv",
        "role": "3468 target statement",
    },
    "bmhat_3467": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3467_BMHAT_ZERO_THEOREM_ATTEMPT.csv",
        "role": "b_mhat zero theorem attempt",
    },
    "mass_product_3467": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3467_SOURCE_PRODUCT_COUPLING_ROWS.csv",
        "role": "mass source-product coupling rows",
    },
    "newton_guard_3467": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3467_NEWTON_G_CALIBRATION_GUARD.csv",
        "role": "Newton/G common-mode guard",
    },
    "alpha_owner_1812": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
        "role": "alpha level/fibre norm owner audit",
    },
    "f2_1805": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_1805_NO_EXTRA_F2_THEOREM_ATTEMPT.csv",
        "role": "no-extra-F2 theorem attempt",
    },
    "hidden_f2_3282": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3282_HIDDEN_F2_SLOT_THEOREM_ATTEMPT.csv",
        "role": "hidden F2 zero routes and countermodel",
    },
    "direct_matter_2612": {
        "type": "local",
        "path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv",
        "role": "alpha/mass/charge vertex classification",
    },
    "typing_2650": {
        "type": "local",
        "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_SOURCE_PREFACTOR_TYPING_GATE.csv",
        "role": "parent typing gate for no hidden source/constant coefficient",
    },
    "no_species_contract": {
        "type": "local",
        "path": OUT / "P8_no_species_source_charge_CONTRACT.csv",
        "role": "constant-sector universality and no species source-charge contract",
    },
    "alpha_bound_3465": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv",
        "role": "alpha-only WEP source-leg bound",
    },
    "mass_row_3466": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv",
        "role": "mass/nuclear WEP material and product bound",
    },
    "envelope_3466": {
        "type": "local",
        "path": OUT / "P8_Y5_R2FR_3466_NO_CANCELLATION_ENVELOPE_UPDATE.csv",
        "role": "no-cancellation envelope containing alpha and mass pieces",
    },
    "dd_map_2441": {
        "type": "local",
        "path": OUT / "P8_Y5_PARENT_QLOC_2441_MTS_TO_DD_CHARGE_MAP.csv",
        "role": "MTS to Damour-Donoghue charge map",
    },
    "material_tensor_2650": {
        "type": "local",
        "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv",
        "role": "material tensor and exact coefficient-basis gap",
    },
    "source_ward_contract": {
        "type": "local",
        "path": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
        "role": "source-current Ward/universality contract",
    },
    "damour_donoghue_arxiv": {
        "type": "external",
        "url": "https://arxiv.org/abs/1007.2792",
        "role": "Damour-Donoghue charge framework",
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
        rows.append(
            {
                "timestamp_utc": stamp,
                "source_id": source_id,
                "source_type": meta["type"],
                "source_path": str(path) if path else "",
                "source_url": url,
                "exists_or_url_present": bool(path.exists()) if isinstance(path, Path) else bool(url),
                "role": meta["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def get_bound_values() -> dict[str, float]:
    alpha_rows = read_csv(SOURCES["alpha_bound_3465"]["path"])
    mass_rows = read_csv(SOURCES["mass_row_3466"]["path"])
    alpha_delta = parse_float(next(row for row in alpha_rows if row["calc_id"] == "AOB3465_1_delta_Q_alpha")["value"])
    alpha_bound = parse_float(next(row for row in alpha_rows if row["calc_id"] == "AOB3465_2_D_e_bound")["value"])
    mass_delta = parse_float(next(row for row in mass_rows if row["component_id"] == "MASS3466_1_alloy_material_charge")["bound_or_value"])
    mass_bound = parse_float(next(row for row in mass_rows if row["component_id"] == "MASS3466_2_alloy_single_channel_bound")["bound_or_value"])
    if None in {alpha_delta, alpha_bound, mass_delta, mass_bound}:
        raise ValueError("required 3465/3466 bound values missing")
    return {
        "alpha_delta": float(alpha_delta),
        "alpha_bound": float(alpha_bound),
        "mass_delta": float(mass_delta),
        "mass_bound": float(mass_bound),
    }


def constant_sector_theorem_attempt() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CSU3468_0_visible_bundle",
            "claim_piece": "visible constant-sector bundle",
            "statement": "Let Theta_vis={Z_EM or alpha_EM, charge-current norm, y_f, v_H/Lambda_QCD, mhat/Lambda_QCD, m_e/Lambda_QCD, nuclear binding coefficients, readout constants}.",
            "proof_status": "OBJECT_DEFINED",
            "proof_or_obstruction": "This packages the alpha and mass-sector gaps into one coefficient-bundle problem.",
            "required_parent_clause": "none for definition",
            "source_path": str(SOURCES["bmhat_3467"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSU3468_1_qbasic_chain_rule",
            "claim_piece": "quotient-basic constant-sector silence",
            "statement": "If Theta_vis=q^*Theta_bar or is fixed superselected representation data, then for every local vertical v in ker(Dq), L_v Theta_vis=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "Chain rule: D(q^*Theta_bar)[v]=DTheta_bar[Dq(v)]=0. This simultaneously kills b_alpha, b_mhat, b_me, and binding-response slopes.",
            "required_parent_clause": "constant-sector universality or superselection theorem",
            "source_path": str(SOURCES["no_species_contract"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSU3468_2_parent_action_owner",
            "claim_piece": "one parent owner for visible coefficients",
            "statement": "Visible coefficients must be typed as fixed representation/fibre data or quotient fields, not as functions of hidden/local invariants.",
            "proof_status": "CONDITIONAL_OBJECT_LANGUAGE_ROUTE",
            "proof_or_obstruction": "2650 gives the needed typing gate shape, but parent sorts and no-marker/readout return are not signed.",
            "required_parent_clause": "parent sorts plus Hom(HiddenInvariant,Coeff_visible)=empty",
            "source_path": str(SOURCES["typing_2650"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSU3468_3_F2_mass_unification",
            "claim_piece": "alpha and mass share the same coefficient-slot obstruction",
            "statement": "The hidden F2 counterterm f_X(I_hid)F^2 and hidden mass/Yukawa/QCD terms y(I_hid)H psi psi, Z_G(I_hid)G^2, B_nuc(I_hid)O_bind are the same kind of forbidden morphism.",
            "proof_status": "DERIVED_CLASSIFICATION",
            "proof_or_obstruction": "This is a real simplification: alpha/F2 and b_mhat are not two unrelated gaps; both are visible-coefficient ownership gaps.",
            "required_parent_clause": "one coefficient-domain exclusion theorem",
            "source_path": str(SOURCES["hidden_f2_3282"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSU3468_4_radiative_readout_preservation",
            "claim_piece": "renormalized/readout constants stay q-basic",
            "statement": "If bare Theta_vis is q-basic and the beta functions, thresholds, Hodge/readout maps, and clock/spectral reductions use only q-basic visible data, then the renormalized/readout Theta_eff is q-basic.",
            "proof_status": "EXACT_CONDITIONAL_FUNCTORIAL_PRESERVATION",
            "proof_or_obstruction": "The preservation theorem is straightforward, but current records keep radiative/readout closure unsigned for alpha and source readout.",
            "required_parent_clause": "radiative and readout closure",
            "source_path": str(SOURCES["f2_1805"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSU3468_5_countermodel",
            "claim_piece": "why covariance/gauge symmetry alone cannot close the theorem",
            "statement": "If I_hid is an allowed scalar, then sqrt(-g)I_hid F^2, y(I_hid)H psi psi, Z_G(I_hid)Tr G^2, and c_N(I_hid)O_bind are local and covariant with the visible gauge symmetries.",
            "proof_status": "EXACT_COUNTERMODEL_CLASS",
            "proof_or_obstruction": "Only a stronger parent q-basic/superselection/no-Hom rule forbids these slots.",
            "required_parent_clause": "no hidden-to-SM coefficient morphism",
            "source_path": str(SOURCES["direct_matter_2612"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSU3468_6_verdict",
            "claim_piece": "promote constant-sector universality from current corpus",
            "statement": "Current MTS does not yet parent-sign the visible constant-sector owner, so b_alpha and b_mhat-like coefficients are retained as finite nonclaim rows.",
            "proof_status": "NOT_PARENT_DERIVED_CURRENT_CORPUS",
            "proof_or_obstruction": "Use the retained coefficient vector until the parent coefficient-domain theorem is signed.",
            "required_parent_clause": "CSU3468_1 through CSU3468_4 closed together, with CSU3468_5 excluded",
            "source_path": str(SOURCES["alpha_owner_1812"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def coefficient_morphism_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "HSM3468_0_F2_alpha",
            "target_coefficient": "b_alpha = L_v ln alpha_EM or L_v ln Z_EM^-1",
            "operator_slot": "F^2 / Hodge / charge-current normalization / readout alpha",
            "zero_route": "unique parent F2 norm plus fixed charge-current owner plus q-basic readout",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "hidden f_X(I_hid)F^2 or readout/radiative alpha drift",
            "source_path": str(SOURCES["hidden_f2_3282"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSM3468_1_Yukawa_Higgs",
            "target_coefficient": "b_y, b_v, b_me",
            "operator_slot": "y_f H psi psi; Higgs vev/electron mass ratio",
            "zero_route": "Yukawa/Higgs constants are fixed representation/superselection data",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "m_e/material-standard and clock sensitivity drift",
            "source_path": str(SOURCES["direct_matter_2612"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSM3468_2_QCD_mass_ratio",
            "target_coefficient": "b_mhat = L_v ln(mhat/Lambda_QCD)",
            "operator_slot": "light-quark mass ratio and QCD-scale ratio",
            "zero_route": "dimensionless mass ratios are q-basic/superselected",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "failure_mode": "MICROSCOPE mass-channel WEP product remains live",
            "source_path": str(SOURCES["bmhat_3467"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSM3468_3_nuclear_binding",
            "target_coefficient": "b_bind / b_nuclear",
            "operator_slot": "nuclear EFT binding operators and isotope/alloy response",
            "zero_route": "binding coefficients descend from the same q-basic visible constants",
            "current_status": "MATERIAL_TENSOR_BASIS_NOT_PARENT_FILLED",
            "failure_mode": "exact isotope/alloy material tensor and binding decomposition remain needed",
            "source_path": str(SOURCES["material_tensor_2650"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSM3468_4_readout_radiative",
            "target_coefficient": "b_readout / b_rad",
            "operator_slot": "clock/spectral/readout and RG threshold maps",
            "zero_route": "readout and radiative reductions are functorial in q-basic visible data",
            "current_status": "UNSIGNED_PRESERVATION_REQUIREMENT",
            "failure_mode": "tree-level zero does not survive clocks, spectra, R10, or WEP readout",
            "source_path": str(SOURCES["f2_1805"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def retained_coefficient_vector(values: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "RCV3468_0_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative of visible alpha/gauge-kinetic normalization after Hodge/current/readout convention",
            "source_product": "D_e_eff := tau_WEP(lambda) * S_E^q * b_alpha",
            "material_or_readout_factor": f"Delta_Q_alpha_abs={values['alpha_delta']:.12e}",
            "current_bound": f"{values['alpha_bound']:.12e}",
            "bound_meaning": "isolated alpha-channel WEP ceiling on abs(D_e_eff)",
            "units": "dimensionless",
            "tests": "WEP; R10; clocks; EM spectra",
            "zero_status": "NOT_PARENT_DERIVED",
            "source_path": str(SOURCES["alpha_bound_3465"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "RCV3468_1_b_mhat",
            "symbol": "b_mhat",
            "definition": "vertical derivative of mhat/Lambda_QCD or equivalent dimensionless light-quark/QCD mass ratio",
            "source_product": "D_mhat_eff := tau_WEP(lambda) * S_E^q * b_mhat",
            "material_or_readout_factor": f"Delta_Qhatm_abs={values['mass_delta']:.12e}",
            "current_bound": f"{values['mass_bound']:.12e}",
            "bound_meaning": "isolated mass-channel WEP ceiling on abs(D_mhat_eff)",
            "units": "dimensionless",
            "tests": "WEP; clocks; nuclear systems",
            "zero_status": "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "source_path": str(SOURCES["mass_product_3467"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "RCV3468_2_b_me",
            "symbol": "b_me",
            "definition": "vertical derivative of m_e/Lambda_QCD or electron Yukawa/Higgs ratio",
            "source_product": "D_me_eff := tau_clock/WEP * S_E^q * b_me",
            "material_or_readout_factor": "MISSING_Delta_Q_me_or_clock_sensitivity",
            "current_bound": "MISSING_NUMERIC_BOUND",
            "bound_meaning": "requires clock/material sensitivity coefficients",
            "units": "dimensionless",
            "tests": "atomic clocks; spectra; WEP subcomponent",
            "zero_status": "RETAINED_COEFFICIENT",
            "source_path": str(SOURCES["direct_matter_2612"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "RCV3468_3_b_bind",
            "symbol": "b_bind / b_nuclear",
            "definition": "vertical derivative of nuclear binding EFT coefficients not already folded into b_mhat proxy",
            "source_product": "D_bind_eff := tau_WEP * S_E^q * b_bind",
            "material_or_readout_factor": "MISSING_exact_binding_material_tensor",
            "current_bound": "FOLDED_ONLY_IN_PROXY_MASS_CHANNEL",
            "bound_meaning": "needs exact isotope/alloy binding decomposition before separate score",
            "units": "dimensionless",
            "tests": "WEP; nuclear clocks; isotope shifts",
            "zero_status": "RETAINED_COEFFICIENT",
            "source_path": str(SOURCES["material_tensor_2650"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "RCV3468_4_b_readout",
            "symbol": "b_readout / b_rad",
            "definition": "vertical derivative regenerated by RG thresholds, clock readout, Hodge projection, or material standards",
            "source_product": "D_readout_eff := tau_arena * S_source * b_readout",
            "material_or_readout_factor": "MISSING_arena_readout_sensitivity",
            "current_bound": "MISSING_NUMERIC_BOUND",
            "bound_meaning": "required to preserve any tree-level zero theorem",
            "units": "dimensionless",
            "tests": "clocks; WEP; R10; EM spectra",
            "zero_status": "UNSIGNED_PRESERVATION_REQUIREMENT",
            "source_path": str(SOURCES["f2_1805"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "RCV3468_5_common_scale",
            "symbol": "b_common",
            "definition": "vertical derivative of a universal source/mass scale common to all local matter",
            "source_product": "common calibration only",
            "material_or_readout_factor": "Delta_AB common mode = 0",
            "current_bound": "not_WEP_source_charge",
            "bound_meaning": "may calibrate measured G/units; cannot hide differential dimensionless drift",
            "units": "dimensionless",
            "tests": "Newton/G calibration; not a standalone WEP numerator",
            "zero_status": "COMMON_MODE_GUARD",
            "source_path": str(SOURCES["newton_guard_3467"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def no_cancellation_envelope(values: dict[str, float]) -> list[dict[str, Any]]:
    alpha_contrib = values["alpha_delta"] * values["alpha_bound"]
    mass_contrib = values["mass_delta"] * values["mass_bound"]
    return [
        {
            "envelope_id": "NCV3468_0_vector_envelope",
            "formula": "abs(Delta_Q_alpha*D_e_eff)+abs(Delta_Qhatm*D_mhat_eff)+abs(Delta_Q_me*D_me_eff)+abs(Delta_Q_bind*D_bind_eff)+abs(readout/direct/shadow/projector) <= eta_TiPt_bound",
            "numeric_piece": f"eta_TiPt_bound={ETA_TIPT_BOUND:.12e}",
            "status": "VECTOR_ENVELOPE_READY_INCOMPLETE",
            "source_path": str(SOURCES["envelope_3466"]["path"]),
            "valid_for_claim": False,
        },
        {
            "envelope_id": "NCV3468_1_alpha_check",
            "formula": "Delta_Q_alpha_abs * alpha_ceiling",
            "numeric_piece": f"{values['alpha_delta']:.12e} * {values['alpha_bound']:.12e} = {alpha_contrib:.12e}",
            "status": "MATCHES_ETA_BOUND_WITH_ROUNDING",
            "source_path": str(SOURCES["alpha_bound_3465"]["path"]),
            "valid_for_claim": False,
        },
        {
            "envelope_id": "NCV3468_2_mass_check",
            "formula": "Delta_Qhatm_abs * mass_ceiling",
            "numeric_piece": f"{values['mass_delta']:.12e} * {values['mass_bound']:.12e} = {mass_contrib:.12e}",
            "status": "MATCHES_ETA_BOUND_WITH_ROUNDING",
            "source_path": str(SOURCES["mass_row_3466"]["path"]),
            "valid_for_claim": False,
        },
        {
            "envelope_id": "NCV3468_3_no_independent_pass",
            "formula": "single-channel ceilings are not simultaneous evidence; final pass requires the absolute vector sum or theorem-zero rows",
            "numeric_piece": "alpha and mass ceilings each saturate eta separately in one-at-a-time conventions",
            "status": "NO_CANCELLATION_GUARD_ACTIVE",
            "source_path": str(SOURCES["envelope_3466"]["path"]),
            "valid_for_claim": False,
        },
    ]


def arena_crosswalk() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ARENA3468_0_WEP_TiPt",
            "uses_coefficients": "b_alpha;b_mhat;b_me;b_bind;b_readout;direct/shadow/projector",
            "numeric_status": "alpha and mhat one-channel ceilings exist; other vector components missing",
            "claim_status": "NONCLAIM_VECTOR_BOUND_ONLY",
            "source_path": str(SOURCES["envelope_3466"]["path"]),
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA3468_1_clocks",
            "uses_coefficients": "b_alpha;b_me;b_mhat;b_bind;b_readout",
            "numeric_status": "clock sensitivity vector not filled in 3468",
            "claim_status": "REQUIRES_CLOCK_SENSITIVITY_ROWS",
            "source_path": str(SOURCES["source_ward_contract"]["path"]),
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA3468_2_R10",
            "uses_coefficients": "b_alpha;charge-current normalization;source/test strength;lambda",
            "numeric_status": "R10 bound curve exists elsewhere but MTS coefficient numerator remains nonclaim",
            "claim_status": "REQUIRES_ALPHA_SOURCE_NUMERATOR",
            "source_path": str(SOURCES["f2_1805"]["path"]),
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA3468_3_local_GR_Newton",
            "uses_coefficients": "b_common plus all differential coefficient slots",
            "numeric_status": "one common G calibration allowed; dimensionless coefficient drift cannot be hidden",
            "claim_status": "LOCAL_GR_SOURCE_COUPLING_STILL_BLOCKED",
            "source_path": str(SOURCES["newton_guard_3467"]["path"]),
            "valid_for_claim": False,
        },
    ]


def claim_gates(theorem_rows: list[dict[str, Any]], vector_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theorem_not_promoted = any(row["theorem_id"] == "CSU3468_6_verdict" and row["proof_status"] == "NOT_PARENT_DERIVED_CURRENT_CORPUS" for row in theorem_rows)
    alpha_vector = any(row["coefficient_id"] == "RCV3468_0_b_alpha" and parse_float(row["current_bound"]) for row in vector_rows)
    mass_vector = any(row["coefficient_id"] == "RCV3468_1_b_mhat" and parse_float(row["current_bound"]) for row in vector_rows)
    missing_rows = [row["coefficient_id"] for row in vector_rows if "MISSING" in row["current_bound"] or "FOLDED_ONLY" in row["current_bound"]]
    return [
        {
            "gate_id": "CG3468_0_constant_sector_zero",
            "gate": "all visible constant coefficients are q-basic/superselected",
            "pass": not theorem_not_promoted,
            "detail": "not parent-derived; exact conditional theorem retained",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3468_1_alpha_mass_vector",
            "gate": "alpha and mhat retained vector rows have numeric one-channel ceilings",
            "pass": alpha_vector and mass_vector,
            "detail": "b_alpha and b_mhat product ceilings are present",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3468_2_full_vector_complete",
            "gate": "all retained coefficient rows are numeric/sourced",
            "pass": False,
            "detail": "missing or folded rows: " + ";".join(missing_rows),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3468_3_no_cancellation",
            "gate": "vector pass may use cancellation",
            "pass": False,
            "detail": "absolute no-cancellation envelope remains mandatory",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3468_4_local_GR_Maxwell_Newton",
            "gate": "local GR/Newton/Maxwell source coupling is derived",
            "pass": False,
            "detail": "blocked by visible coefficient owner, readout/radiative, source leg, and full vector completion",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3468_0_unification",
            "decision": "Treat alpha/F2 and mass/nuclear coupling as one visible-coefficient-owner problem.",
            "reason": "Both fail for the same reason: hidden/local scalar morphisms into visible coefficient slots are not parent-excluded.",
            "next_action": "Do not chase alpha and mass as unrelated branches unless the unified theorem fails per coefficient.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3468_1_no_claim",
            "decision": "Do not claim constant-sector universality yet.",
            "reason": "The q-basic/superselection theorem is exact but parent object-language, no-Hom, and readout/radiative clauses remain unsigned.",
            "next_action": "Keep retained coefficient vector active.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3468_2_next_route",
            "decision": "Next best move is a coefficient-domain owner contract or executable vector runner.",
            "reason": "The proof target is sharp, while alpha and mhat already have first numeric ceilings; missing rows need either theorem-zero or scoring machinery.",
            "next_action": "3469 should build the visible-coefficient owner contract and, if not closed, a WEP/clocks/R10 coefficient-vector runner schema.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3469-Y5-R2FR-visible-coefficient-owner-contract-or-multiarena-vector-runner.md",
            "next_script": "scripts/Y5_R2FR_3469_visible_coefficient_owner_contract_or_multiarena_vector_runner.py",
            "objective": "Write the exact parent contract that would make visible coefficient slots q-basic/superselected; if unsigned, turn the 3468 retained coefficient vector into an executable WEP/clocks/R10 schema with missing-row blockers.",
            "success_gate": "Either a parent-owned no-HiddenInvariant-to-Coeff_visible theorem is signed as an exact contract, or the retained vector has runnable schema rows for WEP, clocks, R10 and local source coupling.",
            "exclude": "GitHub action; formalization-workbench edits; public local-GR/WEP claim; cancellation-based pass; hiding dimensionless drifts inside Newton G.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validate(
    outputs: dict[str, Path],
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    morphism_rows: list[dict[str, Any]],
    vector_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    values: dict[str, float],
) -> list[dict[str, Any]]:
    stamp = now()
    local_sources_ok = all(row["exists_or_url_present"] for row in source_rows if row["source_type"] == "local")
    exact_theorem_present = any(row["theorem_id"] == "CSU3468_1_qbasic_chain_rule" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows)
    countermodel_present = any(row["theorem_id"] == "CSU3468_5_countermodel" and row["proof_status"] == "EXACT_COUNTERMODEL_CLASS" for row in theorem_rows)
    not_promoted = any(row["theorem_id"] == "CSU3468_6_verdict" and row["proof_status"] == "NOT_PARENT_DERIVED_CURRENT_CORPUS" for row in theorem_rows)
    gates_cover_targets = {row["gate_id"] for row in morphism_rows} == {
        "HSM3468_0_F2_alpha",
        "HSM3468_1_Yukawa_Higgs",
        "HSM3468_2_QCD_mass_ratio",
        "HSM3468_3_nuclear_binding",
        "HSM3468_4_readout_radiative",
    }
    vector_has_alpha_mass = all(
        any(row["coefficient_id"] == coeff and parse_float(row["current_bound"]) for row in vector_rows)
        for coeff in ("RCV3468_0_b_alpha", "RCV3468_1_b_mhat")
    )
    alpha_recomputed = values["alpha_delta"] * values["alpha_bound"]
    mass_recomputed = values["mass_delta"] * values["mass_bound"]
    envelope_ok = abs(alpha_recomputed - ETA_TIPT_BOUND) < 1e-26 and abs(mass_recomputed - ETA_TIPT_BOUND) < 1e-26
    no_cancellation_active = any(row["envelope_id"] == "NCV3468_3_no_independent_pass" and row["status"] == "NO_CANCELLATION_GUARD_ACTIVE" for row in envelope_rows)
    arena_crosswalk_present = len(arena_rows) >= 4
    local_gr_blocked = any(row["gate_id"] == "CG3468_4_local_GR_Maxwell_Newton" and row["pass"] is False for row in gate_rows)
    no_claim_rows = not any(
        str(value).lower() == "true"
        for rows in (theorem_rows, morphism_rows, vector_rows, envelope_rows, arena_rows, gate_rows)
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
        matches = list(FORMALIZATION.rglob("*3468*"))
        formalization_ok = not matches
        formalization_detail = f"formalization_exists=True; 3468_outputs_in_formalization={len(matches)}"

    rows = [
        {"validation_id": "VAL3468_0_local_sources_exist", "pass": local_sources_ok, "detail": "all local sources exist", "timestamp_utc": stamp},
        {"validation_id": "VAL3468_1_theorem_exact_but_not_promoted", "pass": exact_theorem_present and countermodel_present and not_promoted, "detail": "q-basic theorem, exact countermodel, and not-parent-derived verdict all present", "timestamp_utc": stamp},
        {"validation_id": "VAL3468_2_morphism_gates_cover_targets", "pass": gates_cover_targets, "detail": "F2, Yukawa/Higgs, QCD/mhat, nuclear binding, readout/radiative gates present", "timestamp_utc": stamp},
        {"validation_id": "VAL3468_3_vector_alpha_mass_numeric", "pass": vector_has_alpha_mass, "detail": "alpha and mhat retained coefficient rows have numeric ceilings", "timestamp_utc": stamp},
        {"validation_id": "VAL3468_4_envelope_recomputed", "pass": envelope_ok and no_cancellation_active, "detail": f"alpha={alpha_recomputed:.12e};mass={mass_recomputed:.12e};eta={ETA_TIPT_BOUND:.12e}", "timestamp_utc": stamp},
        {"validation_id": "VAL3468_5_arena_crosswalk_present", "pass": arena_crosswalk_present, "detail": "WEP, clocks, R10, local GR/Newton crosswalk rows present", "timestamp_utc": stamp},
        {"validation_id": "VAL3468_6_local_GR_claim_blocked", "pass": local_gr_blocked, "detail": "local GR/Maxwell/Newton source claim remains false", "timestamp_utc": stamp},
        {"validation_id": "VAL3468_7_no_claim_rows", "pass": no_claim_rows, "detail": "all claim_allowed and valid_for_claim flags remain false", "timestamp_utc": stamp},
        {"validation_id": "VAL3468_8_csv_parse", "pass": csv_parse_ok, "detail": ";".join(parse_counts), "timestamp_utc": stamp},
        {"validation_id": "VAL3468_9_formalization_untouched_by_3468", "pass": formalization_ok, "detail": formalization_detail, "timestamp_utc": stamp},
    ]
    rows.append(
        {
            "validation_id": "VAL3468_SUMMARY",
            "pass": all(str(row["pass"]).lower() == "true" for row in rows),
            "detail": "PASS" if all(str(row["pass"]).lower() == "true" for row in rows) else "FAIL",
            "timestamp_utc": stamp,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    morphism_rows: list[dict[str, Any]],
    vector_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    values: dict[str, float],
) -> None:
    doc = f"""# 3468 - Constant-Sector Universality Or Hidden SM Coefficient Morphism

**Current verdict:** alpha/F2 and mass/nuclear coupling are now one problem: visible coefficient ownership. If `Theta_vis` is `q`-basic or superselected parent data, then all vertical constant-sector slopes vanish by the same chain rule; current MTS has not parent-signed the no-hidden-to-SM-coefficient morphism, so the zero theorem remains conditional.

**Concrete progress:** retained coefficient vector written. The existing numeric one-channel ceilings are `|D_e_eff| <= {values['alpha_bound']:.12e}` for alpha and `|D_mhat_eff| <= {values['mass_bound']:.12e}` for mass; both stay nonclaim and cannot be combined by cancellation.

## Source Register
{md_table(source_rows)}

## Constant-Sector Theorem Attempt
{md_table(theorem_rows)}

## Hidden-To-SM Coefficient Morphism Gates
{md_table(morphism_rows)}

## Retained Coefficient Vector
{md_table(vector_rows)}

## No-Cancellation Envelope
{md_table(envelope_rows)}

## Arena Crosswalk
{md_table(arena_rows)}

## Claim Gates
{md_table(gate_rows)}

## Decision Ledger
{md_table(decision_rows)}

## Validation
{md_table(validation_rows)}

## Next Target
{md_table(next_rows)}

## Short Readout
- Clean theorem: `Theta_vis=q^*Theta_bar` or fixed superselection data implies `L_v Theta_vis=0`.
- Clean obstruction: hidden scalar morphisms into `F^2`, Yukawa/Higgs, QCD/mass-ratio, or nuclear-binding slots remain legal unless parent-forbidden.
- Practical result: alpha and mhat now sit in one retained coefficient vector with first numeric WEP ceilings.
- Still missing: `b_me`, exact nuclear binding, readout/radiative rows, and the parent no-Hom coefficient-domain proof.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register()
    values = get_bound_values()
    theorem_rows = constant_sector_theorem_attempt()
    morphism_rows = coefficient_morphism_gates()
    vector_rows = retained_coefficient_vector(values)
    envelope_rows = no_cancellation_envelope(values)
    arena_rows = arena_crosswalk()
    gate_rows = claim_gates(theorem_rows, vector_rows)
    decision_rows = decision_ledger()
    next_rows = next_target()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3468_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R2FR_3468_CONSTANT_SECTOR_THEOREM_ATTEMPT.csv",
        "morphism": OUT / "P8_Y5_R2FR_3468_HIDDEN_TO_SM_COEFFICIENT_MORPHISM_GATES.csv",
        "vector": OUT / "P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv",
        "envelope": OUT / "P8_Y5_R2FR_3468_NO_CANCELLATION_VECTOR_ENVELOPE.csv",
        "arena": OUT / "P8_Y5_R2FR_3468_ARENA_CROSSWALK.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3468_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3468_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3468_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3468_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["theorem"], theorem_rows)
    write_csv(outputs["morphism"], morphism_rows)
    write_csv(outputs["vector"], vector_rows)
    write_csv(outputs["envelope"], envelope_rows)
    write_csv(outputs["arena"], arena_rows)
    write_csv(outputs["claim_gates"], gate_rows)
    write_csv(outputs["decision"], decision_rows)
    write_csv(outputs["next"], next_rows)
    validation_rows = validate(outputs, source_rows, theorem_rows, morphism_rows, vector_rows, envelope_rows, arena_rows, gate_rows, values)
    write_csv(outputs["validation"], validation_rows)
    write_doc(source_rows, theorem_rows, morphism_rows, vector_rows, envelope_rows, arena_rows, gate_rows, decision_rows, validation_rows, next_rows, values)

    summary = next(row for row in validation_rows if row["validation_id"] == "VAL3468_SUMMARY")
    print(summary["detail"])
    print(DOC)


if __name__ == "__main__":
    main()

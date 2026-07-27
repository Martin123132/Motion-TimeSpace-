from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "3443-Y5-R2FR-source-normalization-Csrc-zero-or-measured-GM-bound-input-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SECONDS_PER_JULIAN_YEAR = 365.25 * 24 * 60 * 60

SOURCES = {
    "doc_3442": ROOT / "3442-Y5-R2FR-common-conformal-trace-coefficient-zero-or-Cassini-R10-bound-input-under-AX1090.md",
    "next_3442": OUT / "P8_Y5_R2FR_3442_NEXT_TARGET.csv",
    "ctrace_3441": OUT / "P8_Y5_R2FR_3441_TRACE_COUPLING_COEFFICIENT_DEFINITION.csv",
    "ctrace_update_3442": OUT / "P8_Y5_R2FR_3442_CTRACE_UPDATE.csv",
    "doc_1012": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
    "owner_attempt_1012": OUT / "P8_Y5_R10_1012_Y5_OWNER_THEOREM_ATTEMPT.csv",
    "sn_vector_1012": OUT / "P8_Y5_R10_1012_R11_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
    "constant_gm_1012": OUT / "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv",
    "claim_gate_1012": OUT / "P8_Y5_R10_1012_CLAIM_GATE.csv",
    "decision_1012": OUT / "P8_Y5_R10_1012_DECISION_LEDGER.csv",
    "doc_1013": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "flux_attempt_1013": OUT / "P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv",
    "gm_obstruction_1013": OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "claim_gate_1013": OUT / "P8_Y5_R10_1013_CLAIM_GATE.csv",
    "doc_1015": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
    "same_object_1015": OUT / "P8_Y5_R10_1015_DE_RHAM_SAME_OBJECT_LEMMA.csv",
    "req_bound_1015": OUT / "P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv",
    "claim_gate_1015": OUT / "P8_Y5_R10_1015_CLAIM_GATE.csv",
    "source_norm_stack": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
    "zero_targets": OUT / "P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv",
    "numeric_template": OUT / "P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv",
    "newton_contract_868": OUT / "P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv",
    "ppn_gdot_wep_map_708": OUT / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv",
    "mass_flux_contract": OUT / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "local_bounds": LOCAL_BOUNDS,
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3443_SOURCE_REGISTER.csv",
    "csrc_zero_theorem_attempt": OUT / "P8_Y5_R2FR_3443_CSRC_ZERO_THEOREM_ATTEMPT.csv",
    "source_owner_signature_audit": OUT / "P8_Y5_R2FR_3443_SOURCE_OWNER_SIGNATURE_AUDIT.csv",
    "csrc_decomposition": OUT / "P8_Y5_R2FR_3443_CSRC_DECOMPOSITION.csv",
    "measured_gm_bound_input": OUT / "P8_Y5_R2FR_3443_MEASURED_GM_BOUND_INPUT.csv",
    "flux_obstruction_link": OUT / "P8_Y5_R2FR_3443_FLUX_OBSTRUCTION_LINK.csv",
    "ctrace_update": OUT / "P8_Y5_R2FR_3443_CTRACE_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3443_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3443_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3443_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3443_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3443_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    return {}


def parse_float(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3442": "handoff selecting C_src after C_conf",
        "next_3442": "machine-readable 3443 target",
        "ctrace_3441": "C_src component definition",
        "ctrace_update_3442": "C_trace update after C_conf",
        "doc_1012": "measured-GM/source-normalization owner checkpoint",
        "owner_attempt_1012": "Y5 owner theorem attempt clauses",
        "sn_vector_1012": "R11/source-normalization coefficient vector",
        "constant_gm_1012": "constant-GM residual rows",
        "claim_gate_1012": "1012 claim gates",
        "decision_1012": "1012 next-root decision",
        "doc_1013": "Pi_M J_H flux closure / obstruction checkpoint",
        "flux_attempt_1013": "flux closure theorem attempt",
        "gm_obstruction_1013": "exact measured-GM obstruction vector",
        "claim_gate_1013": "1013 claim gates",
        "doc_1015": "topological-Hilbert equality checkpoint",
        "same_object_1015": "de Rham same-object lemma",
        "req_bound_1015": "R_eq/I_commutator bound input rows",
        "claim_gate_1015": "1015 claim gates",
        "source_norm_stack": "source-normalization theorem stack",
        "zero_targets": "derived-zero target map",
        "numeric_template": "source-normalization numeric input template",
        "newton_contract_868": "Newton source-normalization contract",
        "ppn_gdot_wep_map_708": "PPN/Gdot/WEP observable map",
        "mass_flux_contract": "mass flux/projector calibration contract",
        "source_measure_flux": "source measure/M_eff flux theorem",
        "local_bounds": "R9 Gdot plus R1/R3/R10 anchors",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def csrc_zero_theorem_attempt() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CSZ3443_0_define",
            "claim_piece": "source-normalization trace coefficient",
            "derivation": "mu_obs := G_eff M_eff + mu_extra; C_src := partial_X ln(mu_obs) in the selected trace branch, equivalently partial_X ln(G_eff M_eff) plus retained mu_extra envelope when mu_extra is small",
            "result": "DEFINITION_SHARP",
            "current_status": "not_a_claim",
            "gap": "X_T normalization, same-frame G_eff/kappa, and M_eff source measure must be parent-owned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSZ3443_1_zero_if_owner_signed",
            "claim_piece": "C_src zero theorem",
            "derivation": "If kappa/G_eff is constant and universal, Pi_M is parent-owned before readout, d(Pi_M J_H)=0 in the compact exterior, worldtube source equals M_eff, mu_extra=0 or bounded, and measured-GM calibration is parent-fixed, then partial_X ln(mu_obs)=0.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "current_status": "CONDITIONAL_ONLY_SOURCE_1012_1013_1015",
            "gap": "same-frame, Pi_M origin, flux closure, worldtube glue, extra-channel silence and calibration are not parent-signed together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSZ3443_2_flux_obstruction_identity",
            "claim_piece": "why M_eff cannot be assumed constant",
            "derivation": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H; the measured-GM obstruction is -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent plus worldtube, equality, boundary and calibration tails.",
            "result": "EXACT_OBSTRUCTION_OBJECT",
            "current_status": "obstruction_retained",
            "gap": "obstruction rows are unfilled and not theorem-zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSZ3443_3_Gdot_bound_route",
            "claim_piece": "time drift bound",
            "derivation": "R9 bounds d_t ln(mu_obs) only after mapping C_src through d_t X_T and separating calibration, frame and source-mass terms",
            "result": "Gdot_TRANSLATION_NONCLAIM",
            "current_status": "bound_anchor_available_inputs_missing",
            "gap": "D_t X_T, stationarity theorem or time-profile row is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CSZ3443_4_verdict",
            "claim_piece": "current C_src zero",
            "derivation": "C_src is exactly the Newton-source bridge coefficient, but current files give only conditional owner theorems and unfilled obstruction rows.",
            "result": "ZERO_THEOREM_NOT_PROMOTED_BOUND_ROWS_REQUIRED",
            "current_status": "nonclaim",
            "gap": "derive Pi_M J_H flux/source selector or fill measured-GM obstruction components",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_owner_signature_audit() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "SOA3443_0_same_frame",
            "required_signature": "matter, clocks, source current and orbital readout use one observed coframe",
            "source_status": "Y5O1012_0_CONDITIONAL_NOT_PARENT_DERIVED",
            "if_signed": "source current is not a hidden frame/readout artifact",
            "if_unsigned": "C_src can move between matter frame, clocks, orbital GM and source current",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SOA3443_1_constant_universal_coupling",
            "required_signature": "G_eff/kappa is constant, universal, and source/range/species/frame blind",
            "source_status": "Y5O1012_1_NOT_PARENT_DERIVED",
            "if_signed": "partial_X ln G_eff and species/range source weights vanish",
            "if_unsigned": "G_eff/kappa derivative is a live C_src component",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SOA3443_2_parent_PiM",
            "required_signature": "Pi_M is parent-owned before readout as the mass/source projector",
            "source_status": "Y5O1012_2_NOT_PARENT_DERIVED",
            "if_signed": "no post-fit measured-GM mask can select the source",
            "if_unsigned": "projector commutator and calibration residuals remain live",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SOA3443_3_flux_closure",
            "required_signature": "d(Pi_M J_H)=0 or exact obstruction vector is theorem-zero/source-bounded",
            "source_status": "Y5O1012_3_EXACT_OBSTRUCTION_NOT_ZERO;PFC1013_8_FAIL_CURRENT_CLAIM",
            "if_signed": "M_eff is radially/time constant across compact exterior annuli",
            "if_unsigned": "dln_Meff_dt, radial hair and R10/PPN source tails remain live",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SOA3443_4_worldtube_glue",
            "required_signature": "worldtube Hilbert source equals exterior parent charge before orbital fitting",
            "source_status": "Y5O1012_4_NOT_DERIVED_CORE_MISSING_PIECE",
            "if_signed": "closed charge is the observed source, not merely a conserved wrong object",
            "if_unsigned": "measured GM substitution is circular",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SOA3443_5_verdict",
            "required_signature": "SOA3443_0 through SOA3443_4 plus mu_extra silence all parent-signed",
            "source_status": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "if_signed": "C_src branch closes",
            "if_unsigned": "finite measured-GM/Gdot/source-flux bound rows are mandatory",
            "valid_for_claim": False,
        },
    ]


def csrc_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "CSD3443_0_total",
            "symbol": "C_src",
            "definition": "partial_X ln(mu_obs) for mu_obs=G_eff M_eff+mu_extra in one fixed trace branch",
            "formula_or_bound": "|C_src| <= |C_G|+|C_M|+|C_species|+|C_radial_range|+|C_calibration|+|C_flux_tail|",
            "required_input": "all components theorem-zero or source-backed numeric in same frame",
            "current_value": "MISSING_COMPONENT_VALUES",
            "status": "ABSOLUTE_ENVELOPE_DEFINED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CSD3443_1_CG",
            "symbol": "C_G",
            "definition": "partial_X ln G_eff or partial_X ln kappa_eff",
            "formula_or_bound": "zero by constant universal coupling, or source row for dln_Geff/dX_T",
            "required_input": "G_eff/kappa owner theorem or derivative coefficient with units/source path",
            "current_value": "MISSING_GEFF_KAPPA_DERIVATIVE",
            "status": "MISSING_COUPLING_OWNER_OR_NUMERIC_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CSD3443_2_CM",
            "symbol": "C_M",
            "definition": "partial_X ln M_eff from Hilbert mass-flux/source-measure variation",
            "formula_or_bound": "zero by d(Pi_M J_H)=0 plus worldtube glue, or bound from measured-GM obstruction vector",
            "required_input": "Pi_M origin, flux closure, M_H_ref, worldtube selector and obstruction components",
            "current_value": "MISSING_MEFF_FLUX_DERIVATIVE",
            "status": "MISSING_FLUX_CLOSURE_OR_OBSTRUCTION_SCORE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CSD3443_3_species",
            "symbol": "C_species",
            "definition": "species/source-only weight in active gravitational source",
            "formula_or_bound": "zero by selector-blind source action, or WEP/source-charge bound row",
            "required_input": "no species source charge theorem or material/source response vector",
            "current_value": "MISSING_SPECIES_SOURCE_WEIGHT",
            "status": "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_WEP_BOUND_INPUT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CSD3443_4_radial_range",
            "symbol": "C_radial_range",
            "definition": "radial/range dependence of mu_obs, including finite-range bulk/source hair",
            "formula_or_bound": "zero by compact exterior no-hair/source identity, or R10/radial profile bound",
            "required_input": "radial profile, lambda_T, alpha(lambda), R10 curve and no-absorption guard",
            "current_value": "MISSING_RADIAL_RANGE_PROFILE",
            "status": "MISSING_RADIAL_RANGE_ZERO_OR_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CSD3443_5_calibration",
            "symbol": "C_calibration",
            "definition": "absolute calibration offset hidden in measured GM, beta/source readout, frame split or reference choice",
            "formula_or_bound": "zero by parent fixed calibration/reference lock, or absolute calibration residual row",
            "required_input": "fixed calibration theorem, reference lock, no orbital-GM denominator laundering",
            "current_value": "MISSING_CALIBRATION_OFFSET",
            "status": "MISSING_FIXED_CALIBRATION_THEOREM_OR_RESIDUAL_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CSD3443_6_flux_tail",
            "symbol": "C_flux_tail",
            "definition": "R_eq, I_commutator, B_zero_flux, Delta_extra_vector, projector stress and anomaly tails",
            "formula_or_bound": "absolute sum of 1013/1015 obstruction rows normalized by M_H_ref",
            "required_input": "source-backed obstruction values or theorem-zero certificates",
            "current_value": "MISSING_OBSTRUCTION_VECTOR_VALUES",
            "status": "MISSING_R_EQ_ICOMMUTATOR_BZERO_EXTRA_VECTOR_VALUES",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def measured_gm_bound_input() -> list[dict[str, Any]]:
    gdot = local_bound("R9_Gdot")
    gdot_bound_yr = parse_float(gdot.get("upper_bound"))
    gdot_bound_s = gdot_bound_yr / SECONDS_PER_JULIAN_YEAR if gdot_bound_yr is not None else None
    return [
        {
            "bound_input_id": "MGB3443_0_Gdot_anchor",
            "observable": "Gdot_over_G",
            "bound_source": "local_bound_claims.csv:R9_Gdot",
            "numeric_bound": gdot_bound_yr if gdot_bound_yr is not None else "MISSING_R9_GDOT_BOUND",
            "units": "yr^-1",
            "reference": gdot.get("reference_path_or_url", "MISSING"),
            "status": "BOUND_ANCHOR_PRESENT" if gdot_bound_yr is not None else "BOUND_ANCHOR_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "MGB3443_1_Gdot_seconds",
            "observable": "Gdot_over_G",
            "bound_source": "local_bound_claims.csv:R9_Gdot",
            "numeric_bound": f"{gdot_bound_s:.12e}" if gdot_bound_s is not None else "MISSING_R9_GDOT_BOUND",
            "units": "s^-1",
            "reference": gdot.get("reference_path_or_url", "MISSING"),
            "status": "UNIT_TRANSLATION_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "MGB3443_2_Csrc_time_map",
            "observable": "C_src via time drift",
            "bound_source": "P8_Y5_R2FR_3443_CSRC_DECOMPOSITION.csv:CSD3443_0_total",
            "numeric_bound": "C_src * D_t X_T bounded by R9 only if D_t X_T and calibration split are sourced",
            "units": "depends_on_X_T_units",
            "reference": "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv:PGW708_3_R9_Gdot",
            "status": "MTS_MAPPING_MISSING_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "MGB3443_3_measured_GM_no_absorption",
            "observable": "mu_obs=G_eff M_eff+mu_extra",
            "bound_source": "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv",
            "numeric_bound": "no numeric C_src bound until G_eff, M_eff, mu_extra and no-absorption rows are filled",
            "units": "dimensionless_or_profile_dependent",
            "reference": "P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def flux_obstruction_link() -> list[dict[str, Any]]:
    return [
        {
            "link_id": "FOL3443_0_exact_obstruction",
            "source_row": "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv:OBS1013_0..7",
            "quantity": "Omega_GM := -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent + R_eq + B_zero_flux + Delta_cal + Delta_PPN",
            "role_in_Csrc": "C_M and C_flux_tail are zero only if Omega_GM is zero or source-bounded",
            "status": "OBSTRUCTION_DEFINED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "link_id": "FOL3443_1_same_object_route",
            "source_row": "P8_Y5_R10_1015_DE_RHAM_SAME_OBJECT_LEMMA.csv:SOL1015_0..6",
            "quantity": "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "role_in_Csrc": "would convert conserved topology into the observed Hilbert source only if same-worldtube/source-measure/boundary-zero clauses are signed",
            "status": "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "link_id": "FOL3443_2_projector_commutator",
            "source_row": "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv:OBS1013_1_PiM_commutator",
            "quantity": "[d,Pi_M]J_H",
            "role_in_Csrc": "next best single obstruction because it directly creates radial/time/source-normalization leakage",
            "status": "NEXT_DERIVATION_TARGET",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def ctrace_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "CTU3443_0_Csrc_status",
            "prior_component": "CT3441_4_C_src",
            "before": "MISSING_SOURCE_NORMALIZATION_COEFFICIENT_OR_OWNER_THEOREM",
            "after": "EXACT_CONDITIONAL_ZERO_OR_MEASURED_GM_GDOT_NONCLAIM_BOUND_INPUT",
            "effect_on_C_trace": "C_trace remains finite/nonclaim until C_src is parent-signed zero or all measured-GM obstruction components are source-bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "CTU3443_1_Ctrace_envelope",
            "prior_component": "CT3441_0_C_trace",
            "before": "|C_trace| <= |C_XR|+|C_XT|+|C_conf_bound|+|C_src|+|C_bdy|",
            "after": "|C_trace| <= |C_XR|+|C_XT|+|C_conf_bound|+|C_src_bound|+|C_bdy| with C_src_bound currently nonclaim",
            "effect_on_C_trace": "source-normalization is no longer a vague gap; it is a measured-GM obstruction vector plus Gdot/R10/WEP interfaces",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3443_0_sources",
            "claim": "all 3443 sources exist",
            "gate_pass": all(path.exists() for path in SOURCES.values()),
            "reason": "source register path check",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3443_1_Csrc_zero",
            "claim": "C_src=0 is parent-signed",
            "gate_pass": False,
            "reason": "source owner, Pi_M origin, flux closure, worldtube glue, mu_extra silence and calibration are not parent-signed together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3443_2_Gdot_bound",
            "claim": "R9 Gdot produces a claim-ready C_src bound",
            "gate_pass": False,
            "reason": "R9 bounds d_t ln(mu_obs); C_src needs D_t X_T, same-frame split and calibration/no-absorption rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3443_3_Newton_source",
            "claim": "Newtonian measured-GM/source side is derived",
            "gate_pass": False,
            "reason": "mu_obs=G_eff M_eff + mu_extra has a conditional owner theorem and explicit obstruction rows, not a proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3443_4_local_GR",
            "claim": "local GR/Newton reduction can be promoted",
            "gate_pass": False,
            "reason": "C_src is only one trace component and remains nonclaim; EH/PPN/residual gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3443_0_Csrc_object",
            "decision": "Treat C_src as partial_X ln(mu_obs), not as a loose coupling word.",
            "because": "Newton's source side depends on the observed product G_eff M_eff plus retained extra source channels",
            "next_action": "derive or bound each component under an absolute no-cancellation envelope",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3443_1_Gdot_status",
            "decision": "Use Gdot/G as a nonclaim time-drift anchor only.",
            "because": "LLR bounds d_t ln(mu_obs), but it does not bound C_src without D_t X_T and calibration split",
            "next_action": "do not divide by an invented time-profile; source D_t X_T or derive stationarity",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3443_2_next_root",
            "decision": "Attack the Pi_M J_H flux obstruction next.",
            "because": "source ownership cannot close while [d,Pi_M]J_H, Pi_M dJ_extra, A_parent and worldtube glue remain live",
            "next_action": "derive [d,Pi_M]J_H=0 from fixed parent chain map or stage I_commutator bound input",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3444-Y5-R2FR-PiM-JH-commutator-zero-or-Icommutator-bound-input-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3444_PiM_JH_commutator_zero_or_Icommutator_bound_input.py",
            "objective": "attack the C_src root obstruction [d,Pi_M]J_H: derive zero from a fixed parent chain-map/source projector, or stage a nonclaim I_commutator bound input linked to measured-GM, PPN, R10 and source-normalization rows",
            "success_condition": "[d,Pi_M]J_H is either parent-signed zero in the selected trace/source branch or represented by schema-valid nonclaim I_commutator rows with units/source paths/no-cancellation rules",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3443_0_Csrc",
            "branch_id": "OC3441_trace_mass_source",
            "zero_claim": False,
            "gdot_numeric_anchor": True,
            "mts_score": False,
            "result": "NOT_SCORED",
            "why": "C_src zero theorem unsigned and Gdot anchor lacks D_t X_T/calibration/source split",
            "valid_for_claim": False,
        }
    ]


def local_bound_row_ids() -> set[str]:
    return {row.get("row_id", "") for row in read_csv(LOCAL_BOUNDS)}


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1 for checked_path in FORMALIZATION.rglob("*") if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if row.get("valid_for_claim") is True or str(row.get("valid_for_claim", "")).lower() == "true":
                nonclaim_ok = False
            if row.get("claim_allowed") is True or str(row.get("claim_allowed", "")).lower() == "true":
                nonclaim_ok = False

    bound_ids = local_bound_row_ids()
    validations = [
        {
            "check_id": "VAL3443_0_sources_exist",
            "condition": "all cited 3443 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3443_1_zero_conditional",
            "condition": "C_src zero theorem is present but not promoted",
            "passed": any(row["theorem_id"] == "CSZ3443_4_verdict" and row["result"] == "ZERO_THEOREM_NOT_PROMOTED_BOUND_ROWS_REQUIRED" for row in rows_by_name["csrc_zero_theorem_attempt"]),
            "detail": "source-owner theorem retained as conditional",
        },
        {
            "check_id": "VAL3443_2_signature_unsigned",
            "condition": "source owner signature remains unsigned",
            "passed": any(row["clause_id"] == "SOA3443_5_verdict" and row["source_status"] == "NOT_PARENT_SIGNED_CURRENT_CORPUS" for row in rows_by_name["source_owner_signature_audit"]),
            "detail": "1012/1013 stricter verdict preserved",
        },
        {
            "check_id": "VAL3443_3_decomposition_complete",
            "condition": "C_src decomposition includes G, M, species, radial/range, calibration and flux-tail components",
            "passed": {"CSD3443_1_CG", "CSD3443_2_CM", "CSD3443_3_species", "CSD3443_4_radial_range", "CSD3443_5_calibration", "CSD3443_6_flux_tail"}.issubset(
                {row["component_id"] for row in rows_by_name["csrc_decomposition"]}
            ),
            "detail": "six retained component classes present",
        },
        {
            "check_id": "VAL3443_4_gdot_anchor",
            "condition": "R9 Gdot anchor is imported and translated as nonclaim",
            "passed": any(row["bound_input_id"] == "MGB3443_0_Gdot_anchor" and row["status"] == "BOUND_ANCHOR_PRESENT" for row in rows_by_name["measured_gm_bound_input"])
            and any(row["bound_input_id"] == "MGB3443_2_Csrc_time_map" and row["status"] == "MTS_MAPPING_MISSING_NONCLAIM" for row in rows_by_name["measured_gm_bound_input"]),
            "detail": "R9 anchor present; C_src map blocked",
        },
        {
            "check_id": "VAL3443_5_flux_obstruction_link",
            "condition": "C_src is linked to exact measured-GM obstruction vector",
            "passed": any(row["link_id"] == "FOL3443_0_exact_obstruction" and row["status"] == "OBSTRUCTION_DEFINED_VALUES_MISSING" for row in rows_by_name["flux_obstruction_link"]),
            "detail": "1013 obstruction object retained",
        },
        {
            "check_id": "VAL3443_6_bound_anchors",
            "condition": "R1/R3/R9/R10 bound anchors are present",
            "passed": {"R1_WEP_source_charge", "R3_gamma", "R9_Gdot", "R10_fifth_force"}.issubset(bound_ids),
            "detail": "local_bound_claims.csv anchors checked",
        },
        {
            "check_id": "VAL3443_7_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3443_8_next_target_commutator",
            "condition": "next target attacks Pi_M commutator",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3444-Y5-R2FR-PiM-JH-commutator"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3443_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3443_10_overall",
            "condition": "3443 C_src checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    gdot_row = next(row for row in rows_by_name["measured_gm_bound_input"] if row["bound_input_id"] == "MGB3443_0_Gdot_anchor")
    text = f"""# 3443 - Source-Normalization Csrc Zero or Measured-GM Bound Input

## Summary
- This checkpoint attacks `C_src`, the source-normalization part of the 3441 trace channel.
- The clean object is `mu_obs = G_eff M_eff + mu_extra`, with `C_src := partial_X ln(mu_obs)` in one fixed branch.
- The zero route is exact but conditional: constant universal `G_eff/kappa`, parent-owned `Pi_M`, compact-exterior flux closure, source worldtube glue, no extra source channels and no measured-GM absorption would give `C_src=0`.
- Current MTS does not parent-sign those clauses together, so no Newton, measured-`GM`, source-coupling, or local-GR pass is claimed.
- The finite route is now explicit: R9 gives `|Gdot/G| <= {gdot_row["numeric_bound"]} {gdot_row["units"]}`, but this only bounds `C_src D_t X_T` after the MTS time/profile and calibration split are supplied.

## Source Register
{md_table(rows_by_name["source_register"])}

## Csrc Zero Theorem Attempt
{md_table(rows_by_name["csrc_zero_theorem_attempt"])}

## Source Owner Signature Audit
{md_table(rows_by_name["source_owner_signature_audit"])}

## Csrc Decomposition
{md_table(rows_by_name["csrc_decomposition"])}

## Measured-GM Bound Input
{md_table(rows_by_name["measured_gm_bound_input"])}

## Flux Obstruction Link
{md_table(rows_by_name["flux_obstruction_link"])}

## Ctrace Update
{md_table(rows_by_name["ctrace_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
`C_src` is the Newton-source bridge in plain clothes. The project does not yet own it, but it is now pinned to the exact measured-`GM` obstruction vector. The next honest forward move is the commutator `[d,Pi_M]J_H`: either prove the projector is a fixed parent chain map, or bound the commutator instead of hiding it inside measured `GM`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "csrc_zero_theorem_attempt": csrc_zero_theorem_attempt(),
        "source_owner_signature_audit": source_owner_signature_audit(),
        "csrc_decomposition": csrc_decomposition(),
        "measured_gm_bound_input": measured_gm_bound_input(),
        "flux_obstruction_link": flux_obstruction_link(),
        "ctrace_update": ctrace_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3443 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

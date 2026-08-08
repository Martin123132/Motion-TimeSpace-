from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3503-Y5-R2FR-observed-Hodge-Maxwell-owner-and-total-Hilbert-current-closure-or-EM-bound.md"
BOUND_VECTOR = OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3503": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3502": {
        "path": ROOT / "3502-Y5-R2FR-dressed-Hilbert-source-measure-Poynting-flux-closure-or-radial-time-bound.md",
        "role": "3502 handoff",
    },
    "next_3502": {
        "path": OUT / "P8_Y5_R2FR_3502_NEXT_TARGET.csv",
        "role": "3502 selected next target",
    },
    "flux_theorem_3502": {
        "path": OUT / "P8_Y5_R2FR_3502_DRESSED_SOURCE_FLUX_CLOSURE_THEOREM.csv",
        "role": "3502 dressed source flux closure theorem",
    },
    "em_flux_vector_3502": {
        "path": OUT / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
        "role": "3502 EM/Poynting source-flux vector",
    },
    "maxwell_poynting_ledger": {
        "path": OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
        "role": "Maxwell stress and Poynting ledger",
    },
    "em_alpha_charge_audit": {
        "path": OUT / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv",
        "role": "EM alpha and charge owner audit",
    },
    "em_owner_package": {
        "path": OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
        "role": "EM owner package audit",
    },
    "maxwell_descent": {
        "path": OUT / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "role": "Maxwell descent attempt",
    },
    "maxwell_kinetic_inheritance": {
        "path": OUT / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "role": "Maxwell kinetic inheritance gate",
    },
    "charge_extraction_spine": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
        "role": "parent charge extraction spine",
    },
    "source_current_closure": {
        "path": OUT / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "role": "source current closure theorem attempt",
    },
    "hilbert_worldtube_glue": {
        "path": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "role": "Hilbert worldtube glue theorem attempt",
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


def owner_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "OHM3503_0_same_observed_Hodge",
            "claim_piece": "observed Hodge/coframe owner",
            "statement": "If the EM Hodge star is exactly the observed gravitational Hodge star, *_EM=*_obs[e_obs(q)], then Maxwell stress, light cones and Poynting flow use the same geometry as the local-GR source measure.",
            "mathematical_form": "S_EM[A,e_obs]=-(4 mu0)^-1 integral F wedge *_obs F; T_EM := 2/sqrt(-g_obs) delta S_EM/delta g_obs",
            "derivation": "Varying this action with respect to e_obs/g_obs produces the EM Hilbert stress tensor, and T_EM^{0i}=S_Poynting^i/c^2 in local inertial readout.",
            "result": "EXACT_CONDITIONAL_IF_OBSERVED_HODGE_PARENT_OWNED",
            "remaining_gap": "MTS has not yet derived *_obs as the unique EM Hodge/flow rule from q/e_obs rather than imported Maxwell structure",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "OHM3503_1_no_independent_F2",
            "claim_piece": "unique Maxwell kinetic owner",
            "statement": "A parent-owned Maxwell stress needs no independent lambda(X) F^2, w_EM F^2, or hidden gauge-kinetic coefficient outside the parent curvature norm.",
            "mathematical_form": "Allowed[S_vis] excludes Delta S=-1/4 integral sqrt(-g_obs) lambda_X(Phi) F^2 and independent w_EM S_EM",
            "derivation": "Otherwise Poynting source strength and EM binding energy can be rescaled independently of the local gravitational source charge.",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "remaining_gap": "operator-domain exhaustion or parent curvature-norm inheritance must forbid independent F2",
            "source_path": str(SOURCES["maxwell_kinetic_inheritance"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "OHM3503_2_charge_current_owner",
            "claim_piece": "charge/current normalization",
            "statement": "A_mu, J^mu, the Maxwell kinetic coefficient and alpha_EM must share one parent convention; gauge rescaling cannot be left as a hidden source-coupling knob.",
            "mathematical_form": "A -> lambda A, J -> J/lambda leaves A.J form-invariant but moves physical normalization unless charge lattice/current owner fixes lambda",
            "derivation": "The Poynting source strength and charged matter Lorentz force are only comparable after the charge/current normalization is parent-owned.",
            "result": "PARENT_CHARGE_SPINE_EXISTS_VALUES_MISSING",
            "remaining_gap": "charge extraction, fixed reference, source denominator and residual charge silence still need rows with values or theorem-zero",
            "source_path": str(SOURCES["charge_extraction_spine"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "OHM3503_3_total_Hilbert_current",
            "claim_piece": "matter plus EM total source current",
            "statement": "Matter-EM Lorentz exchange cancels only in the total Hilbert current, not in matter alone; the source current for M_H must be J_H_total.",
            "mathematical_form": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda; nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda; nabla_mu T_total^{mu nu}=0",
            "derivation": "This is the exact stress-exchange identity: internal EM work is bookkeeping inside T_total, while external/radiative flux remains a boundary coefficient.",
            "result": "CONDITIONAL_TOTAL_CURRENT_CLOSURE",
            "remaining_gap": "charged matter coupling, EM current owner and observed Hodge owner must be the same parent structure",
            "source_path": str(SOURCES["maxwell_poynting_ledger"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "OHM3503_4_projected_total_current_closure",
            "claim_piece": "d(Pi_M J_H_total)=0 stationary exterior",
            "statement": "If J_H_total is closed in the stationary source-free exterior and Pi_M is parent-natural, then the projected source charge has no radial/time drift.",
            "mathematical_form": "d(Pi_M J_H_total)=Pi_M dJ_H_total+[d,Pi_M]J_H_total=0",
            "derivation": "Use source-free total Hilbert current closure plus projector naturality. This is the common gate behind D_r M_H=0 and D_t M_H=0.",
            "result": "CONDITIONAL_ZERO_CHAIN_NOT_FULLY_SIGNED",
            "remaining_gap": "metric projector stress, radiative flux, nonEH source charge, frame/domain leakage and reference terms remain active",
            "source_path": str(SOURCES["source_current_closure"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "OHM3503_5_verdict",
            "claim_piece": "EM source owner package",
            "statement": "3503 does not promote EM/local-GR; it converts the Poynting intuition into a four-clause parent-owner contract plus a bound vector.",
            "mathematical_form": "*_EM=*_obs(q), no independent F2, fixed charge/current normalization, d(Pi_M J_H_total)=0",
            "derivation": "All four clauses are necessary together. Missing any one leaves an explicit coefficient rather than a silent Newton source.",
            "result": "BOUND_VECTOR_REQUIRED",
            "remaining_gap": "observed Hodge/flow rule is the best next single derivation target",
            "source_path": str(SOURCES["flux_theorem_3502"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def current_closure_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "THC3503_0_Hodge_q_eobs",
            "gate": "observed Hodge/coframe is q/e_obs-owned",
            "required_identity": "*_EM = *_obs[e_obs(q)] and delta_v *_EM=0 for vertical v in ker(Dq)",
            "current_status": "CONDITIONAL_STANDARD_FORM_NOT_PARENT_DERIVED",
            "failure_mode": "Delta_Hodge_EM",
            "blocks": "Maxwell stress source; Poynting flow; light-cone/local-GR compatibility",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "THC3503_1_AQ_projection",
            "gate": "observed EM connection is parent-projected",
            "required_identity": "A_parent=A_Q T_Q + A_perp with A_Q selected before readout",
            "current_status": "TEMPLATE_ONLY_NOT_SIGNED",
            "failure_mode": "Delta_AQ_projection",
            "blocks": "Maxwell descent; charge/current owner",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "THC3503_2_unique_F2",
            "gate": "no independent Maxwell kinetic multiplier",
            "required_identity": "Allowed[S_vis] contains only the parent curvature norm for observed F_Q^2",
            "current_status": "FAILED_CURRENT_CORPUS_LEGAL_COUNTERTERM",
            "failure_mode": "w_EM;C_XF2",
            "blocks": "alpha owner; EM stress normalization; Poynting source strength",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "THC3503_3_charge_current",
            "gate": "charge/current normalization fixed",
            "required_identity": "J_Q is the Noether/Ward current of the same T_Q owner and charges are representation data",
            "current_status": "PARENT_CHARGE_SPINE_EXISTS_VALUES_MISSING",
            "failure_mode": "C_JQ;Delta_charge_norm",
            "blocks": "Lorentz readout; EM stress scale; source-side WEP",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "THC3503_4_total_current",
            "gate": "matter plus EM total Hilbert current closes",
            "required_identity": "dJ_H_total=0 after matter-EM exchange cancellation in source-free stationary exterior",
            "current_status": "CONDITIONAL_TOTAL_CURRENT_CLOSURE",
            "failure_mode": "Delta_J_total",
            "blocks": "D_r M_H; D_t M_H; source normalization",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "THC3503_5_PiM_projection",
            "gate": "projected total current closes",
            "required_identity": "d(Pi_M J_H_total)=0 with [d,Pi_M]J_H_total=0",
            "current_status": "PROJECTOR_GAMMA_PART_CANDIDATE_METRIC_STRESS_OPEN",
            "failure_mode": "Delta_PiM_metric;Delta_PiM_comm",
            "blocks": "radial GM hair; PPN/R11 source stress",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "THC3503_6_stationary_flux",
            "gate": "no radiative/background Poynting leakage",
            "required_identity": "integral_boundary S_Poynting dot n dA=0 or explicitly bounded over the local window",
            "current_status": "RETAINED_FLUX_COEFFICIENT_REQUIRED",
            "failure_mode": "Phi_EM_rad",
            "blocks": "D_t M_H; local Gdot silence",
            "valid_for_claim": "False",
        },
    ]


def bound_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "EMB3503_0_Delta_Hodge_EM",
            "coefficient": "Delta_Hodge_EM",
            "meaning": "EM Hodge/constitutive flow rule differs from observed gravitational Hodge/coframe",
            "formula": "*_EM - *_obs[e_obs(q)] or chi_EM - chi_obs",
            "units": "dimensionless_or_tensor",
            "zero_route": "derive observed Hodge/flow rule from q/e_obs and no independent constitutive tensor",
            "if_nonzero_maps_to": "Maxwell_limit;light_cone;Poynting_flow;clock;PPN",
            "bound_source_needed": "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "bound_id": "EMB3503_1_w_EM",
            "coefficient": "w_EM",
            "meaning": "independent multiplier of the observed Maxwell action/stress",
            "formula": "S_EM -> w_EM S_EM; T_EM -> w_EM T_EM",
            "units": "dimensionless",
            "zero_route": "unique Maxwell curvature norm plus alpha/charge-current owner",
            "if_nonzero_maps_to": "EM_binding;WEP;clock;source_normalization",
            "bound_source_needed": "P8_EM_action_normalization_multiplier_bound.csv",
            "current_status": "RETAINED_NORMALIZATION_COEFFICIENT",
            "source_path": str(SOURCES["em_alpha_charge_audit"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "bound_id": "EMB3503_2_C_XF2",
            "coefficient": "C_XF2",
            "meaning": "hidden/motion/time field couples directly to F^2 or F*F",
            "formula": "Delta S ~ integral sqrt(-g) f_X(Phi) F_mn F^mn",
            "units": "model_dependent",
            "zero_route": "operator-domain exhaustion forbids hidden-visible EM coefficient morphisms",
            "if_nonzero_maps_to": "alpha_EM;clock;WEP;R10;PPN",
            "bound_source_needed": "P8_EM_nonminimal_XF2_bound_vector.csv",
            "current_status": "RETAINED_OPERATOR_COEFFICIENT",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "bound_id": "EMB3503_3_C_JQ",
            "coefficient": "C_JQ",
            "meaning": "charge/current normalization not fixed by the same parent owner as A_Q and F_Q^2",
            "formula": "A -> lambda A and J -> J/lambda normalization ambiguity",
            "units": "dimensionless",
            "zero_route": "T_Q owner, representation weights, current normalization and alpha readout fixed together",
            "if_nonzero_maps_to": "Lorentz_force;source_charge;WEP;EM_stress_scale",
            "bound_source_needed": "P8_EM_charge_current_normalization_bound.csv",
            "current_status": "PARENT_CHARGE_VALUES_MISSING",
            "source_path": str(SOURCES["charge_extraction_spine"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "bound_id": "EMB3503_4_Phi_EM_rad",
            "coefficient": "Phi_EM_rad/(G_ref M_H)",
            "meaning": "net radiative/background EM energy flux through the local boundary",
            "formula": "Phi_EM_rad = integral_boundary S_Poynting dot n dA",
            "units": "time^-1_or_dimensionless_window",
            "zero_route": "stationary isolated local branch with no external/background Poynting leakage",
            "if_nonzero_maps_to": "Gdot_over_G;clock_drift;time_MH_hair",
            "bound_source_needed": "P8_EM_Poynting_flux_bound.csv",
            "current_status": "RETAINED_FLUX_COEFFICIENT",
            "source_path": str(SOURCES["em_flux_vector_3502"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "bound_id": "EMB3503_5_C_EM_readout",
            "coefficient": "C_EM_readout",
            "meaning": "effective readout, loop, clock or spectroscopy map regenerates EM coefficient dependence",
            "formula": "S_eff or readout map contains f_X F^2, alpha_X, or EM binding response",
            "units": "model_dependent",
            "zero_route": "radiative/readout closure preserves visible pullback and unique EM owner",
            "if_nonzero_maps_to": "clock;WEP;alpha_EM;binding_response",
            "bound_source_needed": "P8_EM_readout_radiative_bound_vector.csv",
            "current_status": "RETAINED_EFFECTIVE_COEFFICIENT",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "bound_id": "EMB3503_6_Delta_J_total",
            "coefficient": "Delta_J_total",
            "meaning": "total Hilbert current does not close after matter-EM exchange and extra-sector terms",
            "formula": "dJ_H_total = Delta_nonEH + Delta_frame + Delta_extra + Delta_boundary + Delta_radiative",
            "units": "current_divergence",
            "zero_route": "same parent variation for matter+EM plus stationary source-free exterior and extra-sector silence",
            "if_nonzero_maps_to": "D_r M_H;D_t M_H;Newton_source_normalization",
            "bound_source_needed": "P8_total_Hilbert_current_closure_bound.csv",
            "current_status": "CONDITIONAL_CLOSURE_NOT_SIGNED",
            "source_path": str(SOURCES["source_current_closure"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "bound_id": "EMB3503_7_Delta_PiM_metric",
            "coefficient": "Delta_PiM_metric",
            "meaning": "mass projector metric stress or non-topological response leaks into source normalization",
            "formula": "d(Pi_M J_H_total)=Pi_M dJ_H_total+[d,Pi_M]J_H_total",
            "units": "projected_current_divergence",
            "zero_route": "topological/metric-independent Pi_M or explicit PPN/R11 bound",
            "if_nonzero_maps_to": "radial_GM_hair;PPN;R11",
            "bound_source_needed": "R11_nonEH_operator_vector_executable.csv",
            "current_status": "GAMMA_PART_CANDIDATE_METRIC_PART_RETAINED",
            "source_path": str(SOURCES["hilbert_worldtube_glue"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3503_0_no_claim",
            "decision": "Do not promote EM/local-GR closure.",
            "rationale": "The theorem chain is exact conditionally, but the observed Hodge owner, unique F2 owner, charge/current normalization and total current closure are not all parent-signed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3503_1_poynting_kept",
            "decision": "Keep Poynting as a diagnostic current, not a side idea.",
            "rationale": "T_EM^{0i}=S_Poynting^i/c^2 makes EM energy flow part of the source-current accounting when the same observed Hodge is used.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3503_2_bound_vector_created",
            "decision": "Create EM/Hodge/current owner bound vector.",
            "rationale": "Every unsigned EM owner clause now has a coefficient row rather than floating as prose.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3503_3_next_target",
            "decision": "Attack observed Hodge/flow rule next.",
            "rationale": "It is the most upstream single clause: without *_EM=*_obs(q), Poynting, light cones and Maxwell stress do not necessarily source the same geometry.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3504-Y5-R2FR-observed-Hodge-flow-rule-from-q-eobs-or-DeltaHodge-bound.md",
            "next_script": "scripts/Y5_R2FR_3504_observed_Hodge_flow_rule_from_q_eobs_or_DeltaHodge_bound.py",
            "objective": "Derive *_EM = *_obs[e_obs(q)] and exclude independent constitutive/Hodge backgrounds, or fill Delta_Hodge_EM bounds with Maxwell/light-cone/clock/PPN links.",
            "success_gate": "EM Hodge star, Poynting vector, Maxwell stress, and null propagation are all q/e_obs-owned with no independent chi_EM tensor or hidden-visible Hodge coefficient.",
            "forbidden_shortcuts": "no importing Maxwell Hodge as an axiom; no unit-rescaling alpha claim; no ignoring constitutive/background field options; no local-GR claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_files = [
        OUT / "P8_Y5_R2FR_3503_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
        OUT / "P8_Y5_R2FR_3503_TOTAL_HILBERT_CURRENT_CLOSURE_GATE.csv",
        OUT / "P8_Y5_R2FR_3503_EM_HODGE_CURRENT_BOUND_VECTOR.csv",
        BOUND_VECTOR,
        OUT / "P8_Y5_R2FR_3503_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3503_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *theorem, *gates, *bounds, *decisions, *next_rows]
    checks = [
        {
            "check_id": "VAL3503_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local source-register paths exist",
        },
        {
            "check_id": "VAL3503_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3503_2_owner_theorem_chain",
            "passed": len(theorem) >= 6 and any(row["theorem_id"] == "OHM3503_0_same_observed_Hodge" for row in theorem),
            "detail": f"theorem_rows={len(theorem)}; observed Hodge theorem row present",
        },
        {
            "check_id": "VAL3503_3_all_success_gate_clauses_present",
            "passed": all(
                any(token in row["gate"] or token in row["required_identity"] for row in gates)
                for token in ["Hodge", "connection", "Maxwell kinetic", "charge/current", "total Hilbert", "projected total current"]
            ),
            "detail": f"gate_rows={len(gates)}",
        },
        {
            "check_id": "VAL3503_4_bound_vector_created",
            "passed": BOUND_VECTOR.exists() and len(read_csv(BOUND_VECTOR)) >= 8,
            "detail": str(BOUND_VECTOR),
        },
        {
            "check_id": "VAL3503_5_required_coefficients_present",
            "passed": all(
                any(row["coefficient"] == coefficient for row in bounds)
                for coefficient in ["Delta_Hodge_EM", "w_EM", "C_XF2", "C_JQ", "Phi_EM_rad/(G_ref M_H)", "Delta_J_total"]
            ),
            "detail": "Delta_Hodge_EM, w_EM, C_XF2, C_JQ, Phi_EM_rad and Delta_J_total rows present",
        },
        {
            "check_id": "VAL3503_6_no_claim",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3503_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs stay under post-checkpoint-work/source-intake",
        },
        {
            "check_id": "VAL3503_8_next_target",
            "passed": len(next_rows) == 1 and "3504" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3503_SUMMARY",
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
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3503 - Observed Hodge/Maxwell Owner and Total Hilbert Current Closure or EM Bound",
                "",
                "## Current Verdict",
                "- **The theorem chain is sharper:** EM/Poynting can join the Newton/local-GR source only if `*_EM = *_obs[e_obs(q)]`, Maxwell has no independent `F^2` multiplier, charge/current normalization is fixed, and `d(Pi_M J_H_total)=0`.",
                "- **No closure smuggled:** the current corpus still leaves unique `F^2`, alpha/charge owner, observed Hodge, and total-current projection unsigned.",
                "- **Poynting survives as useful physics:** `T_EM^{0i}=S_Poynting^i/c^2` makes energy flow a source-current diagnostic, not a decorative analogy.",
                "- **Next best move:** derive the observed Hodge/flow rule from `q/e_obs`, because without that the EM field may not source the same geometry at all.",
                "",
                "## Owner Theorem Chain",
                markdown_table(
                    theorem,
                    ["theorem_id", "claim_piece", "statement", "result", "remaining_gap", "valid_for_claim"],
                ),
                "",
                "## Total Hilbert Current Closure Gates",
                markdown_table(
                    gates,
                    ["gate_id", "gate", "required_identity", "current_status", "failure_mode", "blocks", "valid_for_claim"],
                ),
                "",
                "## EM Hodge/Current Bound Vector",
                markdown_table(
                    bounds,
                    [
                        "bound_id",
                        "coefficient",
                        "meaning",
                        "zero_route",
                        "if_nonzero_maps_to",
                        "current_status",
                        "valid_for_claim",
                    ],
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
    theorem_rows = owner_theorem_rows()
    gate_rows = current_closure_gate_rows()
    bound_rows = bound_vector_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    bound_fields = [
        "bound_id",
        "coefficient",
        "meaning",
        "formula",
        "units",
        "zero_route",
        "if_nonzero_maps_to",
        "bound_source_needed",
        "current_status",
        "source_path",
        "valid_for_claim",
    ]

    write_csv(
        OUT / "P8_Y5_R2FR_3503_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
        theorem_rows,
        [
            "theorem_id",
            "claim_piece",
            "statement",
            "mathematical_form",
            "derivation",
            "result",
            "remaining_gap",
            "source_path",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3503_TOTAL_HILBERT_CURRENT_CLOSURE_GATE.csv",
        gate_rows,
        ["gate_id", "gate", "required_identity", "current_status", "failure_mode", "blocks", "valid_for_claim"],
    )
    write_csv(OUT / "P8_Y5_R2FR_3503_EM_HODGE_CURRENT_BOUND_VECTOR.csv", bound_rows, bound_fields)
    write_csv(BOUND_VECTOR, bound_rows, bound_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3503_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3503_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation_rows = validate(source_rows, theorem_rows, gate_rows, bound_rows, decision_ledger_rows, next_rows)
    write_csv(
        OUT / "P8_Y5_BRR545_3503_VALIDATION.csv",
        validation_rows,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(theorem_rows, gate_rows, bound_rows, decision_ledger_rows, next_rows, validation_rows)


if __name__ == "__main__":
    main()

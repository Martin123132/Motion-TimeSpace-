from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3504-Y5-R2FR-observed-Hodge-flow-rule-from-q-eobs-or-DeltaHodge-bound.md"
DELTA_HODGE_BOUND = OUT / "P8_EM_Hodge_flow_rule_bound_or_zero.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3504": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3503": {
        "path": ROOT / "3503-Y5-R2FR-observed-Hodge-Maxwell-owner-and-total-Hilbert-current-closure-or-EM-bound.md",
        "role": "3503 handoff",
    },
    "next_3503": {
        "path": OUT / "P8_Y5_R2FR_3503_NEXT_TARGET.csv",
        "role": "3503 selected next target",
    },
    "owner_theorem_3503": {
        "path": OUT / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
        "role": "3503 observed Hodge/Maxwell owner theorem",
    },
    "bound_vector_3503": {
        "path": OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "role": "3503 EM/Hodge/current bound vector",
    },
    "maxwell_poynting_ledger": {
        "path": OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
        "role": "Maxwell stress and Poynting ledger",
    },
    "em_owner_package": {
        "path": OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
        "role": "EM owner package audit",
    },
    "coframe_spin_theorem": {
        "path": OUT / "P8_Y5_R2FR_3494_COFRAME_SPIN_THEOREM_ATTEMPT.csv",
        "role": "owned coframe/spin action theorem attempt",
    },
    "projector_naturality_3498": {
        "path": OUT / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        "role": "q/e_obs chain-rule naturality theorem",
    },
    "readout_lemma": {
        "path": OUT / "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637_CONDITIONAL_READOUT_LEMMA.csv",
        "role": "readout-after-variation lemma",
    },
    "readout_domain_certificate": {
        "path": OUT / "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637_CLOSED_DOMAIN_CERTIFICATE_ATTEMPT.csv",
        "role": "readout/domain certificate attempt",
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


def hodge_uniqueness_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "HFR3504_0_coframe_metric",
            "claim_piece": "coframe determines observed metric",
            "statement": "A parent-owned observed coframe fixes the observed metric and volume/orientation data used by local matter and source readout.",
            "mathematical_form": "g_obs = eta_ab e_obs^a tensor e_obs^b; vol_obs = det(e_obs) d^4x",
            "derivation": "Once e_obs is a q-owned branch field/readout, g_obs and vol_obs are not separate hidden variables.",
            "result": "EXACT_CONDITIONAL",
            "remaining_gap": "e_obs itself is still a branch signature rather than a globally signed parent theorem",
            "source_path": str(SOURCES["coframe_spin_theorem"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HFR3504_1_hodge_uniqueness",
            "claim_piece": "unique Hodge star from metric plus orientation",
            "statement": "On an oriented metric four-manifold, the Hodge star is uniquely determined by the observed metric and volume form.",
            "mathematical_form": "alpha wedge *_obs beta = <alpha,beta>_g_obs vol_obs",
            "derivation": "There is no extra Hodge degree of freedom once the metric/coframe and orientation are fixed. Any different EM flow rule is an independent constitutive tensor, not the same Hodge star.",
            "result": "MATHEMATICAL_UNIQUENESS_LEMMA",
            "remaining_gap": "the EM action must be parent-signed to use *_obs rather than a separate chi_EM",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HFR3504_2_vertical_chain_rule",
            "claim_piece": "q/e_obs Hodge vertical silence",
            "statement": "If e_obs descends through q and orientation is fixed, then the observed Hodge star is vertical-silent along ker(Dq).",
            "mathematical_form": "e_obs = e_bar(q), v in ker(Dq) => D_v e_obs=0 => D_v g_obs=0 => D_v *_obs=0",
            "derivation": "This is the same chain-rule mechanism used in the 3498 projector naturality theorem, now applied to the EM Hodge star.",
            "result": "EXACT_CONDITIONAL_ZERO_FOR_DELTA_HODGE_REPRESENTATIVE",
            "remaining_gap": "requires EM action domain to use only *_obs and no independent constitutive/background field",
            "source_path": str(SOURCES["projector_naturality_3498"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HFR3504_3_action_variation",
            "claim_piece": "Maxwell stress and Poynting from same Hodge",
            "statement": "If S_EM is built from F and *_obs, its stress tensor and Poynting current are variations/readouts of the same observed coframe geometry.",
            "mathematical_form": "S_EM=-(4 mu0)^-1 int F wedge *_obs F; T_EM = 2/sqrt(-g_obs) delta S_EM/delta g_obs; T_EM^{0i}=S^i/c^2",
            "derivation": "The Hodge star is where the background flow rule enters. If that star is *_obs, EM stress dresses M_H; if not, Delta_Hodge_EM is live.",
            "result": "CONDITIONAL_EM_SOURCE_ALIGNMENT",
            "remaining_gap": "Maxwell normalization and charge/current owner remain separate gates",
            "source_path": str(SOURCES["maxwell_poynting_ledger"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HFR3504_4_conformal_caveat",
            "claim_piece": "light cone does not fix full source normalization",
            "statement": "In four spacetime dimensions the Hodge star on two-forms is conformally invariant, so null-cone agreement alone fixes only the conformal class, not the full clock/source normalization.",
            "mathematical_form": "g -> Omega^2 g leaves * on 2-forms invariant in 4D, but clocks, volumes, masses and source normalization still need owned scale data",
            "derivation": "This prevents a false victory: matching Maxwell light cones helps, but does not by itself derive w_EM, alpha_EM, charge/current normalization, or M_H calibration.",
            "result": "NO_OVERCLAIM_GUARD",
            "remaining_gap": "clock/scale/charge-current owner and unique F2 remain required",
            "source_path": str(SOURCES["owner_theorem_3503"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HFR3504_5_constitutive_countermodel",
            "claim_piece": "independent constitutive tensor counterbranch",
            "statement": "A diffeomorphism/gauge-covariant EM action may use an independent constitutive tensor chi_EM or hidden-visible Hodge coefficient unless the parent action forbids it.",
            "mathematical_form": "S_EM=-1/4 int F_ab chi_EM^{abcd} F_cd vol_obs; chi_EM != chi(g_obs)",
            "derivation": "Such a term can change propagation, birefringence, stress, Poynting flow, or readout without violating gauge covariance. It must be excluded by parent grammar or bounded.",
            "result": "COUNTERMODEL_RETAINED",
            "remaining_gap": "operator-domain exhaustion/no-constitutive-background theorem missing",
            "source_path": str(SOURCES["bound_vector_3503"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HFR3504_6_verdict",
            "claim_piece": "Delta_Hodge_EM fate",
            "statement": "Delta_Hodge_EM has a clean conditional zero route, but not a live claim: the Hodge star is unique once e_obs is used, yet the current corpus has not globally forbidden independent EM constitutive structure.",
            "mathematical_form": "Delta_Hodge_EM=0 if S_EM[A_Q,e_obs(q)] uses only *_obs and Allowed[S_vis] excludes chi_EM/f_H(Phi)*_obs/background constitutive maps",
            "derivation": "This is a real narrowing of the throat: prove the action-domain exclusion next or keep the bound vector.",
            "result": "CONDITIONAL_ZERO_ROUTE_PLUS_BOUND_VECTOR",
            "remaining_gap": "visible EM action-domain exhaustion",
            "source_path": str(SOURCES["em_owner_package"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def parent_signature_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "HSG3504_0_eobs_q_basic",
            "gate": "e_obs is q/e_obs-owned",
            "required_identity": "e_obs=e_bar(q) and D_v e_obs=0 for v in ker(Dq)",
            "current_status": "CANDIDATE_BRANCH_CONDITIONAL",
            "failure_mode": "frame/readout split",
            "blocks": "Hodge silence; matter/source same frame; local light cone",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "HSG3504_1_orientation_fixed",
            "gate": "orientation and time orientation are parent-fixed",
            "required_identity": "vol_obs and sign convention are fixed branch data, not readout-tuned",
            "current_status": "ASSUMED_IN_STANDARD_FORM_NOT_SOURCE_SIGNED",
            "failure_mode": "orientation/volume readout drift",
            "blocks": "Hodge definition; Poynting sign; charge flux orientation",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "HSG3504_2_EM_uses_star_obs",
            "gate": "Maxwell action uses *_obs",
            "required_identity": "S_EM[A_Q,e_obs]=-(4 mu0)^-1 int F_Q wedge *_obs F_Q",
            "current_status": "CONDITIONAL_STANDARD_FORM",
            "failure_mode": "Delta_Hodge_EM",
            "blocks": "EM stress source alignment; Poynting current alignment",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "HSG3504_3_no_chi_EM",
            "gate": "no independent constitutive tensor",
            "required_identity": "Allowed[S_vis] excludes chi_EM^{abcd}(Phi) not equal to chi(g_obs)",
            "current_status": "NOT_DERIVED_COUNTERMODEL_RETAINED",
            "failure_mode": "Delta_chi_principal;Delta_chi_skewon;Delta_chi_axion",
            "blocks": "Maxwell limit; birefringence; null cone; Poynting stress",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "HSG3504_4_no_hidden_hodge_coefficient",
            "gate": "no hidden-visible Hodge coefficient",
            "required_identity": "Allowed[S_vis] excludes f_H(Phi) F wedge *_obs F and hidden/disformal Hodge maps",
            "current_status": "NOT_DERIVED_OVERLAPS_UNIQUE_F2_GATE",
            "failure_mode": "C_XF2;w_EM;C_EM_readout",
            "blocks": "alpha owner; source normalization; EM binding response",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "HSG3504_5_readout_after_variation",
            "gate": "no readout Hodge backreaction",
            "required_identity": "any post-solution EM readout map is not varied as S_red with a new Hodge/medium field",
            "current_status": "CONDITIONAL_READOUT_THEOREM_UNSIGNED",
            "failure_mode": "C_EM_readout;section_backreaction",
            "blocks": "clock/spectroscopy regeneration; local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "HSG3504_6_conformal_scale_owner",
            "gate": "conformal scale and clock/source normalization owned separately",
            "required_identity": "light-cone/Hodge agreement is supplemented by clock, charge-current and M_H calibration ownership",
            "current_status": "SEPARATE_GATES_OPEN",
            "failure_mode": "w_EM;C_JQ;Delta_calibration",
            "blocks": "Newton constant appearance; alpha_EM; local clocks",
            "valid_for_claim": "False",
        },
    ]


def delta_hodge_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DHB3504_0_Delta_Hodge_EM",
            "coefficient": "Delta_Hodge_EM",
            "meaning": "aggregate mismatch between EM flow/Hodge rule and observed gravitational coframe",
            "formula": "*_EM - *_obs[e_obs(q)]",
            "units": "dimensionless_or_tensor",
            "zero_condition": "HSG3504_0 through HSG3504_5 all theorem-zero",
            "observable_links": "Maxwell_limit;light_cone;Poynting_flow;clock;PPN",
            "bound_or_source_needed": "derive parent action-domain exclusion or fill component rows below",
            "current_status": "CONDITIONAL_ZERO_ROUTE_NOT_CLAIMED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DHB3504_1_principal_cone",
            "coefficient": "Delta_chi_principal",
            "meaning": "principal constitutive tensor changes EM cone, anisotropy, birefringence, or effective metric",
            "formula": "chi_EM_principal - chi(g_obs)",
            "units": "tensor_dimensionless_or_declared",
            "zero_condition": "no independent principal constitutive tensor beyond g_obs",
            "observable_links": "null_propagation;vacuum_birefringence;Shapiro/lensing consistency;Maxwell waves",
            "bound_or_source_needed": "P8_EM_principal_constitutive_bound.csv",
            "current_status": "RETAINED_COMPONENT_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DHB3504_2_skewon",
            "coefficient": "Delta_chi_skewon",
            "meaning": "skewon/nonreciprocal or dissipative constitutive component",
            "formula": "chi_EM_skewon",
            "units": "tensor_dimensionless_or_declared",
            "zero_condition": "parent action is conservative/reciprocal and excludes skewon-like background",
            "observable_links": "polarization;dispersion;energy_flux_nonconservation;Poynting_anisotropy",
            "bound_or_source_needed": "P8_EM_skewon_bound.csv",
            "current_status": "RETAINED_COMPONENT_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DHB3504_3_axion_gradient",
            "coefficient": "Delta_chi_axion_gradient",
            "meaning": "axion-like F wedge F term or gradient alters polarization/current while constant term may be topological",
            "formula": "theta_EM(Phi) F wedge F; d theta_EM != 0 is active",
            "units": "dimensionless_or_inverse_length_for_gradient",
            "zero_condition": "theta_EM is absent or parent-fixed constant with zero gradient",
            "observable_links": "polarization_rotation;effective_current;clock/EM_readout",
            "bound_or_source_needed": "P8_EM_axion_gradient_bound.csv",
            "current_status": "RETAINED_COMPONENT_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DHB3504_4_hidden_disformal_hodge",
            "coefficient": "C_Hodge_hidden",
            "meaning": "hidden/motion/time field defines a disformal or medium-like EM Hodge star",
            "formula": "g_EM_ab = g_obs_ab + C_H u_a u_b + C_X X_ab or *_EM=*(g_EM)",
            "units": "dimensionless_or_declared",
            "zero_condition": "operator-domain rule forbids hidden-visible Hodge maps",
            "observable_links": "preferred_frame;alpha1/alpha2;light_speed_anisotropy;clock",
            "bound_or_source_needed": "P8_EM_hidden_Hodge_map_bound.csv",
            "current_status": "RETAINED_COMPONENT_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DHB3504_5_readout_hodge",
            "coefficient": "C_Hodge_readout",
            "meaning": "post-solution readout/clock/spectroscopy map regenerates an effective EM Hodge or alpha response",
            "formula": "Obs_EM = R_EM(Sol,parent; chi_readout) with varied S_red counterbranch if used dynamically",
            "units": "model_dependent",
            "zero_condition": "readout-after-variation theorem plus no reduced-action theorem credit",
            "observable_links": "clock;spectroscopy;alpha_EM;binding_response",
            "bound_or_source_needed": "P8_EM_readout_Hodge_bound.csv",
            "current_status": "RETAINED_READOUT_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DHB3504_6_conformal_scale_residual",
            "coefficient": "Delta_conformal_scale",
            "meaning": "EM null cone agrees but clock/source scale or volume normalization remains unowned",
            "formula": "g_EM = Omega^2 g_obs leaves * on 2-forms unchanged in 4D, but source/clock scale may shift",
            "units": "dimensionless",
            "zero_condition": "clock, charge-current, w_EM, and M_H calibration owners close",
            "observable_links": "clock_redshift;source_normalization;alpha_EM;Newton_G",
            "bound_or_source_needed": "P8_EM_conformal_scale_owner_bound.csv",
            "current_status": "SEPARATE_SCALE_GATE_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DHB3504_7_orientation_flux",
            "coefficient": "Delta_orientation_flux",
            "meaning": "orientation/time-orientation or boundary flux convention differs between EM and source charge",
            "formula": "vol_EM sign/time orientation - vol_obs sign/time orientation",
            "units": "discrete_or_dimensionless",
            "zero_condition": "orientation and source-boundary conventions are parent-fixed before readout",
            "observable_links": "Poynting_sign;charge_flux;boundary_source_orientation",
            "bound_or_source_needed": "P8_EM_orientation_flux_convention_bound.csv",
            "current_status": "PARENT_CONVENTION_REQUIRED",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3504_0_derivation_progress",
            "decision": "Delta_Hodge_EM has a mathematically clean conditional zero route.",
            "rationale": "A q/e_obs-owned coframe uniquely determines the observed Hodge star, and vertical silence follows by the chain rule.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3504_1_no_public_promotion",
            "decision": "Do not claim observed-Hodge closure yet.",
            "rationale": "The parent action still has to forbid independent chi_EM, hidden Hodge maps, and readout Hodge backreaction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3504_2_conformal_caution",
            "decision": "Do not infer clock/source normalization from light-cone agreement.",
            "rationale": "In 4D Maxwell theory, the Hodge star on two-forms is conformally invariant, so null propagation is not enough to own w_EM, alpha, or M_H calibration.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3504_3_next_target",
            "decision": "Next target is visible EM action-domain exhaustion.",
            "rationale": "The route now needs a grammar theorem excluding chi_EM, f_H(Phi)F^2, hidden/disformal Hodge maps, and readout-regenerated Hodge coefficients.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3505-Y5-R2FR-visible-EM-action-domain-exhaustion-no-chiEM-no-hidden-Hodge-or-bound.md",
            "next_script": "scripts/Y5_R2FR_3505_visible_EM_action_domain_exhaustion_no_chiEM_no_hidden_Hodge_or_bound.py",
            "objective": "Prove the visible EM action domain admits only A_Q, F_Q, e_obs(q), fixed orientation and fixed representation data, excluding chi_EM, f_H(Phi)F^2, hidden/disformal Hodge maps, and readout Hodge backreaction; otherwise keep component bounds.",
            "success_gate": "Allowed[S_EM] = {-1/(4 mu0) int F_Q wedge *_obs F_Q + A_Q.J_Q} modulo fixed parent constants, with no independent constitutive/Hodge/background/readout EM maps.",
            "forbidden_shortcuts": "no Maxwell-Hodge import by taste; no light-cone-only source claim; no unit-rescaling alpha claim; no local-GR promotion",
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
        OUT / "P8_Y5_R2FR_3504_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
        OUT / "P8_Y5_R2FR_3504_PARENT_SIGNATURE_GATE.csv",
        OUT / "P8_Y5_R2FR_3504_DELTA_HODGE_BOUND_VECTOR.csv",
        DELTA_HODGE_BOUND,
        OUT / "P8_Y5_R2FR_3504_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3504_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *theorem, *gates, *bounds, *decisions, *next_rows]
    checks = [
        {
            "check_id": "VAL3504_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local source-register paths exist",
        },
        {
            "check_id": "VAL3504_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3504_2_hodge_uniqueness_present",
            "passed": any(row["theorem_id"] == "HFR3504_1_hodge_uniqueness" for row in theorem)
            and any(row["theorem_id"] == "HFR3504_2_vertical_chain_rule" for row in theorem),
            "detail": "Hodge uniqueness and q/e_obs vertical chain-rule rows present",
        },
        {
            "check_id": "VAL3504_3_conformal_caution",
            "passed": any(row["theorem_id"] == "HFR3504_4_conformal_caveat" for row in theorem),
            "detail": "4D conformal caveat prevents light-cone overclaim",
        },
        {
            "check_id": "VAL3504_4_bound_vector_created",
            "passed": DELTA_HODGE_BOUND.exists() and len(read_csv(DELTA_HODGE_BOUND)) >= 8,
            "detail": str(DELTA_HODGE_BOUND),
        },
        {
            "check_id": "VAL3504_5_countermodel_retained",
            "passed": any(row["coefficient"] == "Delta_chi_principal" for row in bounds)
            and any(row["coefficient"] == "C_Hodge_hidden" for row in bounds),
            "detail": "principal constitutive and hidden/disformal Hodge counterbranches retained",
        },
        {
            "check_id": "VAL3504_6_no_claim",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3504_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs stay under post-checkpoint-work/source-intake",
        },
        {
            "check_id": "VAL3504_8_next_target",
            "passed": len(next_rows) == 1 and "3505" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3504_SUMMARY",
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
                "# 3504 - Observed Hodge Flow Rule from q/e_obs or DeltaHodge Bound",
                "",
                "## Current Verdict",
                "- **Good derivation:** if `e_obs=e_bar(q)` and the EM action uses only `*_obs[e_obs]`, then `Delta_Hodge_EM=0` follows by Hodge uniqueness plus the q/e_obs chain rule.",
                "- **No overclaim:** the current corpus still permits independent constitutive/Hodge structure unless the visible EM action domain is exhausted.",
                "- **Important caveat:** in 4D, Maxwell `*` on two-forms is conformally invariant, so light-cone agreement alone does not derive clock/source normalization, `w_EM`, `alpha_EM`, or `M_H` calibration.",
                "- **Next best move:** prove the visible EM action has no `chi_EM`, hidden/disformal Hodge map, `f_H(Phi)F^2`, or readout Hodge backreaction.",
                "",
                "## Hodge Uniqueness Theorem",
                markdown_table(
                    theorem,
                    ["theorem_id", "claim_piece", "statement", "result", "remaining_gap", "valid_for_claim"],
                ),
                "",
                "## Parent Signature Gates",
                markdown_table(
                    gates,
                    ["gate_id", "gate", "required_identity", "current_status", "failure_mode", "blocks", "valid_for_claim"],
                ),
                "",
                "## Delta Hodge Bound Vector",
                markdown_table(
                    bounds,
                    [
                        "row_id",
                        "coefficient",
                        "meaning",
                        "zero_condition",
                        "observable_links",
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
    theorem_rows = hodge_uniqueness_rows()
    gate_rows = parent_signature_gate_rows()
    bound_rows = delta_hodge_bound_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    bound_fields = [
        "row_id",
        "coefficient",
        "meaning",
        "formula",
        "units",
        "zero_condition",
        "observable_links",
        "bound_or_source_needed",
        "current_status",
        "valid_for_claim",
    ]

    write_csv(
        OUT / "P8_Y5_R2FR_3504_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
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
        OUT / "P8_Y5_R2FR_3504_PARENT_SIGNATURE_GATE.csv",
        gate_rows,
        ["gate_id", "gate", "required_identity", "current_status", "failure_mode", "blocks", "valid_for_claim"],
    )
    write_csv(OUT / "P8_Y5_R2FR_3504_DELTA_HODGE_BOUND_VECTOR.csv", bound_rows, bound_fields)
    write_csv(DELTA_HODGE_BOUND, bound_rows, bound_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3504_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3504_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation_rows = validate(source_rows, theorem_rows, gate_rows, bound_rows, decision_ledger_rows, next_rows)
    write_csv(
        OUT / "P8_Y5_BRR545_3504_VALIDATION.csv",
        validation_rows,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(theorem_rows, gate_rows, bound_rows, decision_ledger_rows, next_rows, validation_rows)


if __name__ == "__main__":
    main()

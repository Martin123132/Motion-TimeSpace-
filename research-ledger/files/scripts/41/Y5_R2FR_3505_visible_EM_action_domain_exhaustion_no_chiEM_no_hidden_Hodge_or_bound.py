from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3505-Y5-R2FR-visible-EM-action-domain-exhaustion-no-chiEM-no-hidden-Hodge-or-bound.md"
DOMAIN_BOUND = OUT / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3505": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3504": {
        "path": ROOT / "3504-Y5-R2FR-observed-Hodge-flow-rule-from-q-eobs-or-DeltaHodge-bound.md",
        "role": "3504 handoff",
    },
    "next_3504": {
        "path": OUT / "P8_Y5_R2FR_3504_NEXT_TARGET.csv",
        "role": "3504 selected next target",
    },
    "hodge_theorem_3504": {
        "path": OUT / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
        "role": "3504 Hodge uniqueness theorem",
    },
    "delta_hodge_bound_3504": {
        "path": OUT / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
        "role": "3504 Delta_Hodge bound vector",
    },
    "em_owner_package": {
        "path": OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
        "role": "EM owner package audit",
    },
    "maxwell_inheritance": {
        "path": OUT / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "role": "Maxwell kinetic inheritance gate",
    },
    "operator_domain_1058": {
        "path": ROOT / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md",
        "role": "visible operator-domain exhaustion attempt",
    },
    "unique_maxwell_1057": {
        "path": ROOT / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md",
        "role": "unique Maxwell subblock/no independent F2 attempt",
    },
    "no_hidden_visible_hom": {
        "path": OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
        "role": "no hidden-visible hom operator-domain attempt",
    },
    "readout_lemma": {
        "path": OUT / "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637_CONDITIONAL_READOUT_LEMMA.csv",
        "role": "readout-after-variation lemma",
    },
    "readout_domain_certificate": {
        "path": OUT / "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637_CLOSED_DOMAIN_CERTIFICATE_ATTEMPT.csv",
        "role": "readout domain certificate attempt",
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


def action_domain_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "VEM3505_0_target_domain",
            "claim_piece": "visible EM action-domain exhaustion target",
            "statement": "The claim-grade EM domain is exhausted only if S_EM has arguments {A_Q, F_Q=dA_Q, e_obs(q), fixed orientation, fixed representation/current data, fixed constants} and nothing else.",
            "mathematical_form": "Allowed[S_EM] = {-1/(4 mu0) int F_Q wedge *_obs F_Q + int A_Q.J_Q} modulo fixed parent constants",
            "derivation": "This is the minimum action grammar that makes Hodge uniqueness useful: it gives the EM sector no independent medium/Hodge/background slot to vary or tune.",
            "result": "TARGET_SHARP",
            "current_blocker": "the parent action-domain grammar is not globally derived from MTS primitives",
            "source_path": str(SOURCES["hodge_theorem_3504"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3505_1_exact_typed_exclusion",
            "claim_piece": "typed-domain exclusion theorem",
            "statement": "If the allowed argument list is closed as above, then chi_EM, hidden/disformal Hodge maps, and readout Hodge fields are not variables; their Euler/source terms are absent by typing.",
            "mathematical_form": "Args(S_EM) cap {chi_EM, g_EM_hidden, f_H(Phi), chi_readout}=empty => delta S_EM/delta chi_EM = 0 by absence",
            "derivation": "Euler derivatives only exist for action arguments. This is a variable-absence theorem, not a small-coupling approximation.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "current_blocker": "Allowed[S_EM] is a contract, not yet a parent-derived theorem",
            "source_path": str(SOURCES["no_hidden_visible_hom"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3505_2_chiEM_countermodel",
            "claim_piece": "independent constitutive tensor",
            "statement": "Gauge and diffeomorphism covariance alone allow a constitutive tensor chi_EM that is not chi(g_obs).",
            "mathematical_form": "S_EM=-1/4 int F_ab chi_EM^{abcd} F_cd vol_obs",
            "derivation": "This countermodel can change principal cone, birefringence, skewon-like response, axion gradients, stress and Poynting flow while remaining gauge-covariant.",
            "result": "COUNTERMODEL_RETAINED",
            "current_blocker": "no parent grammar theorem excluding chi_EM",
            "source_path": str(SOURCES["delta_hodge_bound_3504"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3505_3_hidden_hodge_countermodel",
            "claim_piece": "hidden/disformal Hodge map",
            "statement": "A hidden or motion/time field may define a disformal effective EM metric or Hodge map unless visible-hidden coefficient morphisms are forbidden.",
            "mathematical_form": "g_EM_ab = g_obs_ab + C_H u_a u_b + C_X X_ab; *_EM=*(g_EM)",
            "derivation": "This is exactly the route by which a background flow/medium can re-enter the visible EM sector if not parent-excluded.",
            "result": "COUNTERMODEL_RETAINED",
            "current_blocker": "no-hidden-visible-hom theorem is exact conditionally but not parent-signed",
            "source_path": str(SOURCES["no_hidden_visible_hom"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3505_4_no_independent_F2_overlap",
            "claim_piece": "f_H(Phi)F^2 and w_EM overlap unique F2",
            "statement": "A hidden Hodge coefficient f_H(Phi)F wedge *_obs F is also an independent Maxwell kinetic multiplier unless the unique F2/operator-domain theorem closes.",
            "mathematical_form": "S_EM -> -1/4 int Z_A(Phi) F wedge *_obs F, Z_A=C_P N_Q + lambda_A + f_H(Phi)+delta_lambda_rad",
            "derivation": "Even if the Hodge star is *_obs, the EM stress strength can still drift through its coefficient.",
            "result": "RETAINED_UNIQUE_F2_GATE",
            "current_blocker": "1057/1058 show ordinary symmetries allow independent F_Q^2",
            "source_path": str(SOURCES["unique_maxwell_1057"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3505_5_readout_backreaction",
            "claim_piece": "readout Hodge backreaction",
            "statement": "Post-solution EM readout maps do not source parent equations if applied after variation; if varied as a reduced action, they define a retained effective branch.",
            "mathematical_form": "R_EM: Sol(S_parent)->Obs is source-silent; S_red[A,g,chi_readout] has E_readout != 0 and must be bounded",
            "derivation": "This is the readout-after-variation theorem: a readout map is harmless only when it is not smuggled back into the varied action.",
            "result": "EXACT_CONDITIONAL_WITH_COUNTERBRANCH",
            "current_blocker": "closed parent field list and no-reduced-action discipline are unsigned globally",
            "source_path": str(SOURCES["readout_lemma"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3505_6_radiative_effective_closure",
            "claim_piece": "effective/radiative closure",
            "statement": "A tree-level EM domain ban is not enough unless loops, thresholds and clock/spectroscopy readout preserve the same domain.",
            "mathematical_form": "S_EM^eff must remain in Image(ParentGenerate[A_Q,e_obs(q),theta_fixed])",
            "derivation": "Otherwise effective terms regenerate F^2 coefficients or Hodge/readout response after reduction.",
            "result": "UNSIGNED_PRESERVATION_REQUIREMENT",
            "current_blocker": "radiative/readout closure remains a retained branch in 1058",
            "source_path": str(SOURCES["operator_domain_1058"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3505_7_verdict",
            "claim_piece": "visible EM domain exhaustion verdict",
            "statement": "3505 gives the exact theorem shape but not a live zero theorem: action-domain exhaustion is the missing parent signature.",
            "mathematical_form": "VEM3505_1 closes Delta_Hodge_EM only if VEM3505_0 is parent-derived and VEM3505_2-6 are excluded",
            "derivation": "The work is now narrowed to a concrete parent-generator signature or first component bounds.",
            "result": "CONTRACT_EXACT_NOT_PARENT_DERIVED",
            "current_blocker": "derive the parent visible EM generator or keep Delta_Hodge components as bounds",
            "source_path": str(SOURCES["operator_domain_1058"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def grammar_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "VGA3505_0_AQ",
            "gate": "observed A_Q is parent-projected",
            "allowed_if_signed": "A_parent=A_Q T_Q + A_perp with T_Q fixed before readout",
            "forbidden_slot": "post-hoc visible EM connection",
            "current_status": "TEMPLATE_ONLY_NOT_SIGNED",
            "failure_coefficient": "Delta_AQ_projection",
            "claim_effect": "Maxwell descent and charge/current owner stay open",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "VGA3505_1_star_obs",
            "gate": "EM uses *_obs[e_obs(q)]",
            "allowed_if_signed": "F_Q wedge *_obs F_Q with *_obs uniquely determined by e_obs and orientation",
            "forbidden_slot": "chi_EM principal/skewon/axion Hodge replacement",
            "current_status": "CONDITIONAL_HODGE_UNIQUENESS_ROUTE",
            "failure_coefficient": "Delta_Hodge_EM",
            "claim_effect": "EM stress/Poynting may align with M_H only conditionally",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "VGA3505_2_no_chiEM",
            "gate": "no independent constitutive tensor",
            "allowed_if_signed": "chi_EM is exactly chi(g_obs) and not an action argument",
            "forbidden_slot": "chi_EM^{abcd}(Phi), medium tensors, birefringent/skewon/axion backgrounds",
            "current_status": "NOT_DERIVED_COUNTERMODEL_RETAINED",
            "failure_coefficient": "Delta_chi_principal;Delta_chi_skewon;Delta_chi_axion_gradient",
            "claim_effect": "Delta_Hodge_EM cannot be zero-claimed",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "VGA3505_3_no_hidden_Hodge",
            "gate": "no hidden/disformal Hodge map",
            "allowed_if_signed": "visible EM coefficients factor only through q/e_obs and fixed representation data",
            "forbidden_slot": "g_EM(g_obs,X,u), C_Hodge_hidden, hidden medium maps",
            "current_status": "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED",
            "failure_coefficient": "C_Hodge_hidden",
            "claim_effect": "preferred-frame/light-speed/clock residuals remain possible",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "VGA3505_4_no_fH_F2",
            "gate": "no hidden Hodge coefficient or independent F2 multiplier",
            "allowed_if_signed": "Maxwell kinetic coefficient is the unique parent curvature norm plus fixed constants",
            "forbidden_slot": "f_H(Phi)F^2, lambda_A F^2, w_EM F^2",
            "current_status": "UNIQUE_F2_NOT_CLOSED",
            "failure_coefficient": "C_XF2;w_EM",
            "claim_effect": "alpha/source normalization remains retained",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "VGA3505_5_no_readout_backreaction",
            "gate": "no readout Hodge/effective medium backreaction",
            "allowed_if_signed": "R_EM is post-variation only; any varied S_red is demoted to retained effective branch",
            "forbidden_slot": "chi_readout, C_Hodge_readout, loop/readout regenerated F2",
            "current_status": "READOUT_THEOREM_CONDITIONAL_DOMAIN_UNSIGNED",
            "failure_coefficient": "C_Hodge_readout;C_EM_readout",
            "claim_effect": "clock/spectroscopy alpha-Hodge response remains active",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "VGA3505_6_fixed_constants",
            "gate": "fixed constants and representation data only",
            "allowed_if_signed": "mu0, charge lattice/current normalization and theta_rep are fixed parent data",
            "forbidden_slot": "source/time/range/species-dependent EM constants",
            "current_status": "CHARGE_CURRENT_AND_ALPHA_OWNER_OPEN",
            "failure_coefficient": "C_JQ;Delta_conformal_scale;w_EM",
            "claim_effect": "Newton/alpha/source normalization cannot be promoted",
            "valid_for_claim": "False",
        },
    ]


def bound_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "VEB3505_0_Delta_Hodge_EM",
            "coefficient": "Delta_Hodge_EM",
            "status": "CONDITIONAL_ZERO_IF_ACTION_DOMAIN_EXHAUSTED",
            "formula": "*_EM - *_obs[e_obs(q)]",
            "zero_or_bound": "zero only if VEM3505_0 through VEM3505_6 close",
            "observable_links": "Maxwell_limit;light_cone;Poynting_flow;clock;PPN",
            "source_path": str(SOURCES["delta_hodge_bound_3504"]["path"]),
            "next_action": "derive parent visible EM generator or score components",
            "valid_for_claim": "False",
        },
        {
            "row_id": "VEB3505_1_Delta_chi_principal",
            "coefficient": "Delta_chi_principal",
            "status": "RETAINED_BOUND_COMPONENT",
            "formula": "chi_EM_principal - chi(g_obs)",
            "zero_or_bound": "no independent principal constitutive tensor or bound birefringence/cone anisotropy",
            "observable_links": "null_propagation;vacuum_birefringence;Shapiro/lensing consistency;Maxwell waves",
            "source_path": str(SOURCES["delta_hodge_bound_3504"]["path"]),
            "next_action": "P8_EM_principal_constitutive_bound.csv",
            "valid_for_claim": "False",
        },
        {
            "row_id": "VEB3505_2_Delta_chi_skewon",
            "coefficient": "Delta_chi_skewon",
            "status": "RETAINED_BOUND_COMPONENT",
            "formula": "chi_EM_skewon",
            "zero_or_bound": "conservative reciprocal EM action excludes skewon or bound dispersion/dissipation",
            "observable_links": "polarization;dispersion;energy_flux_nonconservation;Poynting_anisotropy",
            "source_path": str(SOURCES["delta_hodge_bound_3504"]["path"]),
            "next_action": "P8_EM_skewon_bound.csv",
            "valid_for_claim": "False",
        },
        {
            "row_id": "VEB3505_3_Delta_chi_axion_gradient",
            "coefficient": "Delta_chi_axion_gradient",
            "status": "RETAINED_BOUND_COMPONENT",
            "formula": "theta_EM(Phi) F wedge F with d theta_EM != 0 active",
            "zero_or_bound": "theta_EM absent or parent-fixed constant; gradient bounded otherwise",
            "observable_links": "polarization_rotation;effective_current;clock/EM_readout",
            "source_path": str(SOURCES["delta_hodge_bound_3504"]["path"]),
            "next_action": "P8_EM_axion_gradient_bound.csv",
            "valid_for_claim": "False",
        },
        {
            "row_id": "VEB3505_4_C_Hodge_hidden",
            "coefficient": "C_Hodge_hidden",
            "status": "RETAINED_BOUND_COMPONENT",
            "formula": "g_EM_ab=g_obs_ab+C_H u_a u_b+C_X X_ab or *_EM=*(g_EM)",
            "zero_or_bound": "no hidden-visible Hodge map theorem or preferred-frame/light-speed bound",
            "observable_links": "preferred_frame;alpha1/alpha2;light_speed_anisotropy;clock",
            "source_path": str(SOURCES["no_hidden_visible_hom"]["path"]),
            "next_action": "P8_EM_hidden_Hodge_map_bound.csv",
            "valid_for_claim": "False",
        },
        {
            "row_id": "VEB3505_5_C_Hodge_readout",
            "coefficient": "C_Hodge_readout",
            "status": "RETAINED_BOUND_COMPONENT",
            "formula": "Obs_EM=R_EM(Sol,parent;chi_readout) or varied S_red counterbranch",
            "zero_or_bound": "readout-after-variation theorem plus no S_red claim credit",
            "observable_links": "clock;spectroscopy;alpha_EM;binding_response",
            "source_path": str(SOURCES["readout_lemma"]["path"]),
            "next_action": "P8_EM_readout_Hodge_bound.csv",
            "valid_for_claim": "False",
        },
        {
            "row_id": "VEB3505_6_C_XF2",
            "coefficient": "C_XF2",
            "status": "RETAINED_BOUND_COMPONENT",
            "formula": "f_H(Phi) F wedge *_obs F or f_X(Phi)F^2",
            "zero_or_bound": "unique F2 and no hidden-visible coefficient theorem",
            "observable_links": "alpha_EM;clock;WEP;R10;PPN;source_normalization",
            "source_path": str(SOURCES["unique_maxwell_1057"]["path"]),
            "next_action": "P8_EM_nonminimal_XF2_bound_vector.csv",
            "valid_for_claim": "False",
        },
        {
            "row_id": "VEB3505_7_Delta_conformal_scale",
            "coefficient": "Delta_conformal_scale",
            "status": "SEPARATE_SCALE_GATE_RETAINED",
            "formula": "g_EM=Omega^2 g_obs leaves 4D Maxwell * unchanged but shifts clocks/source scale",
            "zero_or_bound": "clock, charge-current, w_EM and M_H calibration owners close",
            "observable_links": "clock_redshift;source_normalization;alpha_EM;Newton_G",
            "source_path": str(SOURCES["delta_hodge_bound_3504"]["path"]),
            "next_action": "P8_EM_conformal_scale_owner_bound.csv",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3505_0_exact_if_signed",
            "decision": "Visible EM action-domain exhaustion would close Delta_Hodge_EM by variable absence.",
            "rationale": "If Args(S_EM) excludes chi_EM, hidden Hodge maps and readout media, no corresponding Euler/source terms exist.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3505_1_not_signed",
            "decision": "Do not promote exhaustion as a theorem yet.",
            "rationale": "Current evidence gives exact conditional contracts and explicit countermodels; ordinary symmetries allow the forbidden slots unless parent grammar excludes them.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3505_2_bounds_retained",
            "decision": "Keep the Delta_Hodge component bound vector live.",
            "rationale": "Principal, skewon, axion-gradient, hidden/disformal, readout, and F2 coefficient branches all remain possible until the action domain is parent-derived.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3505_3_next_target",
            "decision": "Next target is the parent visible EM generator signature.",
            "rationale": "The action-domain theorem now needs a concrete generator derivation from motion/time/space primitives, not another broad scan.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3506-Y5-R2FR-parent-visible-EM-generator-signature-or-first-constitutive-bound-runner.md",
            "next_script": "scripts/Y5_R2FR_3506_parent_visible_EM_generator_signature_or_first_constitutive_bound_runner.py",
            "objective": "Try to derive the parent visible EM generator set {A_Q,F_Q,e_obs(q),orientation,theta_rep} from MTS primitives; if not, fill the first executable Delta_chi_principal/Delta_Hodge bound runner rows.",
            "success_gate": "a source-backed parent signature showing why chi_EM, hidden/disformal Hodge maps, f_H(Phi)F2 and readout-Hodge fields are not legal action arguments; otherwise bound rows become executable.",
            "forbidden_shortcuts": "no declaring the action domain by taste; no covariance-only ban; no light-cone-only local-GR claim; no unit-rescaling alpha claim",
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
        OUT / "P8_Y5_R2FR_3505_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3505_VISIBLE_EM_ACTION_DOMAIN_THEOREM.csv",
        OUT / "P8_Y5_R2FR_3505_ACTION_GRAMMAR_GATE.csv",
        OUT / "P8_Y5_R2FR_3505_VISIBLE_EM_BOUND_VECTOR.csv",
        DOMAIN_BOUND,
        OUT / "P8_Y5_R2FR_3505_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3505_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *theorem, *gates, *bounds, *decisions, *next_rows]
    checks = [
        {
            "check_id": "VAL3505_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local source-register paths exist",
        },
        {
            "check_id": "VAL3505_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3505_2_exact_typed_theorem_present",
            "passed": any(row["theorem_id"] == "VEM3505_1_exact_typed_exclusion" for row in theorem),
            "detail": "typed variable-absence theorem row present",
        },
        {
            "check_id": "VAL3505_3_countermodels_retained",
            "passed": any(row["theorem_id"] == "VEM3505_2_chiEM_countermodel" for row in theorem)
            and any(row["theorem_id"] == "VEM3505_3_hidden_hodge_countermodel" for row in theorem),
            "detail": "chi_EM and hidden/disformal Hodge countermodels retained",
        },
        {
            "check_id": "VAL3505_4_bound_vector_created",
            "passed": DOMAIN_BOUND.exists() and len(read_csv(DOMAIN_BOUND)) >= 8,
            "detail": str(DOMAIN_BOUND),
        },
        {
            "check_id": "VAL3505_5_required_bound_components",
            "passed": all(
                any(row["coefficient"] == coefficient for row in bounds)
                for coefficient in ["Delta_Hodge_EM", "Delta_chi_principal", "Delta_chi_skewon", "Delta_chi_axion_gradient", "C_Hodge_hidden", "C_Hodge_readout", "C_XF2"]
            ),
            "detail": "Delta_Hodge/chi/Hodge-hidden/readout/XF2 components present",
        },
        {
            "check_id": "VAL3505_6_no_claim",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3505_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs stay under post-checkpoint-work/source-intake",
        },
        {
            "check_id": "VAL3505_8_next_target",
            "passed": len(next_rows) == 1 and "3506" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3505_SUMMARY",
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
                "# 3505 - Visible EM Action-Domain Exhaustion, No chiEM, No Hidden Hodge, or Bound",
                "",
                "## Current Verdict",
                "- **Exact theorem shape:** if `Args(S_EM)` is exhausted by `{A_Q,F_Q,e_obs(q),orientation,theta_rep}` plus fixed constants, then `chi_EM`, hidden Hodge maps and readout media are absent by type.",
                "- **Not yet derived:** ordinary covariance and gauge symmetry still allow `chi_EM`, `lambda_A F_Q^2`, hidden `f_H(Phi)F^2`, and reduced-action readout counterbranches.",
                "- **No closure smuggled:** `Delta_Hodge_EM` remains conditional, with principal/skewon/axion/hidden/readout/F2 components retained as explicit bounds.",
                "- **Next best move:** try to derive the parent visible EM generator signature from MTS primitives, or make the first constitutive bound runner executable.",
                "",
                "## Visible EM Action-Domain Theorem",
                markdown_table(
                    theorem,
                    ["theorem_id", "claim_piece", "statement", "result", "current_blocker", "valid_for_claim"],
                ),
                "",
                "## Action Grammar Gates",
                markdown_table(
                    gates,
                    [
                        "gate_id",
                        "gate",
                        "allowed_if_signed",
                        "forbidden_slot",
                        "current_status",
                        "failure_coefficient",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Visible EM Bound Vector",
                markdown_table(
                    bounds,
                    [
                        "row_id",
                        "coefficient",
                        "status",
                        "zero_or_bound",
                        "observable_links",
                        "next_action",
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
    theorem_rows = action_domain_theorem_rows()
    gate_rows = grammar_gate_rows()
    bound_rows = bound_vector_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    bound_fields = [
        "row_id",
        "coefficient",
        "status",
        "formula",
        "zero_or_bound",
        "observable_links",
        "source_path",
        "next_action",
        "valid_for_claim",
    ]

    write_csv(
        OUT / "P8_Y5_R2FR_3505_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3505_VISIBLE_EM_ACTION_DOMAIN_THEOREM.csv",
        theorem_rows,
        [
            "theorem_id",
            "claim_piece",
            "statement",
            "mathematical_form",
            "derivation",
            "result",
            "current_blocker",
            "source_path",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3505_ACTION_GRAMMAR_GATE.csv",
        gate_rows,
        [
            "gate_id",
            "gate",
            "allowed_if_signed",
            "forbidden_slot",
            "current_status",
            "failure_coefficient",
            "claim_effect",
            "valid_for_claim",
        ],
    )
    write_csv(OUT / "P8_Y5_R2FR_3505_VISIBLE_EM_BOUND_VECTOR.csv", bound_rows, bound_fields)
    write_csv(DOMAIN_BOUND, bound_rows, bound_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3505_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3505_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation_rows = validate(source_rows, theorem_rows, gate_rows, bound_rows, decision_ledger_rows, next_rows)
    write_csv(
        OUT / "P8_Y5_BRR545_3505_VALIDATION.csv",
        validation_rows,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(theorem_rows, gate_rows, bound_rows, decision_ledger_rows, next_rows, validation_rows)


if __name__ == "__main__":
    main()

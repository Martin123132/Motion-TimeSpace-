from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_topological_Hilbert_equality_attempt_parent_glue_missing_projector_stress_fill_template_nonclaim"
CLAIM_CEILING = "topological_Hilbert_equality_gate_only_no_closed_Hilbert_flux_no_radial_zero_no_cmu_zero_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "661-Y5-R10-topological-Hilbert-current-equality-or-projector-stress-fill.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "501_topological_Hilbert": ROOT / "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
    "500_topological_PiM": ROOT / "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
    "660_commutator": ROOT / "660-Y5-R10-PiM-commutator-zero-or-projector-stress-vector.md",
    "659_parent_source": ROOT / "659-Y5-R10-parent-source-identity-for-closed-PiM-flux-or-radial-profile-fill.md",
    "458_Hamiltonian_Gauss": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
    "523_Gauss_orbital": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "402_source_normalization": ROOT / "402-EH-source-normalization-parent-pair.md",
    "459_PG_residual": ROOT / "459-PG-calibration-residual-mapper.md",
    "450_Hilbert_monopole": ROOT / "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
    "660_validation": RESIDUALS / "P8_Y5_BRR545_660_VALIDATION.csv",
    "660_commutator_audit": RESIDUALS / "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
    "660_projector_stress": RESIDUALS / "P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv",
    "659_closure_identity": RESIDUALS / "P8_Y5_R10_659_CLOSURE_IDENTITY.csv",
    "659_obstruction_audit": RESIDUALS / "P8_Y5_R10_659_OBSTRUCTION_AUDIT.csv",
    "PG_calibration_residual": RESIDUALS / "P8_PG_calibration_residual_MAP.csv",
    "PiM_projector_algebra": RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
    "Hilbert_monopole_contract": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "501_topological_Hilbert": "prior equality theorem attempt and radial residual fallback",
        "500_topological_PiM": "closed topological current clause and Hilbert equality blocker",
        "660_commutator": "immediate predecessor retaining projector commutator stress",
        "659_parent_source": "parent-source identity and obstruction split",
        "458_Hamiltonian_Gauss": "Hamiltonian boundary charge and Gauss calibration gate",
        "523_Gauss_orbital": "orbital/source-normalization residual scoring gate",
        "402_source_normalization": "EH source-normalization parent-pair gate",
        "459_PG_residual": "Poisson/Gauss calibration residual map",
        "450_Hilbert_monopole": "Hilbert source to measured monopole calibration contract",
        "660_validation": "prior checkpoint validation status",
        "660_commutator_audit": "commutator zero clauses feeding equality target",
        "660_projector_stress": "projector-stress rows to inherit if equality fails",
        "659_closure_identity": "exact d(Pi_M J_H) identity decomposition",
        "659_obstruction_audit": "extra current, commutator, anomaly obstruction audit",
        "PG_calibration_residual": "measured-GM calibration residual source",
        "PiM_projector_algebra": "Pi_M algebra parent contract",
        "Hilbert_monopole_contract": "Hilbert-to-monopole parent contract",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def equality_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "attempt_id": "EQ661_0_target_identity",
            "route": "topological_Hilbert_current_equality_target",
            "equation_or_clause": "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "derivation_value": "makes the closed topological current the observed Hilbert mass current if R_eq=0 and the boundary improvement has zero compact flux",
            "current_status": "identity_target_written_not_parent_derived",
            "current_blocker": "R_eq and boundary flux are not parent-proved zero",
            "source_paths": source_list("501_topological_Hilbert", "500_topological_PiM", "660_commutator"),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "EQ661_1_closed_topological_current",
            "route": "closed_J_M_top",
            "equation_or_clause": "J_M_top = Q_M omega_M_top with dJ_M_top=0 when Q_M and omega_M_top are parent-owned closed data",
            "derivation_value": "gives a clean conserved object without metric projector stress in the exterior",
            "current_status": "conditional_topological_current_only",
            "current_blocker": "a closed object is not yet the same object as Pi_M J_H",
            "source_paths": source_list("500_topological_PiM", "501_topological_Hilbert"),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "EQ661_2_worldtube_charge_route",
            "route": "define_topological_charge_from_same_parent_Hilbert_source",
            "equation_or_clause": "Q_M := integral_{Sigma_source} rho_H dV_parent before readout; J_M_top := PD(parent Hilbert source worldtube)",
            "derivation_value": "best non-cheat route because the topological charge and Hilbert source charge are born as one parent object",
            "current_status": "best_route_but_missing_glue",
            "current_blocker": "no parent worldtube selector, source measure, or frame-free compact-support rule is signed",
            "source_paths": source_list("501_topological_Hilbert", "450_Hilbert_monopole", "402_source_normalization"),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "EQ661_3_Ward_current_route",
            "route": "Hilbert_source_current_Ward_identity",
            "equation_or_clause": "nabla_mu T_H^{mu nu}=0 plus a legal mass/time projection implies d(Pi_M J_H)=0 only if hidden exchange and boundary/domain flux vanish",
            "derivation_value": "could close Pi_M J_H directly without needing an independent topological label",
            "current_status": "conditional_sublemma_only",
            "current_blocker": "hidden exchange, bulk/domain current, and boundary flux are not parent-zero",
            "source_paths": source_list("659_parent_source", "659_obstruction_audit", "660_commutator_audit"),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "EQ661_4_parent_glue_multiplier",
            "route": "late_equality_multiplier",
            "equation_or_clause": "S_glue = int Lambda_eq wedge (Pi_M J_H - J_M_top - dB_zero)",
            "derivation_value": "would impose the equality as an Euler equation",
            "current_status": "rejected_as_derivation_unless_independently_owned",
            "current_blocker": "without a gauge, topological, Ward, or source-measure origin it relabels the desired Newton closure",
            "source_paths": source_list("501_topological_Hilbert", "660_projector_stress"),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "EQ661_5_Hamiltonian_boundary_dictionary",
            "route": "boundary_charge_to_Hilbert_to_Gauss_dictionary",
            "equation_or_clause": "B_xi/G_parent = Q_M = M_eff[Pi_M J_H] and Delta Phi = 4 pi G_parent rho_H",
            "derivation_value": "could calibrate topological charge to measured orbital GM after the equality theorem",
            "current_status": "conditional_downstream_not_current_proof",
            "current_blocker": "EH constraint algebra, boundary integrability, no extra charge, and Poisson/Gauss calibration remain open",
            "source_paths": source_list("458_Hamiltonian_Gauss", "523_Gauss_orbital", "459_PG_residual"),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "EQ661_6_residual_fallback",
            "route": "retain_exact_equality_residual_and_projector_stress",
            "equation_or_clause": "R_eq := Pi_M J_H - J_M_top - dB_zero; epsilon_eq[r1,r2] := c_M/M_eff_ref integral_A dR_eq plus boundary and channel terms",
            "derivation_value": "keeps the local/source-normalization branch falsifiable without pretending the equality was derived",
            "current_status": "fallback_template_written_not_filled",
            "current_blocker": "numeric residual, boundary flux, and channel integrals are not sourced",
            "source_paths": source_list("501_topological_Hilbert", "659_obstruction_audit", "660_projector_stress"),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def equality_obstruction_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "obstruction_id": "OB661_0_independent_topological_label",
            "obstruction": "Q_M can be an independent conserved topological label rather than the Hilbert source charge",
            "exact_failure": "dJ_M_top=0 does not imply d(Pi_M J_H)=0",
            "required_parent_input": "Q_M defined from the same parent Hilbert compact-source variation before observational readout",
            "affected_rows": "EQ661_1;EQ661_2",
            "observable_link": "Newton/source-normalization;orbital GM;R10;R11",
            "current_status": "not_parent_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OB661_1_worldtube_domain_selector",
            "obstruction": "the source worldtube or S2 class may be chosen by a metric, readout, or fitted-domain rule",
            "exact_failure": "parent covariance and local PPN silence are not guaranteed",
            "required_parent_input": "covariant compact-support/worldtube selector fixed before scoring and independent of fitted mass residuals",
            "affected_rows": "EQ661_2;EQ661_6",
            "observable_link": "PPN;WEP;clock;orbital residuals",
            "current_status": "missing_parent_worldtube_glue",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OB661_2_source_measure_and_frame",
            "obstruction": "rho_H dV_parent is not yet a signed parent measure tied to the same Hilbert variation",
            "exact_failure": "Q_M may inherit preferred-frame or representative dependence",
            "required_parent_input": "measure/coframe/connection descent showing source charge is frame-free and same-frame Hilbert",
            "affected_rows": "EQ661_2;EQ661_5",
            "observable_link": "source normalization;PPN gamma/beta/alpha_i;local clocks",
            "current_status": "measure_descent_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OB661_3_boundary_improvement_flux",
            "obstruction": "dB_zero may be exact locally but carry nonzero compact boundary flux",
            "exact_failure": "closed topological current can differ from measured monopole by a boundary charge",
            "required_parent_input": "zero-flux theorem for B_zero or a sourced boundary-charge row",
            "affected_rows": "EQ661_0;EQ661_4;EQ661_6",
            "observable_link": "orbital GM;R10;galaxy source normalization",
            "current_status": "fail_open",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OB661_4_hidden_exchange_current",
            "obstruction": "Hilbert matter can exchange projected mass current with hidden/bulk/domain/non-EH sectors",
            "exact_failure": "d(Pi_M J_H) inherits -Pi_M dJ_extra plus anomaly terms",
            "required_parent_input": "Pi_M dJ_extra=0 from legal-owner/topological/no-hair theorem",
            "affected_rows": "EQ661_3;EQ661_6",
            "observable_link": "R10;PPN;cosmology/local decoupling",
            "current_status": "not_parent_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OB661_5_projector_commutator_stress",
            "obstruction": "if Pi_M is metric/readout dependent, [d,Pi_M]J_H is retained as projector stress",
            "exact_failure": "commutator silence requires a fixed topological chain map on the Hilbert source-current domain",
            "required_parent_input": "metric-independent Pi_M, fixed domain, chain-map property, and Hilbert equality",
            "affected_rows": "EQ661_0;EQ661_3;EQ661_6",
            "observable_link": "local GR;PPN;R10;R11",
            "current_status": "inherited_from_660_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OB661_6_universal_calibration",
            "obstruction": "even equality does not by itself fix the universal G/kappa dictionary",
            "exact_failure": "Q_M may not equal the measured Poisson/Gauss/orbital source normalization",
            "required_parent_input": "Hamiltonian boundary charge, Hilbert monopole, Poisson/Gauss source, and orbital GM all map to the same constant",
            "affected_rows": "EQ661_5;EQ661_6",
            "observable_link": "Newtonian limit;orbital systems;SPARC/ETG;R11",
            "current_status": "calibration_gate_open",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OB661_7_second_order_and_PPN_stability",
            "obstruction": "first-order current equality may fail to silence second-order local residuals",
            "exact_failure": "local GR/PPN needs the same equality to remain stable under perturbations and compact-source matching",
            "required_parent_input": "second-order PPN/source-stability proof or sourced residual bound vector",
            "affected_rows": "EQ661_2;EQ661_5;EQ661_6",
            "observable_link": "PPN gamma,beta,alpha_i;clocks;orbital precession",
            "current_status": "not_scored",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OB661_8_multiplier_cheat_guard",
            "obstruction": "an equality multiplier can force the desired closure without explaining why nature owns it",
            "exact_failure": "formal consistency would be bought by inserting the answer",
            "required_parent_input": "independent topological, Ward, gauge, or source-measure origin for the equality constraint",
            "affected_rows": "EQ661_4",
            "observable_link": "theory credibility;local-GR claim discipline",
            "current_status": "forbidden_as_derivation",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_or_stress_template_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "template_id": "BS661_0_equality_residual_integral",
            "quantity": "R_eq_integral",
            "definition": "integral_A dR_eq where R_eq = Pi_M J_H - J_M_top - dB_zero",
            "units": "source_current_flux_units_to_be_sourced",
            "source_requirement": "real parent or phenomenological residual extraction with system_id, radius interval, norm convention, and uncertainty",
            "linked_obstructions": "OB661_0;OB661_4;OB661_5",
            "observable_link": "epsilon_radial_Meff;R10;R11;local source-normalization",
            "current_status": "MISSING_NUMERIC_RESIDUAL_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "BS661_1_boundary_improvement_flux",
            "quantity": "B_zero_flux",
            "definition": "integral_boundary dB_zero or equivalent compact boundary charge correction",
            "units": "mass_or_GM_equivalent_units_to_be_sourced",
            "source_requirement": "zero-flux theorem or sourced boundary-charge coefficient",
            "linked_obstructions": "OB661_3;OB661_6",
            "observable_link": "orbital GM;Poisson/Gauss calibration",
            "current_status": "MISSING_BOUNDARY_ZERO_PROOF_OR_BOUND_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "BS661_2_hidden_exchange_integral",
            "quantity": "I_extra_channel",
            "definition": "integral_A Pi_M dJ_extra split by legal owner and hidden/non-EH sector",
            "units": "source_current_flux_units_to_be_sourced",
            "source_requirement": "channelwise owner, projection, units, sign, and uncertainty",
            "linked_obstructions": "OB661_4",
            "observable_link": "R10;PPN;cosmology/local decoupling",
            "current_status": "MISSING_CHANNEL_RESIDUAL_INPUTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "BS661_3_worldtube_domain_shift",
            "quantity": "Delta_worldtube_domain",
            "definition": "change in Q_M or M_eff induced by allowed compact-source worldtube/domain choices",
            "units": "dimensionless_fractional_mass_or_GM_shift",
            "source_requirement": "covariant domain selector proof or numerical domain-sensitivity bound",
            "linked_obstructions": "OB661_1;OB661_2;OB661_7",
            "observable_link": "PPN;orbital;clock;WEP",
            "current_status": "MISSING_DOMAIN_SELECTOR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "BS661_4_epsilon_equality",
            "quantity": "epsilon_eq_Meff",
            "definition": "epsilon_eq[r1,r2] = c_M/M_eff_ref * (R_eq_integral + B_zero_flux + I_extra_channel + Delta_worldtube_domain)",
            "units": "dimensionless",
            "source_requirement": "all component rows numeric, unit-consistent, source-backed, and uncertainty-bearing",
            "linked_obstructions": "OB661_0;OB661_1;OB661_3;OB661_4;OB661_5;OB661_6",
            "observable_link": "R10 alpha/lambda;R11 source normalization;local PPN residuals",
            "current_status": "MISSING_COMPONENT_INPUTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "BS661_5_projector_stress_crosswalk",
            "quantity": "projector_stress_vector",
            "definition": "carry forward 660 TPS rows when equality or chain-map proof is absent",
            "units": "mixed_dimension_template_from_660",
            "source_requirement": "replace MISSING_PARENT_INPUT rows with sourced coefficients before scoring",
            "linked_obstructions": "OB661_5;OB661_7",
            "observable_link": "R10;PPN;clocks;orbital tests",
            "current_status": "INHERITED_NONCLAIM_TEMPLATE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G661_0_target_written",
            "gate": "exact equality target includes R_eq and boundary improvement",
            "result": "pass",
            "detail": "Pi_M J_H = J_M_top + dB_zero + R_eq is recorded as target, not as theorem",
            "claim_effect": "no promotion",
            "generated_utc": now,
        },
        {
            "gate_id": "G661_1_closed_top_current",
            "gate": "closed topological current retained",
            "result": "pass",
            "detail": "J_M_top remains a conditional closed current if Q_M and omega_M_top are parent-owned",
            "claim_effect": "wrong-object risk remains",
            "generated_utc": now,
        },
        {
            "gate_id": "G661_2_best_route_selected",
            "gate": "best non-cheat derivation route selected",
            "result": "pass",
            "detail": "define Q_M from same parent Hilbert source worldtube before readout",
            "claim_effect": "next derivation target fixed",
            "generated_utc": now,
        },
        {
            "gate_id": "G661_3_Hilbert_equality_parent_signed",
            "gate": "Hilbert/topological equality parent signed",
            "result": "blocked_as_expected",
            "detail": "worldtube selector, source measure, boundary flux, hidden exchange, and commutator stress remain unsigned",
            "claim_effect": "blocks closed Hilbert flux and local GR",
            "generated_utc": now,
        },
        {
            "gate_id": "G661_4_multiplier_guard",
            "gate": "late equality multiplier is not allowed as derivation",
            "result": "pass",
            "detail": "S_glue is recorded only as closure unless it gets independent parent ownership",
            "claim_effect": "prevents smuggled Newton closure",
            "generated_utc": now,
        },
        {
            "gate_id": "G661_5_bound_template",
            "gate": "fallback residual/stress template exists",
            "result": "pass_nonclaim",
            "detail": "R_eq, boundary, hidden exchange, domain shift, epsilon_eq, and projector-stress rows are staged with missing inputs",
            "claim_effect": "scoreability scaffold only",
            "generated_utc": now,
        },
        {
            "gate_id": "G661_6_calibration_not_promoted",
            "gate": "measured GM and Poisson/Gauss calibration not promoted",
            "result": "pass",
            "detail": "boundary/Hilbert/Gauss/orbital dictionary remains downstream and conditional",
            "claim_effect": "blocks Newton/source-normalization claim",
            "generated_utc": now,
        },
        {
            "gate_id": "G661_7_claim_guard",
            "gate": "no R10, R11, PPN, Newton, or local-GR claim",
            "result": "pass",
            "detail": CLAIM_CEILING,
            "claim_effect": "private theorem audit only",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D661_0_equality",
            "status": "not_derived",
            "meaning": "the closed topological current has still not been proved equal to the observed Hilbert Pi_M mass current",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D661_1_best_route",
            "status": "worldtube_source_measure_glue",
            "meaning": "the cleanest route is to make Q_M the parent Hilbert compact-source charge before readout, not a late fitted label",
            "claim_status": "false",
            "next_action": "derive a covariant Hilbert worldtube/source-measure selector or explicitly bound the equality residual",
            "generated_utc": now,
        },
        {
            "decision_id": "D661_2_stress_fallback",
            "status": "template_written_not_filled",
            "meaning": "if the glue theorem fails, carry R_eq, boundary flux, hidden exchange, domain shift, and projector stress into a sourced bound runner",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D661_3_local_GR",
            "status": "blocked",
            "meaning": "local GR remains blocked because equality, source normalization, calibration, and PPN stability are not parent-signed",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows(
    equality_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    blocked_gates = [row["gate_id"] for row in gate_rows if row["result"] in {"blocked_as_expected", "pass_nonclaim"}]
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "equality_attempt_rows": str(len(equality_rows)),
            "obstruction_rows": str(len(obstruction_rows)),
            "bound_or_stress_rows": str(len(template_rows)),
            "blocked_or_nonclaim_scoreability_gates": ";".join(blocked_gates),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def validation_rows(
    source_rows: list[dict[str, str]],
    equality_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": now,
            }
        )

    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    add("V661_0_sources_exist", not missing_sources, "missing=" + ";".join(missing_sources))

    validation_660 = read_csv(SOURCE_PATHS["660_validation"])
    prior_failures = [row.get("check_id", "?") for row in validation_660 if row.get("result") != "pass"]
    add("V661_1_prior_660_validation_clean", not prior_failures, "prior_failures=" + ";".join(prior_failures))

    all_valid_flags = [
        row.get("valid_for_claim")
        for row_group in (equality_rows, obstruction_rows, template_rows)
        for row in row_group
    ]
    add("V661_2_no_claim_rows", all(flag == "false" for flag in all_valid_flags), "valid_for_claim_flags=" + ";".join(sorted(set(all_valid_flags))))

    equality_target = [
        row
        for row in equality_rows
        if row["attempt_id"] == "EQ661_0_target_identity" and "R_eq" in row["equation_or_clause"]
    ]
    add("V661_3_equality_target_contains_residual", len(equality_target) == 1, "target_rows=" + str(len(equality_target)))

    best_route = [row for row in equality_rows if row["attempt_id"] == "EQ661_2_worldtube_charge_route"]
    add("V661_4_best_noncheat_route_selected", len(best_route) == 1, "best_route_rows=" + str(len(best_route)))

    obstruction_ids = {row["obstruction_id"] for row in obstruction_rows}
    required_obstructions = {
        "OB661_0_independent_topological_label",
        "OB661_1_worldtube_domain_selector",
        "OB661_2_source_measure_and_frame",
        "OB661_3_boundary_improvement_flux",
        "OB661_4_hidden_exchange_current",
        "OB661_5_projector_commutator_stress",
        "OB661_6_universal_calibration",
        "OB661_7_second_order_and_PPN_stability",
        "OB661_8_multiplier_cheat_guard",
    }
    add(
        "V661_5_obstruction_coverage",
        required_obstructions.issubset(obstruction_ids),
        "covered=" + ";".join(sorted(obstruction_ids)),
    )

    missing_templates = [
        row["template_id"]
        for row in template_rows
        if "MISSING" in row["current_status"] or row["current_status"] == "INHERITED_NONCLAIM_TEMPLATE"
    ]
    add("V661_6_bound_stress_templates_unfilled_nonclaim", len(missing_templates) == len(template_rows), "template_rows=" + str(len(template_rows)))

    gate_ids = {row["gate_id"] for row in gate_rows}
    required_gates = {"G661_3_Hilbert_equality_parent_signed", "G661_4_multiplier_guard", "G661_7_claim_guard"}
    add("V661_7_gate_coverage", required_gates.issubset(gate_ids), "gate_ids=" + ";".join(sorted(gate_ids)))

    blocked_gate = [
        row
        for row in gate_rows
        if row["gate_id"] == "G661_3_Hilbert_equality_parent_signed" and row["result"] == "blocked_as_expected"
    ]
    add("V661_8_parent_equality_not_signed", len(blocked_gate) == 1, "blocked_gate_rows=" + str(len(blocked_gate)))

    multiplier_guard = [
        row
        for row in equality_rows
        if row["attempt_id"] == "EQ661_4_parent_glue_multiplier" and "rejected" in row["current_status"]
    ]
    add("V661_9_multiplier_cheat_rejected", len(multiplier_guard) == 1, "multiplier_guard_rows=" + str(len(multiplier_guard)))

    next_target_rows = [row for row in decision if row["next_action"] == NEXT_TARGET or row["status"] == "worldtube_source_measure_glue"]
    add("V661_10_next_target_selected", bool(next_target_rows), NEXT_TARGET)

    changed = formalization_changed_after_cutoff()
    add("V661_11_formalization_workbench_untouched", changed == 0, "formalization_changed_after_cutoff=" + str(changed))

    add("V661_12_doc_scope_post_checkpoint", str(DOC_PATH).startswith(str(ROOT)), "doc_path=" + str(DOC_PATH))

    add("V661_13_status_nonclaim", "no_local_GR_claim" in CLAIM_CEILING and STATUS.endswith("nonclaim"), STATUS)

    return rows


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    equality_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 661 - Y5 R10 Topological Hilbert Current Equality Or Projector Stress Fill

## Verdict

The derivation swing does not close yet. The clean target remains

```text
Pi_M J_H = J_M_top + dB_zero + R_eq.
```

`J_M_top` can be a closed topological current, but 661 still cannot prove it is the observed Hilbert mass current. The best route is not a late equality multiplier; it is to define `Q_M` from the same parent Hilbert compact-source worldtube before readout. That parent worldtube/source-measure glue is still missing, so the local branch remains nonclaim.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Equality Attempt

{markdown_table(equality_rows, ["attempt_id", "route", "equation_or_clause", "current_status", "current_blocker", "valid_for_claim"])}

## Equality Obstruction Audit

{markdown_table(obstruction_rows, ["obstruction_id", "obstruction", "exact_failure", "required_parent_input", "current_status", "valid_for_claim"])}

## Bound Or Stress Template

{markdown_table(template_rows, ["template_id", "quantity", "definition", "current_status", "observable_link", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "detail", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "equality_attempt_rows", "obstruction_rows", "bound_or_stress_rows", "blocked_or_nonclaim_scoreability_gates", "validation_failures", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is a useful failure, not a dead failure. We have narrowed the local-GR bottleneck to a precise object-identity problem:

```text
closed topological source current = observed Hilbert mass current
```

The theory is not allowed to win by declaring that equality. It must either derive the parent source-worldtube measure that makes the two currents the same object, or carry the residual `R_eq`, boundary improvement, hidden exchange, domain shift, and projector stress into a sourced bound runner.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    equality_rows = equality_attempt_rows()
    obstruction_rows = equality_obstruction_rows()
    template_rows = bound_or_stress_template_rows()
    gate_rows = scoreability_gate_rows()
    decision = decision_rows()
    validation = validation_rows(source_rows, equality_rows, obstruction_rows, template_rows, gate_rows, decision)
    summary_rows = nonclaim_summary_rows(equality_rows, obstruction_rows, template_rows, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_661_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_661_EQUALITY_ATTEMPT.csv",
        equality_rows,
        [
            "attempt_id",
            "route",
            "equation_or_clause",
            "derivation_value",
            "current_status",
            "current_blocker",
            "source_paths",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_661_EQUALITY_OBSTRUCTION_AUDIT.csv",
        obstruction_rows,
        [
            "obstruction_id",
            "obstruction",
            "exact_failure",
            "required_parent_input",
            "affected_rows",
            "observable_link",
            "current_status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_661_BOUND_OR_STRESS_TEMPLATE.csv",
        template_rows,
        [
            "template_id",
            "quantity",
            "definition",
            "units",
            "source_requirement",
            "linked_obstructions",
            "observable_link",
            "current_status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_661_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_661_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_661_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "equality_attempt_rows",
            "obstruction_rows",
            "bound_or_stress_rows",
            "blocked_or_nonclaim_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_661_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(source_rows, equality_rows, obstruction_rows, template_rows, gate_rows, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"equality_attempt_rows={len(equality_rows)}")
    print(f"obstruction_rows={len(obstruction_rows)}")
    print(f"bound_or_stress_rows={len(template_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

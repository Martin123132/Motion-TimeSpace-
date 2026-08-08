from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_Hilbert_worldtube_source_measure_glue_conditional_theorem_written_parent_unsigned_residual_bound_template_nonclaim"
CLAIM_CEILING = "Hilbert_worldtube_glue_gate_only_no_closed_Hilbert_flux_no_source_normalized_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "661_doc": ROOT / "661-Y5-R10-topological-Hilbert-current-equality-or-projector-stress-fill.md",
    "661_validation": RESIDUALS / "P8_Y5_BRR545_661_VALIDATION.csv",
    "661_equality_attempt": RESIDUALS / "P8_Y5_R10_661_EQUALITY_ATTEMPT.csv",
    "661_obstruction_audit": RESIDUALS / "P8_Y5_R10_661_EQUALITY_OBSTRUCTION_AUDIT.csv",
    "661_bound_template": RESIDUALS / "P8_Y5_R10_661_BOUND_OR_STRESS_TEMPLATE.csv",
    "537_doc": ROOT / "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
    "536_doc": ROOT / "536-Y5-Hilbert-worldtube-glue-theorem-or-PiM-input-audit.md",
    "510_doc": ROOT / "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
    "450_doc": ROOT / "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
    "458_doc": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "HWT536_attempt": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
    "HWG535_certificate": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
    "PAC537_contract": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
    "WT510_theorem": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "WT510_clauses": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
    "WT510_proof": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
    "Hilbert_monopole": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "source_measure_residual_map": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
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
        "661_doc": "immediate equality failure and next target",
        "661_validation": "prior validation clean/nonclaim status",
        "661_equality_attempt": "topological-Hilbert equality rows to be glued or bounded",
        "661_obstruction_audit": "worldtube, measure, boundary, hidden exchange, commutator, calibration blockers",
        "661_bound_template": "residual/stress components inherited if glue fails",
        "537_doc": "parent-action contract for Hilbert worldtube glue",
        "536_doc": "Hilbert-worldtube theorem attempt and Pi_M input audit",
        "510_doc": "GR/EH-style worldtube source-measure reference theorem",
        "450_doc": "Hilbert source to measured monopole calibration gate",
        "458_doc": "Hamiltonian charge to Poisson/Gauss calibration gate",
        "523_doc": "Gauss/orbital source-normalization residual scorecard",
        "HWT536_attempt": "machine theorem-step rows for Hilbert worldtube glue",
        "HWG535_certificate": "certificate rows still missing from the worldtube route",
        "PAC537_contract": "parent action clauses needed to derive HWT536",
        "WT510_theorem": "EH-style conditional theorem and MTS transfer condition",
        "WT510_clauses": "worldtube source-measure clause statuses",
        "WT510_proof": "Noether/Stokes proof sketch for dressed charge",
        "Hilbert_monopole": "measured-GM calibration blockers downstream of glue",
        "source_measure_residual_map": "residual map for missing source-measure theorem",
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


def conditional_glue_theorem_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "theorem_id": "TH662_0_conditional_same_object_theorem",
            "statement": "If the parent action owns a compact Hilbert source worldtube, the observed Hilbert measure, a dressed Noether/Hamiltonian source charge, a fixed Pi_M chain map, a matching topological Poincare-dual representative, zero reference/boundary improvement flux, and silent extra-sector charge, then Pi_M J_H equals J_M_top up to zero-boundary exact terms.",
            "mathematical_form": "Q_H[W]=H_tau[S]-H_ref=(4*pi*G_ref)^-1 int_S Pi_M J_H; J_M_top=Q_H[W] PD(W); Pi_M J_H=J_M_top+dB_zero with int_boundary dB_zero=0",
            "what_it_derives_if_signed": "R_eq=0, fixed worldtube source charge, no conserved-wrong-object failure, and a candidate closed Hilbert mass flux",
            "current_MTS_status": "conditional_theorem_only_parent_clauses_unsigned",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "536_doc", "537_doc", "661_doc"),
            "generated_utc": now,
        },
        {
            "theorem_id": "TH662_1_dressed_charge_guardrail",
            "statement": "The source measure cannot be bare rest mass if the goal is gravitational source normalization; it must be the dressed parent Hamiltonian/Noether charge including owned binding, boundary, and field contributions.",
            "mathematical_form": "M_source[W] := H_tau[S_outer]-H_tau[reference], not M_bare:=int_W rho_rest dV",
            "what_it_derives_if_signed": "prevents false equality between matter bookkeeping mass and measured gravitational source mass",
            "current_MTS_status": "definition_guardrail_adopted_not_calibrated",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "WT510_theorem", "PAC537_contract"),
            "generated_utc": now,
        },
        {
            "theorem_id": "TH662_2_residual_identity_when_unsigned",
            "statement": "When any parent glue clause remains unsigned, equality must be replaced by an exact residual identity with no cancellation-only credit.",
            "mathematical_form": "R_glue := Pi_M J_H - J_M_top - dB_zero = R_worldtube + R_measure + R_PiM + R_top + R_boundary + R_extra",
            "what_it_derives_if_signed": "a finite residual-bound problem rather than a hidden closure axiom",
            "current_MTS_status": "residual_identity_written_not_numeric",
            "valid_for_claim": "false",
            "source_paths": source_list("661_bound_template", "source_measure_residual_map", "HWT536_attempt"),
            "generated_utc": now,
        },
    ]


def proof_chain_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "step_id": "P662_0_parent_variation",
            "step": "Start from a diffeomorphism-covariant parent action with a covariant symplectic potential.",
            "equation": "delta L = E_A delta Phi^A + dTheta(Phi,delta Phi)",
            "dependency": "PAC537_0;WG510_0",
            "current_status": "formal_reference_step_available",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "P662_1_observed_source_current",
            "step": "Define the Hilbert/coframe source current in the same observed frame used by clocks, rods, and orbital readout.",
            "equation": "J_H[tau] := (delta S_matter/delta e_obs) contracted with tau",
            "dependency": "PAC537_1;HWT536_1;HM0",
            "current_status": "same_frame_measure_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "P662_2_worldtube_support",
            "step": "Select the compact source worldtube from parent source support before any fitted mass or radius readout.",
            "equation": "W_source := supp(J_H[tau]); S_1,S_2 link the same W_source",
            "dependency": "PAC537_2;HWT536_0;OB661_1",
            "current_status": "worldtube_selector_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "P662_3_Noether_charge",
            "step": "Use the parent Noether current to define a dressed exterior charge on linking surfaces.",
            "equation": "J_tau = Theta(Phi,L_tau Phi) - tau dot L = dQ_tau + C_tau",
            "dependency": "T510_0;P510_1;P510_2;PAC537_0",
            "current_status": "GR_style_reference_available_MTS_transfer_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "P662_4_Stokes_linking",
            "step": "Integrate between two linked surfaces and require exterior constraints and side fluxes to vanish or be retained.",
            "equation": "int_S2 Q_tau - int_S1 Q_tau = int_A C_tau + int_boundary_flux",
            "dependency": "P510_3;P510_4;PAC537_6;OB661_3",
            "current_status": "conditional_reference_boundary_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "P662_5_PiM_chain_map",
            "step": "Identify the surface charge with the Pi_M-projected Hilbert current using a parent-owned chain map.",
            "equation": "(4*pi*G_ref)^-1 int_S Pi_M J_H = H_tau[S]-H_ref",
            "dependency": "PAC537_4;HWT536_3;OB661_5",
            "current_status": "PiM_owner_and_commutator_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "P662_6_topological_PD_match",
            "step": "Choose the topological representative as the Poincare-dual representative of the same Hilbert source worldtube, not as an independent label.",
            "equation": "J_M_top := Q_H[W] PD(W_source), with int_link(W_source) omega_M_top=1",
            "dependency": "HWT536_4;HWG535_2;OB661_0",
            "current_status": "topological_same_object_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "P662_7_residual_branch",
            "step": "If any clause fails, carry every difference into R_glue and bound it against local/R10/R11 locks.",
            "equation": "epsilon_glue = c_M/M_ref * integral_A dR_glue",
            "dependency": "661_bound_template;SMR509;HWT536",
            "current_status": "template_written_not_filled",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def parent_clause_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "CL662_0_covariant_parent_action",
            "required_clause": "explicit diffeomorphism-covariant parent action with symplectic potential",
            "math_form": "delta L=E_A delta Phi^A+dTheta",
            "closes_steps": "P662_0;P662_3",
            "current_status": "contract_only_no_full_Lagrangian",
            "failure_mode": "worldtube charge is postulated rather than derived",
            "residual_if_missing": "R_action",
            "valid_for_claim": "false",
            "source_paths": source_list("PAC537_contract", "WT510_clauses"),
            "generated_utc": now,
        },
        {
            "clause_id": "CL662_1_same_observed_source_frame",
            "required_clause": "matter couples to one observed metric/coframe used by source, clocks, rods, and orbital readout",
            "math_form": "S_matter=S_matter[e_obs,psi_m]",
            "closes_steps": "P662_1",
            "current_status": "not_yet_derived",
            "failure_mode": "source mass and orbital mass can differ by frame choice",
            "residual_if_missing": "R_measure;Delta_frame",
            "valid_for_claim": "false",
            "source_paths": source_list("PAC537_contract", "Hilbert_monopole"),
            "generated_utc": now,
        },
        {
            "clause_id": "CL662_2_parent_fixed_worldtube",
            "required_clause": "compact support and linking surfaces are fixed by source support before fitted readout",
            "math_form": "W_source=supp(J_H); S_1,S_2 link W_source",
            "closes_steps": "P662_2",
            "current_status": "not_yet_derived",
            "failure_mode": "mass channel can be retuned per radius/system",
            "residual_if_missing": "R_worldtube;Delta_worldtube_domain",
            "valid_for_claim": "false",
            "source_paths": source_list("HWT536_attempt", "HWG535_certificate", "661_obstruction_audit"),
            "generated_utc": now,
        },
        {
            "clause_id": "CL662_3_dressed_charge_definition",
            "required_clause": "source charge is dressed Hamiltonian/Noether charge, not bare rest mass",
            "math_form": "M_source[W]=H_tau[S]-H_ref",
            "closes_steps": "P662_3;P662_4",
            "current_status": "guardrail_adopted_not_MTS_derived",
            "failure_mode": "binding/reference/field energy can be silently dropped",
            "residual_if_missing": "R_dressing;Delta_symp",
            "valid_for_claim": "false",
            "source_paths": source_list("WT510_theorem", "PAC537_contract"),
            "generated_utc": now,
        },
        {
            "clause_id": "CL662_4_action_owned_PiM_chain_map",
            "required_clause": "Pi_M is fixed by the parent algebra and commutes with d on the Hilbert source-current complex",
            "math_form": "Pi_M^2=Pi_M; [d,Pi_M]J_H=0; int_S Pi_M J_H = 4*pi*G_ref(H_tau-H_ref)",
            "closes_steps": "P662_5",
            "current_status": "not_derived",
            "failure_mode": "Pi_M is an empirical mass selector or retains projector stress",
            "residual_if_missing": "R_PiM;I_commutator;T_PiM",
            "valid_for_claim": "false",
            "source_paths": source_list("PAC537_contract", "661_obstruction_audit"),
            "generated_utc": now,
        },
        {
            "clause_id": "CL662_5_topological_same_worldtube",
            "required_clause": "topological representative is the Poincare-dual representative of the same Hilbert worldtube",
            "math_form": "J_M_top=Q_H[W]PD(W_source), not Q_independent omega_independent",
            "closes_steps": "P662_6",
            "current_status": "not_derived",
            "failure_mode": "closed topological current conserves the wrong object",
            "residual_if_missing": "R_top",
            "valid_for_claim": "false",
            "source_paths": source_list("661_equality_attempt", "HWT536_attempt"),
            "generated_utc": now,
        },
        {
            "clause_id": "CL662_6_reference_boundary_zero",
            "required_clause": "reference, exact improvement, and compact boundary terms have zero linked flux or sourced coefficients",
            "math_form": "int_boundary dB_zero=0; Delta_symp=0; H_ref fixed once",
            "closes_steps": "P662_4;P662_7",
            "current_status": "missing_certificate_or_bound",
            "failure_mode": "surface charge equality is shifted by boundary bookkeeping",
            "residual_if_missing": "R_boundary;B_zero_flux",
            "valid_for_claim": "false",
            "source_paths": source_list("HWG535_certificate", "661_bound_template"),
            "generated_utc": now,
        },
        {
            "clause_id": "CL662_7_extra_sector_mass_silence",
            "required_clause": "non-EH, memory, domain, motion, time, range, boundary, and frame sectors carry no independent local mass charge",
            "math_form": "Delta_extra=Delta_nonEH=Delta_frame=0 or source-backed below local locks",
            "closes_steps": "P662_4;P662_7",
            "current_status": "field_specific_queue_open",
            "failure_mode": "hidden channels repair fits while breaking local GR",
            "residual_if_missing": "R_extra;Delta_extra_vector",
            "valid_for_claim": "false",
            "source_paths": source_list("source_measure_residual_map", "523_doc"),
            "generated_utc": now,
        },
        {
            "clause_id": "CL662_8_readout_and_PPN_stability",
            "required_clause": "same source charge controls the 1/r metric coefficient and survives second-order PPN expansion",
            "math_form": "g_00=-1+2G_ref M_source/r+O(r^-2); Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi}",
            "closes_steps": "P662_7",
            "current_status": "not_reached",
            "failure_mode": "leading Newton-looking charge is not local GR",
            "residual_if_missing": "Delta_cal;Delta_PPN",
            "valid_for_claim": "false",
            "source_paths": source_list("458_doc", "523_doc", "Hilbert_monopole"),
            "generated_utc": now,
        },
    ]


def residual_decomposition_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "residual_id": "RG662_0_R_worldtube",
            "definition": "failure of W_source and linking surfaces to be fixed by parent Hilbert support before readout",
            "symbol": "R_worldtube",
            "enters": "R_glue",
            "zero_condition": "CL662_2 parent fixed worldtube",
            "observable_lock": "R10;R11;PPN;orbital domain sensitivity",
            "current_status": "MISSING_PARENT_WORLDTUBE_SELECTOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RG662_1_R_measure",
            "definition": "same-frame Hilbert measure/coframe/source-current ownership failure",
            "symbol": "R_measure;Delta_frame",
            "enters": "R_glue",
            "zero_condition": "CL662_1 same observed source frame",
            "observable_lock": "WEP;clocks;PPN preferred frame",
            "current_status": "MISSING_SAME_FRAME_MEASURE_PROOF",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RG662_2_R_PiM",
            "definition": "Pi_M chain-map, commutator, or projector-stress failure",
            "symbol": "R_PiM;I_commutator;T_PiM",
            "enters": "R_glue",
            "zero_condition": "CL662_4 action-owned Pi_M chain map",
            "observable_lock": "R10;PPN gamma/beta/alpha_i;local GR",
            "current_status": "MISSING_PIM_CHAIN_MAP_OR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RG662_3_R_top",
            "definition": "topological representative is not proven to be the Poincare dual of the same Hilbert source worldtube",
            "symbol": "R_top",
            "enters": "R_glue",
            "zero_condition": "CL662_5 topological same-worldtube theorem",
            "observable_lock": "Newton/source normalization;R10;R11",
            "current_status": "MISSING_TOPOLOGICAL_SAME_OBJECT_PROOF",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RG662_4_R_boundary",
            "definition": "reference/background/exact improvement flux shifts the compact source charge",
            "symbol": "R_boundary;B_zero_flux;Delta_symp",
            "enters": "R_glue",
            "zero_condition": "CL662_6 reference and boundary zero theorem",
            "observable_lock": "orbital GM;Poisson/Gauss;R10",
            "current_status": "MISSING_BOUNDARY_ZERO_PROOF_OR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RG662_5_R_extra",
            "definition": "non-EH/domain/memory/range/connection/source channels carry independent compact mass charge",
            "symbol": "R_extra;Delta_extra_vector",
            "enters": "R_glue",
            "zero_condition": "CL662_7 extra sector mass silence",
            "observable_lock": "R10;R11;PPN;clocks;orbital",
            "current_status": "MISSING_EXTRA_SECTOR_SILENCE_OR_COEFFICIENTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RG662_6_R_readout",
            "definition": "dressed source charge does not calibrate to inverse-square orbital GM or second-order PPN source vector",
            "symbol": "Delta_cal;Delta_PPN",
            "enters": "post_glue_readout_residual",
            "zero_condition": "CL662_8 readout and PPN stability",
            "observable_lock": "Newton;PPN;local GR",
            "current_status": "NOT_REACHED_UNTIL_GLUE_CLOSES",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_input_template_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "input_id": "BI662_0_R_glue_integral",
            "quantity": "R_glue_integral",
            "definition": "int_A dR_glue with R_glue=Pi_M J_H-J_M_top-dB_zero",
            "required_columns": "system_id;r1;r2;R_glue_integral;M_ref;units;normalization;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "source-backed non-placeholder row with unit-consistent normalization and uncertainty",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BI662_1_worldtube_domain_shift",
            "quantity": "Delta_worldtube_domain",
            "definition": "fractional change in Q_H[W] under allowed worldtube/linking-surface choices",
            "required_columns": "system_id;domain_rule;Delta_worldtube_domain;M_ref;units;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "parent selector theorem or bounded sensitivity below mapped local locks",
            "current_status": "MISSING_DOMAIN_SELECTOR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BI662_2_measure_frame_shift",
            "quantity": "Delta_frame_source",
            "definition": "same-frame Hilbert source measure mismatch between source, metric, clocks, and orbits",
            "required_columns": "system_id;frame_pair;Delta_frame_source;local_lock;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "single observed frame theorem or source-backed WEP/clock/PPN bound",
            "current_status": "MISSING_FRAME_BOUND_OR_THEOREM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BI662_3_boundary_reference_flux",
            "quantity": "B_zero_flux;Delta_symp",
            "definition": "reference, exact improvement, and symplectic boundary charge shift",
            "required_columns": "system_id;boundary_rule;B_zero_flux;Delta_symp;M_ref;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "boundary convention fixed once plus zero theorem or numeric bound",
            "current_status": "MISSING_BOUNDARY_REFERENCE_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BI662_4_PiM_commutator_stress",
            "quantity": "I_commutator;T_PiM_munu",
            "definition": "commutator integral and projector stress equivalent inherited from unsigned Pi_M chain map",
            "required_columns": "system_id;operator_family;I_commutator;projector_stress_beta_equiv;affected_PPN_rows;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "parent Pi_M chain-map proof or source-backed local-bound stress map",
            "current_status": "MISSING_PIM_BOUND_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BI662_5_extra_charge_vector",
            "quantity": "Delta_extra_vector",
            "definition": "channelwise non-EH/domain/memory/range/connection/motion/time/boundary/frame compact mass charge",
            "required_columns": "system_id;channel;Delta_charge;M_ref;local_lock;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "each channel theorem-zero or individually below lock; no cancellation-only envelope",
            "current_status": "MISSING_CHANNEL_COEFFICIENTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BI662_6_epsilon_glue",
            "quantity": "epsilon_glue_Meff",
            "definition": "epsilon_glue = c_M/M_ref * int_A dR_glue plus listed component shifts",
            "required_columns": "system_id;epsilon_glue;component_sum_abs;M_ref;normalization;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "all components numeric/source-backed or theorem-zero before any R10/R11/local use",
            "current_status": "MISSING_COMPONENT_INPUTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G662_0_conditional_theorem_written",
            "gate": "same-object worldtube glue theorem is written conditionally",
            "result": "pass",
            "detail": "the theorem states exactly when Q_H[W], Pi_M J_H, and J_M_top become the same object",
            "claim_effect": "no promotion without signed premises",
            "generated_utc": now,
        },
        {
            "gate_id": "G662_1_dressed_charge_guardrail",
            "gate": "bare rest mass is not used as gravitational source charge",
            "result": "pass",
            "detail": "M_source is treated as dressed Hamiltonian/Noether charge",
            "claim_effect": "prevents false measured-GM claim",
            "generated_utc": now,
        },
        {
            "gate_id": "G662_2_parent_clause_status",
            "gate": "all parent glue clauses are audited",
            "result": "blocked_as_expected",
            "detail": "worldtube selector, same-frame measure, Pi_M chain map, topological match, boundary zero, extra silence, and PPN readout remain unsigned",
            "claim_effect": "blocks closed Hilbert flux and local GR",
            "generated_utc": now,
        },
        {
            "gate_id": "G662_3_no_multiplier_or_definition_cheat",
            "gate": "equality is not imposed by a late multiplier or definition swap",
            "result": "pass",
            "detail": "the only legal proof path is parent variation plus Noether/Stokes plus same-worldtube topological representative",
            "claim_effect": "keeps derivation discipline",
            "generated_utc": now,
        },
        {
            "gate_id": "G662_4_residual_decomposition_written",
            "gate": "unsigned clauses map to R_glue components",
            "result": "pass_nonclaim",
            "detail": "R_worldtube, R_measure, R_PiM, R_top, R_boundary, R_extra, and readout/PPN residuals are separated",
            "claim_effect": "scoreability scaffold only",
            "generated_utc": now,
        },
        {
            "gate_id": "G662_5_bound_inputs_unfilled",
            "gate": "residual-bound rows stay unfilled and nonclaim",
            "result": "pass_nonclaim",
            "detail": "all BI662 rows carry MISSING status and valid_for_claim=false",
            "claim_effect": "no R10/R11/local pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G662_6_downstream_calibration_not_promoted",
            "gate": "measured-GM/Newton/PPN calibration not promoted",
            "result": "pass",
            "detail": "even successful glue would still need Gauss/orbital and second-order PPN readout",
            "claim_effect": "blocks local GR overclaim",
            "generated_utc": now,
        },
        {
            "gate_id": "G662_7_claim_guard",
            "gate": "no R10, R11, PPN, Newton, or local-GR claim",
            "result": "pass",
            "detail": CLAIM_CEILING,
            "claim_effect": "private derivation audit only",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D662_0_theorem_route",
            "status": "conditional_same_object_theorem_written",
            "meaning": "there is a real GR-style Noether/Stokes route to make the worldtube source charge and exterior Hilbert charge the same object if the parent clauses are signed",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D662_1_current_MTS_status",
            "status": "parent_unsigned",
            "meaning": "current MTS has not yet derived the worldtube selector, same-frame measure, Pi_M chain map, topological same-worldtube match, boundary zero, extra-sector silence, or PPN readout",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D662_2_bound_route",
            "status": "residual_bound_template_written",
            "meaning": "if the next Euler/Ward variation does not close, R_glue and its components are ready to become source-backed bound inputs",
            "claim_status": "false",
            "next_action": "fill BI662 rows only with real theorem-zero or sourced numeric inputs",
            "generated_utc": now,
        },
        {
            "decision_id": "D662_3_local_GR",
            "status": "blocked",
            "meaning": "local GR is still blocked; 662 improves the spine by making the same-object requirement exact, not by claiming it",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows(
    theorem_rows: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
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
            "conditional_theorem_rows": str(len(theorem_rows)),
            "proof_chain_rows": str(len(proof_rows)),
            "parent_clause_rows": str(len(clause_rows)),
            "residual_rows": str(len(residual_rows)),
            "bound_input_rows": str(len(input_rows)),
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
    theorem_rows: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
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
    add("V662_0_sources_exist", not missing_sources, "missing=" + ";".join(missing_sources))

    validation_661 = read_csv(SOURCE_PATHS["661_validation"])
    prior_failures = [row.get("check_id", "?") for row in validation_661 if row.get("result") != "pass"]
    add("V662_1_prior_661_validation_clean", not prior_failures, "prior_failures=" + ";".join(prior_failures))

    all_valid_flags = [
        row.get("valid_for_claim")
        for row_group in (theorem_rows, proof_rows, clause_rows, residual_rows, input_rows)
        for row in row_group
    ]
    add("V662_2_no_claim_rows", all(flag == "false" for flag in all_valid_flags), "valid_for_claim_flags=" + ";".join(sorted(set(all_valid_flags))))

    same_object = [row for row in theorem_rows if row["theorem_id"] == "TH662_0_conditional_same_object_theorem" and "Pi_M J_H" in row["mathematical_form"] and "J_M_top" in row["mathematical_form"]]
    add("V662_3_conditional_same_object_theorem_written", len(same_object) == 1, "same_object_rows=" + str(len(same_object)))

    proof_steps = {row["step_id"] for row in proof_rows}
    required_proof = {"P662_0_parent_variation", "P662_3_Noether_charge", "P662_4_Stokes_linking", "P662_5_PiM_chain_map", "P662_6_topological_PD_match", "P662_7_residual_branch"}
    add("V662_4_proof_chain_coverage", required_proof.issubset(proof_steps), "proof_steps=" + ";".join(sorted(proof_steps)))

    clause_ids = {row["clause_id"] for row in clause_rows}
    required_clauses = {f"CL662_{index}_{suffix}" for index, suffix in [
        (0, "covariant_parent_action"),
        (1, "same_observed_source_frame"),
        (2, "parent_fixed_worldtube"),
        (3, "dressed_charge_definition"),
        (4, "action_owned_PiM_chain_map"),
        (5, "topological_same_worldtube"),
        (6, "reference_boundary_zero"),
        (7, "extra_sector_mass_silence"),
        (8, "readout_and_PPN_stability"),
    ]}
    add("V662_5_parent_clause_coverage", required_clauses.issubset(clause_ids), "clause_ids=" + ";".join(sorted(clause_ids)))

    residual_ids = {row["residual_id"] for row in residual_rows}
    required_residuals = {"RG662_0_R_worldtube", "RG662_1_R_measure", "RG662_2_R_PiM", "RG662_3_R_top", "RG662_4_R_boundary", "RG662_5_R_extra", "RG662_6_R_readout"}
    add("V662_6_residual_decomposition_coverage", required_residuals.issubset(residual_ids), "residual_ids=" + ";".join(sorted(residual_ids)))

    missing_inputs = [row["input_id"] for row in input_rows if "MISSING" in row["current_status"]]
    add("V662_7_bound_inputs_unfilled_nonclaim", len(missing_inputs) == len(input_rows), "input_rows=" + str(len(input_rows)))

    residual_formula = [row for row in theorem_rows if row["theorem_id"] == "TH662_2_residual_identity_when_unsigned" and "R_glue" in row["mathematical_form"]]
    add("V662_8_R_glue_formula_written", len(residual_formula) == 1, "R_glue_rows=" + str(len(residual_formula)))

    blocked_gate = [row for row in gate_rows if row["gate_id"] == "G662_2_parent_clause_status" and row["result"] == "blocked_as_expected"]
    add("V662_9_parent_unsigned_gate_blocks_claim", len(blocked_gate) == 1, "blocked_gate_rows=" + str(len(blocked_gate)))

    guardrail_gate = [row for row in gate_rows if row["gate_id"] == "G662_1_dressed_charge_guardrail" and row["result"] == "pass"]
    add("V662_10_dressed_charge_guardrail", len(guardrail_gate) == 1, "guardrail_rows=" + str(len(guardrail_gate)))

    next_target_rows = [row for row in decision if row["next_action"] == NEXT_TARGET]
    add("V662_11_next_target_selected", bool(next_target_rows), NEXT_TARGET)

    changed = formalization_changed_after_cutoff()
    add("V662_12_formalization_workbench_untouched", changed == 0, "formalization_changed_after_cutoff=" + str(changed))

    add("V662_13_status_nonclaim", "no_source_normalized_Newton" in CLAIM_CEILING and STATUS.endswith("nonclaim"), STATUS)

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
    theorem_rows: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 662 - Y5 R10 Hilbert Worldtube Source-Measure Glue Or Equality Residual Bound

## Verdict

The theorem route is real but still conditional. A GR-style parent action can make the compact source worldtube charge and exterior Hilbert charge the same object through Noether/Stokes machinery, but current MTS has not yet signed the parent clauses needed to inherit that theorem.

The sharp conditional target is:

```text
Q_H[W] = H_tau[S] - H_ref = (4*pi*G_ref)^-1 int_S Pi_M J_H
J_M_top = Q_H[W] PD(W_source)
Pi_M J_H = J_M_top + dB_zero
```

If any clause fails, the branch must use:

```text
R_glue := Pi_M J_H - J_M_top - dB_zero
       = R_worldtube + R_measure + R_PiM + R_top + R_boundary + R_extra.
```

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Conditional Glue Theorem

{markdown_table(theorem_rows, ["theorem_id", "statement", "mathematical_form", "current_MTS_status", "valid_for_claim"])}

## Proof Chain

{markdown_table(proof_rows, ["step_id", "step", "equation", "dependency", "current_status", "valid_for_claim"])}

## Parent Clause Audit

{markdown_table(clause_rows, ["clause_id", "required_clause", "math_form", "current_status", "failure_mode", "residual_if_missing", "valid_for_claim"])}

## Residual Decomposition

{markdown_table(residual_rows, ["residual_id", "definition", "symbol", "zero_condition", "observable_lock", "current_status", "valid_for_claim"])}

## Bound Input Template

{markdown_table(input_rows, ["input_id", "quantity", "definition", "required_columns", "current_status", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "detail", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "conditional_theorem_rows", "proof_chain_rows", "parent_clause_rows", "residual_rows", "bound_input_rows", "blocked_or_nonclaim_scoreability_gates", "validation_failures", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is a narrowing win. The local branch is not allowed to say "the source charge just is the topological charge." It must either derive a same-object theorem from a parent action or pay a fully itemized residual bill.

The best next derivation is the Euler/Ward variation test: can a minimal parent action actually output the worldtube selector, same-frame Hilbert measure, fixed `Pi_M` chain map, and topological Poincare-dual representative?

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = conditional_glue_theorem_rows()
    proof_rows = proof_chain_rows()
    clause_rows = parent_clause_audit_rows()
    residual_rows = residual_decomposition_rows()
    input_rows = bound_input_template_rows()
    gate_rows = scoreability_gate_rows()
    decision = decision_rows()
    validation = validation_rows(source_rows, theorem_rows, proof_rows, clause_rows, residual_rows, input_rows, gate_rows, decision)
    summary_rows = nonclaim_summary_rows(theorem_rows, proof_rows, clause_rows, residual_rows, input_rows, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_662_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_662_CONDITIONAL_GLUE_THEOREM.csv",
        theorem_rows,
        ["theorem_id", "statement", "mathematical_form", "what_it_derives_if_signed", "current_MTS_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_662_PROOF_CHAIN.csv",
        proof_rows,
        ["step_id", "step", "equation", "dependency", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv",
        clause_rows,
        ["clause_id", "required_clause", "math_form", "closes_steps", "current_status", "failure_mode", "residual_if_missing", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_662_RESIDUAL_DECOMPOSITION.csv",
        residual_rows,
        ["residual_id", "definition", "symbol", "enters", "zero_condition", "observable_lock", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv",
        input_rows,
        ["input_id", "quantity", "definition", "required_columns", "acceptance_rule", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_662_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_662_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_662_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "conditional_theorem_rows",
            "proof_chain_rows",
            "parent_clause_rows",
            "residual_rows",
            "bound_input_rows",
            "blocked_or_nonclaim_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_662_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(source_rows, theorem_rows, proof_rows, clause_rows, residual_rows, input_rows, gate_rows, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"conditional_theorem_rows={len(theorem_rows)}")
    print(f"proof_chain_rows={len(proof_rows)}")
    print(f"parent_clause_rows={len(clause_rows)}")
    print(f"residual_rows={len(residual_rows)}")
    print(f"bound_input_rows={len(input_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

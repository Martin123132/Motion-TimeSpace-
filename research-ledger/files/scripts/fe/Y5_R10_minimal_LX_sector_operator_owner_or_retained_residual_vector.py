from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_minimal_LX_operator_owner_attempted_no_source_zero_or_no_pole_retained_residual_vector_nonclaim"
CLAIM_CEILING = "minimal_LX_operator_owner_or_retained_residual_vector_only_no_FB5540_zero_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "670-Y5-R10-no-pole-quotient-LX-route-or-positive-sourcefree-operator-proof.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "506_doc": ROOT / "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
    "579_doc": ROOT / "579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md",
    "580_doc": ROOT / "580-Y5-R10-explicit-parent-X-block-ansatz-or-finite-residual-score.md",
    "615_doc": ROOT / "615-Y5-R10-explicit-parent-X-block-short-range-origin-or-range-closure.md",
    "616_doc": ROOT / "616-Y5-R10-vacuum-scale-parent-X-block-owner-or-demote-to-range-closure.md",
    "621_doc": ROOT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
    "622_doc": ROOT / "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "656_doc": ROOT / "656-Y5-R10-R11-executable-vector-minimum-skeleton-under-WEP-closure.md",
    "667_doc": ROOT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
    "668_doc": ROOT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
    "579_contract": RESIDUALS / "P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv",
    "580_candidates": RESIDUALS / "P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv",
    "506_energy_identity": RESIDUALS / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "506_silence_status": RESIDUALS / "P8_MTS_SECTOR_SILENCE_STATUS.csv",
    "667_ansatz": RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
    "667_variation": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "668_sector_audit": RESIDUALS / "P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
    "668_queue": RESIDUALS / "P8_Y5_R10_668_RESIDUAL_DEMOTION_QUEUE.csv",
    "668_impact": RESIDUALS / "P8_Y5_R10_668_FB5540_IMPACT_MAP.csv",
    "668_validation": RESIDUALS / "P8_Y5_BRR545_668_VALIDATION.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


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


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "506_doc": "extra-sector silence theorem target and positive-operator template",
        "579_doc": "parent Hessian/source-charge fill attempt",
        "580_doc": "explicit parent X-block branch ranking",
        "615_doc": "short-range origin/range closure blocker",
        "616_doc": "vacuum-scale parent X-block owner demotion",
        "621_doc": "matter-coupling normal-form theorem context",
        "622_doc": "parent matter-sector contract context",
        "655_doc": "EH operator selection and retained R11 context",
        "656_doc": "R11 executable vector context",
        "667_doc": "parent-boundary action and variation scaffold",
        "668_doc": "immediate predecessor selecting L_X as next hinge",
        "579_contract": "explicit parent X-block contract clauses",
        "580_candidates": "ranked X-block parent candidates",
        "506_energy_identity": "positive/source-free energy identity templates",
        "506_silence_status": "sector silence/open-row status",
        "667_ansatz": "parent-boundary action ansatz rows",
        "667_variation": "variation ledger rows feeding Theta and Q",
        "668_sector_audit": "sector Lagrangian owner audit",
        "668_queue": "residual demotion queue selecting L_X first",
        "668_impact": "FB5540 impact map from missing L_X",
        "668_validation": "prior checkpoint validation",
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


def minimal_lx_operator_candidate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        {
            "candidate_id": "LX669_0_absent_quotient_variable",
            "parent_block": "X is not a primitive physical field; it is a readout or coordinate artefact removed by q",
            "minimal_LX_form": "no independent L_X term; S_parent=S_obs[q(Phi)]+S_matter[psi,g_obs(q(Phi))]+S_top",
            "physical_pole_status": "none_if_parent_quotient_is_signed",
            "source_status": "no_source_because_no_independent_X_variation",
            "R10_R11_consequence": "K_X=0 and no Yukawa/PPN pole if q removes X before variation",
            "owner_status": "best_GR_reduction_route_not_derived",
            "blocker": "must prove X is absent from physical tangent space, not merely set to zero after readout",
            "recommended_rank": "1",
            "valid_for_claim": "false",
            "source_paths": source_list("580_candidates", "668_sector_audit", "668_queue"),
            "generated_utc": now,
        },
        {
            "candidate_id": "LX669_1_vertical_constraint",
            "parent_block": "X is a vertical gauge or constraint direction in ker(Dq)",
            "minimal_LX_form": "S_parent=S_obs[q(Phi)]+int Lambda C_X(Phi)+S_matter[psi,g_obs(q(Phi))]",
            "physical_pole_status": "none_if_constraint_algebra_closes_and_boundary_charge_vanishes",
            "source_status": "Noether/quotient identity would force Qbar_XH=0 or qbar_XT=0",
            "R10_R11_consequence": "R10/R11 silent only after first-class constraint and boundary audit",
            "owner_status": "best_active_theorem_route_not_signed",
            "blocker": "needs actual vertical generator, first-class closure, and boundary charge silence",
            "recommended_rank": "2",
            "valid_for_claim": "false",
            "source_paths": source_list("580_candidates", "616_doc", "668_sector_audit"),
            "generated_utc": now,
        },
        {
            "candidate_id": "LX669_2_positive_sourcefree_massive",
            "parent_block": "X is a physical local mode with positive elliptic operator but no local source",
            "minimal_LX_form": "1/2 int sqrt(h) [ Z_X |grad X|^2 + M_X^2 X^2 ] with J_X=0",
            "physical_pole_status": "yes_but_unexcited_in_local_exterior_if_sourcefree_and_boundary_silent",
            "source_status": "source_zero_not_parent_owned",
            "R10_R11_consequence": "X=0 by positive no-hair only if Z_X>0, M_X^2>0, J_X=0, and boundary_flux=0",
            "owner_status": "conditional_sourcefree_operator_route",
            "blocker": "Z_X, M_X^2, field normalization, matter pullback, hidden sources, and boundary class unsigned",
            "recommended_rank": "3",
            "valid_for_claim": "false",
            "source_paths": source_list("506_energy_identity", "579_contract", "580_candidates", "615_doc"),
            "generated_utc": now,
        },
        {
            "candidate_id": "LX669_3_massive_sourced_residual",
            "parent_block": "X is a physical local mode with finite coupling to matter/source readouts",
            "minimal_LX_form": "1/2 int sqrt(h) [ Z_X |grad X|^2 + M_X^2 X^2 ] - int sqrt(h) X J_X",
            "physical_pole_status": "physical_pole_retained",
            "source_status": "J_X and source charges must be measured or derived",
            "R10_R11_consequence": "lambda_X=sqrt(Z_X/M_X^2), alpha_X=K_X Qbar_XH qbar_XT enters R10/R11 residual vector",
            "owner_status": "retained_residual_vector_route",
            "blocker": "numerical parent coefficients and source paths are missing",
            "recommended_rank": "4",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "580_candidates", "616_doc", "656_doc"),
            "generated_utc": now,
        },
        {
            "candidate_id": "LX669_4_universal_conformal_countermodel",
            "parent_block": "matter sees exp(2 a_X X) g_obs with X a physical scalar",
            "minimal_LX_form": "L_X plus universal conformal matter coupling a_X X T",
            "physical_pole_status": "physical_pole_present",
            "source_status": "generic matter source nonzero",
            "R10_R11_consequence": "generically violates local silence unless a_X=0 is separately derived",
            "owner_status": "countermodel_not_solution",
            "blocker": "shows why source-zero cannot be assumed",
            "recommended_rank": "5",
            "valid_for_claim": "false",
            "source_paths": source_list("580_candidates", "621_doc", "622_doc"),
            "generated_utc": now,
        },
        {
            "candidate_id": "LX669_5_memory_kernel_or_nonlocal",
            "parent_block": "X is a local face of a memory/history kernel rather than a simple finite-range field",
            "minimal_LX_form": "int X K_ret X + source/history terms, or local auxiliary-field lift if possible",
            "physical_pole_status": "unknown_until_kernel_spectrum_is_owned",
            "source_status": "history and boundary injection not proven silent",
            "R10_R11_consequence": "must enter residual vector unless kernel is positive, local, causal, and source-free",
            "owner_status": "retained_nonlocal_residual_route",
            "blocker": "no parent kernel, spectrum, or local auxiliary-field reduction supplied",
            "recommended_rank": "6",
            "valid_for_claim": "false",
            "source_paths": source_list("506_energy_identity", "506_silence_status", "668_sector_audit"),
            "generated_utc": now,
        },
    ]
    return rows


def lx_owner_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G669_0_branch_extremum",
            "gate": "prove E_X|0=0",
            "pass_condition": "explicit parent Euler expression for X vanishes on the local vacuum branch",
            "current_result": "not_parent_filled",
            "blocker": "579 records branch extremum as not parent-filled",
            "result": "blocked_as_expected",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "668_sector_audit"),
            "generated_utc": now,
        },
        {
            "gate_id": "G669_1_positive_kinetic",
            "gate": "prove Z_X>0 with normalization",
            "pass_condition": "second variation fixes positive kinetic residue and field units",
            "current_result": "formula_only",
            "blocker": "Z_X is a formula without parent Hessian normalization",
            "result": "blocked_as_expected",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "615_doc", "616_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "G669_2_positive_mass_gap",
            "gate": "prove M_X^2>0 and lambda_X",
            "pass_condition": "parent Hessian ratio gives M_X^2/Z_X with units",
            "current_result": "formula_only_or_range_closure",
            "blocker": "range selection remains demoted to closure in 616",
            "result": "blocked_as_expected",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "615_doc", "616_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "G669_3_source_zero",
            "gate": "prove J_X=0 in local matter",
            "pass_condition": "observed matter functor and hidden sources are X-blind channel by channel",
            "current_result": "not_signed",
            "blocker": "matter pullback, hidden source silence, and quotient descent are not parent-owned",
            "result": "blocked_as_expected",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "580_candidates", "668_sector_audit"),
            "generated_utc": now,
        },
        {
            "gate_id": "G669_4_boundary_flux_zero",
            "gate": "prove boundary_flux_X=0",
            "pass_condition": "boundary class/no-hair theorem removes X hair and topological leakage",
            "current_result": "not_signed",
            "blocker": "668 leaves B_class/C_top/no-hair and projector silence open",
            "result": "blocked_as_expected",
            "valid_for_claim": "false",
            "source_paths": source_list("506_energy_identity", "668_impact", "668_sector_audit"),
            "generated_utc": now,
        },
        {
            "gate_id": "G669_5_no_pole_quotient",
            "gate": "prove no physical X pole",
            "pass_condition": "X is absent from the physical quotient or is a first-class vertical constraint",
            "current_result": "best_route_not_signed",
            "blocker": "actual q map and vertical generator are not enough to erase the pole yet",
            "result": "blocked_as_expected",
            "valid_for_claim": "false",
            "source_paths": source_list("580_candidates", "616_doc", "668_sector_audit"),
            "generated_utc": now,
        },
        {
            "gate_id": "G669_6_theta_QX_owner",
            "gate": "compute Theta_X and Q_X from L_X",
            "pass_condition": "variation of a signed L_X gives symplectic potential, charge, and constraint term",
            "current_result": "formal_variation_only",
            "blocker": "without a signed L_X, Theta_X/Q_X are symbols not owned charges",
            "result": "blocked_as_expected",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_sector_audit", "668_impact"),
            "generated_utc": now,
        },
        {
            "gate_id": "G669_7_retained_residual_vector",
            "gate": "stage nonclaim residual vector",
            "pass_condition": "missing coefficients are explicit, source-file tracked, and valid_for_claim=false",
            "current_result": "ready_as_nonclaim_plumbing",
            "blocker": "no numeric or parent-signed coefficients yet",
            "result": "pass_nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("656_doc", "668_queue", "668_impact"),
            "generated_utc": now,
        },
    ]


def theta_qx_variation_ledger_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "step_id": "V669_0_variation",
            "variational_object": "delta L_X",
            "formal_statement": "delta L_X = E_X delta X + d Theta_X(delta X)",
            "owned_if": "L_X is parent-signed with field normalization and boundary class",
            "current_result": "formula_written_not_owned",
            "residual_if_fail": "Theta_X_residual",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_sector_audit"),
            "generated_utc": now,
        },
        {
            "step_id": "V669_1_current",
            "variational_object": "Noether current",
            "formal_statement": "J_tau^X = Theta_X(L_tau X) - i_tau L_X",
            "owned_if": "tau action on X and L_X are both parent-defined",
            "current_result": "formula_written_not_owned",
            "residual_if_fail": "tau_X_current_residual",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_impact"),
            "generated_utc": now,
        },
        {
            "step_id": "V669_2_charge",
            "variational_object": "charge decomposition",
            "formal_statement": "J_tau^X = d Q_tau^X + C_tau^X",
            "owned_if": "constraint decomposition exists for the signed sector",
            "current_result": "formula_written_not_owned",
            "residual_if_fail": "Q_tau_X_and_C_tau_X_residual",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_impact"),
            "generated_utc": now,
        },
        {
            "step_id": "V669_3_symplectic",
            "variational_object": "sector symplectic form",
            "formal_statement": "omega_X = delta Theta_X",
            "owned_if": "Theta_X is explicit and integrability curl vanishes on the branch",
            "current_result": "formula_written_not_owned",
            "residual_if_fail": "symplectic_boundary_flux_X",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_impact"),
            "generated_utc": now,
        },
        {
            "step_id": "V669_4_integrability",
            "variational_object": "Hamiltonian integrability",
            "formal_statement": "nonintegrable contribution is int_S i_tau omega_X",
            "owned_if": "boundary class and L_X force the surface integral to vanish or be exact",
            "current_result": "not_signed",
            "residual_if_fail": "delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_impact"),
            "generated_utc": now,
        },
        {
            "step_id": "V669_5_source_equation",
            "variational_object": "linearized source equation",
            "formal_statement": "O_X X = J_X",
            "owned_if": "parent Hessian O_X and source functional J_X are explicit",
            "current_result": "operator_and_source_missing",
            "residual_if_fail": "J_X_source_residual",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "580_candidates"),
            "generated_utc": now,
        },
        {
            "step_id": "V669_6_yukawa_projection",
            "variational_object": "R10 finite-range projection",
            "formal_statement": "lambda_X=sqrt(Z_X/M_X^2), alpha_X=K_X Qbar_XH qbar_XT",
            "owned_if": "Z_X, M_X^2, K_X, Qbar_XH, and qbar_XT are numeric or theorem-zero",
            "current_result": "all_coefficients_missing_or_unsigned",
            "residual_if_fail": "R10_alpha_lambda_residual",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "580_candidates", "615_doc", "616_doc"),
            "generated_utc": now,
        },
        {
            "step_id": "V669_7_r11_vector",
            "variational_object": "R11 operator vector",
            "formal_statement": "non-EH local operators and X-sector couplings become executable residual coefficients",
            "owned_if": "EH-only/no-pole/sourcefree theorem removes them, or coefficients are sourced",
            "current_result": "skeleton_context_only_coefficients_missing",
            "residual_if_fail": "R11_operator_coefficients",
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "656_doc", "668_queue"),
            "generated_utc": now,
        },
    ]


def r10_r11_residual_vector_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "residual_id": "RV669_0_Z_X",
            "coefficient": "Z_X",
            "meaning": "kinetic residue / field normalization for X",
            "required_parent_input": "second variation Hessian with units",
            "value_status": "MISSING_PARENT_INPUT",
            "units_status": "MISSING_UNITS",
            "source_status": "source_path_exists_but_value_missing",
            "feeds": "lambda_X;positive_operator;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "615_doc", "616_doc"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_1_M_X2",
            "coefficient": "M_X^2",
            "meaning": "mass gap / inverse range squared for X",
            "required_parent_input": "parent Hessian curvature in X direction",
            "value_status": "MISSING_PARENT_INPUT",
            "units_status": "MISSING_UNITS",
            "source_status": "source_path_exists_but_value_missing",
            "feeds": "lambda_X;positive_operator;R10",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "615_doc", "616_doc"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_2_J_X",
            "coefficient": "J_X",
            "meaning": "local matter/hidden source current for X",
            "required_parent_input": "matter pullback and hidden source variation with respect to X",
            "value_status": "MISSING_SOURCE_ZERO_PROOF",
            "units_status": "MISSING_UNITS",
            "source_status": "source_path_exists_but_zero_not_derived",
            "feeds": "local_silence;R10;R11",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "580_candidates", "668_sector_audit"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_3_qbar_XT",
            "coefficient": "qbar_XT",
            "meaning": "test-body X charge per source/readout unit",
            "required_parent_input": "projection of matter action into X channel",
            "value_status": "MISSING_ARENA_PROJECTION",
            "units_status": "MISSING_UNITS",
            "source_status": "no_numeric_source",
            "feeds": "alpha_X;WEP;R10",
            "valid_for_claim": "false",
            "source_paths": source_list("580_candidates", "656_doc"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_4_Qbar_XH",
            "coefficient": "Qbar_XH",
            "meaning": "heavy/source body X charge per Hamiltonian/source mass unit",
            "required_parent_input": "Hamiltonian/readout projection into X channel",
            "value_status": "MISSING_ARENA_PROJECTION",
            "units_status": "MISSING_UNITS",
            "source_status": "no_numeric_source",
            "feeds": "alpha_X;R10;FB5540",
            "valid_for_claim": "false",
            "source_paths": source_list("580_candidates", "656_doc", "668_impact"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_5_K_X",
            "coefficient": "K_X",
            "meaning": "normalization converting X exchange to force potential",
            "required_parent_input": "Green function residue and coupling convention",
            "value_status": "MISSING_PARENT_INPUT",
            "units_status": "MISSING_UNITS",
            "source_status": "no_numeric_source",
            "feeds": "alpha_X;R10",
            "valid_for_claim": "false",
            "source_paths": source_list("579_contract", "580_candidates", "616_doc"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_6_lambda_X",
            "coefficient": "lambda_X",
            "meaning": "finite range of X-mediated local residual",
            "required_parent_input": "sqrt(Z_X/M_X^2) with units",
            "value_status": "MISSING_PARENT_INPUT",
            "units_status": "MISSING_UNITS",
            "source_status": "range_closure_not_parent_value",
            "feeds": "R10_bound_interpolation",
            "valid_for_claim": "false",
            "source_paths": source_list("615_doc", "616_doc"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_7_boundary_flux_X",
            "coefficient": "boundary_flux_X",
            "meaning": "surface/hair leakage of X energy or symplectic flux",
            "required_parent_input": "boundary class/no-hair and projector silence",
            "value_status": "MISSING_BOUNDARY_LOCK",
            "units_status": "MISSING_UNITS",
            "source_status": "source_path_exists_but_zero_not_derived",
            "feeds": "FB5540;local_silence;PPN",
            "valid_for_claim": "false",
            "source_paths": source_list("506_energy_identity", "668_impact"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_8_theta_QX_normalization",
            "coefficient": "Theta_X/Q_X normalization",
            "meaning": "charge normalization for sector Hamiltonian contribution",
            "required_parent_input": "signed L_X variation and boundary reference",
            "value_status": "MISSING_PARENT_INPUT",
            "units_status": "MISSING_UNITS",
            "source_status": "formal_symbol_only",
            "feeds": "FB5540;Hamiltonian_source_charge",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_impact"),
            "generated_utc": now,
        },
        {
            "residual_id": "RV669_9_R11_operator_coefficients",
            "coefficient": "R11 non-EH operator vector",
            "meaning": "local metric/operator deviations retained if EH-only/no-pole route fails",
            "required_parent_input": "operator basis and coefficients",
            "value_status": "MISSING_PARENT_INPUT",
            "units_status": "MISSING_UNITS",
            "source_status": "skeleton_context_only",
            "feeds": "R11;local_GR_reduction",
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "656_doc"),
            "generated_utc": now,
        },
    ]


def fb5540_impact_map_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "impact_id": "IM669_0_delta_H_tau",
            "FB5540_quantity": "delta_H_tau_nonintegrable_over_MH",
            "L_X_dependency": "Theta_X, omega_X, and tau action from signed L_X",
            "current_status": "not_zero_not_numeric",
            "effect": "FB5540_0 cannot be proved because integrability is still open",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "impact_id": "IM669_1_C_extra",
            "FB5540_quantity": "C_extra/MH or X-sector constraint leakage",
            "L_X_dependency": "constraint decomposition J_tau^X=dQ_tau^X+C_tau^X",
            "current_status": "symbolic_only",
            "effect": "extra-sector contribution cannot be erased without no-pole or sourcefree proof",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "impact_id": "IM669_2_boundary_flux",
            "FB5540_quantity": "symplectic_boundary_flux_over_MH",
            "L_X_dependency": "boundary flux from positive/no-hair identity or charge decomposition",
            "current_status": "boundary_lock_missing",
            "effect": "boundary channel stays in residual vector",
            "next_action": "after no-pole/sourcefree gate, return to B_class/no-hair",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "impact_id": "IM669_3_R10",
            "FB5540_quantity": "R10 alpha-lambda channel",
            "L_X_dependency": "Z_X, M_X^2, K_X, Qbar_XH, qbar_XT",
            "current_status": "coefficient_vector_missing",
            "effect": "no fifth-force pass; only nonclaim residual rows are staged",
            "next_action": "derive no-pole K_X=0 or sourcefree alpha_X=0; else source coefficients",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "impact_id": "IM669_4_R11",
            "FB5540_quantity": "R11 local operator vector",
            "L_X_dependency": "EH-only/no-pole proof or non-EH operator coefficients",
            "current_status": "skeleton_only",
            "effect": "local-GR reduction remains conditional",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    candidate_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    any_claim_candidate = any(row["valid_for_claim"] == "true" for row in candidate_rows)
    any_claim_gate = any(row["valid_for_claim"] == "true" for row in gate_rows)
    any_claim_residual = any(row["valid_for_claim"] == "true" for row in residual_rows)
    return [
        {
            "evaluator_id": "EV669_0_minimal_LX_owner",
            "target": "claim a parent-owned minimal L_X sector",
            "status": "fail_nonclaim",
            "reason": "no branch proves no-pole, source-zero, positive operator, and boundary silence together",
            "claim_effect": "no FB5540_0, R10, R11, or local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV669_1_best_route",
            "target": "choose next derivation route",
            "status": "no_pole_quotient_first_then_positive_sourcefree",
            "reason": "the quotient/no-pole route removes the whole local fifth-force channel with less empirical coefficient debt",
            "claim_effect": "next target only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV669_2_residual_plumbing",
            "target": "stage R10/R11 residual vector",
            "status": "pass_nonclaim",
            "reason": "missing coefficients are explicit and all rows remain invalid for claim",
            "claim_effect": "makes failure modes executable later",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV669_3_safety",
            "target": "prevent silent claim promotion",
            "status": "pass" if not (any_claim_candidate or any_claim_gate or any_claim_residual) else "fail",
            "reason": "all candidate, gate, and residual rows keep valid_for_claim=false",
            "claim_effect": "private checkpoint remains nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D669_0",
            "status": STATUS,
            "meaning": "669 did not derive a signed L_X owner; it ranked the allowed branches and staged explicit missing coefficients",
            "claim_status": CLAIM_CEILING,
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    candidate_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    variation_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    prior_668 = read_csv(SOURCE_PATHS["668_validation"])
    prior_668_failures = [row for row in prior_668 if row.get("result") != "pass"]
    required_candidates = {
        "LX669_0_absent_quotient_variable",
        "LX669_1_vertical_constraint",
        "LX669_2_positive_sourcefree_massive",
        "LX669_3_massive_sourced_residual",
        "LX669_4_universal_conformal_countermodel",
        "LX669_5_memory_kernel_or_nonlocal",
    }
    candidate_ids = {row["candidate_id"] for row in candidate_rows}
    gate_ids = {row["gate_id"] for row in gate_rows}
    variation_ids = {row["step_id"] for row in variation_rows}
    residual_markers = ";".join(row["value_status"] for row in residual_rows)
    formalization_count = formalization_changed_count()
    generated_outputs = [
        RESIDUALS / "P8_Y5_R10_669_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
        RESIDUALS / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
        RESIDUALS / "P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv",
        RESIDUALS / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
        RESIDUALS / "P8_Y5_R10_669_FB5540_IMPACT_MAP.csv",
        RESIDUALS / "P8_Y5_R10_669_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_669_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_669_NONCLAIM_SUMMARY.csv",
    ]
    all_generated_in_post_checkpoint = all(str(path).startswith(str(ROOT)) for path in generated_outputs + [DOC_PATH])
    return [
        {
            "check_id": "V669_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in source_rows) else "fail",
            "detail": "all cited source paths exist" if all(row["exists"] == "true" for row in source_rows) else "one or more cited source paths missing",
            "generated_utc": now,
        },
        {
            "check_id": "V669_1_prior_668_clean",
            "result": "pass" if not prior_668_failures else "fail",
            "detail": f"668 validation failures={len(prior_668_failures)}",
            "generated_utc": now,
        },
        {
            "check_id": "V669_2_candidate_branch_coverage",
            "result": "pass" if required_candidates.issubset(candidate_ids) else "fail",
            "detail": f"candidate_rows={len(candidate_rows)} required_covered={bool_text(required_candidates.issubset(candidate_ids))}",
            "generated_utc": now,
        },
        {
            "check_id": "V669_3_owner_gate_coverage",
            "result": "pass" if len(gate_ids) >= 8 and "G669_7_retained_residual_vector" in gate_ids else "fail",
            "detail": f"gate_rows={len(gate_rows)} retained_vector_gate={'G669_7_retained_residual_vector' in gate_ids}",
            "generated_utc": now,
        },
        {
            "check_id": "V669_4_theta_Qx_variation_coverage",
            "result": "pass" if len(variation_ids) >= 8 and "V669_6_yukawa_projection" in variation_ids else "fail",
            "detail": f"variation_rows={len(variation_rows)} yukawa_projection={'V669_6_yukawa_projection' in variation_ids}",
            "generated_utc": now,
        },
        {
            "check_id": "V669_5_residual_vector_missing_markers",
            "result": "pass"
            if len(residual_rows) >= 10
            and "MISSING_PARENT_INPUT" in residual_markers
            and "MISSING_ARENA_PROJECTION" in residual_markers
            and all(row["valid_for_claim"] == "false" for row in residual_rows)
            else "fail",
            "detail": f"residual_rows={len(residual_rows)} markers={residual_markers}",
            "generated_utc": now,
        },
        {
            "check_id": "V669_6_no_claim_rows_promoted",
            "result": "pass"
            if all(row["valid_for_claim"] == "false" for row in candidate_rows + gate_rows + variation_rows + residual_rows + impact_rows + evaluator_data)
            else "fail",
            "detail": "all generated candidate/gate/variation/residual/impact/evaluator rows remain valid_for_claim=false",
            "generated_utc": now,
        },
        {
            "check_id": "V669_7_next_target_selected",
            "result": "pass" if decision and decision[0]["next_action"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "check_id": "V669_8_generated_outputs_scoped",
            "result": "pass" if all_generated_in_post_checkpoint else "fail",
            "detail": "all 669 outputs target post-checkpoint-work",
            "generated_utc": now,
        },
        {
            "check_id": "V669_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
            "generated_utc": now,
        },
        {
            "check_id": "V669_10_status_nonclaim",
            "result": "pass" if "no_R10" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING else "fail",
            "detail": CLAIM_CEILING,
            "generated_utc": now,
        },
        {
            "check_id": "V669_11_668_LX_first_confirmed",
            "result": "pass"
            if any(row.get("next_target") == "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md" for row in read_csv(SOURCE_PATHS["668_queue"]))
            else "fail",
            "detail": "668 residual queue selects L_X first",
            "generated_utc": now,
        },
        {
            "check_id": "V669_12_evaluator_nonclaim_passes",
            "result": "pass" if any(row["status"] == "pass_nonclaim" for row in evaluator_data) else "fail",
            "detail": ";".join(row["status"] for row in evaluator_data),
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows(
    candidate_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    variation_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    blocked_gates = [row["gate_id"] for row in gate_rows if row["result"] == "blocked_as_expected"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "candidate_rows": str(len(candidate_rows)),
            "owner_gate_rows": str(len(gate_rows)),
            "variation_rows": str(len(variation_rows)),
            "residual_rows": str(len(residual_rows)),
            "impact_rows": str(len(impact_rows)),
            "evaluator_rows": str(len(evaluator_data)),
            "blocked_gates": ";".join(blocked_gates),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    candidate_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    variation_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    validation_table = markdown_table(validation, ["check_id", "result", "detail"]) if validation else "_Validation pending final write._\n"
    doc = f"""# 669 - Y5 R10 Minimal L_X Sector Operator Owner Or Retained Residual Vector

## Verdict

669 attacked the L_X hinge selected in 668. The result is useful but non-claim:

```text
No signed minimal L_X owner yet.
No derived no-pole theorem yet.
No derived source-zero theorem yet.
No positive source-free no-hair closure yet.
Therefore R10/R11/FB5540/local-GR remain blocked, but the missing vector is now explicit.
```

The clean route is still derivation-first: prove X is absent from the physical quotient, or prove it is a vertical first-class/no-pole direction. If that fails, the next best theorem is the positive source-free operator route. If that also fails, the X-sector must remain an executable residual vector with real coefficients.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Minimal L_X Operator Candidates

{markdown_table(candidate_rows, ["candidate_id", "parent_block", "minimal_LX_form", "physical_pole_status", "source_status", "R10_R11_consequence", "owner_status", "blocker", "recommended_rank", "valid_for_claim"])}

## L_X Owner Gate Tests

{markdown_table(gate_rows, ["gate_id", "gate", "pass_condition", "current_result", "blocker", "result", "valid_for_claim"])}

## Theta/QX Variation Ledger

{markdown_table(variation_rows, ["step_id", "variational_object", "formal_statement", "owned_if", "current_result", "residual_if_fail", "valid_for_claim"])}

## R10/R11 Residual Vector

{markdown_table(residual_rows, ["residual_id", "coefficient", "meaning", "required_parent_input", "value_status", "units_status", "source_status", "feeds", "valid_for_claim"])}

## FB5540 Impact Map

{markdown_table(impact_rows, ["impact_id", "FB5540_quantity", "L_X_dependency", "current_status", "effect", "next_action", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_data, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "candidate_rows", "owner_gate_rows", "variation_rows", "residual_rows", "impact_rows", "evaluator_rows", "blocked_gates", "validation_failures", "next_target"])}

## Validation

{validation_table}

## Interpretation

This checkpoint does not give the local-GR prize. It does, however, sharpen the fight into three exact branches:

1. **No-pole quotient branch:** derive that X is not a physical tangent direction, so there is no local Green function and `K_X=0`.
2. **Vertical constraint branch:** derive that X is in `ker(Dq)` with a first-class generator and no boundary charge.
3. **Positive source-free branch:** derive `Z_X>0`, `M_X^2>0`, `J_X=0`, and `boundary_flux_X=0`, so the local X profile vanishes by the energy identity.

If none of these can be parent-signed, MTS does not get to smuggle silence into the local branch; it carries the explicit R10/R11 residual vector above.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    candidate_rows = minimal_lx_operator_candidate_rows()
    gate_rows = lx_owner_gate_rows()
    variation_rows = theta_qx_variation_ledger_rows()
    residual_rows = r10_r11_residual_vector_rows()
    impact_rows = fb5540_impact_map_rows()
    evaluator_data = evaluator_rows(candidate_rows, gate_rows, residual_rows)
    decision = decision_rows()

    write_csv(RESIDUALS / "P8_Y5_R10_669_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
        candidate_rows,
        [
            "candidate_id",
            "parent_block",
            "minimal_LX_form",
            "physical_pole_status",
            "source_status",
            "R10_R11_consequence",
            "owner_status",
            "blocker",
            "recommended_rank",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
        gate_rows,
        ["gate_id", "gate", "pass_condition", "current_result", "blocker", "result", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv",
        variation_rows,
        [
            "step_id",
            "variational_object",
            "formal_statement",
            "owned_if",
            "current_result",
            "residual_if_fail",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
        residual_rows,
        [
            "residual_id",
            "coefficient",
            "meaning",
            "required_parent_input",
            "value_status",
            "units_status",
            "source_status",
            "feeds",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_669_FB5540_IMPACT_MAP.csv",
        impact_rows,
        ["impact_id", "FB5540_quantity", "L_X_dependency", "current_status", "effect", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_669_EVALUATOR.csv",
        evaluator_data,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_669_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )

    write_document(source_rows, candidate_rows, gate_rows, variation_rows, residual_rows, impact_rows, evaluator_data, decision, [], [])

    validation = validation_rows(source_rows, candidate_rows, gate_rows, variation_rows, residual_rows, impact_rows, evaluator_data, decision)
    summary_rows = nonclaim_summary_rows(candidate_rows, gate_rows, variation_rows, residual_rows, impact_rows, evaluator_data, validation)
    write_csv(
        RESIDUALS / "P8_Y5_R10_669_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "candidate_rows",
            "owner_gate_rows",
            "variation_rows",
            "residual_rows",
            "impact_rows",
            "evaluator_rows",
            "blocked_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_669_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_document(source_rows, candidate_rows, gate_rows, variation_rows, residual_rows, impact_rows, evaluator_data, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"candidate_rows={len(candidate_rows)}")
    print(f"owner_gate_rows={len(gate_rows)}")
    print(f"variation_rows={len(variation_rows)}")
    print(f"residual_rows={len(residual_rows)}")
    print(f"impact_rows={len(impact_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

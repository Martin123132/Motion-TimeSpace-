from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_Hamiltonian_PiM_orthogonality_attempted_Qbar_edge_zero_unsigned_edge_coefficient_acquisition_ledger_staged_nonclaim"
CLAIM_CEILING = "Hamiltonian_PiM_orthogonality_and_edge_coefficient_acquisition_only_no_Qbar_edge_zero_no_R10_no_R11_no_PPN_no_local_GR_claim"
NEXT_TARGET = "674-Y5-R10-edge-coefficient-row-fill-or-parent-PiM-clause.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_PATH = ROOT / "673-Y5-R10-edge-coefficient-source-acquisition-or-Hamiltonian-PiM-orthogonality-proof.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "458_doc": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
    "458_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "510_doc": ROOT / "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
    "539_validation": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_VALIDATION.csv",
    "539_branch": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv",
    "539_gates": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv",
    "540_doc": ROOT / "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
    "540_validation": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_READOUT_VALIDATION.csv",
    "540_source_measure": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv",
    "540_gauss_ppn": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv",
    "541_doc": ROOT / "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
    "541_validation": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_VALIDATION.csv",
    "541_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "541_scorecard": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
    "542_doc": ROOT / "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md",
    "542_validation": RESIDUALS / "P8_Y5_SOURCE_MEASURE_THEOREM_VALIDATION.csv",
    "542_decision": RESIDUALS / "P8_Y5_SOURCE_MEASURE_THEOREM_DECISION.csv",
    "543_doc": ROOT / "543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md",
    "543_validation": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_VALIDATION.csv",
    "543_decision": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_DECISION.csv",
    "544_doc": ROOT / "544-Y5-boundary-reference-first-row-data-or-theorem-zero.md",
    "544_validation": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_544_VALIDATION.csv",
    "544_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "544_decision": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_544_DECISION.csv",
    "583_edge": RESIDUALS / "P8_Y5_R10_583_EDGE_RESIDUAL_DEMOTION.csv",
    "584_input_contract": RESIDUALS / "P8_Y5_R10_584_EDGE_CLAIM_INPUT_CONTRACT.csv",
    "589_edge_template": RESIDUALS / "P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv",
    "629_doc": ROOT / "629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md",
    "629_validation": RESIDUALS / "P8_Y5_BRR545_629_VALIDATION.csv",
    "629_source_search": RESIDUALS / "P8_Y5_R10_629_SOURCE_SEARCH_STATUS.csv",
    "629_curve_audit": RESIDUALS / "P8_Y5_R10_629_R10_CURVE_PROMOTION_AUDIT.csv",
    "bound_real_contract": RESIDUALS / "P8_Y5_R10_BOUND_CURVE_REAL_DATA_CONTRACT.csv",
    "bound_digitization_contract": RESIDUALS / "P8_Y5_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv",
    "bound_live_placeholder": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
    "bound_review_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
    "671_doc": ROOT / "671-Y5-R10-parent-Omega-DCX-boundary-charge-owner-or-edge-residual-vector.md",
    "671_validation": RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv",
    "671_edge": RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
    "672_doc": ROOT / "672-Y5-R10-boundary-exactness-projector-orthogonality-or-edge-coefficient-source-plan.md",
    "672_validation": RESIDUALS / "P8_Y5_BRR545_672_VALIDATION.csv",
    "672_source_plan": RESIDUALS / "P8_Y5_R10_672_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
    "672_decision": RESIDUALS / "P8_Y5_R10_672_ZERO_OR_SOURCE_DECISION.csv",
    "672_evaluator": RESIDUALS / "P8_Y5_R10_672_EVALUATOR.csv",
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


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_PATHS[source_id]) if row.get("result") != "pass"]


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
        "458_doc": "Hamiltonian charge to Poisson/Gauss calibration gate",
        "458_contract": "Poisson/Gauss calibration contract",
        "510_doc": "worldtube source-measure glue and Meff residual runner",
        "539_doc": "Hamiltonian Pi_M charge-map candidate and topological demotion",
        "539_validation": "539 validation gate",
        "539_branch": "Hamiltonian Pi_M branch definition rows",
        "539_gates": "Hamiltonian Pi_M open gate rows",
        "540_doc": "Hamiltonian Pi_M source-measure and PPN readout test",
        "540_validation": "540 validation gate",
        "540_source_measure": "Hamiltonian Pi_M source-measure tests",
        "540_gauss_ppn": "Hamiltonian Pi_M Gauss and PPN tests",
        "541_doc": "Hamiltonian Pi_M source-measure contract and residual scorecard",
        "541_validation": "541 validation gate",
        "541_contract": "source-measure contract rows",
        "541_scorecard": "source-measure scorecard rows",
        "542_doc": "source-measure theorem attempt",
        "542_validation": "542 validation gate",
        "542_decision": "source-measure theorem decision rows",
        "543_doc": "boundary/reference residual theorem attempt",
        "543_validation": "543 validation gate",
        "543_decision": "boundary/reference decision rows",
        "544_doc": "boundary/reference first-row data/theorem audit",
        "544_validation": "544 validation gate",
        "544_status": "boundary/reference first-row status",
        "544_decision": "boundary/reference first-row decision rows",
        "583_edge": "edge residual demotion rows",
        "584_input_contract": "edge claim input contract",
        "589_edge_template": "source-backed edge product template",
        "629_doc": "R10 bound curve digitization or c_g projection smoke runner",
        "629_validation": "629 validation gate",
        "629_source_search": "R10 source search status",
        "629_curve_audit": "R10 curve promotion audit",
        "bound_real_contract": "real R10 bound curve data contract",
        "bound_digitization_contract": "R10 bound curve digitization contract",
        "bound_live_placeholder": "live digitized bound file still placeholder",
        "bound_review_candidate": "private vector review candidate, nonclaim pressure wall",
        "671_doc": "parent Omega/DCX boundary charge owner and edge residual vector",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector",
        "672_doc": "boundary exactness / projector orthogonality / source plan handoff",
        "672_validation": "672 validation gate",
        "672_source_plan": "edge coefficient source plan",
        "672_decision": "zero-or-source decision rows",
        "672_evaluator": "672 evaluator rows",
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


def pim_orthogonality_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "proof_id": "HPO673_0_charge_map_defined",
            "clause": "Pi_M^H is the parent Hamiltonian mass-charge map",
            "mathematical_test": "Pi_M J_H := Pi_M^H J_H = ell_H[J_H;tau,S] omega_M^H",
            "current_result": "candidate_definition_only",
            "obstruction": "539 defines the repair candidate, but adoption, integrability, and source-measure glue remain unsigned",
            "would_close": "prevents Pi_M from being a post-readout mask",
            "fallback": "retain Hamiltonian projector residuals",
            "valid_for_claim": "false",
            "source_paths": source_list("539_doc", "539_branch", "539_gates"),
            "generated_utc": now,
        },
        {
            "proof_id": "HPO673_1_integrable_fixed_reference",
            "clause": "Hamiltonian charge is integrable with fixed reference and time generator",
            "mathematical_test": "delta H_tau = integral_S(delta Q_tau - i_tau theta), reference fixed once",
            "current_result": "not_derived_for_current_MTS",
            "obstruction": "boundary/reference terms B_zero_flux and Delta_symp remain unfilled",
            "would_close": "makes Pi_M^H a stable mass functional rather than a gauge/reference choice",
            "fallback": "source boundary/reference residual envelope",
            "valid_for_claim": "false",
            "source_paths": source_list("541_contract", "542_doc", "543_doc", "544_status"),
            "generated_utc": now,
        },
        {
            "proof_id": "HPO673_2_edge_mass_orthogonality",
            "clause": "edge charge lies in the kernel of the Hamiltonian mass projection",
            "mathematical_test": "Pi_M^H[Q_edge^H(lambda)] = 0 for every active local lambda",
            "current_result": "not_signed",
            "obstruction": "no parent theorem proves Q_edge is exact, proper-gauge-only, or mass-cohomology-orthogonal",
            "would_close": "Qbar_edge_XH(lambda)=0",
            "fallback": "source Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "672_source_plan", "672_decision"),
            "generated_utc": now,
        },
        {
            "proof_id": "HPO673_3_boundary_exact_or_zero_flux",
            "clause": "edge boundary representative has zero Hamiltonian flux",
            "mathematical_test": "Q_edge^H = integral_boundary epsilon B_X = 0 or B_X=d_boundary b_X with zero compact class",
            "current_result": "conditional_narrow_only",
            "obstruction": "672 keeps proper-boundary and exact-sector zeros but does not kill measured edge charge",
            "would_close": "removes edge channel before coefficient sourcing",
            "fallback": "retain B_X boundary momentum acquisition row",
            "valid_for_claim": "false",
            "source_paths": source_list("672_doc", "672_source_plan", "671_edge"),
            "generated_utc": now,
        },
        {
            "proof_id": "HPO673_4_source_measure_same_frame",
            "clause": "Hamiltonian source measure and observed local readout use the same frame",
            "mathematical_test": "M_source[W]=H_tau[S]-H_ref and Q_edge are evaluated in e_obs before orbital fitting",
            "current_result": "not_derived",
            "obstruction": "worldtube source support, time generator, and readout frame are still gates, not theorems",
            "would_close": "blocks fake cancellation between source frame and edge projection frame",
            "fallback": "source Delta_frame/Delta_cal or prove same-frame matter coupling",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "540_doc", "541_contract", "542_doc"),
            "generated_utc": now,
        },
        {
            "proof_id": "HPO673_5_commutator_projector_silence",
            "clause": "Pi_M^H commutes with exterior closure and has no projector-stress leakage",
            "mathematical_test": "d(Pi_M^H J_H)=Pi_M^H dJ_H and delta(Pi_M^H J_H)=Pi_M^H delta J_H",
            "current_result": "not_parent_derived",
            "obstruction": "commutator, metric/domain variation, and projector stress rows remain active",
            "would_close": "prevents an edge term from re-entering through projector variation",
            "fallback": "retain I_commutator and projector-stress residuals",
            "valid_for_claim": "false",
            "source_paths": source_list("539_gates", "541_scorecard", "544_status"),
            "generated_utc": now,
        },
        {
            "proof_id": "HPO673_6_extra_sector_charge_silence",
            "clause": "edge/boundary/memory/range sectors carry zero independent Hamiltonian mass charge",
            "mathematical_test": "Delta_nonEH=Delta_extra=Delta_PiM=Delta_frame=Delta_boundary=0",
            "current_result": "not_field_specific_derived",
            "obstruction": "existing silence is conditional, not an owned parent-action result for the edge channel",
            "would_close": "prevents Qbar_edge from being an omitted local source",
            "fallback": "source channelwise edge coefficients",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "541_contract", "671_edge", "672_source_plan"),
            "generated_utc": now,
        },
        {
            "proof_id": "HPO673_7_verdict",
            "clause": "Hamiltonian Pi_M orthogonality proof of Qbar_edge_XH=0",
            "mathematical_test": "HPO673_0 through HPO673_6 all pass as parent-signed theorem clauses",
            "current_result": "proof_failed_nonclaim",
            "obstruction": "multiple parent clauses remain candidate, conditional, unfilled, or not derived",
            "would_close": "R10 edge alpha branch could remove Qbar_edge_XH rather than source it",
            "fallback": "edge coefficient acquisition ledger staged",
            "valid_for_claim": "false",
            "source_paths": source_list("672_evaluator", "539_validation", "540_validation", "541_validation", "544_validation"),
            "generated_utc": now,
        },
    ]


def source_measure_glue_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "glue_id": "SMG673_0_conditional_theorem_shape",
            "requirement": "source-measure theorem premises HSM541_1 through HSM541_3",
            "mathematical_form": "integrable charge + observed Hilbert worldtube + zero exterior C-terms",
            "current_status": "conditional_theorem_only",
            "residual_if_fail": "B_zero_flux;Delta_symp;Delta_frame;epsilon_radial_Meff",
            "effect_on_Qbar_edge": "cannot use Pi_M orthogonality as measured-source theorem",
            "valid_for_claim": "false",
            "source_paths": source_list("542_doc", "542_decision", "541_contract"),
            "generated_utc": now,
        },
        {
            "glue_id": "SMG673_1_boundary_reference_first_row",
            "requirement": "B_zero_flux, Delta_symp, and M_H_ref are theorem-zero or source-backed",
            "mathematical_form": "epsilon_boundary_reference_abs=(|B_zero_flux|+|Delta_symp|)/M_H_ref",
            "current_status": "unfilled_no_claim_valid_zero",
            "residual_if_fail": "epsilon_boundary_reference_abs",
            "effect_on_Qbar_edge": "edge projection denominator/reference cannot be promoted",
            "valid_for_claim": "false",
            "source_paths": source_list("543_doc", "544_doc", "544_status", "544_decision"),
            "generated_utc": now,
        },
        {
            "glue_id": "SMG673_2_radial_closure",
            "requirement": "Hamiltonian charge is radially closed in compact source-free exterior",
            "mathematical_form": "int_A(C_EH+C_extra+C_projector+C_boundary)=0",
            "current_status": "conditional_EH_reference_C_terms_open",
            "residual_if_fail": "epsilon_radial_Meff;dln_Meff",
            "effect_on_Qbar_edge": "edge source could mimic radial/local mass drift",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "541_contract", "541_scorecard"),
            "generated_utc": now,
        },
        {
            "glue_id": "SMG673_3_Gauss_orbital_readout",
            "requirement": "same charge controls Poisson/Gauss and pure inverse-square orbital readout",
            "mathematical_form": "nabla^2 Phi=4*pi*G_ref*rho_H and a_r=-G_ref*M_source/r^2",
            "current_status": "not_derived",
            "residual_if_fail": "Delta_cal;alpha_lambda;partial_r_ln_mu_obs",
            "effect_on_Qbar_edge": "R10/local force mapping remains blocked at measured alpha(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("458_doc", "458_contract", "540_gauss_ppn", "541_scorecard"),
            "generated_utc": now,
        },
        {
            "glue_id": "SMG673_4_constant_universal_coupling",
            "requirement": "G_eff/kappa is constant, universal, source-blind, range-blind, and frame-blind",
            "mathematical_form": "partial_t,r,A,lambda,frame G_eff=0",
            "current_status": "conditional_not_parent_derived",
            "residual_if_fail": "Gdot;source_charge;range_dependence",
            "effect_on_Qbar_edge": "cannot absorb edge alpha into a constant calibration",
            "valid_for_claim": "false",
            "source_paths": source_list("540_gauss_ppn", "541_contract", "541_scorecard"),
            "generated_utc": now,
        },
        {
            "glue_id": "SMG673_5_PPN_followthrough",
            "requirement": "same source normalization survives second-order PPN",
            "mathematical_form": "Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi}=0 or below locks",
            "current_status": "not_reached",
            "residual_if_fail": "delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi",
            "effect_on_Qbar_edge": "even a Newton-looking branch would still not be local GR",
            "valid_for_claim": "false",
            "source_paths": source_list("540_gauss_ppn", "541_contract", "541_scorecard"),
            "generated_utc": now,
        },
        {
            "glue_id": "SMG673_6_edge_specific_projection",
            "requirement": "Q_edge has no measured mass projection after source-measure glue",
            "mathematical_form": "Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H=0",
            "current_status": "not_signed",
            "residual_if_fail": "Qbar_edge_XH(lambda)",
            "effect_on_Qbar_edge": "the exact target coefficient remains live",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "672_source_plan", "672_decision"),
            "generated_utc": now,
        },
    ]


def acquisition_ledger_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "acquisition_id": "ECA673_0_lambda_edge",
            "coefficient": "lambda_edge or F_lambda support",
            "formula_role": "selects R10/local bound scale and active edge support",
            "acceptable_theorem_zero": "edge support is absent by parent boundary/no-edge theorem",
            "required_source_or_data": "positive length grid or compact support envelope with units and parent source path",
            "current_status": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "units": "length, preferably m",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "672_source_plan", "584_input_contract"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "ECA673_1_K_edge",
            "coefficient": "K_edge(lambda)",
            "formula_role": "edge Green/boundary kernel normalization in alpha_edge(lambda)",
            "acceptable_theorem_zero": "edge kernel inactive because Q_edge theorem-zero",
            "required_source_or_data": "parent boundary Green kernel normalization, sign convention, and observed-unit map",
            "current_status": "MISSING_SOURCE_BACKED_K_EDGE",
            "units": "dimensionless or explicitly declared",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "672_source_plan", "589_edge_template"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "ECA673_2_Qbar_edge_XH",
            "coefficient": "Qbar_edge_XH(lambda)",
            "formula_role": "Hamiltonian mass projection of the edge charge divided by M_H",
            "acceptable_theorem_zero": "Pi_M^H[Q_edge^H(lambda)]=0 including reference and boundary terms",
            "required_source_or_data": "Hamiltonian projection row with numerator, denominator, source path, and same-frame assumptions",
            "current_status": "MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "units": "dimensionless or explicitly declared",
            "valid_for_claim": "false",
            "source_paths": source_list("539_doc", "540_doc", "541_contract", "671_edge", "672_source_plan"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "ECA673_3_qbar_XT",
            "coefficient": "qbar_XT",
            "formula_role": "test-body response to X/edge sector",
            "acceptable_theorem_zero": "quotient-invariant matter action gives no test-body marker",
            "required_source_or_data": "composition/readout response coefficient or theorem-zero with matter action source path",
            "current_status": "MISSING_SOURCE_BACKED_QBAR_XT_OR_THEOREM_ZERO",
            "units": "dimensionless or explicitly declared",
            "valid_for_claim": "false",
            "source_paths": source_list("589_edge_template", "672_source_plan"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "ECA673_4_BX_boundary_momentum",
            "coefficient": "B_X^nu=n_mu P^{mu nu}+B_ct^nu",
            "formula_role": "boundary primitive/momentum entering Q_edge",
            "acceptable_theorem_zero": "B_X exact, pure-gauge, or proper-boundary zero from parent boundary action",
            "required_source_or_data": "parent boundary action/current representative fixing B_X and counterterm",
            "current_status": "MISSING_BOUNDARY_OWNER",
            "units": "boundary momentum/current units",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "672_source_plan", "543_doc", "544_status"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "ECA673_5_M_H_ref",
            "coefficient": "M_H or M_H_ref",
            "formula_role": "positive denominator for Qbar_edge_XH and boundary/reference residuals",
            "acceptable_theorem_zero": "not a zero target; must be fixed as observed Hamiltonian source mass",
            "required_source_or_data": "same-frame Hamiltonian source mass definition, reference subtraction, and observed calibration",
            "current_status": "MISSING_SOURCE_BACKED_M_H_REF_FOR_CURRENT_BRANCH",
            "units": "mass or geometrized mass with convention",
            "valid_for_claim": "false",
            "source_paths": source_list("541_contract", "544_status", "458_contract"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "ECA673_6_alpha_bound_lambda",
            "coefficient": "alpha_bound(lambda)",
            "formula_role": "R10 comparator bound curve",
            "acceptable_theorem_zero": "not a theory zero; empirical curve still needed for scoring nonzero edge rows",
            "required_source_or_data": "machine-readable or digitized source-backed R10 bound curve with units, method, and promotion QA",
            "current_status": "REVIEW_CANDIDATE_AVAILABLE_LIVE_CLAIM_FILE_PLACEHOLDER",
            "units": "lambda in m, alpha dimensionless",
            "valid_for_claim": "false",
            "source_paths": source_list("629_source_search", "629_curve_audit", "bound_real_contract", "bound_digitization_contract", "bound_live_placeholder", "bound_review_candidate"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "ECA673_7_runner_mapping",
            "coefficient": "alpha_edge(lambda) mapping",
            "formula_role": "maps K_edge Qbar_edge_XH qbar_XT and bound curve into executable R10 comparison",
            "acceptable_theorem_zero": "all edge factors theorem-zero before runner is used for claim",
            "required_source_or_data": "numeric rows for all active factors, no MISSING markers, valid_for_claim true only after parent sourcing",
            "current_status": "RUNNER_SCHEMA_READY_BUT_MTS_EDGE_ROWS_NONCLAIM",
            "units": "dimensionless alpha with declared force-law convention",
            "valid_for_claim": "false",
            "source_paths": source_list("672_source_plan", "629_validation", "bound_real_contract", "589_edge_template"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D673_0_Hamiltonian_PiM_orthogonality",
            "target": "Qbar_edge_XH(lambda)=0",
            "result": "not_signed",
            "reason": "Pi_M^H is candidate-useful, but integrability, same-frame source measure, projector stress, and edge-kernel orthogonality are not parent-signed",
            "next_action": "source Qbar_edge_XH(lambda) or find parent action clause making Q_edge mass-orthogonal",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D673_1_source_measure_glue",
            "target": "measured source mass branch",
            "result": "conditional_only_not_current_MTS_theorem",
            "reason": "510-544 give a clean conditional route but no current-MTS boundary/reference/source-measure theorem zero",
            "next_action": "keep source-measure residuals active in edge scoring",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D673_2_edge_coefficients",
            "target": "R10 edge branch evidence",
            "result": "acquisition_ledger_required",
            "reason": "if no theorem kills the edge term, the honest path is source-backed coefficient rows and real bound-curve QA",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D673_3_no_promotion",
            "target": "R10/R11/PPN/local-GR claims",
            "result": "blocked_nonclaim",
            "reason": "no generated row is valid_for_claim and the proof route did not sign Qbar_edge_XH=0",
            "next_action": "continue private derivation and source acquisition only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    proof_rows: list[dict[str, str]],
    glue_rows: list[dict[str, str]],
    acquisition_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    proof_claim_rows = sum(1 for row in proof_rows if row["valid_for_claim"] == "true")
    glue_claim_rows = sum(1 for row in glue_rows if row["valid_for_claim"] == "true")
    acquisition_claim_rows = sum(1 for row in acquisition_rows if row["valid_for_claim"] == "true")
    return [
        {
            "evaluator_id": "EV673_0_PiM_orthogonality",
            "target": "derive Qbar_edge_XH(lambda)=0",
            "status": "fail_nonclaim",
            "reason": "Hamiltonian projection target is exact but parent clauses remain unsigned",
            "claim_effect": "Qbar_edge_XH remains live",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV673_1_source_measure",
            "target": "inherit measured source mass theorem",
            "status": "fail_nonclaim",
            "reason": "source-measure theorem is conditional and boundary/reference first row is still unfilled",
            "claim_effect": "no measured-GM/Newton promotion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV673_2_acquisition_ledger",
            "target": "stage edge coefficient source rows",
            "status": "pass_nonclaim",
            "reason": f"proof_claim_rows={proof_claim_rows};glue_claim_rows={glue_claim_rows};acquisition_claim_rows={acquisition_claim_rows}",
            "claim_effect": "future source-backed run prepared, not claimed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV673_3_R10_branch",
            "target": "R10 alpha(lambda) edge comparison",
            "status": "blocked_nonclaim",
            "reason": "live bound file is placeholder and MTS edge rows lack parent coefficients",
            "claim_effect": "R10 remains blocked for this branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV673_4_next",
            "target": "select next target",
            "status": "edge_coefficient_row_fill_or_parent_PiM_clause",
            "reason": "the next useful work is either source-backed coefficients or a sharper parent action clause killing Q_edge projection",
            "claim_effect": "next private checkpoint only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS673_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Hamiltonian Pi_M orthogonality does not yet prove Qbar_edge_XH(lambda)=0",
            "blocked_claims": "Qbar_edge_zero;R10;R11;PPN;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def missing_markers(rows: list[dict[str, str]]) -> list[str]:
    markers = []
    for row in rows:
        combined = " ".join(str(value) for value in row.values()).upper()
        for marker in ("MISSING", "PLACEHOLDER", "NONCLAIM", "NOT_DERIVED", "NOT_SIGNED", "CONDITIONAL"):
            if marker in combined:
                markers.append(marker)
    return sorted(set(markers))


def validation_rows(
    source_rows: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    glue_rows: list[dict[str, str]],
    acquisition_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    evaluator: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    rows.append(
        {
            "check_id": "V673_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
            "generated_utc": now,
        }
    )

    validation_ids = [
        "539_validation",
        "540_validation",
        "541_validation",
        "542_validation",
        "543_validation",
        "544_validation",
        "629_validation",
        "671_validation",
        "672_validation",
    ]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append(
        {
            "check_id": "V673_1_prior_validations_clean",
            "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail",
            "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()),
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V673_2_orthogonality_proof_coverage",
            "result": "pass" if len(proof_rows) >= 8 else "fail",
            "detail": f"proof_rows={len(proof_rows)}",
            "generated_utc": now,
        }
    )

    required_proof_results = [row["current_result"] for row in proof_rows]
    unsigned_results = [result for result in required_proof_results if result in {"not_signed", "proof_failed_nonclaim", "not_parent_derived", "not_derived_for_current_MTS"}]
    rows.append(
        {
            "check_id": "V673_3_Qbar_edge_zero_not_promoted",
            "result": "pass" if unsigned_results and all(row["valid_for_claim"] == "false" for row in proof_rows) else "fail",
            "detail": "Qbar_edge_XH retained live; proof rows all nonclaim",
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V673_4_source_measure_glue_coverage",
            "result": "pass" if len(glue_rows) >= 7 else "fail",
            "detail": f"glue_rows={len(glue_rows)}",
            "generated_utc": now,
        }
    )

    required_coefficients = {
        "lambda_edge or F_lambda support",
        "K_edge(lambda)",
        "Qbar_edge_XH(lambda)",
        "qbar_XT",
        "B_X^nu=n_mu P^{mu nu}+B_ct^nu",
        "M_H or M_H_ref",
        "alpha_bound(lambda)",
        "alpha_edge(lambda) mapping",
    }
    actual_coefficients = {row["coefficient"] for row in acquisition_rows}
    rows.append(
        {
            "check_id": "V673_5_acquisition_required_coefficients",
            "result": "pass" if required_coefficients.issubset(actual_coefficients) else "fail",
            "detail": f"missing={';'.join(sorted(required_coefficients - actual_coefficients))}",
            "generated_utc": now,
        }
    )

    markers = missing_markers(acquisition_rows)
    rows.append(
        {
            "check_id": "V673_6_acquisition_rows_nonclaim_with_markers",
            "result": "pass" if markers and all(row["valid_for_claim"] == "false" for row in acquisition_rows) else "fail",
            "detail": "markers=" + ";".join(markers),
            "generated_utc": now,
        }
    )

    all_generated_rows = proof_rows + glue_rows + acquisition_rows + decision + evaluator
    claim_rows = [row for row in all_generated_rows if row.get("valid_for_claim") == "true"]
    rows.append(
        {
            "check_id": "V673_7_no_claim_rows_promoted",
            "result": "pass" if not claim_rows else "fail",
            "detail": "all generated rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}",
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V673_8_next_target_selected",
            "result": "pass" if any(row["next_action"] == NEXT_TARGET for row in decision) else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": now,
        }
    )

    output_paths = [
        RESIDUALS / "P8_Y5_R10_673_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_673_HAMILTONIAN_PIM_ORTHOGONALITY_PROOF_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_673_SOURCE_MEASURE_GLUE_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
        RESIDUALS / "P8_Y5_R10_673_ZERO_OR_SOURCE_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_673_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_673_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_673_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append(
        {
            "check_id": "V673_9_generated_outputs_scoped",
            "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail",
            "detail": "all 673 outputs target post-checkpoint-work",
            "generated_utc": now,
        }
    )

    changed_count = formalization_changed_count()
    rows.append(
        {
            "check_id": "V673_10_formalization_workbench_untouched",
            "result": "pass" if changed_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed_count}",
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V673_11_status_nonclaim",
            "result": "pass" if "no_Qbar_edge_zero" in CLAIM_CEILING and "no_R10" in CLAIM_CEILING else "fail",
            "detail": CLAIM_CEILING,
            "generated_utc": now,
        }
    )

    evaluator_statuses = [row["status"] for row in evaluator]
    rows.append(
        {
            "check_id": "V673_12_evaluator_nonclaim_passes",
            "result": "pass" if all("claim" in status or status == "edge_coefficient_row_fill_or_parent_PiM_clause" for status in evaluator_statuses) else "fail",
            "detail": ";".join(evaluator_statuses),
            "generated_utc": now,
        }
    )

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    glue_rows: list[dict[str, str]],
    acquisition_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 673 - Y5 R10 Edge Coefficient Source Acquisition Or Hamiltonian PiM Orthogonality Proof

## Verdict

673 tried the derivation route first: can Hamiltonian `Pi_M^H` make the edge charge invisible to the measured mass projection?

Result: not yet.

```text
Qbar_edge_XH(lambda) = Pi_M^H[Q_edge^H(lambda)] / M_H
```

is still unsigned because the Hamiltonian charge-map is candidate-useful but not parent-signed through integrability, fixed reference, same-frame source measure, projector-stress silence, and edge-kernel orthogonality.

So the edge branch remains nonclaim, but the source/acquisition target is now sharper: either find a parent action clause that makes `Q_edge` mass-orthogonal, or fill the edge coefficient rows with source-backed values.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Hamiltonian PiM Orthogonality Proof Audit

{markdown_table(proof_rows, ["proof_id", "clause", "mathematical_test", "current_result", "obstruction", "would_close", "fallback", "valid_for_claim"])}

## Source Measure Glue Audit

{markdown_table(glue_rows, ["glue_id", "requirement", "mathematical_form", "current_status", "residual_if_fail", "effect_on_Qbar_edge", "valid_for_claim"])}

## Edge Coefficient Acquisition Ledger

{markdown_table(acquisition_rows, ["acquisition_id", "coefficient", "formula_role", "acceptable_theorem_zero", "required_source_or_data", "current_status", "units", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default route: try one more parent-clause kill-shot only if it is genuinely sharper than the current gates. Otherwise fill edge coefficient rows as private, source-backed, nonclaim inputs and run the R10 comparator as a pressure test.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    proof_rows = pim_orthogonality_audit_rows()
    glue_rows = source_measure_glue_rows()
    acquisition_rows = acquisition_ledger_rows()
    decision = decision_rows()
    evaluator = evaluator_rows(proof_rows, glue_rows, acquisition_rows)
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, proof_rows, glue_rows, acquisition_rows, decision, evaluator)

    write_csv(RESIDUALS / "P8_Y5_R10_673_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_673_HAMILTONIAN_PIM_ORTHOGONALITY_PROOF_AUDIT.csv",
        proof_rows,
        ["proof_id", "clause", "mathematical_test", "current_result", "obstruction", "would_close", "fallback", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_673_SOURCE_MEASURE_GLUE_AUDIT.csv",
        glue_rows,
        ["glue_id", "requirement", "mathematical_form", "current_status", "residual_if_fail", "effect_on_Qbar_edge", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
        acquisition_rows,
        ["acquisition_id", "coefficient", "formula_role", "acceptable_theorem_zero", "required_source_or_data", "current_status", "units", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_673_ZERO_OR_SOURCE_DECISION.csv",
        decision,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_673_EVALUATOR.csv",
        evaluator,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_673_NONCLAIM_SUMMARY.csv",
        summary,
        ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_673_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, proof_rows, glue_rows, acquisition_rows, decision, evaluator, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"proof_rows={len(proof_rows)}")
    print(f"glue_rows={len(glue_rows)}")
    print(f"acquisition_rows={len(acquisition_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

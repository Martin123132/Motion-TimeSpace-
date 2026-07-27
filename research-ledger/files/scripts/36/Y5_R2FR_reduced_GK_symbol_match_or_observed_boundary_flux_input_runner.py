from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1649"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1649-Y5-R2FR-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md"

SOURCE_FILES = {
    "1648_doc": ROOT / "1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
    "1648_validation": OUT / "P8_Y5_BRR545_1648_VALIDATION.csv",
    "1648_next": OUT / "P8_Y5_PARENT_QLOC_1648_NEXT_TARGET.csv",
    "1648_clause_gate": OUT / "P8_Y5_PARENT_QLOC_1648_OBSERVED_FLUX_ZERO_CLAUSE_GATE.csv",
    "1648_component_fill": OUT / "P8_Y5_PARENT_QLOC_1648_DELTAH_CURL_COMPONENT_FILL.csv",
    "1590_doc": ROOT / "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md",
    "1590_owner": OUT / "P8_Y5_PARENT_QLOC_1590_OWNER_BUNDLE_SYNTHESIS.csv",
    "1618_doc": ROOT / "1618-Y5-R2FR-metric-response-Helmholtz-audit-or-q_loc-bound-schema.md",
    "1618_validation": OUT / "P8_Y5_BRR545_1618_VALIDATION.csv",
    "1618_metric": OUT / "P8_Y5_PARENT_QLOC_1618_METRIC_RESPONSE_AUDIT.csv",
    "1618_helmholtz": OUT / "P8_Y5_PARENT_QLOC_1618_HELMHOLTZ_AUDIT.csv",
    "1618_bound_schema": OUT / "P8_Y5_PARENT_QLOC_1618_QLOC_BOUND_SCHEMA_UPGRADE.csv",
    "1619_doc": ROOT / "1619-Y5-R2FR-positive-auxiliary-SGK-normal-form-or-q_loc-profile-row.md",
    "1619_validation": OUT / "P8_Y5_BRR545_1619_VALIDATION.csv",
    "1619_normal_form": OUT / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv",
    "1619_calculus": OUT / "P8_Y5_PARENT_QLOC_1619_METRIC_HELMHOLTZ_CALCULABILITY.csv",
    "1619_silence": OUT / "P8_Y5_PARENT_QLOC_1619_LOCAL_SILENCE_THEOREM.csv",
    "1619_profile": OUT / "P8_Y5_PARENT_QLOC_1619_QLOC_PROFILE_ROW.csv",
    "755_obstruction": OUT / "P8_Y5_R10_755_GK_SYMBOL_MATCH_OBSTRUCTION_LEDGER.csv",
    "756_metric": OUT / "P8_Y5_R10_756_METRIC_RESPONSE_SYMBOL_MATCH_AUDIT.csv",
    "756_validation": OUT / "P8_Y5_BRR545_756_VALIDATION.csv",
    "774_doc": ROOT / "774-Y5-R10-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md",
    "774_reentry": OUT / "P8_Y5_R10_774_REDUCED_GK_SYMBOL_MATCH_REENTRY_AUDIT.csv",
    "774_schema": OUT / "P8_Y5_R10_774_BOBS_INPUT_RUNNER_SCHEMA.csv",
    "774_dryrun": OUT / "P8_Y5_R10_774_BOBS_INPUT_RUNNER_DRYRUN.csv",
}

NEEDLES = {
    "1648_doc": ["1649-Y5-R2FR-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md", "B_observed_reduced_flux_over_MH"],
    "1648_validation": ["VAL1648_OVERALL", "PASS"],
    "1648_next": ["1649-Y5-R2FR-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md", "Gamma_eff"],
    "1648_clause_gate": ["OFC1648_1_Gamma_Khat_Ploc_owner", "BLOCKED_BY_REDUCED_GK_SYMBOL_MATCH"],
    "1648_component_fill": ["BCF1648_5_total_B_observed", "MISSING_COMPONENTS"],
    "1590_doc": ["OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS", "Gamma/Khat/Ploc owner bundle"],
    "1590_owner": ["OBS1590_5_owner_verdict", "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS"],
    "1618_doc": ["METRIC_RESPONSE_GATE_FAILS_CURRENT_CLAIM", "Helmholtz"],
    "1618_validation": ["VAL1618_OVERALL", "PASS"],
    "1618_metric": ["MRG1618_7_verdict", "METRIC_RESPONSE_GATE_FAILS_CURRENT_CLAIM"],
    "1618_helmholtz": ["HLA1618_5_verdict", "HELMHOLTZ_NOT_RUNNABLE_INPUTS_MISSING"],
    "1618_bound_schema": ["QBS1618_0_profile", "MISSING_QLOC_PROFILE_OPERATOR"],
    "1619_doc": ["FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED", "F_1=0"],
    "1619_validation": ["VAL1619_OVERALL", "PASS"],
    "1619_normal_form": ["NF1619_6_verdict", "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED"],
    "1619_calculus": ["CAL1619_3_Helmholtz_symmetry", "HELMHOLTZ_PASS_FOR_CONSTRUCTED_NORMAL_FORM_NOT_MTS"],
    "1619_silence": ["LS1619_3_q_loc_zero", "CONDITIONAL_QLOC_ZERO_FOR_NORMAL_FORM"],
    "1619_profile": ["QPR1619_0_normal_form_profile", "MISSING_PARENT_SIGNATURE"],
    "755_obstruction": ["GKO755_0_Gamma_scalar_density", "GKO755_2_Ploc_owner"],
    "756_metric": ["MRM756_5_verdict", "metric_response_symbol_match_not_accepted"],
    "756_validation": ["V756_3_symbol_match_failed_cleanly", "pass"],
    "774_doc": ["reduced GK symbol match still fails for current MTS", "observed `B_obs` component runner"],
    "774_reentry": ["RGM774_7_verdict", "fail_current_corpus"],
    "774_schema": ["BIR774_5_total_Bobs", "MISSING_COMPONENTS"],
    "774_dryrun": ["BDR774_0_symbol_match_certificate_absent", "blocked"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1649_SOURCE_REGISTER.csv"
SYMBOL_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1649_REDUCED_GK_SYMBOL_MATCH_AUDIT.csv"
REPAIR_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1649_RESPONSE_DISPLACEMENT_REPAIR_CONTRACT.csv"
BOBS_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1649_BOBS_INPUT_RUNNER_SCHEMA.csv"
BOBS_DRYRUN = OUT / "P8_Y5_PARENT_QLOC_1649_BOBS_INPUT_RUNNER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1649_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1649_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1649_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1649_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    SYMBOL_AUDIT,
    REPAIR_CONTRACT,
    BOBS_SCHEMA,
    BOBS_DRYRUN,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    SYMBOL_AUDIT,
    REPAIR_CONTRACT,
    BOBS_SCHEMA,
    BOBS_DRYRUN,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    SYMBOL_AUDIT: [
        QUARANTINE / "REDUCED_GK_SYMBOL_MATCH_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_reduced_GK_symbol_match_audit_nonclaim_1649.csv",
        QUEUE / "JR1649_REDUCED_GK_SYMBOL_MATCH_AUDIT_NONCLAIM.csv",
    ],
    REPAIR_CONTRACT: [
        QUARANTINE / "RESPONSE_DISPLACEMENT_REPAIR_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_response_displacement_repair_contract_nonclaim_1649.csv",
        QUEUE / "JR1649_RESPONSE_DISPLACEMENT_REPAIR_CONTRACT_NONCLAIM.csv",
    ],
    BOBS_SCHEMA: [
        QUARANTINE / "BOBS_INPUT_RUNNER_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Bobs_input_runner_schema_nonclaim_1649.csv",
        QUEUE / "JR1649_BOBS_INPUT_RUNNER_SCHEMA_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1649.csv",
        QUEUE / "JR1649_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {"valid_for_claim", "valid_for_mts_claim", "claim_allowed", "score_allowed", "reopens_local_claim"}
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1649 reduced GK symbol match and Bobs runner gate",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def symbol_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "match_id": "RGM1649_0_variational_contract",
            "target": "reduced GK Hilbert-stress owner",
            "required_identity": "S_GK^red = -int sqrt(-g_obs) gamma[Phi_red,g_obs] + boundary; T_GK^{mu nu}=Gamma_eff g_obs^{mu nu}-K_hat^{mu nu}",
            "current_evidence": "1648 and 774 retain the Ward route; 1590/1618/1619 show why the route is coherent.",
            "result": "PASS_CONDITIONAL_CONTRACT_ONLY",
            "repair_or_fallback": "use only as theorem contract until Gamma_eff/K_hat/P_loc clauses close",
            "blocks": "none by itself",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "match_id": "RGM1649_1_Gamma_scalar_density",
            "target": "Gamma_eff == gamma[g_obs,Phi_red,nablaPhi,D,...]",
            "required_identity": "Gamma_eff must be an explicit covariant scalar density with units, no fitted readout selector, and a source path to parent fields.",
            "current_evidence": "1618 says Gamma_eff is not yet a source-signed scalar density; 1590 says the owner bundle is not closed.",
            "result": "FAIL_CURRENT_CORPUS",
            "repair_or_fallback": "parent-sign the 1619 normal-form gamma or keep Gamma_eff as residual bookkeeping",
            "blocks": "Hilbert-stress owner and observed Ward no-flux theorem",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "match_id": "RGM1649_2_Khat_metric_response",
            "target": "K_hat == K_gamma",
            "required_identity": "K_gamma^{mu nu}=2/sqrt(-g_obs) delta[sqrt(-g_obs) gamma]/delta g_obs_{mu nu}, including derivative, boundary, projector, and domain terms.",
            "current_evidence": "1618 and 756 say K_hat has not been computed as the metric response of the current Gamma_eff.",
            "result": "FAIL_CURRENT_CORPUS",
            "repair_or_fallback": "compute K_gamma from a parent-signed gamma and compare tensor slots; otherwise carry Khat_unmatched_over_MH",
            "blocks": "Ward divergence identity for the current T_GK",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "match_id": "RGM1649_3_Helmholtz_integrability",
            "target": "stress tensor is variational",
            "required_identity": "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} has symmetric second-variation/Helmholtz structure up to boundary and gauge terms.",
            "current_evidence": "1618 makes the test exact but not runnable without explicit gamma/K_gamma; 1619 passes only for the constructed normal form.",
            "result": "NOT_CLOSED_CURRENT_CORPUS",
            "repair_or_fallback": "run Helmholtz only after explicit gamma and Khat are parent-signed",
            "blocks": "existence of a true S_GK owner",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "match_id": "RGM1649_4_Ploc_projector_descent",
            "target": "P_loc parent owner and commutator silence",
            "required_identity": "P_loc must descend from parent data and commute with local/readout/Hodge split on the allowed compact exterior domain.",
            "current_evidence": "755/756 and 1648 keep P_loc ownership, projector commutator, and tau/surface lock open.",
            "result": "OPEN_CURRENT_CORPUS",
            "repair_or_fallback": "derive parent projector algebra or keep B_obs_projector_commutator_over_MH live",
            "blocks": "projected q_loc and observed B_obs zero claims",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "match_id": "RGM1649_5_boundary_source_metric_terms",
            "target": "boundary/source/domain metric variations",
            "required_identity": "boundary, source-measure, compact-domain, and reference variations are included in K_gamma or theorem-zero/fixed-reference.",
            "current_evidence": "1648 stages B_obs_bulk, boundary, source-measure, corner/edge, and projector components as live missing rows.",
            "result": "OPEN_CURRENT_CORPUS",
            "repair_or_fallback": "fill Bobs component rows or prove observed reduced no-flux clauses",
            "blocks": "deltaH curl closure and local GR promotion",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "match_id": "RGM1649_6_response_doublet_rescue",
            "target": "positive auxiliary / response-displacement normal form",
            "required_identity": "formal Z field must be parent-signed to observed q_loc/Y5/Y6/PPN/boundary/coupling residual vector.",
            "current_evidence": "1619 proves a real formal double-zero/Helmholtz mechanism, but marks it not parent-signed for current MTS.",
            "result": "FORMAL_MECHANISM_RETAINED_NOT_MATCH",
            "repair_or_fallback": "turn Z into the actual vertical generator or switch to source-backed Bobs component inputs",
            "blocks": "using formal F_1=0 as observed local-GR proof",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "match_id": "RGM1649_7_verdict",
            "target": "accept reduced GK symbol match for current MTS",
            "required_identity": "RGM1649_1 through RGM1649_5 close without placeholders, and RGM1649_6 is parent-signed if used.",
            "current_evidence": "Gamma owner, Khat response, Helmholtz, P_loc descent, and observed boundary/source terms remain unsigned.",
            "result": "FAIL_CURRENT_CORPUS",
            "repair_or_fallback": "stage Bobs input runner and target response-displacement parent owner/source acquisition next",
            "blocks": "observed flux zero, deltaH zero, local GR, Newton, PPN, R10/R11 claims",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def repair_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "repair_id": "RDR1649_0_parent_response_field",
            "repair_route": "construct a parent response/displacement field Z_A whose scalar projection is gamma and whose tensor response is K_gamma",
            "required_deliverable": "explicit field variables; action density; units; variation with respect to g_obs; source path",
            "pass_condition": "Gamma_eff=gamma and K_hat=K_gamma are both derived from one parent object",
            "current_status": "NOT_FILLED",
            "fallback_if_missing": "Bobs component rows",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "repair_id": "RDR1649_1_vertical_generator_lock",
            "repair_route": "map response-displacement Z_A to the actual vertical generator / quotient kernel used by q_loc",
            "required_deliverable": "Dq(Z)=0 or exact quotient descent map; source-current coupling ledger; no hidden representative tuning",
            "pass_condition": "Z is not an auxiliary fiction but the real local residual coordinate",
            "current_status": "NOT_FILLED",
            "fallback_if_missing": "formal 1619 mechanism remains nonclaim",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "repair_id": "RDR1649_2_metric_response_computation",
            "repair_route": "compute K_gamma including derivative/boundary/domain terms",
            "required_deliverable": "tensor slot comparison table Khat-K_gamma with sign convention and boundary terms",
            "pass_condition": "all tensor components match or unmatched pieces are separately residualized",
            "current_status": "WAITING_ON_EXPLICIT_GAMMA_KGAMMA",
            "fallback_if_missing": "Khat_unmatched_over_MH and B_obs_boundary_improvement_over_MH rows",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "repair_id": "RDR1649_3_Helmholtz_integrability_test",
            "repair_route": "test whether proposed T_GK is variational",
            "required_deliverable": "second-variation symmetry/Helmholtz ledger for sqrt(-g)T_GK",
            "pass_condition": "stress derives from a scalar action up to declared exact boundary improvements",
            "current_status": "WAITING_ON_EXPLICIT_ACTION",
            "fallback_if_missing": "treat q_loc/B_obs as nonvariational residual",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "repair_id": "RDR1649_4_projector_descent",
            "repair_route": "derive P_loc from parent projector algebra before readout",
            "required_deliverable": "P_loc owner, commutator [d,P_loc] proof, and no hidden component tuning",
            "pass_condition": "P_loc may be applied after the Ward identity without creating leakage",
            "current_status": "OPEN",
            "fallback_if_missing": "B_obs_projector_commutator_over_MH row",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "repair_id": "RDR1649_5_no_public_claim_guard",
            "repair_route": "do not promote local GR from the contract alone",
            "required_deliverable": "all rows above parent-signed or source-backed",
            "pass_condition": "no MISSING markers and validation confirms no candidate artifacts were fabricated",
            "current_status": "GUARD_ACTIVE",
            "fallback_if_missing": "nonclaim status retained",
            "reopens_local_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def bobs_schema_rows() -> list[dict[str, object]]:
    rows = [
        ("BIR1649_0_bulk_Euler_flux", "B_obs_bulk_Euler_over_MH", "abs(P_loc sum_A E_A nabla^nu Phi_A contribution to curl(deltaH))/M_H_ref", "system_id;annulus;field_A;E_A;nabla_Phi_A;P_loc_component;M_H_ref;units;source_path;assumptions;valid_for_claim", "reduced Euler equations/profile or theorem-zero certificate", "MISSING_REDUCED_EULER_ZERO_OR_NUMERIC"),
        ("BIR1649_1_boundary_improvement_flux", "B_obs_boundary_improvement_over_MH", "abs(P_loc B_GK^nu plus reference/improvement contribution to curl(deltaH))/M_H_ref", "system_id;surface_id;boundary_class;B_GK_component;B_ref_component;P_loc_component;M_H_ref;units;source_path;assumptions;valid_for_claim", "fixed-reference no-flux theorem or finite-boundary flux source", "MISSING_BOUNDARY_REFERENCE_NO_FLUX_OR_NUMERIC"),
        ("BIR1649_2_source_measure_flux", "B_obs_source_measure_over_MH", "abs(P_loc B_source_measure^nu or C_qmu q_loc projected source-strength term)/M_H_ref", "system_id;source_channel;coupling_descent_status;C_qmu;flux_value;M_H_ref;units;source_path;assumptions;valid_for_claim", "same-frame source measure/no-marker theorem plus PiM closure or sourced coefficient", "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC"),
        ("BIR1649_3_corner_edge_flux", "B_obs_corner_edge_over_MH", "abs(non-proper observed edge/corner symplectic flux contribution)/M_H_ref", "system_id;corner_id;edge_mode_class;flux_value;proper_or_improper;M_H_ref;units;source_path;assumptions;valid_for_claim", "observed edge-mode zero theorem or corner flux source", "MISSING_OBSERVED_EDGE_MODE_ZERO_OR_NUMERIC"),
        ("BIR1649_4_projector_commutator_flux", "B_obs_projector_commutator_over_MH", "abs(integral_A [d,P_loc]J_red or [d,Pi_M]J_H contribution)/M_H_ref", "system_id;projector_id;commutator_value;domain_dependence;M_H_ref;units;source_path;assumptions;valid_for_claim", "parent-owned topological/projector descent theorem or finite commutator bound", "MISSING_PROJECTOR_DESCENT_ZERO_OR_NUMERIC"),
        ("BIR1649_5_total_Bobs", "B_observed_reduced_flux_over_MH", "sum of nonnegative BIR1649 components with no cancellation credit", "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim", "all component rows zero/bounded and no MISSING markers", "MISSING_COMPONENTS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": input_id,
            "quantity": quantity,
            "formula": formula,
            "required_columns": required_columns,
            "source_requirement": source_requirement,
            "current_status": current_status,
            "score_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for input_id, quantity, formula, required_columns, source_requirement, current_status in rows
    ]


def dryrun_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "BDR1649_0_symbol_match_certificate_absent",
            "check": "reduced GK symbol match claim data",
            "input_state": f"exists=False path={OUT / 'P8_Y5_PARENT_QLOC_1649_REDUCED_GK_SYMBOL_MATCH_CERTIFICATE.csv'}",
            "runner_effect": "symbol theorem cannot promote observed no-flux",
            "claim_status": "BLOCKED",
            "score_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "BDR1649_1_Bobs_candidate_absent",
            "check": "observed boundary flux numeric/theorem input",
            "input_state": f"exists=False path={OUT / 'P8_Y5_PARENT_QLOC_1649_BOBS_NUMERIC_INPUT_CANDIDATE.csv'}",
            "runner_effect": "no Bobs score is run; schema only",
            "claim_status": "BLOCKED",
            "score_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "BDR1649_2_missing_markers_guard",
            "check": "component rows contain MISSING status",
            "input_state": "BIR1649 rows intentionally MISSING_* until theorem/source rows exist",
            "runner_effect": "valid_for_claim remains false",
            "claim_status": "GUARD_PASSED",
            "score_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "BDR1649_3_no_cancellation_guard",
            "check": "total Bobs is nonnegative component sum",
            "input_state": "no cancellation credit allowed between bulk, boundary, source, edge, and projector pieces",
            "runner_effect": "future bounds must close every component or carry total residual",
            "claim_status": "GUARD_PASSED",
            "score_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1649_0_reduced_GK_symbol_match",
            "claim": "current Gamma_eff/K_hat/P_loc are parent-owned reduced variational objects",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "GAMMA_OWNER_KHAT_RESPONSE_HELMHOLTZ_PLOC_BOUNDARY_SOURCE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1649_1_formal_normal_form",
            "claim": "1619 formal normal form proves current MTS local GR",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "FORMAL_MECHANISM_NOT_PARENT_SIGNED_TO_CURRENT_MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1649_2_Bobs_runner",
            "claim": "Bobs component runner can score",
            "gate_pass": False,
            "status": "NOT_SCORED",
            "blocker": "COMPONENT_ROWS_AND_M_H_REF_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1649_3_local_GR_PPN_R10",
            "claim": "local GR, Newton, PPN, R10, or WEP pass follows from 1649",
            "gate_pass": False,
            "status": "NO_CLAIM",
            "blocker": "SYMBOL_MATCH_FAILS_AND_BOBS_REMAINS_LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1649_4_guardrail",
            "claim": "reduced GK symbol match guardrail is installed",
            "gate_pass": "INTERNAL_ONLY",
            "status": "PASS_AS_INTERNAL_GUARDRAIL_ONLY",
            "blocker": "guardrail is not evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1649_0_contract_retained",
            "decision": "retain reduced GK Ward route as a conditional theorem contract",
            "reason": "the algebra/action shape is coherent and remains the clean derivation path if ownership is supplied",
            "claim_status": "CONTRACT_ONLY",
            "next_target": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1649_1_symbol_match_fails",
            "decision": "do not accept current Gamma_eff/K_hat/P_loc as reduced GK variational objects",
            "reason": "Gamma scalar density, Khat metric response, Helmholtz, P_loc descent, and observed boundary/source accounting remain unsigned",
            "claim_status": "BLOCKED_FOR_CLAIM",
            "next_target": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1649_2_formal_mechanism_kept",
            "decision": "keep the 1619 positive auxiliary normal form as a real derivation mechanism but not a current promotion",
            "reason": "it proves F_1=0 and q_loc silence inside the constructed class, but not the parent signature to actual MTS variables",
            "claim_status": "FORMAL_ONLY_NONCLAIM",
            "next_target": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1649_3_Bobs_runner_staged",
            "decision": "stage observed-boundary-flux input runner without candidate data",
            "reason": "1648 made B_observed_reduced_flux_over_MH the live deltaH curl component if symbol ownership is not repaired",
            "claim_status": "SCHEMA_ONLY_NONCLAIM",
            "next_target": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1649_4_next_target",
            "decision": "hunt parent signature for response-displacement while preparing source acquisition for Bobs rows",
            "reason": "this keeps derivation-first alive but gives a bounded fallback if the owner cannot be parent-signed",
            "claim_status": "NEXT_TARGET_SELECTED",
            "next_target": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
            "script": "scripts/Y5_R2FR_response_displacement_parent_owner_or_Bobs_source_acquisition.py",
            "objective": "attempt to parent-sign the 1619 response-displacement/positive-auxiliary mechanism to the actual vertical generator; if not, acquire source-ready Bobs component inputs",
            "success_condition": "Z is mapped to the actual quotient vertical generator and Gamma_eff/K_hat/P_loc become one variational object, or every Bobs component row becomes source-backed nonclaim input",
            "forbidden_shortcuts": "no formal-normal-form promotion without parent signature; no representative boundary zero; no cancellation between Bobs components; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    symbol_rows: list[dict[str, object]],
    repair_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    dryrun: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = (
        FORMALIZATION.exists()
        and any(path.name.startswith("P8_Y5_PARENT_QLOC_1649") or "1649" in path.name for path in FORMALIZATION.rglob("*") if path.is_file())
    )

    checks = [
        (
            "VAL1649_0_sources_exist",
            all(row["path_exists"] and row["needles_found"] for row in source_rows),
            "all cited 1649 source paths exist and needles are present",
        ),
        (
            "VAL1649_1_symbol_audit_complete",
            len(symbol_rows) == 8 and any(row["match_id"] == "RGM1649_7_verdict" for row in symbol_rows),
            "reduced GK symbol match rows complete",
        ),
        (
            "VAL1649_2_symbol_match_failed_cleanly",
            any(row["match_id"] == "RGM1649_7_verdict" and row["result"] == "FAIL_CURRENT_CORPUS" for row in symbol_rows),
            "current corpus verdict remains fail_current_corpus",
        ),
        (
            "VAL1649_3_formal_mechanism_not_promoted",
            any(row["match_id"] == "RGM1649_6_response_doublet_rescue" and row["result"] == "FORMAL_MECHANISM_RETAINED_NOT_MATCH" for row in symbol_rows),
            "1619 normal-form mechanism retained as nonclaim",
        ),
        (
            "VAL1649_4_repair_contract_written",
            len(repair_rows) == 6 and all(row["valid_for_claim"] is False for row in repair_rows),
            "response-displacement repair contract written",
        ),
        (
            "VAL1649_5_Bobs_runner_schema_complete",
            len(schema_rows) == 6 and any(row["quantity"] == "B_observed_reduced_flux_over_MH" for row in schema_rows),
            "Bobs component input runner rows complete",
        ),
        (
            "VAL1649_6_runner_missing_markers",
            any(str(row["current_status"]).startswith("MISSING") for row in schema_rows),
            "runner rows stay MISSING_* until theorem/source rows exist",
        ),
        (
            "VAL1649_7_dryrun_blocks_without_data",
            any(row["dryrun_id"] == "BDR1649_0_symbol_match_certificate_absent" and row["claim_status"] == "BLOCKED" for row in dryrun)
            and any(row["dryrun_id"] == "BDR1649_1_Bobs_candidate_absent" and row["claim_status"] == "BLOCKED" for row in dryrun),
            "dry-run does not score absent symbol or Bobs candidates",
        ),
        (
            "VAL1649_8_claim_gates_safe",
            all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim_rows),
            "all claim gates keep MTS claims false",
        ),
        (
            "VAL1649_9_next_target_selected",
            next_targets[0]["next_target"] == "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
            "next target selects response-displacement parent owner / Bobs source acquisition",
        ),
        (
            "VAL1649_10_decision_matrix_safe",
            any(row["decision_id"] == "DEC1649_1_symbol_match_fails" for row in decisions)
            and any(row["decision_id"] == "DEC1649_4_next_target" for row in decisions),
            "decision matrix records failure and next target",
        ),
        (
            "VAL1649_11_csv_parse",
            generated_csv_parse,
            "all generated 1649 CSVs parse",
        ),
        (
            "VAL1649_12_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1649 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1649_13_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1649_14_queue_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1649_15_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1649_16_formalization_untouched",
            not formalization_dirty,
            "no 1649 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1649_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1649 reduced GK symbol match and Bobs input runner validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    symbol_rows: list[dict[str, object]],
    repair_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    dryrun: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1649 - Reduced GK Symbol Match Or Observed Boundary Flux Input Runner

**Private status:** nonclaim checkpoint. No reduced GK symbol match, observed reduced flux zero, `delta_H_tau` zero, stable Hamiltonian charge, `M_H_ref`, `M_*`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

The reduced GK/Ward route is still alive, but current MTS has not paid the entry fee.

The required contract is:

```text
S_GK^red = -int sqrt(-g_obs) gamma[Phi_red,g_obs] + boundary
T_GK^{{mu nu}} = Gamma_eff g_obs^{{mu nu}} - K_hat^{{mu nu}}
K_hat^{{mu nu}} = K_gamma^{{mu nu}} = 2/sqrt(-g_obs) delta[sqrt(-g_obs) gamma]/delta g_obs_{{mu nu}}
q_loc^nu = P_loc nabla_mu T_GK^{{mu nu}}
```

The 1619 positive auxiliary / response-displacement normal form gives a genuine formal mechanism: inside that constructed class it can own `Gamma_eff`, define `K_hat`, pass Helmholtz by construction, and give `F_1=0`. But it is **not yet parent-signed to the current MTS variables**, the actual vertical generator, source-current descent, `P_loc`, and observed boundary/source terms. So the symbol match fails for current-claim purposes, and `B_observed_reduced_flux_over_MH` remains the fallback component runner.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Reduced GK Symbol Match Audit

{markdown_table(symbol_rows, ["match_id", "target", "required_identity", "result", "repair_or_fallback", "blocks"])}

## Response-Displacement Repair Contract

{markdown_table(repair_rows, ["repair_id", "repair_route", "required_deliverable", "pass_condition", "current_status", "fallback_if_missing"])}

## Bobs Input Runner Schema

{markdown_table(schema_rows, ["input_id", "quantity", "formula", "required_columns", "source_requirement", "current_status"])}

## Runner Dry Run

{markdown_table(dryrun, ["dryrun_id", "check", "input_state", "runner_effect", "claim_status"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is not a dead end. It is a narrowing of the throat. The cleanest route now is to try to make the 1619 response-displacement field the actual parent vertical generator. If that works, the formal mechanism becomes a real local-GR derivation route. If it fails, the honest fallback is source-backed `B_obs` component bounds, not a plateau axiom or representative-boundary shortcut.
"""
    DOC.write_text(text, encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    symbol_rows = symbol_audit_rows()
    repair_rows = repair_contract_rows()
    schema_rows = bobs_schema_rows()
    dryrun = dryrun_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(SYMBOL_AUDIT, symbol_rows)
    write_csv(REPAIR_CONTRACT, repair_rows)
    write_csv(BOBS_SCHEMA, schema_rows)
    write_csv(BOBS_DRYRUN, dryrun)
    write_csv(CLAIM_GATE, claim_rows)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_targets)
    copy_outputs()

    validation = validation_rows(source_rows, symbol_rows, repair_rows, schema_rows, dryrun, claim_rows, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, symbol_rows, repair_rows, schema_rows, dryrun, claim_rows, decisions, next_targets, validation)
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()

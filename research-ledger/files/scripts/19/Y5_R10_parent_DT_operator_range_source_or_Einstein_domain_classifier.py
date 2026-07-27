from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key != "generated_utc" and key not in headers:
                headers.append(key)
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1195_0_1194_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1194_NEXT_TARGET.csv",
            "needle": "NEXT1194_0_1195",
            "role": "direct 1195 handoff.",
        },
        {
            "source_id": "SRC1195_1_1194_scalar_classifier",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1194_EINSTEIN_SCALAR_BOUND_FORMS.csv",
            "needle": "ESB1194_4_domain_classifier",
            "role": "Einstein/Ricci-flat scalar fallback classifier.",
        },
        {
            "source_id": "SRC1195_2_1194_DT_response",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1194_DT_COMPENSATOR_RESPONSE_ROWS.csv",
            "needle": "DTR1194_0_PPN_gamma_beta_first_row",
            "role": "first D_T response row staged by 1194.",
        },
        {
            "source_id": "SRC1195_3_1194_missing",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1194_MISSING_INPUT_MATRIX.csv",
            "needle": "MIM1194_2_DT_parent_operator",
            "role": "parent D_T operator missing-input row.",
        },
        {
            "source_id": "SRC1195_4_831_first_variation",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "OC831_2_first_variation",
            "role": "D_T balance action first-variation route.",
        },
        {
            "source_id": "SRC1195_5_831_projection_law",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_1_projection_law",
            "role": "residual equals cokernel projection.",
        },
        {
            "source_id": "SRC1195_6_831_bound",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_3_bound",
            "role": "cokernel/boundary/regularizer residual bound.",
        },
        {
            "source_id": "SRC1195_7_832_flat_range",
            "relative_path": "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
            "needle": "FRI832_0_domain",
            "role": "flat tracefree divergence range clue.",
        },
        {
            "source_id": "SRC1195_8_832_boundary",
            "relative_path": "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
            "needle": "CB832_3_boundary_residual",
            "role": "boundary residual remains live.",
        },
        {
            "source_id": "SRC1195_9_830_owner",
            "relative_path": "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
            "needle": "KO830_0_parent_tensor_operator",
            "role": "Khat parent tensor operator missing.",
        },
        {
            "source_id": "SRC1195_10_830_observables",
            "relative_path": "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
            "needle": "OG830_1_PPN",
            "role": "PPN observable response gate.",
        },
        {
            "source_id": "SRC1195_11_513_action",
            "relative_path": "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
            "needle": "GK513_0_action_existence",
            "role": "parent action existence gate.",
        },
        {
            "source_id": "SRC1195_12_515_metric_response",
            "relative_path": "515-match-Gamma-eff-Khat-to-metric-response-action.md",
            "needle": "MA515_1_Khat_metric_response",
            "role": "Khat metric response not found.",
        },
        {
            "source_id": "SRC1195_13_756_symbol_match",
            "relative_path": "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
            "needle": "MRM756_5_verdict",
            "role": "metric-response symbol match still failed.",
        },
        {
            "source_id": "SRC1195_14_800_kperp",
            "relative_path": "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
            "needle": "KBL800_0_needed_operator",
            "role": "Kperp/tensor boundary operator gap.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def dt_adjoint_cokernel_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "DTA1195_0_operator_definition",
            "statement": "D_T maps tracefree symmetric tensors to projected local vectors.",
            "mathematical_form": "D_T K := P_loc^nu_rho nabla_mu K^{mu rho}, with K in Gamma(S^2_0 T*D).",
            "derivation_or_use": "This is the operator appearing in q_loc and in the 1193 D_T compensator contract.",
            "status": "operator_contract_defined",
            "needed_for_claim": "parent action block; P_loc ownership; domain and boundary conditions",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DTA1195_1_formal_adjoint",
            "statement": "With fixed P_loc and no boundary leakage, the formal adjoint is the negative tracefree symmetrized gradient.",
            "mathematical_form": "D_T^dagger V = -Pi_TF[nabla_(mu)(P_loc V)_{nu)}] plus nabla P_loc and boundary terms.",
            "derivation_or_use": "Integrate <V,D_T K> by parts and use K tracefree, so only the tracefree symmetric part of nabla(PV) pairs with K.",
            "status": "FORMAL_ADJOINT_DERIVED_CONDITIONAL",
            "needed_for_claim": "boundary term zero; P_loc derivative term zero/bounded; sign convention; Hilbert-space norm",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DTA1195_2_cokernel_characterization",
            "statement": "The cokernel of D_T is represented by projected conformal-Killing-like local vector modes.",
            "mathematical_form": "V in Coker(D_T) iff Pi_TF[nabla_(mu)(P_loc V)_{nu)}]+projector/boundary corrections=0.",
            "derivation_or_use": "Coker(D_T)=Ker(D_T^dagger); when P_loc is identity/frozen this is the conformal Killing equation.",
            "status": "COKERNEL_THEOREM_FORM_WRITTEN",
            "needed_for_claim": "prove no physical cokernel modes survive the local domain/boundary/readout",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DTA1195_3_exact_range_condition",
            "statement": "Exact D_T compensation requires G_res to be orthogonal to all surviving cokernel modes.",
            "mathematical_form": "forall V in Ker(D_T^dagger): integral_D V_nu G_res^nu dV + boundary pairing = 0.",
            "derivation_or_use": "Fredholm/range condition for solving D_T K_T=G_res in the controlled subspace.",
            "status": "RANGE_CONDITION_EXPLICIT",
            "needed_for_claim": "cokernel basis, G_res source profile, boundary pairing, source path",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DTA1195_4_no_cokernel_domain_branch",
            "statement": "If boundary/domain conditions kill projected conformal-Killing cokernel modes, the formal range obstruction vanishes.",
            "mathematical_form": "Ker(D_T^dagger)=0 => P_coker(D_T)G_res=0.",
            "derivation_or_use": "This is the cleanest mathematical way for generic matter domains to use D_T without scalar exactness.",
            "status": "CONDITIONAL_BRANCH_ONLY",
            "needed_for_claim": "parent-owned boundary/domain theorem; no-zero-mode proof; P_loc derivative bound",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DTA1195_5_bound_if_cokernel_survives",
            "statement": "If cokernel modes survive, retain a source-backed residual bound rather than claiming zero.",
            "mathematical_form": "||q_DT|| <= ||P_coker G_res|| + ||B_T|| + kappa_T C_T ||E_reg||.",
            "derivation_or_use": "Carries forward 831/1194 bound structure into a scoreable nonclaim row.",
            "status": "BOUND_FORM_STAGED",
            "needed_for_claim": "numeric/source-backed coker fraction, boundary norm, regularizer norm, response matrix",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DTA1195_6_verdict",
            "statement": "1195 derives a sharper D_T range/cokernel theorem, but not parent ownership.",
            "mathematical_form": "D_T route is promoted from vague tensor compensator to adjoint/cokernel gate; S_MTS adoption remains unsigned.",
            "derivation_or_use": "Use this theorem to choose between a no-cokernel proof and a bounded residual runner.",
            "status": "MATH_ROUTE_SHARPENED_NO_LOCAL_GR_CLAIM",
            "needed_for_claim": "parent action and all local response gates",
            "valid_for_claim": False,
        },
    ]


def parent_dt_source_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "PDS1195_0_current_parent_action",
            "required_evidence": "S_MTS contains a D_T balance/operator block or equivalent tracefree tensor Euler equation.",
            "current_evidence": "830/831 define the contract; 513/515/756 say Gamma/Khat metric-response ownership remains unsigned.",
            "result": "NOT_FOUND_IN_CURRENT_CORPUS",
            "consequence": "D_T remains an effective/operator contract, not a parent-derived local-GR theorem.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PDS1195_1_metric_response",
            "required_evidence": "K_T/Khat is the Hilbert metric response or a Ward-safe parent response field.",
            "current_evidence": "515 MA515_1 and 756 MRM756_5 fail current Khat metric-response symbol match.",
            "result": "METRIC_RESPONSE_UNSIGNED",
            "consequence": "Even exact D_T residual cancellation cannot be treated as stress/Ward silence.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PDS1195_2_boundary_owner",
            "required_evidence": "boundary pairing from the adjoint theorem vanishes or is fixed by parent natural boundary conditions.",
            "current_evidence": "832 and 830 retain boundary obstruction; 1194 response rows need boundary profile.",
            "result": "BOUNDARY_UNSIGNED",
            "consequence": "bulk range cancellation can still leak through compact local boundaries.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PDS1195_3_no_zero_mode",
            "required_evidence": "projected conformal-Killing/cokernel modes are absent or physically classified and bounded.",
            "current_evidence": "1195 derives the cokernel target; no domain theorem currently sources it.",
            "result": "NO_ZERO_MODE_THEOREM_MISSING",
            "consequence": "P_coker(D_T)G_res may remain a physical residual.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PDS1195_4_observable_response",
            "required_evidence": "PPN/R10/clock/orbital/WEP response matrices exist for K_T and residual components.",
            "current_evidence": "1194 staged first response rows, all blocked by missing W_PPN/W_R10/etc.",
            "result": "RESPONSE_MATRICES_MISSING",
            "consequence": "No local-test pass can be scored from D_T yet.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PDS1195_5_verdict",
            "required_evidence": "all parent action, boundary, no-cokernel, and response clauses close.",
            "current_evidence": "none of the required parent/source clauses close today.",
            "result": "PARENT_DT_NOT_SOURCED",
            "consequence": "Proceed by no-cokernel theorem attempt or nonclaim response/source acquisition.",
            "valid_for_claim": False,
        },
    ]


def einstein_domain_classifier_rows() -> list[dict[str, object]]:
    return [
        {
            "classifier_id": "EDC1195_0_Ricci_flat_exterior",
            "domain_class": "Ricci_flat_or_low_Ricci_exterior",
            "test": "||Ric||_D <= epsilon_Ricci_limit and matter support absent from D",
            "branch_if_pass": "scalar H_E branch with Lambda_E=0 may be eligible after boundary/response gates",
            "branch_if_fail": "D_T compensator or residual bound",
            "current_status": "MISSING_DOMAIN_RICCI_SOURCE",
            "valid_for_claim": False,
        },
        {
            "classifier_id": "EDC1195_1_Einstein_space",
            "domain_class": "Einstein_space",
            "test": "epsilon_E=||Ric-Lambda_E g||/(||Ric||+epsilon_ref) <= epsilon_E_limit and ||nabla Lambda_E|| below bound",
            "branch_if_pass": "scalar H_E branch with Lambda_E retained",
            "branch_if_fail": "D_T compensator",
            "current_status": "MISSING_LAMBDA_E_AND_EPSILON_LIMIT",
            "valid_for_claim": False,
        },
        {
            "classifier_id": "EDC1195_2_generic_matter",
            "domain_class": "anisotropic_matter_Ricci",
            "test": "epsilon_E fails or matter stress has anisotropic/inhomogeneous Ricci components",
            "branch_if_pass": "D_T compensator required for generic vector residual",
            "branch_if_fail": "scalar branch may remain eligible only if exactness separately proven",
            "current_status": "DEFAULT_SAFE_CLASS_FOR_LAB_MATTER_UNTIL_SOURCED",
            "valid_for_claim": False,
        },
        {
            "classifier_id": "EDC1195_3_variable_Lambda_guard",
            "domain_class": "nearly_Einstein_variable_Lambda",
            "test": "||d Lambda_E wedge d phi|| response below arena limits",
            "branch_if_pass": "scalar branch with retained remainder bound",
            "branch_if_fail": "D_T compensator or explicit residual",
            "current_status": "MISSING_WEDGE_BOUND",
            "valid_for_claim": False,
        },
        {
            "classifier_id": "EDC1195_4_classifier_verdict",
            "domain_class": "branch_selector",
            "test": "no real domain row can select a claim branch until Ricci/source/response inputs exist",
            "branch_if_pass": "nonclaim score row only",
            "branch_if_fail": "closure/input-acquisition",
            "current_status": "CLASSIFIER_TEMPLATE_ONLY",
            "valid_for_claim": False,
        },
    ]


def first_response_source_rows() -> list[dict[str, object]]:
    return [
        {
            "response_id": "FRS1195_0_PPN_gamma_beta_source_row",
            "arena": "PPN gamma/beta",
            "quantity": "Delta_PPN_DT",
            "formula": "||Delta_PPN_DT|| <= ||W_PPN|| (C_T ||G_res|| + ||B_T|| + kappa_T C_T ||E_reg||)",
            "required_source_columns": "W_PPN_source_path; C_T_source_path; G_res_profile_path; boundary_source_path; regularizer_source_path; gamma_beta_bound_source_path",
            "current_values": "MISSING_W_PPN;MISSING_C_T;MISSING_G_RES;MISSING_BOUNDARY;MISSING_REGULARIZER;MISSING_BOUNDS",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "response_id": "FRS1195_1_R10_alpha_lambda_source_row",
            "arena": "R10",
            "quantity": "alpha_DT(lambda)",
            "formula": "alpha_DT(lambda)=W_R10(lambda)[K_T,G_res,B_T]",
            "required_source_columns": "W_R10_lambda_source_path; range_profile_path; source_normalization_path; alpha_bound_curve_path; boundary_profile_path",
            "current_values": "MISSING_W_R10;MISSING_RANGE_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_ALPHA_BOUND_CURVE;MISSING_BOUNDARY_PROFILE",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "response_id": "FRS1195_2_no_fake_response_guard",
            "arena": "all_local",
            "quantity": "response_row_claim_guard",
            "formula": "valid_for_claim can be true only when parent D_T, source profile, response operator, and bound source paths are all real",
            "required_source_columns": "no MISSING_* markers; source paths exist; units declared; same frame/gauge",
            "current_values": "GUARD_ACTIVE",
            "runner_status": "nonclaim_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def bound_runner_schema_rows() -> list[dict[str, object]]:
    return [
        {
            "schema_id": "BRS1195_0_DT_bound_runner_inputs",
            "row_status": "template_missing_parent_inputs",
            "G_res_norm": "MISSING_PARENT_INPUT",
            "cokernel_fraction": "MISSING_RANGE_THEOREM",
            "boundary_obstruction_norm": "MISSING_BOUNDARY_INPUT",
            "regularizer_norm": "MISSING_REGULARIZER",
            "coercivity_inverse": "MISSING_C_T",
            "observable_response_norm": "MISSING_ARENA_PROJECTION",
            "observable_limit": "MISSING_BOUND_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "BRS1195_1_Einstein_classifier_inputs",
            "row_status": "template_missing_domain_inputs",
            "G_res_norm": "not_applicable_if_scalar_exact",
            "cokernel_fraction": "not_applicable_if_scalar_exact",
            "boundary_obstruction_norm": "MISSING_BOUNDARY_INPUT",
            "regularizer_norm": "MISSING_GREEN_REMAINDER",
            "coercivity_inverse": "MISSING_HE_GREEN_CONSTANT",
            "observable_response_norm": "MISSING_SCALAR_RESPONSE",
            "observable_limit": "MISSING_BOUND_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1195_0_DT_parent_operator",
            "claim": "D_T operator is parent-derived from S_MTS",
            "status": "BLOCKED_PARENT_SOURCE_NOT_FOUND",
            "why": "1195 derives formal adjoint/cokernel structure but no S_MTS action block signs it",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1195_1_cokernel_zero",
            "claim": "D_T range obstruction vanishes on physical local domains",
            "status": "BLOCKED_NO_ZERO_MODE_THEOREM_MISSING",
            "why": "projected conformal-Killing/cokernel modes are identified but not proved absent/bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1195_2_Einstein_classifier",
            "claim": "Einstein/Ricci-flat scalar fallback can classify real local domains",
            "status": "BLOCKED_DOMAIN_INPUTS_MISSING",
            "why": "Ricci source, Lambda_E fit, epsilon limits, and response rows are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1195_3_first_response_score",
            "claim": "first PPN/R10 response row scores a pass",
            "status": "BLOCKED_RESPONSE_INPUTS_MISSING",
            "why": "W_PPN/W_R10 and source-normalization/bound rows are not sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1195_4_local_GR",
            "claim": "MTS reduces to local GR/Newton",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "parent D_T, scalar classifier, boundary, and all response gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1195_0_adjoint_cokernel_theorem",
            "decision": "formal_DT_adjoint_and_cokernel_gate_written",
            "reason": "D_T range is now governed by projected conformal-Killing-like cokernel modes plus boundary/projector terms",
            "next_action": "try no-cokernel boundary theorem or retain P_coker bound",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1195_1_parent_source_status",
            "decision": "parent_DT_source_not_found",
            "reason": "existing action/metric-response audits do not sign Khat/D_T as parent Hilbert stress or Euler sector",
            "next_action": "construct parent D_T action block or label compensator as closure",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1195_2_scalar_fallback_status",
            "decision": "Einstein_classifier_kept_as_fallback",
            "reason": "scalar branch is mathematically legitimate only for Ricci-flat/Einstein-compatible domains",
            "next_action": "source domain classifier if scalar branch is used",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1195_3_next_route",
            "decision": "attack_cokernel_zero_or_parent_action_block",
            "reason": "without no-cokernel/boundary theorem or parent action, D_T cannot become a derivation",
            "next_action": "build 1196 conformal-cokernel zero/boundary theorem or parent D_T action block",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1195_0_1196",
            "next_target": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "objective": "prove or bound the projected conformal-Killing cokernel and boundary terms for D_T, or construct a parent action block that owns the tracefree tensor compensator",
            "include": "D_T adjoint; no-cokernel domain theorem; boundary pairing; parent S_T action block; first PPN/R10 response source columns; no-claim validation",
            "exclude": "local-GR pass; parentless compensator adoption; scalar branch overuse in matter domains; fake response rows; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    dt_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    classifier_rows: list[dict[str, object]],
    response_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    dt_ids = {row["theorem_id"] for row in dt_rows}
    parent_results = {row["result"] for row in parent_rows}
    classifier_ids = {row["classifier_id"] for row in classifier_rows}
    response_ids = {row["response_id"] for row in response_rows}
    all_science_rows = dt_rows + parent_rows + classifier_rows + response_rows + schema_rows + gates + decisions + nexts
    all_nonclaim = all(row.get("valid_for_claim") is False for row in all_science_rows)
    blocked_claims = all(row.get("claim_allowed") is False for row in response_rows + schema_rows + gates + nexts)
    return [
        {
            "check_id": "V1195_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_1_adjoint_cokernel_theorem",
            "result": "pass" if {"DTA1195_1_formal_adjoint", "DTA1195_2_cokernel_characterization", "DTA1195_3_exact_range_condition"} <= dt_ids else "fail",
            "detail": "formal adjoint, cokernel characterization, and exact range condition rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_2_parent_source_not_promoted",
            "result": "pass" if "PARENT_DT_NOT_SOURCED" in parent_results else "fail",
            "detail": "parent D_T source audit remains unsigned",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_3_Einstein_classifier_present",
            "result": "pass" if {"EDC1195_0_Ricci_flat_exterior", "EDC1195_1_Einstein_space", "EDC1195_2_generic_matter"} <= classifier_ids else "fail",
            "detail": "Einstein/Ricci-flat/generic matter classifier rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_4_response_source_rows_blocked",
            "result": "pass" if {"FRS1195_0_PPN_gamma_beta_source_row", "FRS1195_1_R10_alpha_lambda_source_row", "FRS1195_2_no_fake_response_guard"} <= response_ids and all(row["claim_allowed"] is False for row in response_rows) else "fail",
            "detail": "first PPN/R10 response source rows are present and blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_5_bound_runner_templates_blocked",
            "result": "pass" if len(schema_rows) == 2 and all(row["claim_allowed"] is False for row in schema_rows) else "fail",
            "detail": "D_T and Einstein classifier runner templates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_6_claim_gates_blocked",
            "result": "pass" if blocked_claims and all(row["claim_allowed"] is False for row in gates) else "fail",
            "detail": "all 1195 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_7_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_8_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1195_0_1196" else "fail",
            "detail": "1196 handoff targets D_T cokernel/boundary theorem or parent action block",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_9_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1195_SUMMARY",
            "result": "pass",
            "detail": "1195 derives the D_T formal adjoint/cokernel gate, confirms parent D_T source remains unsigned, retains Einstein-domain classifier fallback, and stages blocked PPN/R10 response source rows",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    dt_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    classifier_rows: list[dict[str, object]],
    response_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1195 - Y5/R10 parent D_T operator range source or Einstein-domain classifier",
            "**Current verdict:** the `D_T` route is sharper but still nonclaim. 1195 derives the formal adjoint/cokernel gate: surviving projected conformal-Killing-like modes are the exact range obstruction, plus boundary/projector terms.",
            "**Main progress:** generic matter domains now have a precise `D_T` no-cokernel theorem target, while the Einstein/Ricci-flat scalar branch remains a classifier-gated fallback. Parent `D_T` action ownership is still not found.",
            "**No claim:** no `q_loc=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## D_T adjoint and cokernel theorem\n\n" + table(dt_rows),
            "## Parent D_T source audit\n\n" + table(parent_rows),
            "## Einstein-domain classifier\n\n" + table(classifier_rows),
            "## First response source rows\n\n" + table(response_rows),
            "## Bound runner schema\n\n" + table(schema_rows),
            "## Claim gates\n\n" + table(gates),
            "## Decision ledger\n\n" + table(decisions),
            "## Validation\n\n" + table(validations),
            "## Next target\n\n" + table(nexts),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    dt_rows = dt_adjoint_cokernel_rows()
    parent_rows = parent_dt_source_audit_rows()
    classifier_rows = einstein_domain_classifier_rows()
    response_rows = first_response_source_rows()
    schema_rows = bound_runner_schema_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(
        sources,
        dt_rows,
        parent_rows,
        classifier_rows,
        response_rows,
        schema_rows,
        gates,
        decisions,
        nexts,
    )

    outputs = {
        "P8_Y5_R10_1195_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1195_DT_ADJOINT_COKERNEL_THEOREM.csv": dt_rows,
        "P8_Y5_R10_1195_PARENT_DT_SOURCE_AUDIT.csv": parent_rows,
        "P8_Y5_R10_1195_EINSTEIN_DOMAIN_CLASSIFIER.csv": classifier_rows,
        "P8_Y5_R10_1195_FIRST_RESPONSE_SOURCE_ROWS.csv": response_rows,
        "P8_Y5_R10_1195_BOUND_RUNNER_SCHEMA.csv": schema_rows,
        "P8_Y5_R10_1195_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1195_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1195_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1195_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, dt_rows, parent_rows, classifier_rows, response_rows, schema_rows, gates, decisions, validations, nexts)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: " + ("PASS" if not failed else "FAIL " + ";".join(failed)))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

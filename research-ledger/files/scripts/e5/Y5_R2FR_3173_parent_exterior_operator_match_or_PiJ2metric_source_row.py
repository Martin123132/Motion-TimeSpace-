from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3173_INPUTS.csv"
OPERATOR = OUT / "P8_Y5_R2FR_3173_OPERATOR_MATCH_DERIVATION.csv"
AUDIT = OUT / "P8_Y5_R2FR_3173_CURRENT_ARTIFACT_AUDIT.csv"
EXTRACTOR = OUT / "P8_Y5_R2FR_3173_PIJ2_EXTRACTOR_CONTRACT.csv"
SOURCE_ROWS = OUT / "P8_Y5_R2FR_3173_SOURCE_READY_NONCLAIM_ROWS.csv"
DECISION = OUT / "P8_Y5_R2FR_3173_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3173_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3172-Y5-R2FR-public-metric-radial-Green-owner-or-J2-channel-closure-under-AX1090.md", "3172 Green-profile handoff and Upsilon_J2 bottleneck"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3172_CLOSURE_CONTRACT.csv", "3172 composite transfer contract"),
        ("3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.md", "public weak-field metric/J2 readout once A_metric is owned"),
        ("3164-Y5-R2FR-Wbar-sensitivity-bound-or-KLambdaW-closure-lane-under-AX1090.md", "K2 as restricted Wbar/Lambda l=2 lane"),
        ("3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090.md", "generic Delta_i=Pi_i,K2 K2 C_K2_unit residual vector"),
        ("04-vacuum-reciprocity-action-contract.md", "local reciprocal-strain parent-action contract"),
        ("07-nonpropagating-reciprocity-constraint.md", "clean R_AB constraint lane and parent-origin gap"),
        ("10-observer-map-symplectic-contract.md", "observer/coframe local-GR no-smuggling contract"),
        ("11-cell-current-origin-attempt.md", "cell-current no-charge obstruction"),
    ]
    return [
        {
            "input_id": f"IN3173_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def operator_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "derivation_id": "OP3173_0_parent_linearization",
            "object": "parent action Hessian",
            "statement": "Let Phi_A be the parent field vector and sigma := K2*C_K2_unit be the small l=2 source/residual lane. Around the local exterior background Phi0, expand the Euler-Lagrange equations to first order.",
            "formula": "0 = E_A[Phi0+deltaPhi;sigma] = L_AB deltaPhi_B + S_A sigma + O(deltaPhi^2,sigma^2)",
            "required_owner": "L_AB = delta E_A/delta Phi_B and S_A = partial E_A/partial sigma from the parent MTS action",
            "status": "derived_formal_operator_identity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "OP3173_1_solution_on_quotient",
            "object": "linearized parent response",
            "statement": "After gauge/constraint quotienting and boundary-condition choice, the first-order response is the parent Green response to the K2 lane.",
            "formula": "deltaPhi_B = - (L^{-1})_BA S_A sigma",
            "required_owner": "invertible or gauge-fixed parent operator on the physical quotient, with no hidden GR field-equation import",
            "status": "conditional_solution_formula",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "OP3173_2_public_metric_readout",
            "object": "surface l=2 public metric amplitude",
            "statement": "Let E_metric map parent perturbations into the public metric perturbation and P_surf,l2 extract the solar-surface quadrupole amplitude.",
            "formula": "A_surface = P_surf,l2 E_metric[deltaPhi]",
            "required_owner": "public metric readout map E_metric and l=2 surface projector P_surf,l2",
            "status": "readout_formula_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "OP3173_3_exact_Upsilon_formula",
            "object": "Upsilon_J2",
            "statement": "Combining the first-order parent response and public metric readout gives the exact non-fitted transfer kernel.",
            "formula": "Upsilon_J2 = - P_surf,l2 E_metric L_parent^{-1} S_K2",
            "required_owner": "all factors must be parent-defined, source-backed, dimensionally checked, and evaluated in the same solar-source/coframe convention",
            "status": "exact_extractor_contract_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "OP3173_4_public_exterior_match",
            "object": "parent exterior operator match",
            "statement": "The 3172 r^-3 theorem applies only if the public metric component produced by E_metric L_parent^{-1} S_K2 obeys the source-free exterior l=2 Laplace/linearized-GR channel outside the source.",
            "formula": "P_ext,l2 E_metric L_parent^{-1} S_K2 -> f_2(r) with r^2 f_2''+2r f_2'-6f_2=0",
            "required_owner": "parent exterior operator reduces to the public weak-field l=2 metric operator on this channel",
            "status": "conditional_operator_match_test",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "OP3173_5_trace_constraint_no_shortcut",
            "object": "R_AB constraint lane versus J2 metric channel",
            "statement": "The R_AB=0 nonpropagating constraint can enforce reciprocal routing/gamma=1 if parent-owned, but it does not by itself create or normalize a tracefree solar quadrupole metric amplitude.",
            "formula": "R_AB=0 does not imply P_surf,l2 E_metric L_parent^{-1} S_K2 = 1",
            "required_owner": "separate spin-2/STF source projection for the J2 channel",
            "status": "shortcut_rejected",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "AU3173_0_parent_action",
            "required_object": "S_parent[Phi;sigma]",
            "current_artifact": "04/07/10/11 provide contracts and toy/constraint lanes, not a full parent action with all fields",
            "can_extract_now": "false",
            "missing": "explicit parent action or field equations containing metric/coframe readout and K2 source lane",
            "effect": "cannot compute L_parent or S_K2 numerically/symbolically yet",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AU3173_1_operator_hessian",
            "required_object": "L_parent",
            "current_artifact": "reciprocal scalar toy operator exists for R_AB only",
            "can_extract_now": "false",
            "missing": "full linearized operator/Hessian for the public metric-producing sector",
            "effect": "cannot prove parent exterior operator match for J2 channel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AU3173_2_K2_source_vector",
            "required_object": "S_K2",
            "current_artifact": "3164 defines K2 := |W_2 M_Lambda| as a restricted scalar closure lane",
            "can_extract_now": "false",
            "missing": "variation of the parent equations with respect to the K2 lane/source deformation",
            "effect": "T_source remains missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AU3173_3_metric_readout",
            "required_object": "E_metric",
            "current_artifact": "3159 gives public weak-field metric convention after A_metric is supplied",
            "can_extract_now": "false",
            "missing": "map from parent fields/coframe variables into public metric perturbation before the GR convention is applied",
            "effect": "Pi_J2_metric remains missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AU3173_4_surface_projector",
            "required_object": "P_surf,l2",
            "current_artifact": "3172 gives public radial l=2 projection rule if A_surface exists",
            "can_extract_now": "conditional",
            "missing": "source radius/domain convention tying K2 lane to solar surface amplitude",
            "effect": "G_ext_l2_surface is conditional, not sufficient",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AU3173_5_no_GR_import",
            "required_object": "operator match without smuggling",
            "current_artifact": "04/09/10 explicitly forbid importing Einstein vacuum equations or Schwarzschild",
            "can_extract_now": "false",
            "missing": "MTS-owned derivation that its exterior operator reduces to the same public weak-field channel",
            "effect": "operator match remains a target, not a result",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def extractor_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "contract_id": "EX3173_0_define_sigma",
            "object": "sigma_K2",
            "definition": "sigma_K2 := K2*C_K2_unit, the first-order amplitude of the l=2 residual/source lane",
            "extraction_rule": "identify how sigma_K2 enters parent boundary/source variables before solving field equations",
            "required_source": "3164/3165 plus explicit parent source/boundary variation",
            "status": "defined_as_lane_not_yet_parent_source",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "EX3173_1_extract_L_parent",
            "object": "L_parent",
            "definition": "linearized parent operator/Hessian on physical quotient",
            "extraction_rule": "L_AB = delta^2 S_parent/(deltaPhi_A deltaPhi_B) or delta E_A/deltaPhi_B at Phi0",
            "required_source": "explicit MTS parent action/field equations",
            "status": "MISSING_PARENT_ACTION_HESSIAN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "EX3173_2_extract_S_K2",
            "object": "S_K2",
            "definition": "source vector induced in the parent equations by the K2 lane",
            "extraction_rule": "S_A = partial E_A/partial sigma_K2 at Phi0, sigma=0",
            "required_source": "parent coupling of W_2/M_Lambda boundary lane to fields",
            "status": "MISSING_K2_SOURCE_VARIATION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "EX3173_3_extract_E_metric",
            "object": "E_metric",
            "definition": "public metric readout map from parent/coframe variables",
            "extraction_rule": "derive delta g_public = E_metric[deltaPhi] in the same observer/coframe convention used for local tests",
            "required_source": "observer/coframe functor, matter coupling, and public metric convention",
            "status": "MISSING_PARENT_TO_PUBLIC_METRIC_READOUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "EX3173_4_compute_kernel",
            "object": "Upsilon_J2",
            "definition": "non-fitted transfer kernel from sigma_K2 to solar-surface public metric quadrupole amplitude",
            "extraction_rule": "Upsilon_J2 = - P_surf,l2 E_metric L_parent^{-1} S_K2",
            "required_source": "EX3173_1 through EX3173_3 plus source radius/domain normalization",
            "status": "EXACT_FORMULA_AVAILABLE_NOT_INSTANTIATED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def source_ready_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "row_id": "SRCROW3173_0_Pi_J2_metric",
            "quantity": "Pi_J2_metric",
            "symbolic_expression": "P_surf,l2 E_metric L_parent^{-1} S_K2 / T_source",
            "units": "dimensionless_if_sigma_and_A_surface_share_dimensionless_metric_amplitude_units",
            "source_path": "MISSING_PARENT_TO_PUBLIC_METRIC_READOUT_SOURCE",
            "equation_ref": "MISSING_E_metric_AND_L_parent_EQUATION",
            "status": "source_ready_placeholder_nonclaim",
            "claim_blockers": "MISSING_PARENT_ACTION_HESSIAN;MISSING_E_metric;MISSING_GAUGE_QUOTIENT;MISSING_SOURCE_RADIUS_NORMALIZATION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "SRCROW3173_1_T_source",
            "quantity": "T_source",
            "symbolic_expression": "source-domain normalization mapping Earth/local K2 lane into solar-source sigma_K2",
            "units": "dimensionless_or_source_normalization_units_to_be_declared",
            "source_path": "MISSING_SOLAR_SOURCE_TRANSFER_OR_UNIVERSALITY_THEOREM",
            "equation_ref": "MISSING_K2_SOURCE_DOMAIN_EQUATION",
            "status": "source_ready_placeholder_nonclaim",
            "claim_blockers": "MISSING_SOURCE_DOMAIN_TRANSFER;MISSING_SOLAR_BOUNDARY_LANE;MISSING_UNIVERSALITY_PROOF",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "SRCROW3173_2_parent_exterior_operator_match",
            "quantity": "operator_match_l2",
            "symbolic_expression": "P_ext,l2 E_metric L_parent^{-1} S_K2 obeys source-free l=2 public metric Laplace channel outside source",
            "units": "operator_statement",
            "source_path": "MISSING_PARENT_EXTERIOR_OPERATOR_DERIVATION",
            "equation_ref": "MISSING_LINEARIZED_PARENT_FIELD_EQUATION",
            "status": "source_ready_placeholder_nonclaim",
            "claim_blockers": "MISSING_L_PARENT;MISSING_NO_GR_IMPORT_PROOF;MISSING_BOUNDARY_CONDITIONS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3173_0_operator_formula_derived",
            "decision": "Pi_J2_metric/Upsilon_J2 is not a free closure; it has an exact parent-action extractor formula",
            "evidence": "OP3173_0 through OP3173_4",
            "effect": "future work must extract L_parent, S_K2, E_metric, and P_surf,l2 rather than guess a coupling",
            "next_action": "try to instantiate the parent Hessian/readout from an explicit action or write the parent action gap as the next hard block",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3173_1_current_artifacts_do_not_close",
            "decision": "current artifacts do not instantiate the extractor",
            "evidence": "AU3173_0 through AU3173_5",
            "effect": "J2/PPN/local-GR scoring remains blocked, but the missing data is now exact rather than vague",
            "next_action": "3174-Y5-R2FR-parent-Hessian-and-metric-readout-extraction-or-action-gap-lock-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3173_2_RAB_no_shortcut",
            "decision": "the reciprocal constraint route cannot be used as a shortcut to set the tracefree J2 metric coupling",
            "evidence": "OP3173_5",
            "effect": "R_AB/local-gamma and J2/STF projection must remain separate lanes until a parent coupling links them",
            "next_action": "avoid claiming Pi_J2_metric=1 from local reciprocity alone",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    operator: list[dict[str, object]],
    audits: list[dict[str, object]],
    extractors: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    exact_formula = any(row["object"] == "Upsilon_J2" and "L_parent" in row["formula"] for row in operator)
    shortcut_rejected = any(row["status"] == "shortcut_rejected" for row in operator)
    artifact_blocks = all(row["can_extract_now"] in {"false", "conditional"} for row in audits)
    extractor_contract = any(row["object"] == "Upsilon_J2" and "NOT_INSTANTIATED" in row["status"] for row in extractors)
    placeholders_refused = all(row["valid_for_claim"] == "false" and "MISSING" in row["claim_blockers"] for row in source_rows)
    next_target = any("3174" in row["next_action"] for row in decisions)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, operator, audits, extractors, source_rows, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3173_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3173_1_exact_extractor_formula_written",
            "status": "pass" if exact_formula else "fail",
            "detail": "Upsilon_J2 = - P_surf,l2 E_metric L_parent^-1 S_K2 recorded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3173_2_RAB_shortcut_rejected",
            "status": "pass" if shortcut_rejected else "fail",
            "detail": "reciprocal trace constraint cannot set tracefree J2 metric coupling",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3173_3_current_artifacts_do_not_instantiate",
            "status": "pass" if artifact_blocks else "fail",
            "detail": "all required extraction objects remain missing or conditional in current artifacts",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3173_4_extractor_contract_not_claim",
            "status": "pass" if extractor_contract else "fail",
            "detail": "formula exists but is not instantiated",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3173_5_source_ready_rows_refused",
            "status": "pass" if placeholders_refused else "fail",
            "detail": "Pi_J2_metric/T_source/operator rows are source-ready placeholders only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3173_6_next_target_selected",
            "status": "pass" if next_target else "fail",
            "detail": "3174 parent Hessian/readout extraction target selected",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3173_7_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3173 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    operator = operator_rows()
    audits = audit_rows()
    extractors = extractor_rows()
    source_rows = source_ready_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, operator, audits, extractors, source_rows, decisions)
    write_csv(INPUTS, inputs)
    write_csv(OPERATOR, operator)
    write_csv(AUDIT, audits)
    write_csv(EXTRACTOR, extractors)
    write_csv(SOURCE_ROWS, source_rows)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3173 validation failed: {failures}")


if __name__ == "__main__":
    main()

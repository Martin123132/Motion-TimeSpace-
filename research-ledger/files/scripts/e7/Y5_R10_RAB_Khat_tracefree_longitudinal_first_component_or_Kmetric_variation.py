from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1287"
TITLE = "1287-Y5-R10-RAB-Khat-tracefree-longitudinal-first-component-or-Kmetric-variation"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
TENSOR_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_TENSOR_SOURCE_AUDIT.csv"
KHAT_COMPONENT_PATH = OUT_DIR / f"{PACK_ID}_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv"
KMETRIC_COMPONENT_PATH = OUT_DIR / f"{PACK_ID}_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv"
DELTAK_STATUS_PATH = OUT_DIR / f"{PACK_ID}_DELTAK_COMPONENT_STATUS_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1287_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        TENSOR_AUDIT_PATH,
        KHAT_COMPONENT_PATH,
        KMETRIC_COMPONENT_PATH,
        DELTAK_STATUS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1287_0_1286_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1286_NEXT_TARGET.csv",
            "needle": "NEXT1286_0_1287",
            "role": "handoff into Khat tracefree-longitudinal or Kmetric variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_1_1286_gamma_row",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv",
            "needle": "RFR1286_0_Gamma_memory_scalar_projection",
            "role": "first Gamma_eff scalar component row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_2_793_balance",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv",
            "needle": "GBS793_1_tracefree_longitudinal_solver",
            "role": "tracefree longitudinal Khat route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_3_794_solver_def",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_794_TRACEFREE_LONGITUDINAL_SOLVER.csv",
            "needle": "TLS794_0_solver_definition",
            "role": "formal K_L tensor definition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_4_794_flat_cancel",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_794_TRACEFREE_LONGITUDINAL_SOLVER.csv",
            "needle": "TLS794_2_flat_cancellation",
            "role": "flat/local divergence cancellation condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_5_794_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_794_CURVATURE_AND_AMPLITUDE_GATES.csv",
            "needle": "CAG794_2_parent_origin",
            "role": "parent origin and amplitude gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_6_796_amplitude",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "needle": "KLB796_0_divergence_zero_not_metric_zero",
            "role": "no-free-lunch amplitude warning",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_7_776_volume",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "needle": "KGL776_0_volume_piece",
            "role": "formal Kmetric volume term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_8_776_match",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "needle": "KGL776_4_current_Khat_match",
            "role": "current Khat/Kgamma match missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_9_1193_ricci_flat",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
            "needle": "RES1193_3_Ricci_flat_limit",
            "role": "Ricci-flat scalar branch equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_10_1194_helmholtz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1194_EINSTEIN_SCALAR_BOUND_FORMS.csv",
            "needle": "ESB1194_0_Helmholtz_equation",
            "role": "Einstein/Ricci-flat scalar Helmholtz branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1287_11_active_gamma_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "needle": "K00_projection_fraction",
            "role": "missing K00 projection and response matrix inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    tensor_audit = [
        {
            "audit_id": "TSA1287_0_tracefree_tensor_definition",
            "candidate": "K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2) g^{mu nu} Box phi",
            "source_anchor": "TLS794_0_solver_definition",
            "status": "FORMAL_TENSOR_COMPONENT_FILLABLE_NONCLAIM",
            "what_it_gives": "trace-free Khat candidate in four dimensions",
            "what_it_does_not_give": "parent origin, boundary data, curvature-safe global solver, or local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TSA1287_1_flat_divergence",
            "candidate": "partial_mu K_L^{mu nu}=(3/2)partial^nu Box phi",
            "source_anchor": "TLS794_1_flat_divergence;TLS794_2_flat_cancellation",
            "status": "FORMAL_FLAT_PATCH_CANCELLATION",
            "what_it_gives": "if Box phi=(2/3)Gamma_eff then div K_L=grad Gamma_eff in flat/local commuting patch",
            "what_it_does_not_give": "curvature correction, boundary/no-flux, amplitude suppression, or source equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TSA1287_2_Einstein_scalar_branch",
            "candidate": "H_E phi=(2/3)(Gamma_eff+C)",
            "source_anchor": "RES1193_3_Ricci_flat_limit;ESB1194_0_Helmholtz_equation",
            "status": "CONDITIONAL_RICCI_FLAT_OR_EINSTEIN_BRANCH",
            "what_it_gives": "domain-limited scalar source equation for phi",
            "what_it_does_not_give": "generic matter-domain theorem or sourced Green/boundary constants",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TSA1287_3_Kmetric_volume_piece",
            "candidate": "delta sqrt(-g) gamma_R gives gamma_R g^{mu nu} volume contribution",
            "source_anchor": "KGL776_0_volume_piece",
            "status": "FORMAL_VOLUME_TERM_ONLY",
            "what_it_gives": "first Kmetric variation sub-piece",
            "what_it_does_not_give": "derivative, projector, boundary, G_AB, or Khat comparison terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TSA1287_4_DeltaK_comparison",
            "candidate": "Delta_K=K_hat-Kmetric[Gamma_eff]",
            "source_anchor": "KGL776_4_current_Khat_match",
            "status": "NOT_COMPUTABLE_CURRENT_KHAT_MATCH_MISSING",
            "what_it_gives": "exact comparison target",
            "what_it_does_not_give": "numerical/symbolic DeltaK component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    khat_component = [
        {
            "row_id": "KTC1287_0_flat_Ricci_scalar_KL00",
            "component_type": "Khat_tracefree_longitudinal_candidate",
            "symbol": "K_L^{00}",
            "formula": "K_L^{00}=2 nabla^0 nabla^0 phi - (1/2) g^{00} Box phi",
            "parent_tensor_formula": "K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2)g^{mu nu}Box phi",
            "source_equation": "Box phi=(2/3)(Gamma_eff+C) in Ricci-flat limit; H_E phi=(2/3)(Gamma_eff+C) in Einstein branch",
            "divergence_condition": "flat/local commuting patch gives partial_mu K_L^{mu nu}=partial^nu Gamma_eff",
            "units": "L^-2_if_phi_dimensionless_and_Gamma_eff_L^-2",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_794_TRACEFREE_LONGITUDINAL_SOLVER.csv",
            "source_anchor": "TLS794_0_solver_definition;TLS794_2_flat_cancellation",
            "supporting_source_path": "source-intake/mts_residuals/P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
            "supporting_source_anchor": "RES1193_3_Ricci_flat_limit",
            "domain_status": "MISSING_RICCI_FLAT_OR_EINSTEIN_DOMAIN_CLASSIFIER",
            "gauge_boundary_status": "MISSING_GREEN_INVERSE_AND_BOUNDARY_CONDITIONS",
            "parent_origin_status": "MISSING_PARENT_ORIGIN_FOR_PHI_OR_A_NU",
            "amplitude_status": "AMPLITUDE_NOT_SAFE_WITHOUT_KL_RESPONSE_BOUND",
            "DeltaK_status": "CANDIDATE_KHAT_COMPONENT_NOT_MATCHED_TO_CURRENT_MTS_KHAT",
            "current_status": "FORMAL_COMPONENT_ROW_FILLED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    kmetric_component = [
        {
            "row_id": "KMC1287_0_volume_metric_response",
            "component_type": "Kmetric_volume_subpiece",
            "symbol": "Kmetric_volume^{mu nu}",
            "formula": "delta sqrt(-g) Gamma_eff supplies the metric-proportional volume contribution Gamma_eff g^{mu nu} up to sign/convention",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "source_anchor": "KGL776_0_volume_piece",
            "units": "same_as_Gamma_eff_times_metric",
            "missing_terms": "MISSING_G_AB_METRIC_DEPENDENCE;MISSING_DERIVATIVE_TERMS;MISSING_BOUNDARY_REFERENCE_TERMS;MISSING_CURRENT_KHAT_MATCH",
            "current_status": "FORMAL_VOLUME_SUBPIECE_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    deltak_status = [
        {
            "status_id": "DKS1287_0_Khat_candidate_exists",
            "needed_for_DeltaK": "candidate Khat tensor component",
            "current_status": "FORMAL_KL00_COMPONENT_EXISTS_NONCLAIM",
            "why_not_enough": "it is a formal candidate, not proven to be existing current-MTS K_hat",
            "next_action": "derive parent origin or declare it a compensator branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "DKS1287_1_Kmetric_subpiece_exists",
            "needed_for_DeltaK": "Kmetric volume subpiece",
            "current_status": "FORMAL_VOLUME_SUBPIECE_EXISTS_NONCLAIM",
            "why_not_enough": "full metric response still needs derivative/projector/boundary terms",
            "next_action": "compute derivative/domain/boundary variation terms for Gamma_eff=L_cg^-2F(m)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "DKS1287_2_component_comparison",
            "needed_for_DeltaK": "Delta_K^{00}=K_hat^{00}-Kmetric^{00}",
            "current_status": "DELTAK_00_NOT_COMPUTABLE_YET",
            "why_not_enough": "current-MTS Khat match and full Kmetric^{00} are missing",
            "next_action": "fill Kmetric derivative/boundary terms or parent-origin K_L branch first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "DKS1287_3_local_claim",
            "needed_for_DeltaK": "q_loc/local-GR claim",
            "current_status": "BLOCKED_NONCLAIM_COMPONENTS_ONLY",
            "why_not_enough": "q_loc cancellation is not amplitude/PPN safety",
            "next_action": "build K_L amplitude/response row from KTC1287_0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1287_0_Khat_component",
            "claim": "first Khat tensor component row exists",
            "current_status": "PASS_NONCLAIM_FORMAL_KL00_ROW",
            "reason": "K_L^{00} row has source anchors but remains formal/conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1287_1_Kmetric_component",
            "claim": "first Kmetric variation component exists",
            "current_status": "PASS_NONCLAIM_VOLUME_SUBPIECE_ONLY",
            "reason": "volume term is sourced, but full Kmetric is not computed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1287_2_DeltaK_component",
            "claim": "Delta_K^{00} is computed",
            "current_status": "BLOCKED_DELTAK_00_NOT_COMPUTABLE",
            "reason": "current Khat match and full Kmetric terms are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1287_3_local_GR",
            "claim": "q_loc/local GR pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "formal divergence cancellation leaves amplitude, response, source, boundary, and parent-origin gates open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1287_0_tensor_progress",
            "decision": "First formal Khat tensor component row is now filled.",
            "because": "the trace-free longitudinal K_L^{00} row is source-backed to the 794 flat/Ricci scalar branch",
            "next_action": "do not call it current-MTS Khat until parent origin or source equation is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1287_1_Kmetric_progress",
            "decision": "First Kmetric volume subpiece is staged.",
            "because": "the volume response is formal-known, but derivative/projector/boundary terms are still missing",
            "next_action": "compute Kmetric derivative/domain/boundary pieces from Gamma_eff=L_cg^-2F(m)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1287_2_next_target",
            "decision": "Next target should quantify the K_L amplitude/response budget for the filled K_L^{00} component.",
            "because": "a divergence-cancelling tensor can still gravitate and fail PPN/Newton",
            "next_action": "build K_L^{00} amplitude/response row or compute missing Kmetric derivative term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1287_0_1288",
            "target_file": "1288-Y5-R10-RAB-KL00-amplitude-response-row-or-Kmetric-derivative-term.md",
            "target_script": "scripts/Y5_R10_RAB_KL00_amplitude_response_row_or_Kmetric_derivative_term.py",
            "task": "use the filled K_L^{00} row to stage a Newton/PPN amplitude-response bound, or compute the first derivative/domain/boundary term in Kmetric[Gamma_eff]",
            "success_condition": "K_L^{00} gets a source-backed nonclaim amplitude/response row, or Kmetric derivative/domain terms are explicitly blocked with required inputs",
            "do_not": "do not treat flat divergence cancellation as local-GR recovery and do not compute Delta_K without full Kmetric/current-Khat comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(TENSOR_AUDIT_PATH, tensor_audit)
    write_csv(KHAT_COMPONENT_PATH, khat_component)
    write_csv(KMETRIC_COMPONENT_PATH, kmetric_component)
    write_csv(DELTAK_STATUS_PATH, deltak_status)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1287_0_sources_exist",
            "all cited local sources exist",
            all(bool(row["exists"]) for row in source_register),
            f"{sum(bool(row['exists']) for row in source_register)}/{len(source_register)} sources exist",
        )
    )
    validations.append(
        validation_row(
            "VAL1287_1_needles_found",
            "all cited local needles found",
            all(bool(row["needle_found"]) for row in source_register),
            f"{sum(bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        )
    )
    validations.append(
        validation_row(
            "VAL1287_2_Khat_component_filled",
            "first Khat formal tensor component row is filled and nonclaim",
            khat_component[0]["current_status"] == "FORMAL_COMPONENT_ROW_FILLED_NONCLAIM"
            and is_false(khat_component[0]["claim_allowed"]),
            "KTC1287_0_flat_Ricci_scalar_KL00",
        )
    )
    validations.append(
        validation_row(
            "VAL1287_3_Kmetric_volume_filled",
            "first Kmetric volume subpiece row is filled and nonclaim",
            kmetric_component[0]["current_status"] == "FORMAL_VOLUME_SUBPIECE_ONLY_NONCLAIM"
            and is_false(kmetric_component[0]["valid_for_claim"]),
            "KMC1287_0_volume_metric_response",
        )
    )
    deltak_verdict = next(row for row in deltak_status if row["status_id"] == "DKS1287_2_component_comparison")
    validations.append(
        validation_row(
            "VAL1287_4_DeltaK_still_blocked",
            "Delta_K^{00} remains not computable",
            deltak_verdict["current_status"] == "DELTAK_00_NOT_COMPUTABLE_YET"
            and is_false(deltak_verdict["claim_allowed"]),
            "DKS1287_2_component_comparison=DELTAK_00_NOT_COMPUTABLE_YET",
        )
    )
    validations.append(
        validation_row(
            "VAL1287_5_claim_gates_blocked",
            "all claim gates remain nonclaim or blocked",
            all(is_false(row["claim_allowed"]) for row in claim_gates)
            and any("BLOCKED" in row["current_status"] for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        TENSOR_AUDIT_PATH,
        KHAT_COMPONENT_PATH,
        KMETRIC_COMPONENT_PATH,
        DELTAK_STATUS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1287_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    validations.append(
        validation_row(
            "VAL1287_7_next_target_1288",
            "next target routes to KL00 amplitude response or Kmetric derivative term",
            next_target[0]["next_id"] == "NEXT1287_0_1288" and "K_L" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1287_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1287_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
                for rows in [source_register, tensor_audit, khat_component, kmetric_component, deltak_status, claim_gates, decision, next_target]
                for row in rows
            ),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1287_10_overall",
            "overall 1287 validation",
            overall_pass,
            "1287 fills a formal nonclaim K_L^{00} tensor component and Kmetric volume subpiece, keeps Delta_K^{00} blocked, and routes to amplitude/response or Kmetric derivative next",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1287 Y5 R10 RAB Khat tracefree-longitudinal first component or Kmetric variation

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1287 fills a first formal **nonclaim** `K_hat` tensor component row: the trace-free longitudinal scalar-branch component `K_L^{{00}}`. It also stages the first `Kmetric` volume subpiece. `Delta_K^{{00}}` is still not computable because the full current-MTS `K_hat` match and full `Kmetric` variation are missing.

**Main progress:** the tensor side is no longer empty. The flat/Ricci scalar branch gives `K_L^{{mu nu}}=2 nabla^mu nabla^nu phi - (1/2)g^{{mu nu}}Box phi`, with `Box phi=(2/3)Gamma_eff` in the Ricci-flat limit. That is an honest first component row, but not local GR: amplitude, boundary, curvature, parent-origin, and PPN response gates remain open.

**Next derivation target:** quantify the `K_L^{{00}}` amplitude/response row, or compute the first derivative/domain/boundary term in `Kmetric[Gamma_eff]`.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Tensor Source Audit

{markdown_table(tensor_audit, ["audit_id", "candidate", "source_anchor", "status", "what_it_gives", "what_it_does_not_give", "valid_for_claim", "claim_allowed"])}

## First Khat Component Row

{markdown_table(khat_component, ["row_id", "component_type", "symbol", "formula", "parent_tensor_formula", "source_equation", "divergence_condition", "units", "source_path", "source_anchor", "supporting_source_path", "supporting_source_anchor", "domain_status", "gauge_boundary_status", "parent_origin_status", "amplitude_status", "DeltaK_status", "current_status", "valid_for_claim", "claim_allowed"])}

## First Kmetric Volume Row

{markdown_table(kmetric_component, ["row_id", "component_type", "symbol", "formula", "source_path", "source_anchor", "units", "missing_terms", "current_status", "valid_for_claim", "claim_allowed"])}

## DeltaK Component Status

{markdown_table(deltak_status, ["status_id", "needed_for_DeltaK", "current_status", "why_not_enough", "next_action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

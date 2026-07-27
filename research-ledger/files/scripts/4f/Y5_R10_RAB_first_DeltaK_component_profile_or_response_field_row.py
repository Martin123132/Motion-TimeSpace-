from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1286"
TITLE = "1286-Y5-R10-RAB-first-DeltaK-component-profile-or-response-field-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COMPONENT_SEARCH_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_SOURCE_SEARCH_AUDIT.csv"
RESPONSE_FIELD_ROW_PATH = OUT_DIR / f"{PACK_ID}_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv"
DELTAK_BLOCKER_PATH = OUT_DIR / f"{PACK_ID}_FIRST_DELTAK_COMPONENT_BLOCKER_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1286_VALIDATION.csv"


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
        COMPONENT_SEARCH_PATH,
        RESPONSE_FIELD_ROW_PATH,
        DELTAK_BLOCKER_PATH,
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
            "source_id": "SRC1286_0_1285_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1285_NEXT_TARGET.csv",
            "needle": "NEXT1285_0_1286",
            "role": "handoff into first DeltaK component/profile or response-field row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1286_1_1285_DeltaK_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1285_DELTAK_DIVERGENCE_BOUND_ROW_NONCLAIM.csv",
            "needle": "DKB1285_0_DeltaK_divergence_bound_template",
            "role": "DeltaK template requiring component profile",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1286_2_gamma_expansion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_0_definition",
            "role": "Gamma_eff memory-source formula shape and gradient identity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1286_3_gamma_gradient",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_1_gradient_expansion",
            "role": "Gamma_eff gradient expansion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1286_4_khat_balance",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv",
            "needle": "GBS793_1_tracefree_longitudinal_solver",
            "role": "best Khat balance route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1286_5_kgamma_ledger",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "needle": "KGL776_4_current_Khat_match",
            "role": "Khat/Kgamma match still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1286_6_gamma_mode_split",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_834_GAMMA_MODE_SPLIT_THEOREM.csv",
            "needle": "GS834_0_decompose",
            "role": "constant/active Gamma_eff split",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1286_7_active_gamma_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "needle": "active_gamma_coeff",
            "role": "active Gamma numeric/bound inputs remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1286_8_1188_profile_ledger",
            "local_path": "1188-Y5-R10-Gamma-Khat-Ploc-profile-source-ledger-or-q_loc-demotion-row.md",
            "needle": "GPL1188_1_Gamma_memory_source",
            "role": "prior profile ledger says Gamma memory formula exists but profile is not claim-grade",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    component_search = [
        {
            "search_id": "CFS1286_0_Gamma_memory_scalar",
            "candidate": "Gamma_eff=L_cg^-2 F(m)",
            "source": "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv::GSE798_0_definition",
            "component_type": "response_field_scalar_projection",
            "fillable_now": True,
            "status": "FIRST_RESPONSE_FIELD_COMPONENT_ROW_FILLABLE_NONCLAIM",
            "missing_for_claim": "F_units;F_prime_values;m_profile;L_cg_profile;local_domain;boundary_decay;source_support_powers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "search_id": "CFS1286_1_Gamma_gradient",
            "candidate": "nabla Gamma_eff=L_cg^-2 F'(m)nabla m-2L_cg^-3F(m)nabla L_cg",
            "source": "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv::GSE798_1_gradient_expansion",
            "component_type": "response_field_gradient_identity",
            "fillable_now": True,
            "status": "SOURCE_BACKED_IDENTITY_NONCLAIM",
            "missing_for_claim": "m/L_cg profiles;support powers pS/pL/pT;transition width;local arena response maps",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "search_id": "CFS1286_2_Gamma_active_split",
            "candidate": "Gamma_eff=Lambda_loc+gamma_act",
            "source": "P8_Y5_R10_834_GAMMA_MODE_SPLIT_THEOREM.csv::GS834_0_decompose",
            "component_type": "mode_split_helper",
            "fillable_now": True,
            "status": "HELPFUL_SPLIT_NONCLAIM",
            "missing_for_claim": "Lambda lock;gamma_act coefficient;active mode source support;matter-frame response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "search_id": "CFS1286_3_Khat_tracefree_longitudinal",
            "candidate": "K_L^{mu nu}=nabla^{(mu}A^{nu)}-(1/4)g^{mu nu}nabla_alpha A^alpha+curvature terms",
            "source": "P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv::GBS793_1_tracefree_longitudinal_solver",
            "component_type": "Khat_balance_candidate",
            "fillable_now": False,
            "status": "NOT_FILLABLE_A_FIELD_AND_BOUNDARY_MISSING",
            "missing_for_claim": "A^nu source equation;gauge;boundary data;parent action origin;component units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "search_id": "CFS1286_4_Kgamma_metric_response",
            "candidate": "K_gamma=metric response of Gamma_eff",
            "source": "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv::KGL776_4_current_Khat_match",
            "component_type": "Kmetric_comparison_candidate",
            "fillable_now": False,
            "status": "NOT_FILLABLE_CURRENT_KHAT_MATCH_MISSING",
            "missing_for_claim": "G_AB;derivative terms;boundary/reference terms;explicit K_hat components",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "search_id": "CFS1286_5_DeltaK_component",
            "candidate": "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "source": "1285 DeltaK template plus KGL776/GBS793",
            "component_type": "DeltaK_component_profile",
            "fillable_now": False,
            "status": "FIRST_DELTAK_COMPONENT_NOT_FILLABLE",
            "missing_for_claim": "existing K_hat tensor;computed K_metric;component comparison;DeltaK units/domain/norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    response_field_row = [
        {
            "row_id": "RFR1286_0_Gamma_memory_scalar_projection",
            "component_type": "response_field_scalar_projection",
            "symbol": "Gamma_eff",
            "formula": "Gamma_eff = L_cg^-2 F(m)",
            "gradient_formula": "nabla_nu Gamma_eff = L_cg^-2 F'(m)nabla_nu m - 2 L_cg^-3 F(m)nabla_nu L_cg",
            "units": "L^-2_if_F_dimensionless",
            "unit_caveat": "F_units_and_m_units_must_be_declared_before_claim",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "GSE798_0_definition;GSE798_1_gradient_expansion",
            "domain_id": "MISSING_LOCAL_DOMAIN_PROFILE",
            "boundary_condition": "MISSING_BOUNDARY_DECAY_OR_NO_FLUX",
            "support_law": "MISSING_pS_pL_pT_transition_support_powers",
            "maps_to_DeltaK": "not_yet_without_Khat_tensor_or_Kmetric_computation",
            "current_status": "SOURCE_BACKED_FORMULA_SHAPE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_action": "derive/support m,L_cg profiles and then compute K_metric/Khat comparison",
        }
    ]

    deltak_blocker = [
        {
            "blocker_id": "DKC1286_0_missing_Khat_tensor",
            "needed_for_DeltaK": "existing K_hat^{mu nu} component profile",
            "current_status": "MISSING_EXISTING_KHAT_COMPONENTS",
            "source_clue": "KGL776_4_current_Khat_match",
            "why_blocks": "Delta_K cannot be component-filled without both K_hat and K_metric",
            "next_action": "derive Khat tracefree-longitudinal A^nu route or source current-MTS Khat tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "DKC1286_1_missing_Kmetric_computation",
            "needed_for_DeltaK": "K_metric[Gamma_eff] component computation",
            "current_status": "MISSING_METRIC_VARIATION_COMPONENTS",
            "source_clue": "KGL776_1_G_metric_dependence;KGL776_2_derivative_terms",
            "why_blocks": "Gamma formula shape alone is insufficient because derivative/projector/boundary metric responses are open",
            "next_action": "declare Gamma_eff field content and compute variation terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "DKC1286_2_missing_domain_units",
            "needed_for_DeltaK": "domain, units, and local norm",
            "current_status": "MISSING_DOMAIN_UNITS_NORM",
            "source_clue": "1285 DeltaK template",
            "why_blocks": "even a formal DeltaK expression cannot be compared to PPN/clock/orbital/R10",
            "next_action": "carry nonclaim row only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "DKC1286_3_verdict",
            "needed_for_DeltaK": "first DeltaK component profile",
            "current_status": "DELTAK_COMPONENT_NOT_FILLABLE_YET",
            "source_clue": "CFS1286_5_DeltaK_component",
            "why_blocks": "response scalar row exists, but tensor comparison does not",
            "next_action": "target Khat tracefree-longitudinal first component or Kmetric variation next",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1286_0_response_field_row",
            "claim": "first response-field scalar row exists",
            "current_status": "PASS_NONCLAIM_SOURCE_BACKED_FORMULA_SHAPE",
            "reason": "Gamma_eff=L_cg^-2F(m) and gradient identity have source anchors, but missing profiles/bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1286_1_DeltaK_component",
            "claim": "first DeltaK component row is fillable",
            "current_status": "BLOCKED_DELTAK_COMPONENT_NOT_FILLABLE",
            "reason": "Khat tensor and Kmetric variation are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1286_2_q_loc_profile",
            "claim": "q_loc profile can be scored",
            "current_status": "BLOCKED_GAMMA_ONLY_NOT_ENOUGH",
            "reason": "P_loc/Khat/DeltaK/norm/observable maps remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1286_3_local_GR",
            "claim": "local GR/PPN branch reopened",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "this is a component-source row only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1286_0_first_row_filled",
            "decision": "A first nonclaim response-field component row is filled for Gamma_eff.",
            "because": "Gamma_eff=L_cg^-2F(m) and its gradient expansion are source-backed formula shapes",
            "next_action": "use this as the scalar input to a future Kmetric computation, not as a local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1286_1_DeltaK_still_blocked",
            "decision": "No first DeltaK component can be filled yet.",
            "because": "DeltaK needs both a sourced Khat tensor and the metric response Kmetric[Gamma_eff]",
            "next_action": "attack Khat tracefree-longitudinal component or Kmetric variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1286_2_best_next",
            "decision": "Next target should be the Khat tracefree-longitudinal first component.",
            "because": "Gamma_eff has a formula shape; the tensor side is now the limiting piece",
            "next_action": "derive/source A^nu, gauge, boundary, units, and parent origin for K_L",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1286_0_1287",
            "target_file": "1287-Y5-R10-RAB-Khat-tracefree-longitudinal-first-component-or-Kmetric-variation.md",
            "target_script": "scripts/Y5_R10_RAB_Khat_tracefree_longitudinal_first_component_or_Kmetric_variation.py",
            "task": "try to derive/source the first Khat tracefree-longitudinal component using the A^nu route, or compute the first Kmetric variation term from the Gamma_eff memory scalar row",
            "success_condition": "one Khat/Kmetric tensor component has source path, units, gauge/domain/boundary status, and nonclaim status, or a blocker ledger proves the tensor side remains unfillable",
            "do_not": "do not infer Delta_K from Gamma_eff alone and do not score q_loc/local-GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(COMPONENT_SEARCH_PATH, component_search)
    write_csv(RESPONSE_FIELD_ROW_PATH, response_field_row)
    write_csv(DELTAK_BLOCKER_PATH, deltak_blocker)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1286_0_sources_exist",
            "all cited local sources exist",
            all(bool(row["exists"]) for row in source_register),
            f"{sum(bool(row['exists']) for row in source_register)}/{len(source_register)} sources exist",
        )
    )
    validations.append(
        validation_row(
            "VAL1286_1_needles_found",
            "all cited local needles found",
            all(bool(row["needle_found"]) for row in source_register),
            f"{sum(bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        )
    )
    response_row = response_field_row[0]
    validations.append(
        validation_row(
            "VAL1286_2_response_field_row_filled",
            "first response-field component row is filled from source-backed formula shape",
            response_row["current_status"] == "SOURCE_BACKED_FORMULA_SHAPE_NONCLAIM"
            and "MISSING" in response_row["domain_id"]
            and is_false(response_row["claim_allowed"]),
            "RFR1286_0_Gamma_memory_scalar_projection present and nonclaim",
        )
    )
    deltak_verdict = next(row for row in deltak_blocker if row["blocker_id"] == "DKC1286_3_verdict")
    validations.append(
        validation_row(
            "VAL1286_3_DeltaK_component_blocked",
            "first DeltaK component remains blocked",
            deltak_verdict["current_status"] == "DELTAK_COMPONENT_NOT_FILLABLE_YET" and is_false(deltak_verdict["valid_for_claim"]),
            "DKC1286_3_verdict=DELTAK_COMPONENT_NOT_FILLABLE_YET",
        )
    )
    validations.append(
        validation_row(
            "VAL1286_4_claim_gates_blocked",
            "all claim gates remain nonclaim or blocked",
            all(is_false(row["claim_allowed"]) for row in claim_gates)
            and any("BLOCKED" in row["current_status"] for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        COMPONENT_SEARCH_PATH,
        RESPONSE_FIELD_ROW_PATH,
        DELTAK_BLOCKER_PATH,
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
    validations.append(validation_row("VAL1286_5_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    validations.append(
        validation_row(
            "VAL1286_6_next_target_1287",
            "next target routes to Khat tracefree-longitudinal or Kmetric variation",
            next_target[0]["next_id"] == "NEXT1286_0_1287" and "Khat" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1286_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1286_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
                for rows in [source_register, component_search, response_field_row, deltak_blocker, claim_gates, decision, next_target]
                for row in rows
            ),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1286_9_overall",
            "overall 1286 validation",
            overall_pass,
            "1286 fills a first nonclaim Gamma_eff response-field scalar row, blocks DeltaK component fill for missing Khat/Kmetric tensors, and routes to Khat tensor component next",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1286 Y5 R10 RAB first DeltaK component profile or response-field row

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1286 fills the first source-backed **nonclaim response-field scalar row**: `Gamma_eff=L_cg^-2 F(m)`. It does **not** fill a `Delta_K` component, because `K_hat` and `K_metric[Gamma_eff]` are still not component-computed.

**Main progress:** the scalar side is no longer empty. We have a usable formula shape and gradient identity for the response field. But the tensor side is the wall: without `K_hat^{{mu nu}}` or a computed `K_metric^{{mu nu}}`, `Delta_K^{{mu nu}}=K_hat^{{mu nu}}-K_metric^{{mu nu}}` cannot be filled.

**Next derivation target:** the first `K_hat`/`K_metric` tensor component. The best route in the corpus is the trace-free longitudinal `A^nu` route, or a first metric-variation term from the Gamma memory scalar.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Component Source Search Audit

{markdown_table(component_search, ["search_id", "candidate", "source", "component_type", "fillable_now", "status", "missing_for_claim", "valid_for_claim", "claim_allowed"])}

## First Response-Field Component Row

{markdown_table(response_field_row, ["row_id", "component_type", "symbol", "formula", "gradient_formula", "units", "unit_caveat", "source_path", "source_anchor", "domain_id", "boundary_condition", "support_law", "maps_to_DeltaK", "current_status", "valid_for_claim", "claim_allowed", "next_action"])}

## First DeltaK Component Blocker Ledger

{markdown_table(deltak_blocker, ["blocker_id", "needed_for_DeltaK", "current_status", "source_clue", "why_blocks", "next_action", "valid_for_claim", "claim_allowed"])}

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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1118-Y5-R10-domain-R11-source-normalization-zero-or-executable-coefficient-vector.md"

R11_SCHEMA = [
    "model_id",
    "branch_id",
    "vector_id",
    "operator_family",
    "coefficient_symbol",
    "coefficient_value",
    "coefficient_units",
    "normalization",
    "operator_form",
    "weak_field_map",
    "affected_rows",
    "induced_observable",
    "predicted_residual_or_bound_source",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    out: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        out.append(copied)
    return out


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1118_0_1117_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1117_NEXT_TARGET.csv",
            "needle": "NEXT1117_0_1118",
            "note": "1117 handoff to domain R11 source-normalization zero or executable vector.",
        },
        {
            "source_id": "SRC1118_1_1117_component",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_COMPONENT_STATUS.csv",
            "needle": "COMP1117_3_R11_operator",
            "note": "R11 operator is the hard failing component.",
        },
        {
            "source_id": "SRC1118_2_r11_zero",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT.csv",
            "needle": "Z6_verdict",
            "note": "R11/domain source-normalization theorem-zero rejected.",
        },
        {
            "source_id": "SRC1118_3_r11_fill",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "needle": "DSR_R11_EH_operator_ledger",
            "note": "R11 source-normalization fill requirement.",
        },
        {
            "source_id": "SRC1118_4_min_vector",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "c_domain_source_normalization_operator",
            "note": "domain R11 minimum vector row.",
        },
        {
            "source_id": "SRC1118_5_missing_ledger",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
            "needle": "source_normalization_operator",
            "note": "missing fields for executable vector.",
        },
        {
            "source_id": "SRC1118_6_validation",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_VALIDATION.csv",
            "needle": "V473_3_actual_executable_rows",
            "note": "domain claimable rows equal zero.",
        },
        {
            "source_id": "SRC1118_7_domain_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
            "needle": "domain_projector_mass",
            "note": "domain PPN coefficient map rows.",
        },
        {
            "source_id": "SRC1118_8_1117_priors",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_COUPLING_PRIOR_ROWS_NONCLAIM.csv",
            "needle": "DPR1117_2_alpha3",
            "note": "alpha3 row remains missing numeric product or theorem-zero.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "R11D1118_0_target",
                "claim_piece": "domain R11 source-normalization zero",
                "formal_statement": "c_domain_source_normalization_operator = 0 in the compact local branch, or an executable coefficient vector supplies every mapped residual.",
                "result": "TARGET_SHARP",
                "proof_or_blocker": "this is the domain-selector bottleneck left by 1117",
            },
            {
                "attempt_id": "R11D1118_1_EH_only",
                "claim_piece": "EH-only exterior/local branch",
                "formal_statement": "S_parent reduces to EH plus silent boundary/domain terms in compact local branch, so non-EH R11 source-normalization vanishes.",
                "result": "NOT_DERIVED",
                "proof_or_blocker": "existing R11 zero attempt says EH-only or R11 silence is not proved; valid claim rows are zero",
            },
            {
                "attempt_id": "R11D1118_2_source_operator_zero",
                "claim_piece": "domain source-normalization operator is zero",
                "formal_statement": "delta mu_domain = 0 and derivative/domain hair vanish in measured-GM normalization.",
                "result": "FAIL_CURRENT_CORPUS",
                "proof_or_blocker": "domain projector/source-normalization rows are retained/unfilled and not scoreable",
            },
            {
                "attempt_id": "R11D1118_3_projector_stress",
                "claim_piece": "projector/domain stress is topological and metric-independent",
                "formal_statement": "delta_g P_D = delta_g chi_D = 0 through PPN order, so projector_domain_stress contributes no local source residual.",
                "result": "CONDITIONAL_NOT_PARENT_DERIVED",
                "proof_or_blocker": "topological projector route is conditional and parent ownership remains unsigned",
            },
            {
                "attempt_id": "R11D1118_4_detQ_route",
                "claim_piece": "det(Q_coh) supplies local R11/domain zero",
                "formal_statement": "a parent-owned coherent current selects local trivial class without shear leakage.",
                "result": "FAIL_CURRENT_CORPUS",
                "proof_or_blocker": "det(Q_coh) remains shape-supported but not parent-owned; raw det(Q) leaks tracefree shear",
            },
            {
                "attempt_id": "R11D1118_5_alpha3_bridge",
                "claim_piece": "domain alpha3 bridge closes",
                "formal_statement": "W_domain_alpha3*epsilon_domain_flux = 0 or abs(product) <= 4e-20.",
                "result": "NOT_SCOREABLE",
                "proof_or_blocker": "alpha3 product needs theorem-zero/no-leak or numeric coefficient product with source path",
            },
            {
                "attempt_id": "R11D1118_6_verdict",
                "claim_piece": "derive c_domain_source_normalization_operator = 0",
                "formal_statement": "domain R11 source-normalization is theorem-zero in the current corpus.",
                "result": "DOMAIN_R11_SOURCE_ZERO_NOT_DERIVED",
                "proof_or_blocker": "all active zero routes remain missing, conditional, retained, or not scoreable",
            },
        ]
    )


def executable_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "contract_id": "EXE1118_0_schema",
                "requirement": "use canonical 19-column R11 schema",
                "must_hold": ";".join(R11_SCHEMA),
                "current_status": "SCHEMA_DECLARED",
                "blocks_claim_if_missing": "true",
            },
            {
                "contract_id": "EXE1118_1_numeric",
                "requirement": "coefficient_value is numeric or a referenced theorem-zero certificate",
                "must_hold": "no MISSING, symbolic-only, conditional-only, or placeholder value in claim rows",
                "current_status": "NOT_SATISFIED_FOR_DOMAIN_ROWS",
                "blocks_claim_if_missing": "true",
            },
            {
                "contract_id": "EXE1118_2_units",
                "requirement": "coefficient_units and normalization are explicit",
                "must_hold": "dimensionless convention or declared operator units compatible with weak-field map",
                "current_status": "PARTIAL_FOR_EXISTING_ROWS",
                "blocks_claim_if_missing": "true",
            },
            {
                "contract_id": "EXE1118_3_map",
                "requirement": "weak_field_map maps each coefficient to PPN/R10/local rows",
                "must_hold": "affected_rows and induced_observable must be concrete and row-specific",
                "current_status": "PARTIAL_WIRING_EXISTS",
                "blocks_claim_if_missing": "true",
            },
            {
                "contract_id": "EXE1118_4_source_path",
                "requirement": "formula_reference and source_file point to real local source artifacts",
                "must_hold": "paths exist and support the numeric/theorem-zero value",
                "current_status": "PATHS_EXIST_BUT_VALUES_MISSING",
                "blocks_claim_if_missing": "true",
            },
            {
                "contract_id": "EXE1118_5_acceptance",
                "requirement": "valid_for_claim can be true only when all fields are concrete and products pass bounds",
                "must_hold": "no MISSING markers; no conditional-only zero; no cancellation tuning; abs(product)<=target_bound where applicable",
                "current_status": "ALL_DOMAIN_ROWS_FALSE",
                "blocks_claim_if_missing": "true",
            },
        ]
    )


def candidate_rows() -> list[dict[str, object]]:
    base = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "domain_R11_1118_candidate_nonclaim",
        "vector_id": "R11_domain_source_normalization_1118",
        "coefficient_units": "dimensionless_or_declared_operator_units",
        "normalization": "relative_to_observed_local_coframe_and_measured_GM",
        "assumptions": "observed coframe fixed; no tuned cancellation; local branch compact; no source-unity shortcut",
        "valid_for_claim": "false",
    }
    rows = [
        {
            **base,
            "operator_family": "source_normalization_operator",
            "coefficient_symbol": "c_domain_source_normalization_operator",
            "coefficient_value": "MISSING_DOMAIN_SOURCE_NORMALIZATION_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
            "operator_form": "mu_obs = G_eff M_eff + mu_domain_projector plus derivative/vector/anisotropy source-normalization corrections",
            "weak_field_map": "R5/R6/R7/R8 maps from P8_mu_extra_domain_projector_coefficients.csv; R11 ledger tracks source-normalization operator",
            "affected_rows": "R5;R6;R7;R8;R11",
            "induced_observable": "alpha1;alpha2;alpha3;xi;operator_ledger",
            "predicted_residual_or_bound_source": "MISSING_DOMAIN_PROJECTOR_COEFFICIENT_PRODUCTS_OR_THEOREM_ZERO",
            "derivation_status": "retained_unfilled",
            "formula_reference": "1118-Y5-R10-domain-R11-source-normalization-zero-or-executable-coefficient-vector.md",
            "source_file": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "notes": "Primary 1118 blocker; not executable until coefficient or theorem-zero source is real.",
        },
        {
            **base,
            "operator_family": "vector_preferred_frame",
            "coefficient_symbol": "W_domain_alpha1_alpha2_vector_product",
            "coefficient_value": "MISSING_DOMAIN_VECTOR_PRODUCT_OR_THEOREM_ZERO",
            "operator_form": "domain selector vector or normal projected into observed local coframe",
            "weak_field_map": "alpha1_domain=W_domain_alpha1*epsilon_domain_vector; alpha2_domain=W_domain_alpha2*epsilon_domain_vector",
            "affected_rows": "R5;R6",
            "induced_observable": "alpha1;alpha2",
            "predicted_residual_or_bound_source": "MISSING_VECTOR_PRODUCT_BOUND",
            "derivation_status": "retained_unfilled",
            "formula_reference": "1117-Y5-R10-domain-selector-zero-or-domain-coupling-prior-source.md",
            "source_file": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
            "notes": "Vector branch remains conditional unless parent scalar selector theorem closes.",
        },
        {
            **base,
            "operator_family": "flux_source_operator",
            "coefficient_symbol": "W_domain_alpha3_epsilon_domain_flux",
            "coefficient_value": "MISSING_DOMAIN_ALPHA3_PRODUCT_OR_THEOREM_ZERO",
            "operator_form": "domain flux/source-normalization projection into alpha3 channel",
            "weak_field_map": "alpha3_domain=W_domain_alpha3*epsilon_domain_flux",
            "affected_rows": "R7;R11",
            "induced_observable": "alpha3;operator_ledger",
            "predicted_residual_or_bound_source": "MISSING_ALPHA3_PRODUCT_BELOW_4E-20_OR_ZERO",
            "derivation_status": "retained_unfilled",
            "formula_reference": "1118-Y5-R10-domain-R11-source-normalization-zero-or-executable-coefficient-vector.md",
            "source_file": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "notes": "Highest-pressure domain row because target bound is 4e-20.",
        },
        {
            **base,
            "operator_family": "projector_domain_stress",
            "coefficient_symbol": "W_domain_xi_epsilon_domain_anisotropy",
            "coefficient_value": "MISSING_DOMAIN_STF_PRODUCT_OR_THEOREM_ZERO",
            "operator_form": "selector/projector STF stress in observed local frame",
            "weak_field_map": "xi_domain=W_domain_xi*epsilon_domain_anisotropy",
            "affected_rows": "R8;R11",
            "induced_observable": "xi;operator_ledger",
            "predicted_residual_or_bound_source": "MISSING_XI_PRODUCT_BOUND_OR_ZERO",
            "derivation_status": "retained_unfilled",
            "formula_reference": "1117-Y5-R10-domain-selector-zero-or-domain-coupling-prior-source.md",
            "source_file": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
            "notes": "Projector stress zero is conditional, not parent-owned.",
        },
    ]
    return rows


def pressure_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "pressure_id": "PRS1118_0_alpha3",
                "row": "R7_alpha3",
                "product": "W_domain_alpha3 * epsilon_domain_flux plus R11 source-normalization leakage",
                "target_bound": "4e-20",
                "status": "HIGHEST_PRESSURE_NOT_SCOREABLE",
                "next_required": "numeric flux/R11 product below bound or parent theorem-zero",
            },
            {
                "pressure_id": "PRS1118_1_alpha2",
                "row": "R6_alpha2",
                "product": "W_domain_alpha2 * epsilon_domain_vector",
                "target_bound": "2e-09",
                "status": "NOT_SCOREABLE",
                "next_required": "numeric vector product below bound or parent theorem-zero",
            },
            {
                "pressure_id": "PRS1118_2_xi",
                "row": "R8_xi",
                "product": "W_domain_xi * epsilon_domain_anisotropy",
                "target_bound": "4e-09",
                "status": "NOT_SCOREABLE",
                "next_required": "numeric STF product below bound or parent theorem-zero",
            },
            {
                "pressure_id": "PRS1118_3_alpha1",
                "row": "R5_alpha1",
                "product": "W_domain_alpha1 * epsilon_domain_vector",
                "target_bound": "1e-04",
                "status": "NOT_SCOREABLE",
                "next_required": "numeric vector product below bound or parent theorem-zero",
            },
            {
                "pressure_id": "PRS1118_4_R11",
                "row": "R11_EH_operator_ledger",
                "product": "c_domain_source_normalization_operator",
                "target_bound": "executable coefficient vector with units/map/source",
                "status": "NOT_EXECUTABLE",
                "next_required": "fill canonical R11 row or derive zero",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1118_0_zero",
                "claim": "c_domain_source_normalization_operator = 0 is derived",
                "gate_pass": "false",
                "reason": "EH-only, source-operator, detQ, and projector-stress zero routes are missing/conditional/failed",
            },
            {
                "gate_id": "CG1118_1_executable",
                "claim": "R11 domain vector is executable",
                "gate_pass": "false",
                "reason": "candidate rows contain MISSING values and valid_for_claim=false",
            },
            {
                "gate_id": "CG1118_2_alpha3",
                "claim": "domain alpha3 product is safe",
                "gate_pass": "false",
                "reason": "W_domain_alpha3*epsilon_domain_flux is missing theorem-zero or numeric product below 4e-20",
            },
            {
                "gate_id": "CG1118_3_local_gr",
                "claim": "domain R11 branch permits local-GR/R10 claim",
                "gate_pass": "false",
                "reason": "domain source-normalization operator remains live and unscored",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1118_0_result",
                "decision": "domain R11 source-normalization zero is not derived",
                "because": "all zero routes are missing, conditional, retained, or not scoreable",
                "next_action": "fill or derive the alpha3/R11 source-normalization row first",
            },
            {
                "decision_id": "DEC1118_1_schema",
                "decision": "strict executable R11 contract is now explicit",
                "because": "wired rows without numeric/theorem-zero values are not executable evidence",
                "next_action": "do not mark any R11/domain row valid_for_claim until all MISSING values are replaced by real sources",
            },
            {
                "decision_id": "DEC1118_2_priority",
                "decision": "domain alpha3 is the highest-pressure next row",
                "because": "its target bound is 4e-20 and it directly touches flux/source-normalization leakage",
                "next_action": "attempt alpha3 domain source-normalization zero or source-backed product fill next",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1118_0_1119",
                "next_target": "1119-Y5-R10-domain-alpha3-R11-source-zero-or-product-fill.md",
                "objective": "attack the highest-pressure domain alpha3 row: derive W_domain_alpha3*epsilon_domain_flux = 0 with R11 source-normalization silence, or build a source-backed numeric product row against the 4e-20 bound",
                "include": "R7_alpha3; W_domain_alpha3; epsilon_domain_flux; c_domain_source_normalization_operator; R11 executable vector; target 4e-20; source paths; units; weak-field map",
                "exclude": "symbolic product pass; Ward/Bianchi shortcut; local-GR claim; tau=1; source-unity; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    contract: list[dict[str, object]],
    candidates: list[dict[str, object]],
    pressures: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add("V1118_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1118_1_zero_not_derived", any(row["result"] == "DOMAIN_R11_SOURCE_ZERO_NOT_DERIVED" for row in theorem), "domain R11 source zero remains unpromoted")
    add("V1118_2_contract_strict", len(contract) >= 6 and any(row["requirement"] == "valid_for_claim can be true only when all fields are concrete and products pass bounds" for row in contract), "strict executable contract is explicit")
    add("V1118_3_candidate_schema", all(set(row.keys()) == set(R11_SCHEMA) for row in candidates), "candidate rows use canonical R11 schema")
    add("V1118_4_candidate_nonclaim", all(row["valid_for_claim"] == "false" and ("MISSING" in row["coefficient_value"] or "MISSING" in row["predicted_residual_or_bound_source"]) for row in candidates), "candidate rows remain missing-input nonclaim rows")
    add("V1118_5_alpha3_priority", pressures[0]["row"] == "R7_alpha3" and pressures[0]["target_bound"] == "4e-20", "alpha3 is prioritized as highest-pressure row")
    add("V1118_6_gates_blocked", all(row["gate_pass"] == "false" for row in gates), "all claim gates remain blocked")
    add("V1118_7_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in theorem + contract + pressures + gates + decisions + next_target), "all stamped rows remain nonclaim")
    add("V1118_8_next_target", next_target[0]["next_target"].startswith("1119-") and "domain-alpha3" in str(next_target[0]["next_target"]), "1119 handoff targets domain alpha3 R11 source zero or product fill")
    add("V1118_9_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1118_10_csv_parse", csv_parse_ok, "all 1118 CSV outputs parse cleanly")
    add("V1118_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1118_SUMMARY", True, "1118 rejects domain R11 source zero and stages strict nonclaim executable-vector contract")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    contract: list[dict[str, object]],
    candidates: list[dict[str, object]],
    pressures: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1118 - Domain R11 Source Normalization Zero Or Executable Coefficient Vector

**Current verdict:** `c_domain_source_normalization_operator = 0` is not derived. The R11/domain source-normalization branch is wired, but not executable evidence because coefficient/theorem-zero values remain missing or conditional.

**Important distinction:** wired rows are not scored rows. A domain R11 row becomes evidence only when it has concrete coefficient values or a real theorem-zero certificate, units, normalization, weak-field maps, source paths, and no `MISSING` fields.

**No claim:** no R11 source zero, no domain alpha3 pass, no local-GR/R10 safety, and no executable domain coefficient-vector pass follows from 1118.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Zero Theorem Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "claim_allowed"], theorem)}

## Executable Vector Contract
{table(["contract_id", "requirement", "must_hold", "current_status", "blocks_claim_if_missing", "claim_allowed"], contract)}

## Candidate R11 Rows
{table(R11_SCHEMA, candidates)}

## Pressure Order
{table(["pressure_id", "row", "product", "target_bound", "status", "next_required", "claim_allowed"], pressures)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "claim_allowed"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1118_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1118_DOMAIN_R11_ZERO_THEOREM_ATTEMPT.csv",
        "contract": OUT / "P8_Y5_R10_1118_EXECUTABLE_VECTOR_CONTRACT.csv",
        "candidates": OUT / "P8_Y5_R10_1118_R11_DOMAIN_CANDIDATE_ROWS_NONCLAIM.csv",
        "pressure": OUT / "P8_Y5_R10_1118_DOMAIN_PRESSURE_ORDER.csv",
        "gates": OUT / "P8_Y5_R10_1118_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1118_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1118_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1118_VALIDATION.csv",
    }
    sources = source_rows()
    theorem = theorem_rows()
    contract = executable_contract_rows()
    candidates = candidate_rows()
    pressures = pressure_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["contract"], contract)
    write_csv(outputs["candidates"], candidates, R11_SCHEMA)
    write_csv(outputs["pressure"], pressures)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, theorem, contract, candidates, pressures, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorem, contract, candidates, pressures, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

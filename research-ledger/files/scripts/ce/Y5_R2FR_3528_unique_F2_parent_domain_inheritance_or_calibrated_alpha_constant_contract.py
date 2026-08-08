from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3528-Y5-R2FR-unique-F2-parent-domain-inheritance-or-calibrated-alpha-constant-contract.md"
CANONICAL_STATUS = OUT / "P8_EM_unique_F2_or_calibrated_alpha_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3528": {"path": Path(__file__).resolve(), "role": "3528 generator"},
    "doc_3527": {
        "path": ROOT / "3527-Y5-R2FR-charge-generator-level-current-owner-or-alpha-ratio-countermodel-kill.md",
        "role": "3527 compact-U1 no-go and remaining route",
    },
    "next_3527": {
        "path": OUT / "P8_Y5_R2FR_3527_NEXT_TARGET.csv",
        "role": "3527-selected unique-F2-or-calibrated-alpha target",
    },
    "status_3527": {
        "path": OUT / "P8_EM_alpha_level_current_owner_status.csv",
        "role": "3527 canonical level/current owner status",
    },
    "no_go_3527": {
        "path": OUT / "P8_Y5_R2FR_3527_LEVEL_CURRENT_NO_GO_THEOREM.csv",
        "role": "compact U1 plus Noether current no-go theorem",
    },
    "req_3527": {
        "path": OUT / "P8_Y5_R2FR_3527_PARENT_PRINCIPLE_REQUIREMENTS.csv",
        "role": "parent principle requirements for alpha",
    },
    "unique_f2_1057": {
        "path": OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "role": "unique Maxwell subblock theorem attempt",
    },
    "operator_audit_1057": {
        "path": OUT / "P8_Y5_R10_1057_OPERATOR_DOMAIN_AUDIT.csv",
        "role": "ordinary symmetry allowance and domain audit",
    },
    "f2_counterterms_1057": {
        "path": OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv",
        "role": "constant, hidden and radiative F2 counterterms",
    },
    "operator_domain_1058": {
        "path": OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
        "role": "visible operator-domain exhaustion attempt",
    },
    "operator_algebra_1058": {
        "path": OUT / "P8_Y5_R10_1058_ALLOWED_OPERATOR_ALGEBRA_AUDIT.csv",
        "role": "allowed visible operator algebra audit",
    },
    "radiative_readout_1058": {
        "path": OUT / "P8_Y5_R10_1058_RADIATIVE_READOUT_CLOSURE_GATE.csv",
        "role": "radiative/readout closure gates",
    },
    "scalar_ratio_3526": {
        "path": OUT / "P8_Y5_R2FR_3526_SCALAR_COUPLING_RATIO_THEOREM.csv",
        "role": "C_XF2 ratio theorem",
    },
    "alpha_bound_rows_3526": {
        "path": OUT / "P8_Y5_R2FR_3526_ALPHA_BOUND_ROWS.csv",
        "role": "finite alpha/WEP/R10/clock/source bound rows",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical bound anchors",
    },
    "tq_signature_1100": {
        "path": OUT / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
        "role": "T_Q gauge-norm and same-current signature clauses",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def inheritance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "IF23528_0_parent_curvature_projection",
            "gate": "parent connection projects to visible charge subblock",
            "mathematical_contract": "A_parent=A_Q T_Q + A_perp and F_parent contains F_Q T_Q with fixed <T_Q,T_Q>_P=N_Q",
            "derivation_result": "conditional sublemma: lambda_parent=C_P N_Q",
            "current_status": "CONDITIONAL_TEMPLATE_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["unique_f2_1057"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "IF23528_1_no_independent_visible_F2",
            "gate": "no independent lambda_A F_Q^2 visible operator",
            "mathematical_contract": "Allowed[S_vis] contains no scalar-density operator outside Image(ParentGenerate)",
            "derivation_result": "would make lambda_A equal to the parent curvature norm rather than a new coefficient",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS",
            "source_path": str(SOURCES["operator_audit_1057"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "IF23528_2_no_hidden_F2_coefficient",
            "gate": "no hidden scalar f(I_hid) multiplying F_Q^2",
            "mathematical_contract": "Hom(C_hid,Coeff(F_Q^2)) is absent, constant, or forbidden by target action domain",
            "derivation_result": "would kill vertical alpha drift from hidden coefficients",
            "current_status": "BLOCKED_BY_SCALAR_OBSTRUCTION",
            "source_path": str(SOURCES["operator_domain_1058"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "IF23528_3_radiative_readout_stability",
            "gate": "loops, thresholds and readout do not regenerate F_Q^2 coefficients",
            "mathematical_contract": "S_vis_eff and alpha readout remain in Image(ParentGenerate) at all relevant scales",
            "derivation_result": "would make a tree-level alpha owner stable in measured clocks/spectra",
            "current_status": "UNSIGNED",
            "source_path": str(SOURCES["radiative_readout_1058"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "IF23528_4_same_current_and_source",
            "gate": "same Noether current/source owner",
            "mathematical_contract": "J_Q=delta S_matter/delta A_Q with fixed Q_* and no c_A(X) weights across source/test/readout",
            "derivation_result": "would transfer alpha owner into WEP/R10/source coupling rather than vacuum-only alpha",
            "current_status": "UNSIGNED",
            "source_path": str(SOURCES["tq_signature_1100"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "IF23528_5_live_verdict",
            "gate": "unique F2 parent-domain inheritance theorem",
            "mathematical_contract": "IF23528_0 through IF23528_4 all signed together",
            "derivation_result": "would derive C_XF2=0 rather than calibrate alpha",
            "current_status": "FAIL_CURRENT_CORPUS_USE_CALIBRATED_ALPHA_CONTRACT",
            "source_path": str(SOURCES["operator_domain_1058"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def operator_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "OP3528_0_parent_F2",
            "operator_class": "parent-generated Maxwell kinetic term",
            "example": "C_P <F_Q T_Q,F_Q T_Q>_P",
            "ordinary_symmetry_status": "ALLOWED",
            "domain_status": "ALLOWED_CONDITIONAL",
            "effect": "candidate parent-owned coefficient if projection and norm are signed",
            "verdict": "KEEP_AS_DERIVATION_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP3528_1_constant_lambda",
            "operator_class": "constant independent visible F2 counterterm",
            "example": "lambda_A F_Q^2",
            "ordinary_symmetry_status": "ALLOWED",
            "domain_status": "FORBIDDEN_ONLY_IF_EXHAUSTION_DERIVED",
            "effect": "blocks alpha derivation but can be absorbed into calibrated alpha_0 if universal and constant",
            "verdict": "RETAIN_OR_CALIBRATE_NOT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP3528_2_hidden_scalar_lambda",
            "operator_class": "hidden scalar gauge-kinetic coefficient",
            "example": "f(I_hid) F_Q^2",
            "ordinary_symmetry_status": "ALLOWED_IF_HIDDEN_INVARIANT_SURVIVES",
            "domain_status": "NOT_FORBIDDEN_CURRENT_CORPUS",
            "effect": "creates alpha drift and local test pressure",
            "verdict": "BOUND_BRANCH_REQUIRED_IF_PRESENT",
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP3528_3_radiative_lambda",
            "operator_class": "loop/threshold/readout regenerated F2",
            "example": "delta_lambda_A(mu,X) F_Q^2",
            "ordinary_symmetry_status": "RETAINED",
            "domain_status": "UNSIGNED_RADIOUT_CLOSURE",
            "effect": "tree-level owner is not enough for clocks/spectroscopy",
            "verdict": "BOUND_BRANCH_REQUIRED_IF_PRESENT",
            "valid_for_claim": "False",
        },
    ]


def calibrated_alpha_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "CA3528_0_definition",
            "constant_or_rule": "alpha_0",
            "contract": "alpha_EM is taken as a measured universal local constant in the low-energy local branch",
            "mathematical_form": "alpha_EM=alpha_0; D_X ln alpha_EM=0 by calibration closure, not theorem",
            "allowed_use": "fixes local Maxwell normalization after calibration",
            "forbidden_use": "cannot be counted as an MTS prediction or as evidence that C_XF2 was derived",
            "test_policy": "only drift, non-universal source coupling and residual C_XF2 branches are testable",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CA3528_1_action_normalization",
            "constant_or_rule": "lambda_A/e_obs^2",
            "contract": "the ratio lambda_A/e_obs^2 is fixed to alpha_0^{-1} in the calibrated local effective action",
            "mathematical_form": "S_EM=-1/2 int lambda_0 F_Q wedge *_obs F_Q + int e_0 A_Q.J_Q with e_0^2/lambda_0=alpha_0 up to convention factors",
            "allowed_use": "lets Maxwell stress be computed consistently in the local branch",
            "forbidden_use": "cannot tune WEP/R10/clock residuals or cancel other source-weight errors",
            "test_policy": "any field-dependent correction delta ln(lambda_A/e_obs^2) must use the 3526 bound rows",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CA3528_2_GR_style_constant_policy",
            "constant_or_rule": "calibrated constants are allowed if labelled",
            "contract": "alpha_0 may be treated like G_N in GR: a universal measured constant of the local effective theory unless a deeper parent derivation is later found",
            "mathematical_form": "Constants enter the action; predictions are variations, relations, limits and residuals, not the numerical constant itself",
            "allowed_use": "moves the local GR/Newton/Maxwell derivation forward without pretending all constants are derived",
            "forbidden_use": "cannot advertise a derived alpha value or alpha-zero theorem",
            "test_policy": "hold alpha fixed for baseline local tests; separately score any proposed alpha-drift branch",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CA3528_3_replacement_policy",
            "constant_or_rule": "future parent derivation can supersede calibration",
            "contract": "if a later parent-domain theorem signs IF23528_0..4, the calibrated-alpha row is demoted to measured boundary condition and C_XF2=0 can be promoted",
            "mathematical_form": "Derived route replaces closure only after source-backed domain proof and radiative/readout stability pass",
            "allowed_use": "keeps derivation-first pressure alive",
            "forbidden_use": "cannot promote on analogy, compact U(1), or field-rescaling arguments",
            "test_policy": "future promotion must pass the same validation gates with no placeholder clauses",
            "valid_for_claim": "False",
        },
    ]


def test_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy_id": "TP3528_0_baseline_Maxwell",
            "arena": "local Maxwell/EM stress",
            "baseline": "use calibrated alpha_0 and observed Hodge/coframe",
            "what_counts_as_test": "source stress, Poynting bookkeeping, readout consistency and deviations from calibrated Maxwell",
            "what_does_not_count": "claiming alpha_0 numerical value as predicted",
            "bound_source": str(SOURCES["scalar_ratio_3526"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "policy_id": "TP3528_1_WEP_clocks_R10",
            "arena": "WEP/clock/R10 alpha drift",
            "baseline": "C_XF2=0 by calibrated-constant closure unless an MTS branch predicts a nonzero correction",
            "what_counts_as_test": "nonzero delta ln(lambda_A/e_obs^2) mapped through source/test/readout kernels and compared to 3526 bounds",
            "what_does_not_count": "using WEP/clock null results as proof alpha was parent-derived",
            "bound_source": str(SOURCES["alpha_bound_rows_3526"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "policy_id": "TP3528_2_local_GR_Newton",
            "arena": "local GR/Newton source coupling",
            "baseline": "alpha calibrated; focus shifts to total Hilbert source, G_N/kappa calibration, source current owner and Newtonian limit",
            "what_counts_as_test": "derive or bound EM+matter stress coupling into the local field equations",
            "what_does_not_count": "reopening alpha unless a specific nonzero C_XF2 branch is proposed",
            "bound_source": str(SOURCES["tq_signature_1100"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "policy_id": "TP3528_3_public_language",
            "arena": "private/public claim hygiene",
            "baseline": "say calibrated, not derived",
            "what_counts_as_test": "clear label on every alpha row: derived, calibrated, or bounded residual",
            "what_does_not_count": "calling calibrated-alpha closure a theorem",
            "bound_source": str(SOURCES["status_3527"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3528_0_unique_F2",
            "quantity": "unique_F2_parent_inheritance",
            "value": "exact_conditional_not_live",
            "meaning": "parent curvature norm plus no-extra-F2 domain would derive alpha, but current corpus does not sign the domain theorem",
            "claim_effect": "no derived-alpha claim",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3528_1_calibrated_alpha",
            "quantity": "alpha_EM_local_branch",
            "value": "calibrated_universal_constant",
            "meaning": "alpha is fixed in the local branch as measured input, not as an MTS prediction",
            "claim_effect": "lets local Maxwell/GR source programme proceed honestly",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3528_2_CXF2",
            "quantity": "C_XF2",
            "value": "zero_by_calibration_or_bounded_if_branch_active",
            "meaning": "baseline sets C_XF2=0 by constant closure; any nonzero branch must be scored with WEP/clock/R10 bounds",
            "claim_effect": "no smuggled theorem-zero",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3528_3_next",
            "quantity": "next_project_focus",
            "value": "calibrated_alpha_to_local_GR_source_coupling_interface",
            "meaning": "return to total Hilbert source, G_N/kappa calibration and Newtonian/PPN reduction",
            "claim_effect": "moves beyond the alpha loop",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3528_0_reject_live_unique_F2_claim",
            "decision": "do not promote unique-F2 inheritance as a current theorem",
            "rationale": "ordinary gauge/diffeomorphism symmetries allow independent F_Q^2 and the parent-domain exhaustion rule is not derived",
            "effect": "prevents a fake alpha derivation",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3528_1_adopt_calibrated_alpha_contract",
            "decision": "adopt alpha as an explicitly calibrated universal local constant for the baseline branch",
            "rationale": "this is honest, GR-compatible methodology and keeps the larger local-GR programme moving",
            "effect": "C_XF2 no longer blocks every next step unless a nonzero branch is proposed",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3528_2_shift_next_to_source_coupling",
            "decision": "move next to the calibrated-alpha source-coupling interface",
            "rationale": "the remaining decisive problem is not alpha value but how matter+EM Hilbert stress couples into local GR/Newton with calibrated constants",
            "effect": "next checkpoint should reconnect Maxwell stress, G_N/kappa and Newtonian limit",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3529-Y5-R2FR-calibrated-alpha-to-local-GR-source-coupling-interface.md",
            "next_script": "scripts/Y5_R2FR_3529_calibrated_alpha_to_local_GR_source_coupling_interface.py",
            "objective": "With alpha explicitly calibrated, build the source-coupling interface: show how calibrated Maxwell stress, matter Hilbert stress, G_N/kappa calibration and source-current ownership enter the local GR/Newton reduction without claiming derived alpha.",
            "success_gate": "A source-coupling ledger separates derived Hilbert identities, calibrated constants, and finite residuals; no local-GR/Newton pass is claimed until G_N/kappa/source normalization and PPN/Newton limits are checked.",
            "why_next": "3528 ends the alpha loop honestly; the goal now needs the GR/Newton source spine sharpened.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    operators: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    policies: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3528_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3528_1_unique_F2_not_promoted", "passed": bool_text(any(row["gate_id"] == "IF23528_5_live_verdict" and row["current_status"] == "FAIL_CURRENT_CORPUS_USE_CALIBRATED_ALPHA_CONTRACT" for row in gates) and any(row["quantity"] == "unique_F2_parent_inheritance" and row["value"] == "exact_conditional_not_live" for row in status)), "detail": "unique-F2 inheritance remains conditional only", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3528_2_counterterms_retained", "passed": bool_text(any(row["operator_id"] == "OP3528_1_constant_lambda" and row["verdict"] == "RETAIN_OR_CALIBRATE_NOT_DERIVED" for row in operators) and any(row["operator_id"] == "OP3528_2_hidden_scalar_lambda" and row["verdict"] == "BOUND_BRANCH_REQUIRED_IF_PRESENT" for row in operators)), "detail": "constant and hidden F2 counterterms are not ignored", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3528_3_calibrated_contract_written", "passed": bool_text(any(row["contract_id"] == "CA3528_0_definition" and "not theorem" in row["mathematical_form"] for row in contract) and any(row["quantity"] == "alpha_EM_local_branch" and row["value"] == "calibrated_universal_constant" for row in status)), "detail": "alpha is explicitly calibrated, not claimed as derived", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3528_4_test_policy_keeps_bounds", "passed": bool_text(any(row["policy_id"] == "TP3528_1_WEP_clocks_R10" and "3526" in row["bound_source"] for row in policies)), "detail": "nonzero C_XF2 branches still route to WEP/clock/R10 bounds", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3528_5_next_target_moves_to_GR_source", "passed": bool_text(next_rows[0]["next_doc"].startswith("3529-Y5-R2FR-calibrated-alpha-to-local-GR-source")), "detail": "next target returns to local GR/source coupling", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3528_6_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + gates + operators + contract + policies + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no alpha/local-GR/Newton claim is promoted", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3528_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3528_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3528_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3528_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    operators: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    policies: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3528 - Unique F2 Parent-Domain Inheritance Or Calibrated Alpha Constant Contract

## Summary
- **Last derivation route tested:** parent curvature-norm inheritance plus no independent `F_Q^2` operator.
- **Result:** exact conditional route, but not live. The parent subblock can supply `C_P N_Q`, yet ordinary gauge/diffeomorphism symmetries still allow `lambda_A F_Q^2` unless a stronger parent-domain theorem is signed.
- **Decision:** adopt `alpha_EM` as an explicit calibrated universal constant in the local baseline branch. This is not a failure; GR also carries calibrated constants. The rule is that we label it honestly.
- **No smuggling:** `C_XF2=0` is now baseline calibration, not theorem-zero. Any nonzero MTS alpha branch must use the WEP/clock/R10/source bound rows from 3526.
- **Next focus:** return to local GR/Newton source coupling: calibrated Maxwell stress, matter Hilbert stress, `G_N/kappa`, and source-current ownership.

## Alpha Contract In One Line
`alpha_EM = alpha_0` in the local calibrated branch, while

`C_XF2 = D_X ln(lambda_A/e_obs^2) = 0`

is a **closure/calibration condition**, not a derived MTS theorem.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Unique F2 Inheritance Gates
{markdown_table(gates, ["gate_id", "gate", "mathematical_contract", "derivation_result", "current_status", "source_path", "valid_for_claim"])}

## Operator Domain Result
{markdown_table(operators, ["operator_id", "operator_class", "example", "ordinary_symmetry_status", "domain_status", "effect", "verdict", "valid_for_claim"])}

## Calibrated Alpha Contract
{markdown_table(contract, ["contract_id", "constant_or_rule", "contract", "mathematical_form", "allowed_use", "forbidden_use", "test_policy", "valid_for_claim"])}

## Test Policy
{markdown_table(policies, ["policy_id", "arena", "baseline", "what_counts_as_test", "what_does_not_count", "bound_source", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    gates = inheritance_gate_rows()
    operators = operator_result_rows()
    contract = calibrated_alpha_contract_rows()
    policies = test_policy_rows()
    status = status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3528_SOURCE_REGISTER.csv",
        "inheritance_gates": OUT / "P8_Y5_R2FR_3528_UNIQUE_F2_INHERITANCE_GATES.csv",
        "operator_result": OUT / "P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv",
        "calibrated_alpha_contract": OUT / "P8_Y5_R2FR_3528_CALIBRATED_ALPHA_CONTRACT.csv",
        "test_policy": OUT / "P8_Y5_R2FR_3528_TEST_POLICY.csv",
        "status": OUT / "P8_Y5_R2FR_3528_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "decision_ledger": OUT / "P8_Y5_R2FR_3528_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3528_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3528_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["inheritance_gates"], gates, ["gate_id", "gate", "mathematical_contract", "derivation_result", "current_status", "source_path", "valid_for_claim"])
    write_csv(outputs["operator_result"], operators, ["operator_id", "operator_class", "example", "ordinary_symmetry_status", "domain_status", "effect", "verdict", "valid_for_claim"])
    write_csv(outputs["calibrated_alpha_contract"], contract, ["contract_id", "constant_or_rule", "contract", "mathematical_form", "allowed_use", "forbidden_use", "test_policy", "valid_for_claim"])
    write_csv(outputs["test_policy"], policies, ["policy_id", "arena", "baseline", "what_counts_as_test", "what_does_not_count", "bound_source", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, gates, operators, contract, policies, status, decisions, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, gates, operators, contract, policies, status, decisions, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()

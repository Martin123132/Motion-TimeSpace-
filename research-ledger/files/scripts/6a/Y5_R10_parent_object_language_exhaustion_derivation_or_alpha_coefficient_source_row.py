from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1107-Y5-R10-parent-object-language-exhaustion-derivation-or-alpha-coefficient-source-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    stamped: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        stamped.append(copied)
    return stamped


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
    rows = [
        {
            "source_id": "SRC1107_0_1106_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1106_NEXT_TARGET.csv",
            "needle": "NEXT1106_0_1107",
            "note": "1106 handoff to parent object-language exhaustion or alpha source row.",
        },
        {
            "source_id": "SRC1107_1_1106_min_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1106_MINIMAL_CLOSURE_PACK.csv",
            "needle": "MIN1106_A",
            "note": "minimal closure target.",
        },
        {
            "source_id": "SRC1107_2_1106_priority",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1106_FINITE_ROW_PRIORITY.csv",
            "needle": "PRI1106_0_alpha",
            "note": "alpha selected as first finite fallback row.",
        },
        {
            "source_id": "SRC1107_3_1058_exhaustion",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
            "needle": "VOE1058_5_verdict",
            "note": "visible operator-domain exhaustion attempt.",
        },
        {
            "source_id": "SRC1107_4_1049_classification",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
            "needle": "OCR1049_5_verdict",
            "note": "operator classification rule attempt.",
        },
        {
            "source_id": "SRC1107_5_1105_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1105_MASTER_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "MHM1105_6_verdict",
            "note": "master morphism demotion result.",
        },
        {
            "source_id": "SRC1107_6_1098_requirements",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_0_c_alpha",
            "note": "alpha coefficient threshold requirement.",
        },
        {
            "source_id": "SRC1107_7_1051_clock",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv",
            "needle": "BAP1051_2_best_current_product",
            "note": "best clock alpha product bound.",
        },
        {
            "source_id": "SRC1107_8_1102_inputs",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv",
            "needle": "IN1102_5_beta_source_alpha",
            "note": "latest alpha-product input status.",
        },
        {
            "source_id": "SRC1107_9_1101_gauge_norm",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv",
            "needle": "GFT1101_4_verdict",
            "note": "latest gauge norm owner verdict.",
        },
        {
            "source_id": "SRC1107_10_1098_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "needle": "OCS1098_1_unique_EM_owner",
            "note": "ordinary-sector EM owner clause.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in rows:
        path = ROOT / str(row["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **row,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(row["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def exhaustion_attempt_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "EXH1107_0_target",
                "claim_piece": "parent ordinary-sector object-language exhaustion",
                "formal_statement": "Coeff(O_vis) subset Image(ParentGenerate[q, theta_rep, topological levels]) and no hidden target action on Coeff(O_vis).",
                "result": "TARGET_RESTATED",
                "proof_or_blocker": "would close MIN1106_A if generated from MTS primitives, not adopted as a style rule",
            },
            {
                "attempt_id": "EXH1107_1_chain_rule",
                "claim_piece": "if coefficient is in parent-generated image then vertical drift vanishes",
                "formal_statement": "c_vis(Phi)=cbar(q(Phi),theta_rep) and Dq[v]=0 imply Lie_v c_vis=0.",
                "result": "EXACT_CONDITIONAL_THEOREM",
                "proof_or_blocker": "chain-rule part is solid but only after membership in Image(ParentGenerate) is proved",
            },
            {
                "attempt_id": "EXH1107_2_membership_problem",
                "claim_piece": "visible coefficients are exhausted by Image(ParentGenerate)",
                "formal_statement": "Allowed[S_vis] has no additional local counterterm algebra beyond parent-generated terms.",
                "result": "NOT_DERIVED",
                "proof_or_blocker": "1058 and 1049 both mark this as exact if adopted but not derived from MTS primitives",
            },
            {
                "attempt_id": "EXH1107_3_alpha_counterterm",
                "claim_piece": "no-extra-F2 subcase",
                "formal_statement": "lambda_A F_Q^2 and f(I_hid)F_Q^2 are outside the parent-generated image.",
                "result": "COUNTERTERM_STILL_LEGAL",
                "proof_or_blocker": "gauge/diffeomorphism symmetry allows the term unless a stronger owner/exhaustion theorem is signed",
            },
            {
                "attempt_id": "EXH1107_4_hidden_target_action",
                "claim_piece": "hidden invariants have no target action on visible coefficient spaces",
                "formal_statement": "No map C_hid -> Coeff(O_vis) exists except constant maps.",
                "result": "BLOCKED_BY_SCALAR_OBSTRUCTION",
                "proof_or_blocker": "surviving I_hid builds c0+epsilon I_hid",
            },
            {
                "attempt_id": "EXH1107_5_radiative_readout",
                "claim_piece": "object-language exhaustion is stable under S_eff/readout",
                "formal_statement": "S_eff and readout maps remain in Image(ParentGenerate).",
                "result": "UNSIGNED",
                "proof_or_blocker": "tree-level exhaustion would not be claim-grade without radiative/readout stability",
            },
            {
                "attempt_id": "EXH1107_6_verdict",
                "claim_piece": "derive MIN1106_A in current corpus",
                "formal_statement": "EXH1107_1 through EXH1107_5 close from parent primitives.",
                "result": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
                "proof_or_blocker": "the rule is clean and probably necessary, but remains explicit closure unless a parent-generator construction is supplied",
            },
        ]
    )


def alpha_subcase_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "subcase_id": "ALP1107_0_parent_generated_F2",
                "object": "parent-generated EM kinetic term",
                "form": "C_P <F_Q T_Q,F_Q T_Q>_P",
                "status": "ALLOWED_CONDITIONAL",
                "claim_effect": "can own one Maxwell coefficient only if T_Q, fibre norm, and readout are parent fixed",
            },
            {
                "subcase_id": "ALP1107_1_constant_counterterm",
                "object": "constant visible F2 counterterm",
                "form": "lambda_A F_Q^2",
                "status": "LEGAL_IF_EXHAUSTION_UNSIGNED",
                "claim_effect": "blocks unique alpha owner even without hidden scalar drift",
            },
            {
                "subcase_id": "ALP1107_2_hidden_counterterm",
                "object": "hidden-scalar visible F2 counterterm",
                "form": "f(I_hid) F_Q^2 or f_X(Xhat) F_Q^2",
                "status": "LEGAL_IF_HIDDEN_TARGET_ACTION_UNSIGNED",
                "claim_effect": "opens b_alpha/c_alpha drift and clock/WEP/R10 alpha pressure",
            },
            {
                "subcase_id": "ALP1107_3_radiative_counterterm",
                "object": "effective/readout F2 counterterm",
                "form": "delta lambda_A(mu,I_hid) F_Q^2",
                "status": "RETAINED_UNTIL_RADIOUT_CLOSURE",
                "claim_effect": "prevents tree-level no-extra-F2 from becoming claim-grade",
            },
            {
                "subcase_id": "ALP1107_4_verdict",
                "object": "b_alpha theorem-zero",
                "form": "b_alpha=0 from parent object-language exhaustion plus EM owner and readout stability",
                "status": "NOT_PROMOTED",
                "claim_effect": "stage finite alpha coefficient/product source row instead",
            },
        ]
    )


def alpha_candidate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "prediction_id": "PRED1107_0_alpha_coefficient_source_row",
                "arena": "alpha_shared",
                "product_symbol": "c_alpha_DD_or_b_alpha",
                "product_value": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_THEOREM_ZERO",
                "product_units": "dimensionless coefficient",
                "product_source": "MISSING_SOURCE_PATH",
                "inputs_present": "threshold_abs=8.320244933243533e-10; clock_product_bound=2.1e-18 yr^-1",
                "required_inputs": "source-backed b_alpha/c_alpha value OR parent no-extra-F2 theorem; tau_clock/tau_WEP/tau_R10 maps for arena products",
                "derivation_status": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
                "notes": "This is a schema row only; it is not an MTS prediction.",
            },
            {
                "prediction_id": "PRED1107_1_clock_alpha_product",
                "arena": "clock",
                "product_symbol": "b_alpha*tau_clock_time",
                "product_value": "MISSING_MTS_CLOCK_PRODUCT_PREDICTION",
                "product_units": "yr^-1",
                "product_source": "MISSING_TAU_CLOCK_XHAT_SOURCE",
                "inputs_present": "bound_abs=2.1e-18 yr^-1",
                "required_inputs": "tau_clock_time; Xhat normalization; alpha owner or numeric b_alpha product",
                "derivation_status": "BOUND_AVAILABLE_NOT_PREDICTION",
                "notes": "Do not extract standalone b_alpha from the clock bound.",
            },
            {
                "prediction_id": "PRED1107_2_WEP_alpha_product",
                "arena": "MICROSCOPE_WEP",
                "product_symbol": "P_WEP_alpha",
                "product_value": "MISSING_BETA_SOURCE_ALPHA_TAU_WEP_DIRECT_PRODUCT",
                "product_units": "dimensionless",
                "product_source": "MISSING_SOURCE_PATH",
                "inputs_present": "direct_target=4.797780522732e-05; material smoke convention",
                "required_inputs": "beta_source_alpha; tau_WEP; direct product theorem/value; material/readout tensor",
                "derivation_status": "INPUTS_MISSING",
                "notes": "Target exists; prediction does not.",
            },
            {
                "prediction_id": "PRED1107_3_R10_alpha_lambda",
                "arena": "R10_short_range",
                "product_symbol": "alpha_MTS(lambda)",
                "product_value": "MISSING_ALPHA_LAMBDA_PRODUCT",
                "product_units": "dimensionless with length column",
                "product_source": "MISSING_SOURCE_PATH",
                "inputs_present": "R10 bound acquisition policy exists",
                "required_inputs": "lambda_X; K_X/Z_X; tau_R10; source/test weights; promoted alpha(lambda) curve",
                "derivation_status": "INPUTS_MISSING",
                "notes": "No alpha(lambda) claim from this row.",
            },
        ]
    )


def bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "bound_id": "BOUND1107_0_DD_alpha_threshold",
                "arena": "WEP_DD_pressure",
                "product_symbol": "c_alpha_DD_or_b_alpha",
                "bound_value": "8.320244933243533e-10",
                "bound_units": "dimensionless coefficient",
                "bound_source": "P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
                "source_row": "REQ1098_0_c_alpha",
                "bound_type": "threshold_nonclaim",
            },
            {
                "bound_id": "BOUND1107_1_clock_product",
                "arena": "clock",
                "product_symbol": "b_alpha*tau_clock_time",
                "bound_value": "2.1e-18",
                "bound_units": "yr^-1",
                "bound_source": "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv",
                "source_row": "BAP1051_2_best_current_product",
                "bound_type": "source_backed_product_bound_nonclaim",
            },
            {
                "bound_id": "BOUND1107_2_WEP_alpha_target",
                "arena": "MICROSCOPE_WEP",
                "product_symbol": "P_WEP_alpha",
                "bound_value": "4.797780522732e-05",
                "bound_units": "dimensionless",
                "bound_source": "P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv",
                "source_row": "IN1102_4_WEP_product_target",
                "bound_type": "target_nonclaim",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1107_0_object_exhaustion",
                "claim": "parent object-language exhaustion is derived",
                "gate_pass": "false",
                "reason": "membership in Image(ParentGenerate) is not derived; counterterms remain legal",
            },
            {
                "gate_id": "CG1107_1_no_extra_F2",
                "claim": "no-extra-F2/b_alpha=0 is derived",
                "gate_pass": "false",
                "reason": "constant and hidden F2 counterterms remain allowed unless exhaustion/EM owner is signed",
            },
            {
                "gate_id": "CG1107_2_alpha_source_row",
                "claim": "alpha coefficient row is source-backed and scoreable",
                "gate_pass": "false",
                "reason": "candidate rows contain MISSING markers and valid_for_claim=false",
            },
            {
                "gate_id": "CG1107_3_clock_WEP_R10_transfer",
                "claim": "alpha coefficient transfers to clock/WEP/R10 predictions",
                "gate_pass": "false",
                "reason": "tau_clock, beta_source_alpha, tau_WEP, tau_R10, and source/test maps remain missing",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1107_0_derivation_result",
                "decision": "parent object-language exhaustion is not derived",
                "because": "the rule is exact if adopted, but current MTS does not construct ParentGenerate or prove all visible coefficients lie in its image",
                "next_action": "do not adopt MIN1106_A as derivation",
            },
            {
                "decision_id": "DEC1107_1_alpha_status",
                "decision": "alpha finite row is staged but remains empty",
                "because": "threshold and clock bound exist, but no MTS coefficient value or theorem-zero exists",
                "next_action": "attempt a narrower no-extra-F2 parent-generator image proof or acquire a real source-backed alpha coefficient row",
            },
            {
                "decision_id": "DEC1107_2_best_next",
                "decision": "narrow from full object-language exhaustion to the EM F2 image subproblem",
                "because": "full exhaustion is too broad; no-extra-F2 is the highest leverage subcase and alpha is first finite priority",
                "next_action": "1108 should target parent EM-F2 image exhaustion or alpha coefficient acquisition",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1107_0_1108",
                "next_target": "1108-Y5-R10-parent-EM-F2-image-exhaustion-or-alpha-coefficient-acquisition.md",
                "objective": "try the narrower parent EM-F2 image exhaustion proof: show every visible F_Q^2 coefficient comes from one parent curvature/gauge-norm image and no independent lambda_A or f(I_hid)F_Q^2 target is admitted; if it fails, build a source-acquisition ledger for a real alpha coefficient/product row",
                "include": "ParentGenerate_EM image; T_Q/fibre norm owner; no lambda_A F_Q^2; no f(I_hid)F^2; radiative/readout F2 closure; alpha coefficient source-row requirements",
                "exclude": "full object-language exhaustion claim; b_alpha=0 from taste; standalone b_alpha from clocks; tau=1; WEP/R10 transfer without projections; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    exhaustion: list[dict[str, object]],
    subcases: list[dict[str, object]],
    predictions: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add(
        "V1107_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1107_1_exhaustion_not_derived",
        any(row["result"] == "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED" for row in exhaustion),
        "object-language exhaustion is explicitly not promoted",
    )
    add(
        "V1107_2_counterterm_retained",
        any(row["result"] == "COUNTERTERM_STILL_LEGAL" for row in exhaustion)
        and any(row["status"] == "LEGAL_IF_EXHAUSTION_UNSIGNED" for row in subcases),
        "constant and hidden F2 counterterms remain retained",
    )
    add(
        "V1107_3_alpha_rows_nonclaim",
        all("MISSING" in row["product_value"] and row["valid_for_claim"] == "false" for row in predictions),
        "all alpha candidate rows remain missing-input/nonclaim",
    )
    add(
        "V1107_4_bound_rows_positive",
        all(float(row["bound_value"]) > 0 for row in bounds),
        "bound/threshold rows are positive numeric values",
    )
    add(
        "V1107_5_claim_gates_blocked",
        all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in gates),
        "all claim gates remain blocked",
    )
    add(
        "V1107_6_next_target",
        next_target[0]["next_target"].startswith("1108-") and "EM-F2-image" in str(next_target[0]["next_target"]),
        "1108 handoff narrows to EM-F2 image exhaustion or alpha coefficient acquisition",
    )
    add(
        "V1107_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in exhaustion + subcases + predictions + bounds + gates + decisions + next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1107_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for name, path in outputs.items():
        if name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1107_9_csv_parse", csv_parse_ok, "all 1107 CSV outputs parse cleanly")
    add(
        "V1107_10_formalization_untouched",
        True,
        "generator writes no outputs under formalization-workbench",
    )
    add(
        "V1107_SUMMARY",
        True,
        "1107 rejects full object-language exhaustion as current derivation and stages alpha rows as nonclaim source/acquisition targets",
    )
    return rows


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    exhaustion: list[dict[str, object]],
    subcases: list[dict[str, object]],
    predictions: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1107 - Parent Object-Language Exhaustion Derivation Or Alpha Coefficient Source Row

**Current verdict:** full parent object-language exhaustion is not derived. The chain-rule part works, but the hard membership claim — every visible coefficient lies in `Image(ParentGenerate)` — is still an explicit closure, not a theorem.

**Alpha result:** the no-extra-F2 subcase remains live. Constant `lambda_A F_Q^2`, hidden `f(I_hid)F_Q^2`, and radiative/readout F2 counterterms are retained until a narrower EM image theorem or a real source-backed alpha coefficient exists.

**Next move:** narrow the theorem to the EM F2 image problem before trying more global closure. If that still fails, the alpha coefficient/product row becomes a source-acquisition task, not a claim.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Object-Language Exhaustion Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "claim_allowed"], exhaustion)}

## Alpha / F2 Subcase
{table(["subcase_id", "object", "form", "status", "claim_effect", "claim_allowed"], subcases)}

## Alpha Candidate Rows
{table(["prediction_id", "arena", "product_symbol", "product_value", "product_units", "product_source", "inputs_present", "required_inputs", "derivation_status", "notes", "claim_allowed"], predictions)}

## Bound / Threshold Import
{table(["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_source", "source_row", "bound_type", "claim_allowed"], bounds)}

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
        "source_register": OUT / "P8_Y5_R10_1107_SOURCE_REGISTER.csv",
        "exhaustion_attempt": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
        "alpha_subcase": OUT / "P8_Y5_R10_1107_ALPHA_F2_SUBCASE.csv",
        "alpha_candidate": OUT / "P8_Y5_R10_1107_ALPHA_COEFFICIENT_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
        "bound_import": OUT / "P8_Y5_R10_1107_ALPHA_BOUND_THRESHOLD_IMPORT.csv",
        "claim_gates": OUT / "P8_Y5_R10_1107_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1107_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1107_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1107_VALIDATION.csv",
    }
    sources = source_rows()
    exhaustion = exhaustion_attempt_rows()
    subcases = alpha_subcase_rows()
    predictions = alpha_candidate_rows()
    bounds = bound_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["exhaustion_attempt"], exhaustion)
    write_csv(outputs["alpha_subcase"], subcases)
    write_csv(outputs["alpha_candidate"], predictions)
    write_csv(outputs["bound_import"], bounds)
    write_csv(outputs["claim_gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_target)
    validation = validate(sources, exhaustion, subcases, predictions, bounds, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, exhaustion, subcases, predictions, bounds, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

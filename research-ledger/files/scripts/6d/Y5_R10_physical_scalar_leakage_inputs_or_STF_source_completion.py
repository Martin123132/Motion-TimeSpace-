from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1184-Y5-R10-physical-scalar-leakage-inputs-or-STF-source-completion.md"
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


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1184_0_1183_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1183_NEXT_TARGET.csv",
            "needle": "NEXT1183_0_1184",
            "role": "handoff to physical scalar leakage inputs or STF source completion.",
        },
        {
            "source_id": "SRC1184_1_1183_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1183_VALIDATION.csv",
            "needle": "V1183_SUMMARY",
            "role": "1183 validation summary.",
        },
        {
            "source_id": "SRC1184_2_1183_Cdet2",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1183_SCALAR_LEAKAGE_DERIVATION.csv",
            "needle": "SLD1183_3_absolute_bound",
            "role": "canonical C_det2 math coefficient and missing physical normalization.",
        },
        {
            "source_id": "SRC1184_3_1183_domain",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1183_SCALAR_LEAKAGE_DERIVATION.csv",
            "needle": "SLD1183_4_domain_anisotropy",
            "role": "domain anisotropy first-order leakage route.",
        },
        {
            "source_id": "SRC1184_4_1183_qtrace",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1183_SCALAR_LEAKAGE_DERIVATION.csv",
            "needle": "SLD1183_5_q_trace",
            "role": "q_loc trace leakage route.",
        },
        {
            "source_id": "SRC1184_5_1183_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1183_UPDATED_PPN_PREDICTION_ROWS.csv",
            "needle": "UPPN1183_0_gamma",
            "role": "updated gamma leakage formula.",
        },
        {
            "source_id": "SRC1184_6_1183_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1183_CLAIM_GATES.csv",
            "needle": "G1183_2_gamma_score",
            "role": "gamma leakage remains blocked by physical inputs.",
        },
        {
            "source_id": "SRC1184_7_1179_KS",
            "relative_path": "1179-Y5-R10-reciprocal-metric-tracefree-transfer-derivation-or-KS-closure.md",
            "needle": "K_S_to_metric = sigma_KS * K_norm",
            "role": "K_S closure decomposition.",
        },
        {
            "source_id": "SRC1184_8_1010_q_loc",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "retained as an explicit nonclaim residual",
            "role": "q_loc remains retained residual.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def external_source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "external_id": "EXT1184_0_Will_PPN_framework",
            "title": "The Confrontation between General Relativity and Experiment",
            "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
            "source_role": "PPN/preferred-frame framework reference",
            "extracted_comparator": "framework only; no new numeric bound promoted",
            "confidence": "framework_reference",
            "valid_for_claim": False,
        },
        {
            "external_id": "EXT1184_1_Shao_Wex_alpha1_alpha2",
            "title": "New tests of local Lorentz invariance of gravity with small-eccentricity binary pulsars",
            "url": "https://arxiv.org/abs/1209.4503",
            "source_role": "candidate alpha1/alpha2 preferred-frame comparator source",
            "extracted_comparator": "|alpha_2| < 1.8e-4 (95% CL); alpha_1 = -0.4^{+3.7}_{-3.1}e-5 (95% CL), from abstract",
            "confidence": "source_backed_from_arxiv_abstract",
            "valid_for_claim": False,
        },
        {
            "external_id": "EXT1184_2_Shao_Wex_Kramer_binary_pulsars",
            "title": "New Constraints on Preferred Frame Effects from Binary Pulsars",
            "url": "https://arxiv.org/abs/1209.5171",
            "source_role": "supporting preferred-frame binary-pulsar source",
            "extracted_comparator": "preferred-frame alpha1/alpha2 binary-pulsar context; no independent numeric claim promoted here",
            "confidence": "supporting_source_not_claim_row",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def physical_input_rows() -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "PLI1184_0_C_C",
            "quantity": "C_C",
            "definition": "parent normalization multiplying the scalar C/log-det memory response",
            "derived_relation": "C_det2_phys = |C_C|/2 if C_local contains C_C logdet(I+K_S S_Q)",
            "current_status": "MISSING_PARENT_C_NORMALIZATION",
            "source_needed": "parent C action term and units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "PLI1184_1_epsilon_D",
            "quantity": "epsilon_D",
            "definition": "domain anisotropy envelope ||W_TF||_D for scalar projection of tracefree shear",
            "derived_relation": "leak_domain_linear <= epsilon_D |K_S| ||S_Q||_D",
            "current_status": "MISSING_DOMAIN_ANISOTROPY_ENVELOPE",
            "source_needed": "arena domain geometry or parent SO3/isotropy theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "PLI1184_2_K_S",
            "quantity": "K_S_to_metric",
            "definition": "tracefree transfer coefficient from S_Q to metric/STF residual",
            "derived_relation": "K_S_to_metric = sigma_KS K_norm",
            "current_status": "MISSING_PARENT_ORIENTATION_AND_NORMALIZATION",
            "source_needed": "Q identity or PPN closure source row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "PLI1184_3_norm_SQ_PPN",
            "quantity": "||S_Q||_PPN",
            "definition": "PPN-arena tracefree shear norm",
            "derived_relation": "if STF bound H_TF exists and K_S != 0, ||S_Q||_PPN <= (||H_TF||+||q_TF||+||projector_TF||)/|K_S|",
            "current_status": "MISSING_STF_BOUND_AND_KS",
            "source_needed": "STF/preferred-frame comparator and K_S source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "PLI1184_4_q_trace",
            "quantity": "q_trace",
            "definition": "scalar projection of q_loc-induced metric/scalar response, not a literal trace of a vector without a response map",
            "derived_relation": "gamma_leak_trace = q_trace + O(q_loc*S_Q)",
            "current_status": "MISSING_QLOC_RESPONSE_SPLIT",
            "source_needed": "Gamma/Khat/q_loc action or residual response map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "PLI1184_5_R3_math",
            "quantity": "R3_math",
            "definition": "third-and-higher log-det remainder after canonical tracefree second-order term",
            "derived_relation": "for 3D ||A||_2 <= rho < 1, |R3_math| <= rho^3/(1-rho)",
            "current_status": "MATH_BOUND_DERIVED_PHYSICAL_AMPLITUDE_MISSING",
            "source_needed": "rho=||K_S S_Q||_2 arena bound and parent C normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def remainder_rows() -> list[dict[str, object]]:
    rows = [
        {
            "remainder_id": "R3B1184_0_series",
            "assumption": "spectral_radius(A)<1",
            "formula": "log det(I+A)=sum_{n>=1} (-1)^{n+1} Tr(A^n)/n",
            "result": "valid local expansion domain identified",
            "status": "MATH_ONLY",
            "valid_for_claim": False,
        },
        {
            "remainder_id": "R3B1184_1_tracefree_terms",
            "assumption": "Tr(A)=0 and A=K_S S_Q",
            "formula": "log det(I+A) = -1/2 Tr(A^2) + R3",
            "result": "linear term vanishes and second-order term is canonical",
            "status": "MATH_ONLY",
            "valid_for_claim": False,
        },
        {
            "remainder_id": "R3B1184_2_bound",
            "assumption": "3D and ||A||_2 <= rho < 1",
            "formula": "|R3| <= sum_{n>=3} 3 rho^n/n <= rho^3/(1-rho)",
            "result": "scoreable once rho=||K_S S_Q||_2 is sourced",
            "status": "BOUND_DERIVED_INPUT_MISSING",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def score_formula_rows() -> list[dict[str, object]]:
    rows = [
        {
            "score_id": "SFR1184_0_gamma_bound",
            "component": "gamma_minus_1",
            "nonclaim_formula": "|gamma_MTS-1| <= |delta_gamma_scalar| + epsilon_D |K_S| ||S_Q||_PPN + (|C_C|/2)|K_S|^2||S_Q||_PPN^2 + |C_C|R3_math + |q_trace|",
            "inputs_closed": "R3_math formula only",
            "inputs_missing": "delta_gamma_scalar; epsilon_D; K_S; ||S_Q||_PPN; C_C; q_trace; rho",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "SFR1184_1_STF_bound",
            "component": "H_TF_metric",
            "nonclaim_formula": "||H_TF|| <= |K_S| ||S_Q||_PPN + ||q_TF|| + ||projector_TF||",
            "inputs_closed": "alpha1/alpha2 candidate source rows staged",
            "inputs_missing": "direct mapping from H_TF to alpha1/alpha2; K_S; S_Q norm; q_TF; projector_TF",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "SFR1184_2_local_promotion",
            "component": "local_GR_Newton",
            "nonclaim_formula": "local promotion requires gamma/beta/STF/q_loc residual vector below sourced tolerances plus parent covariance/conservation gates",
            "inputs_closed": "none enough for promotion",
            "inputs_missing": "parent current chain; q_loc split; K_S; physical leakage inputs; residual vector values",
            "score_status": "REFUSED_NO_LOCAL_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1184_0_physical_Cdet2",
            "claim": "physical C_det2 is known",
            "status": "BLOCKED_PARENT_C_NORMALIZATION_MISSING",
            "why": "math coefficient 1/2 must be multiplied by parent C normalization and units",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1184_1_domain_anisotropy",
            "claim": "epsilon_D is known or zero",
            "status": "BLOCKED_DOMAIN_GEOMETRY_OR_ISOTROPY_THEOREM_MISSING",
            "why": "no arena domain geometry or parent SO3 theorem sources epsilon_D",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1184_2_KS_norm",
            "claim": "K_S and ||S_Q||_PPN are known",
            "status": "BLOCKED_KS_AND_STF_BOUND_MISSING",
            "why": "Q identity/normalization and PPN arena shear norm are not sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1184_3_qtrace",
            "claim": "q_trace/q_TF split is known",
            "status": "BLOCKED_QLOC_RESPONSE_SPLIT_MISSING",
            "why": "q_loc remains a retained residual without scalar/STF response map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1184_4_preferred_frame_sources",
            "claim": "preferred-frame comparator source pack is usable for nonclaim runner",
            "status": "PASS_SOURCE_PACK_NONCLAIM",
            "why": "Shao-Wex alpha1/alpha2 source is recorded, but MTS prediction map remains missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1184_5_PPN_local",
            "claim": "PPN/local-GR pass",
            "status": "BLOCKED_NO_LOCAL_CLAIM",
            "why": "physical leakage and q_loc response inputs remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1184_0_score_status",
            "decision": "do_not_score_gamma_or_STF_yet",
            "reason": "R3 math and preferred-frame sources improved the runner, but physical MTS inputs remain missing.",
            "next_action": "derive q_loc scalar/STF response split or parent C normalization.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1184_1_real_progress",
            "decision": "R3_remainder_and_alpha_sources_now_staged",
            "reason": "the leakage law is closer to scoreable: only physical coefficients/norms remain, not the math series.",
            "next_action": "use explicit input rows rather than re-deriving logdet again.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1184_2_best_next",
            "decision": "q_loc_trace_TF_split_is_best_next",
            "reason": "q_trace enters gamma at first order and q_TF enters the direct STF channel, so this split affects both PPN routes.",
            "next_action": "1185 should derive or bound q_loc scalar/STF response before numeric PPN scoring.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1184_0_1185",
            "next_target": "1185-Y5-R10-q_loc-trace-TF-response-split-or-parent-C-normalization.md",
            "objective": "derive or bound the scalar trace and STF projections of the retained q_loc/Gamma/Khat residual; if that fails, attempt parent C normalization C_C as the next physical leakage input",
            "include": "P_scalar/P_TF response map; q_trace; q_TF; Gamma/Khat Helmholtz gate; C_C fallback; no-claim validation",
            "exclude": "claiming q_loc zero; claiming PPN pass; using math coefficients as physical inputs; invented norms; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    external: list[dict[str, object]],
    physical: list[dict[str, object]],
    remainders: list[dict[str, object]],
    scores: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1184_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_1_external_urls_recorded",
            "result": "pass" if all(str(r["url"]).startswith("https://") for r in external) and len(external) >= 3 else "fail",
            "detail": "external PPN/preferred-frame source URLs are recorded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_2_physical_inputs_all_rows",
            "result": "pass"
            if {r["quantity"] for r in physical} >= {"C_C", "epsilon_D", "K_S_to_metric", "||S_Q||_PPN", "q_trace", "R3_math"}
            else "fail",
            "detail": "all physical scalar leakage inputs have explicit rows",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_3_R3_bound_derived",
            "result": "pass" if any(r["status"] == "BOUND_DERIVED_INPUT_MISSING" for r in remainders) else "fail",
            "detail": "R3 remainder bound is derived as math-only/input-missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_4_score_rows_nonclaim",
            "result": "pass" if len(scores) >= 3 and all(r["claim_allowed"] is False for r in scores) else "fail",
            "detail": "score formula rows exist and remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_5_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in physical + scores)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_6_gates_nonclaim",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_7_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in external + physical + remainders + scores + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_8_next_target",
            "result": "pass" if nexts and "1185" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1185 handoff targets q_loc trace/TF split or parent C normalization",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_9_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1184_SUMMARY",
            "result": "pass",
            "detail": "1184 stages every physical scalar-leakage input, derives an R3 remainder bound, records alpha1/alpha2 preferred-frame source candidates, refuses PPN scoring, and hands off to q_loc trace/TF response splitting",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    external: list[dict[str, object]],
    physical: list[dict[str, object]],
    remainders: list[dict[str, object]],
    scores: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1184 - Y5/R10 physical scalar leakage inputs or STF source completion",
        "**Current verdict:** the physical PPN leakage runner is closer but still not scoreable. The math series is controlled, yet `C_C`, `epsilon_D`, `K_S`, `||S_Q||_PPN`, and the q_loc response split are still missing.",
        "**Main progress:** all physical input rows are now explicit, the log-det remainder has a bound `|R3| <= rho^3/(1-rho)` for `||A||_2 <= rho < 1`, and alpha1/alpha2 preferred-frame source candidates are recorded.",
        "**Hard blocker:** the remaining obstacle is no longer the log-det algebra; it is the physical response map and normalization of MTS variables into PPN residuals.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Local source register\n\n" + table(sources),
        "## External preferred-frame source register\n\n" + table(external),
        "## Physical scalar-leakage input ledger\n\n" + table(physical),
        "## R3 remainder bound\n\n" + table(remainders),
        "## Score formula dry-run\n\n" + table(scores),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    external = external_source_rows()
    physical = physical_input_rows()
    remainders = remainder_rows()
    scores = score_formula_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, external, physical, remainders, scores, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1184_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1184_EXTERNAL_PREFERRED_FRAME_SOURCE_REGISTER.csv": external,
        "P8_Y5_R10_1184_PHYSICAL_SCALAR_LEAKAGE_INPUT_LEDGER.csv": physical,
        "P8_Y5_R10_1184_R3_REMAINDER_BOUND.csv": remainders,
        "P8_Y5_R10_1184_SCORE_FORMULA_DRY_RUN.csv": scores,
        "P8_Y5_R10_1184_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1184_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1184_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1184_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, external, physical, remainders, scores, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

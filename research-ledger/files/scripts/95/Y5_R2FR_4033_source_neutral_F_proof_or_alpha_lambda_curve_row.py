from __future__ import annotations

import csv
import hashlib
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main\post-checkpoint-work"
)
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4033-Y5-R2FR-source-neutral-F-proof-or-alpha-lambda-curve-row.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4033_SOURCE_REGISTER.csv",
    "f_decomposition": SOURCE_DIR / "P8_Y5_R2FR_4033_SOURCE_NEUTRAL_F_DECOMPOSITION.csv",
    "neutrality_gate": SOURCE_DIR / "P8_Y5_R2FR_4033_F_NEUTRALITY_GATE.csv",
    "alpha_row": SOURCE_DIR / "P8_Y5_R2FR_4033_ALPHA_LAMBDA_SCALAR_HAIR_ROW.csv",
    "alpha_curve": SOURCE_DIR / "R10_alpha_lambda_curve_MTS_4033_SCALAR_HAIR_TEMPLATE_NONCLAIM.csv",
    "evaluator_cases": SOURCE_DIR / "P8_Y5_R2FR_4033_EVALUATOR_CASES.csv",
    "evaluator_results": SOURCE_DIR / "P8_Y5_R2FR_4033_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4033_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4033_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4033_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4033_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4033_VALIDATION.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def short_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "SRC4033_0_4032_doc",
            "path": "4032-Y5-R2FR-scalar-charge-zero-or-Yukawa-hair-bound-input.md",
            "needle": "source branch has neutral `F` charge",
            "role": "selects source-neutral F as the next exact clause",
        },
        {
            "source_id": "SRC4033_1_4032_charge",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4032_SCALAR_CHARGE_IDENTITY.csv",
            "needle": "int_W F dV",
            "role": "provides Q_phi dependence on integrated F",
        },
        {
            "source_id": "SRC4033_2_4032_zero_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4032_QPHI_ZERO_GATE.csv",
            "needle": "QG4032_1_source_neutrality",
            "role": "defines source-neutrality gate to sharpen",
        },
        {
            "source_id": "SRC4033_3_4032_alpha",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4032_ALPHA_LAMBDA_SCALAR_HAIR_MAP.csv",
            "needle": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "role": "requires alpha(lambda) row if Q_phi survives",
        },
        {
            "source_id": "SRC4033_4_4029_owner",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4029_PHI_OWNER_EULER_DERIVATION.csv",
            "needle": "F:=Gamma_eff+C",
            "role": "defines F in the phi-owner equation",
        },
        {
            "source_id": "SRC4033_5_4026_gamma",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4026_EXPLICIT_GAMMA_DENSITY_CANDIDATE.csv",
            "needle": "gamma:=Gamma_eff-Gamma_0",
            "role": "supplies C=-Gamma0 subtraction route and response field gamma",
        },
        {
            "source_id": "SRC4033_6_gamma_owner",
            "path": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            "needle": "Gamma_eff = Gamma0",
            "role": "supports response/doublet owner candidate, while not proving adoption",
        },
        {
            "source_id": "SRC4033_7_live_alpha_template",
            "path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "needle": "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION",
            "role": "confirms live alpha curve remains blocked",
        },
    ]


def build_source_register(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        full = ROOT / spec["path"]
        text = read_text(full)
        rows.append(
            {
                **spec,
                "absolute_path": str(full),
                "exists": full.exists(),
                "needle_found": spec["needle"] in text,
                "sha256_16": short_hash(full),
                "timestamp_utc": ts,
            }
        )
    return rows


def build_f_decomposition(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decomp_id": "F4033_0_definition",
            "object": "phi source F",
            "formula": "F:=Gamma_eff+C",
            "meaning": "the scalar charge is sourced by the integrated response part of Gamma_eff after subtraction",
            "status": "F_OBJECT_FIXED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decomp_id": "F4033_1_vacuum_subtraction",
            "object": "fixed subtraction",
            "formula": "choose C=-Gamma_0, with Gamma_0 fixed by the vacuum/cosmology branch, not by the local source",
            "meaning": "then F=Gamma_eff-Gamma_0=gamma plus exact/topological remainder",
            "status": "BEST_SOURCE_NEUTRAL_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decomp_id": "F4033_2_response_field",
            "object": "response mode",
            "formula": "gamma:=Gamma_eff-Gamma_0; local fixed branch requires gamma=0 and A_mu=0",
            "meaning": "if the response fields are positive/no-source/no-flux, int_W F dV=0 follows",
            "status": "CONDITIONAL_RESPONSE_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decomp_id": "F4033_3_exact_remainder",
            "object": "exact/topological pieces",
            "formula": "F = gamma + div J_F + F_top + F_source_leak",
            "meaning": "divergence/topological terms are neutral only with fixed/no-flux boundary data",
            "status": "REMAINDER_SPLIT_WRITTEN",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decomp_id": "F4033_4_failure",
            "object": "source leakage",
            "formula": "F_source_leak := F - gamma - div J_F - F_top",
            "meaning": "any unneutralized matter-trace, boundary, or class charge sources Q_phi and activates alpha(lambda)",
            "status": "FAILURE_TERM_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_neutrality_gate(ts: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "FNG4033_0_subtraction",
            "clause": "C=-Gamma_0 is fixed before local source readout and cannot be source-fit",
            "current_result": "written as 4026 required clause, not parent-adopted",
            "int_F_zero": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "FNG4033_1_positive_response",
            "clause": "gamma/A_mu response sector has positive operator, mass gap or admissible zero-mode gauge, and no source charge",
            "current_result": "Gamma_quad candidate has sign/gap contract, not live proof",
            "int_F_zero": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "FNG4033_2_no_linear_matter_source",
            "clause": "F_source_leak has no matter trace, EM stress, boundary class, or source-normalization linear term after EH/Newton routing",
            "current_result": "not proven; this is the main obstruction",
            "int_F_zero": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "FNG4033_3_exact_no_flux",
            "clause": "div J_F and topological parts have zero flux on the source worldtube boundary",
            "current_result": "not signed",
            "int_F_zero": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "FNG4033_4_fixed_branch",
            "clause": "gamma=0 on the compact fixed branch or int_W gamma dV=0 by a positive energy identity",
            "current_result": "conditional route only",
            "int_F_zero": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "FNG4033_5_if_all_signed",
            "clause": "FNG4033_0 through FNG4033_4 all hold",
            "current_result": "conditional theorem: int_W F dV=0 and Q_phi source term vanishes",
            "int_F_zero": True,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_alpha_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "alpha_row_id": "ALPHAROW4033_0_zero_candidate",
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "scalar_phi_hair_zero_candidate_4033",
            "curve_id": "R10_alpha_lambda_curve_MTS_4033_SCALAR_HAIR_TEMPLATE_NONCLAIM",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "0_IF_F_SOURCE_NEUTRAL_AND_QPHI_ZERO_SIGNED",
            "alpha_bound": "not_applicable_until_theorem_zero_signed",
            "alpha_bound_source": "not_applicable_until_theorem_zero_signed",
            "force_law_form": "theorem_zero_candidate",
            "derivation_status": "conditional_theorem_not_parent_signed",
            "formula_reference": "4033::int_W F dV=0 => Q_phi=0 => alpha_phi(lambda)=0",
            "source_file": str(DOC_PATH),
            "assumptions": "C=-Gamma0; no source leak; no flux; fixed response branch",
            "valid_for_claim": "false",
            "notes": "Do not promote to alpha=0 until F-neutrality and Q_phi=0 gates are live-signed.",
            "timestamp_utc": ts,
        },
        {
            "alpha_row_id": "ALPHAROW4033_1_hair_template",
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "scalar_phi_hair_bound_4033",
            "curve_id": "R10_alpha_lambda_curve_MTS_4033_SCALAR_HAIR_TEMPLATE_NONCLAIM",
            "lambda_value": "lambda_phi=1/mu_phi",
            "lambda_units": "m",
            "alpha_predicted": "C_alpha_phi*(Q_phi/M_H)*(q_test/m_test)",
            "alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
            "alpha_bound_source": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv::live_placeholder_blocked; 563 anchors nonclaim",
            "force_law_form": "Yukawa_scalar_hair",
            "derivation_status": "symbolic_Qphi_lambda_nonclaim",
            "formula_reference": "4032::alpha_phi(lambda_phi)=C_alpha_phi*(Q_phi/M_H)*(q_test/m_test)",
            "source_file": str(DOC_PATH),
            "assumptions": "same-frame Hilbert mass M_H; scalar test response not yet universal or numeric",
            "valid_for_claim": "false",
            "notes": "Executable only after Q_phi, lambda_phi, C_alpha_phi, test response, and bound curve are sourced.",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_cases(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4033_0_all_neutral",
            "input_condition": "C=-Gamma0 fixed; response branch zero; no source leak; no exact/topological flux",
            "expected_verdict": "SOURCE_NEUTRAL_F_PROVES_QPHI_ZERO_IF_SIGNED",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4033_1_current",
            "input_condition": "current source hierarchy after 4033",
            "expected_verdict": "F_NEUTRALITY_CONDITIONAL_ALPHA_ROW_STAGED_NONCLAIM",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4033_2_hair",
            "input_condition": "F_source_leak or flux survives",
            "expected_verdict": "SCALAR_HAIR_ALPHA_ROW_SYMBOLIC_NOT_EXECUTABLE",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_results(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4033_0_all_neutral",
            "verdict": "SOURCE_NEUTRAL_F_PROVES_QPHI_ZERO_IF_SIGNED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4033",
            "next_action": "then remove scalar-hair alpha branch and continue boundary/source-current closure",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4033_1_current",
            "verdict": "F_NEUTRALITY_CONDITIONAL_ALPHA_ROW_STAGED_NONCLAIM",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4033",
            "next_action": "4034 should attack F_source_leak/no-linear-matter-source first",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4033_2_hair",
            "verdict": "SCALAR_HAIR_ALPHA_ROW_SYMBOLIC_NOT_EXECUTABLE",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4033",
            "next_action": "if proof fails, source Q_phi, lambda_phi, C_alpha_phi and reviewed bound curve",
            "timestamp_utc": ts,
        },
    ]


def build_decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4033_0_F_route",
            "decision": "source-neutral F route is C=-Gamma0 plus positive response zero plus no linear source leak plus no exact/topological flux",
            "status": "THEOREM_ROUTE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4033_1_current",
            "decision": "current corpus has not live-signed F neutrality; do not set Q_phi or alpha(lambda) to zero",
            "status": "PRIVATE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4033_2_alpha_row",
            "decision": "stage scalar-hair alpha(lambda) rows as nonclaim templates so the fallback is executable-shaped",
            "status": "ALPHA_TEMPLATE_STAGED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4033_3_next",
            "decision": "move to 4034-Y5-R2FR-no-linear-source-leak-proof-or-Qphi-coefficient-fill.md",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_claims(ts: str) -> list[dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4033_0_F_neutral",
            "claim": "int_W F dV=0 in the live parent theory",
            "allowed": False,
            "reason": "C=-Gamma0 and positive response route are conditional; no-linear-source-leak is not proven",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4033_1_Qphi_zero",
            "claim": "Q_phi=0",
            "allowed": False,
            "reason": "requires F neutrality plus fixed/no-flux u clauses",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4033_2_alpha_pass",
            "claim": "R10 alpha(lambda) passes",
            "allowed": False,
            "reason": "alpha rows are symbolic/nonclaim and bound curve is not full claim-ready",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4033_3_local_GR",
            "claim": "local-GR branch passes",
            "allowed": False,
            "reason": "scalar/source/boundary/adoption gates remain open",
            "timestamp_utc": ts,
        },
    ]


def build_next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT4033_0",
            "next_doc": "4034-Y5-R2FR-no-linear-source-leak-proof-or-Qphi-coefficient-fill.md",
            "next_script": "scripts/Y5_R2FR_4034_no_linear_source_leak_proof_or_Qphi_coefficient_fill.py",
            "why": "F_source_leak is now the first exact obstruction to Q_phi=0",
            "fallback": "if no-linear-source-leak fails, fill Q_phi/lambda_phi/C_alpha_phi coefficients for the staged alpha curve",
            "timestamp_utc": ts,
        }
    ]


def build_status(ts: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS4033_0",
            "checkpoint": "4033",
            "headline": "source-neutral F route sharpened and scalar-hair alpha(lambda) rows staged nonclaim",
            "verdict": "F_NEUTRALITY_CONDITIONAL_ALPHA_ROW_STAGED_NONCLAIM",
            "claim_allowed": False,
            "formalization_workbench_modified": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: list[dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    return f"""# 4033 - Source Neutral F Proof Or Alpha Lambda Curve Row

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4033 sharpens the `Q_phi=0` route. Since

`F:=Gamma_eff+C`,

the clean subtraction is

`C=-Gamma_0`,

so

`F=Gamma_eff-Gamma_0=gamma`

up to exact/topological and source-leak pieces. The source-neutral route is therefore:

`F = gamma + div J_F + F_top + F_source_leak`.

If `gamma=0` on the compact fixed branch, `div J_F` has zero flux, `F_top` carries no local source charge, and `F_source_leak=0`, then

`int_W F dV=0`.

Combined with the 4032 identity, this kills the source term in `Q_phi`.

## What Did Not Close

The current corpus has not yet signed the hardest clause:

`F_source_leak=0`.

That means we still cannot claim `Q_phi=0`, R10 silence, or local-GR passage.

## Alpha Lambda Fallback

4033 stages a nonclaim scalar-hair curve file:

`source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_4033_SCALAR_HAIR_TEMPLATE_NONCLAIM.csv`.

The live symbolic row is

`alpha_phi(lambda_phi)=C_alpha_phi*(Q_phi/M_H)*(q_test/m_test)`.

It remains invalid for claim until `Q_phi`, `lambda_phi`, `C_alpha_phi`, test response, and a reviewed alpha-bound curve are sourced.

## Current Verdict

- Current evaluator result: `F_NEUTRALITY_CONDITIONAL_ALPHA_ROW_STAGED_NONCLAIM`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4033`.
- Source needles found: `{found}/{len(sources)}`.

## Next Target

- `4034-Y5-R2FR-no-linear-source-leak-proof-or-Qphi-coefficient-fill.md`
- `scripts/Y5_R2FR_4034_no_linear_source_leak_proof_or_Qphi_coefficient_fill.py`
"""


def add_validation(rows: list[dict[str, object]], check_id: str, passed: bool, detail: str, ts: str) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts})


def build_validation_rows(
    ts: str,
    sources: list[dict[str, object]],
    decomp: list[dict[str, object]],
    gates: list[dict[str, object]],
    alpha_rows: list[dict[str, object]],
    results: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_target: list[dict[str, object]],
    compile_ok: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    decomp_ids = {str(row["decomp_id"]) for row in decomp}
    gate_ids = {str(row["gate_id"]) for row in gates}
    alpha_ids = {str(row["alpha_row_id"]) for row in alpha_rows}
    verdicts = {str(row["verdict"]) for row in results}

    add_validation(rows, "VAL4033_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", ts)
    add_validation(rows, "VAL4033_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found", ts)
    add_validation(rows, "VAL4033_02_F_definition", "F4033_0_definition" in decomp_ids, "F definition row present", ts)
    add_validation(rows, "VAL4033_03_subtraction", "F4033_1_vacuum_subtraction" in decomp_ids, "C=-Gamma0 route row present", ts)
    add_validation(rows, "VAL4033_04_failure_term", "F4033_4_failure" in decomp_ids, "F_source_leak retained row present", ts)
    add_validation(rows, "VAL4033_05_no_linear_gate", "FNG4033_2_no_linear_matter_source" in gate_ids, "no-linear-source-leak gate present", ts)
    add_validation(rows, "VAL4033_06_all_signed_gate", "FNG4033_5_if_all_signed" in gate_ids, "all-signed F-neutrality gate present", ts)
    add_validation(rows, "VAL4033_07_alpha_zero_row", "ALPHAROW4033_0_zero_candidate" in alpha_ids, "zero candidate alpha row present", ts)
    add_validation(rows, "VAL4033_08_alpha_hair_row", "ALPHAROW4033_1_hair_template" in alpha_ids, "hair alpha row present", ts)
    add_validation(rows, "VAL4033_09_alpha_file_written", OUTPUTS["alpha_curve"].exists(), "nonclaim alpha curve file written", ts)
    add_validation(rows, "VAL4033_10_alpha_nonclaim", all(str(row["valid_for_claim"]).lower() == "false" for row in alpha_rows), "all alpha rows invalid for claim", ts)
    add_validation(rows, "VAL4033_11_current_verdict", "F_NEUTRALITY_CONDITIONAL_ALPHA_ROW_STAGED_NONCLAIM" in verdicts, "current evaluator verdict present", ts)
    add_validation(rows, "VAL4033_12_no_claims", all(str(row.get("allowed", "False")) == "False" for row in claims), "all claim gates remain false", ts)
    add_validation(rows, "VAL4033_13_next_decision", any("4034" in str(row["decision"]) for row in decisions), "4034 next decision present", ts)
    add_validation(rows, "VAL4033_14_next_target", bool(next_target and "4034" in str(next_target[0]["next_doc"])), "next target row present", ts)
    add_validation(rows, "VAL4033_15_doc_written", DOC_PATH.exists() and "What Actually Moved" in read_text(DOC_PATH), "checkpoint doc written", ts)
    add_validation(rows, "VAL4033_16_no_formalization_output", "formalization-workbench" not in str(DOC_PATH) and all("formalization-workbench" not in str(path) for path in OUTPUTS.values()), "no output targets formalization-workbench", ts)
    add_validation(rows, "VAL4033_17_script_compiles", compile_ok, "script compiles", ts)
    add_validation(rows, "VAL4033_18_private_nonclaim", all(str(row.get("valid_for_claim", "False")) == "False" for row in decomp + gates + decisions), "all theorem/gate rows remain nonclaim", ts)
    return rows


def main() -> None:
    ts = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = build_source_register(ts)
    decomp = build_f_decomposition(ts)
    gates = build_neutrality_gate(ts)
    alpha_rows = build_alpha_rows(ts)
    cases = build_evaluator_cases(ts)
    results = build_evaluator_results(ts)
    decisions = build_decisions(ts)
    claims = build_claims(ts)
    next_target = build_next_target(ts)
    status = build_status(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["f_decomposition"], decomp)
    write_csv(OUTPUTS["neutrality_gate"], gates)
    write_csv(OUTPUTS["alpha_row"], alpha_rows)
    write_csv(OUTPUTS["alpha_curve"], alpha_rows)
    write_csv(OUTPUTS["evaluator_cases"], cases)
    write_csv(OUTPUTS["evaluator_results"], results)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(
        ts,
        sources,
        decomp,
        gates,
        alpha_rows,
        results,
        decisions,
        claims,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4033 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
MICROSCOPE_TEX = ROOT / "source-intake" / "external-sources" / "microscope_2209.15488_source" / "chap9.tex"

DOC = ROOT / "3260-Y5-R2FR-fixed-EM-owner-zero-theorem-or-DD-WEP-bound-runner-under-AX1090.md"

ETA_CENTRAL = -1.5e-15
ETA_STAT = 2.3e-15
ETA_SYST = 1.5e-15
ETA_QUAD = math.sqrt(ETA_STAT**2 + ETA_SYST**2)
ETA_REPORTED_LEVEL = 2.7e-15

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3260_SOURCE_REGISTER.csv",
    "microscope_evidence": OUT / "P8_Y5_R2FR_3260_MICROSCOPE_SOURCE_EVIDENCE_LINES.csv",
    "fixed_zero_audit": OUT / "P8_Y5_R2FR_3260_FIXED_EM_ZERO_THEOREM_AUDIT.csv",
    "bound_inputs": OUT / "P8_Y5_R2FR_3260_MICROSCOPE_DD_BOUND_INPUTS.csv",
    "bound_outputs": OUT / "P8_Y5_R2FR_3260_DD_WEP_BOUND_OUTPUT_NONCLAIM.csv",
    "interpretation": OUT / "P8_Y5_R2FR_3260_BOUND_INTERPRETATION_GUARDS.csv",
    "gates": OUT / "P8_Y5_R2FR_3260_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3260_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3260_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3260_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:280]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def line_hit(path: Path, needle: str) -> tuple[int | None, str]:
    if not path.exists():
        return None, "MISSING_SOURCE"
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            if needle in line:
                return line_number, " ".join(line.strip().split())
    return None, "NO_MATCH"


def float_or_none(value: Any) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def dd_delta_qe() -> float:
    path = OUT / "P8_Y5_R2FR_3259_DD_CALIBRATED_EM_RESIDUAL_VECTOR_NONCLAIM.csv"
    for row in read_csv(path):
        if row.get("residual_id") == "RV3259_TA6V_minus_PtRh10_unit_product":
            value = float_or_none(row.get("Qe_prime_DD"))
            if value is None:
                raise ValueError("missing DD delta Qe")
            return value
    raise ValueError("missing RV3259_TA6V_minus_PtRh10_unit_product")


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3260_3259_handoff",
            ROOT / "3259-Y5-R2FR-parent-alpha-map-owner-or-DD-comparator-demotion-under-AX1090.md",
            "3259 selected fixed-EM zero theorem or DD WEP bound runner",
            ["NEXT3259_0_3260", "DeltaQ'_e", "B_alpha^MTS"],
        ),
        (
            "SRC3260_3259_residual_vector",
            OUT / "P8_Y5_R2FR_3259_DD_CALIBRATED_EM_RESIDUAL_VECTOR_NONCLAIM.csv",
            "DD-calibrated Ti/Pt EM residual vector",
            ["RV3259_TA6V_minus_PtRh10_unit_product", "-1.982376296670e-03"],
        ),
        (
            "SRC3260_3259_parent_audit",
            OUT / "P8_Y5_R2FR_3259_PARENT_ALPHA_OWNER_AUDIT.csv",
            "parent alpha owner clauses",
            ["AUD3259_0_EM_owner", "AUD3259_1_no_counterterm"],
        ),
        (
            "SRC3260_1055_parent_contract",
            OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "fixed EM owner candidate",
            ["PAC1055_1_EM_owner", "Lie_v ell_EM=0"],
        ),
        (
            "SRC3260_1397_unique_F2",
            OUT / "P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv",
            "unique F2/no counterterm audit",
            ["UMF1397_7_current_verdict", "lambda_A"],
        ),
        (
            "SRC3260_MICROSCOPE_tex",
            MICROSCOPE_TEX,
            "MICROSCOPE final Ti/Pt WEP result source",
            ["eta({\\rm{Ti, Pt}})", "2.7\\times{}10^{-15}", "platinum  and titanium alloys"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def microscope_evidence_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "MIC3260_abstract_result",
            "\\eta({\\rm{Ti, Pt}}) =[-1.5\\pm{}2.3{\\rm (stat)}\\pm{}1.5{\\rm (syst)}] \\times{}10^{-15}",
            "central Ti/Pt WEP result with statistical/systematic uncertainties",
        ),
        (
            "MIC3260_reported_level",
            "2.7\\times{}10^{-15}",
            "reported combined no-violation sensitivity level",
        ),
        (
            "MIC3260_materials",
            "made from platinum  and titanium alloys",
            "source confirms Ti/Pt material pair in the reported test",
        ),
        (
            "MIC3260_material_composition_PtRh",
            "The PtRh10 platinum-rhodium alloy contains 90\\% by mass of Pt",
            "source confirms PtRh10 composition context",
        ),
        (
            "MIC3260_material_composition_TA6V",
            "SUEP’s outer test-mass is made of 90\\% titanium",
            "source confirms TA6V composition context",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for evidence_id, needle, role in specs:
        line_number, text = line_hit(MICROSCOPE_TEX, needle)
        rows.append(
            {
                "evidence_id": evidence_id,
                "source_path": str(MICROSCOPE_TEX),
                "line_number": line_number if line_number is not None else "NO_MATCH",
                "text_excerpt": text,
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def fixed_zero_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "zero_clause_id": "ZEM3260_0_parent_EM_owner",
            "required_clause": "observed EM connection and kinetic normalization fixed by parent representation/topological data",
            "source_anchor": "PAC1055_1_EM_owner",
            "current_status": "CANDIDATE_PRESENT",
            "effect": "supports Lie_v alpha_EM=0 if combined with no-counterterm/readout/no-vertex clauses",
            "zero_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "zero_clause_id": "ZEM3260_1_no_F2_counterterm",
            "required_clause": "no independent lambda_A F_Q^2 or f(X)F_Q^2 term",
            "source_anchor": "UMF1397_7_current_verdict",
            "current_status": "FAILS_CURRENT_CORPUS_WHILE_DELTA_S_LAMBDA_ALLOWED",
            "effect": "blocks fixed-EM zero theorem until operator domain is closed",
            "zero_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "zero_clause_id": "ZEM3260_2_readout_descent",
            "required_clause": "Hodge/coframe/hbar*c/readout factors quotient-fixed",
            "source_anchor": "REM1400_2_readout",
            "current_status": "CONDITIONAL_UNSIGNED",
            "effect": "prevents alpha drift through unit/readout changes",
            "zero_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "zero_clause_id": "ZEM3260_3_no_extra_matter_alpha_vertex",
            "required_clause": "no hidden alpha/mass/binding vertex after quotient",
            "source_anchor": "AUD3259_3_no_extra_matter_vertex",
            "current_status": "CONDITIONAL_UNSIGNED",
            "effect": "would set Delta r_AB^EM=0",
            "zero_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "zero_clause_id": "ZEM3260_4_verdict",
            "required_clause": "all fixed-EM zero clauses signed",
            "source_anchor": "ZEM3260_0..3",
            "current_status": "ZERO_THEOREM_NOT_CLAIMED",
            "effect": "use DD WEP bound branch as fallback",
            "zero_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    delta = dd_delta_qe()
    return [
        {
            "input_id": "BIN3260_0_eta_central",
            "quantity": "eta_TiPt_central",
            "value": f"{ETA_CENTRAL:.12e}",
            "units": "dimensionless",
            "source": str(MICROSCOPE_TEX),
            "line_anchor": "MIC3260_abstract_result",
            "valid_for_claim": "false",
        },
        {
            "input_id": "BIN3260_1_eta_stat",
            "quantity": "eta_TiPt_stat_uncertainty",
            "value": f"{ETA_STAT:.12e}",
            "units": "dimensionless",
            "source": str(MICROSCOPE_TEX),
            "line_anchor": "MIC3260_abstract_result",
            "valid_for_claim": "false",
        },
        {
            "input_id": "BIN3260_2_eta_syst",
            "quantity": "eta_TiPt_syst_uncertainty",
            "value": f"{ETA_SYST:.12e}",
            "units": "dimensionless",
            "source": str(MICROSCOPE_TEX),
            "line_anchor": "MIC3260_abstract_result",
            "valid_for_claim": "false",
        },
        {
            "input_id": "BIN3260_3_eta_quad_level",
            "quantity": "eta_TiPt_quadrature_uncertainty",
            "value": f"{ETA_QUAD:.12e}",
            "units": "dimensionless",
            "source": "sqrt(stat^2+syst^2)",
            "line_anchor": "computed_from_MIC3260_abstract_result",
            "valid_for_claim": "false",
        },
        {
            "input_id": "BIN3260_4_eta_reported_level",
            "quantity": "eta_TiPt_reported_no_violation_level",
            "value": f"{ETA_REPORTED_LEVEL:.12e}",
            "units": "dimensionless",
            "source": str(MICROSCOPE_TEX),
            "line_anchor": "MIC3260_reported_level",
            "valid_for_claim": "false",
        },
        {
            "input_id": "BIN3260_5_delta_Qe_DD",
            "quantity": "DeltaQe_DD_TA6V_minus_PtRh10",
            "value": f"{delta:.12e}",
            "units": "dimensionless",
            "source": str(OUT / "P8_Y5_R2FR_3259_DD_CALIBRATED_EM_RESIDUAL_VECTOR_NONCLAIM.csv"),
            "line_anchor": "RV3259_TA6V_minus_PtRh10_unit_product",
            "valid_for_claim": "false",
        },
    ]


def bound_output_rows() -> list[dict[str, Any]]:
    delta = dd_delta_qe()
    abs_delta = abs(delta)
    b_central = ETA_CENTRAL / delta
    b_stat = ETA_STAT / abs_delta
    b_syst = ETA_SYST / abs_delta
    b_quad = ETA_QUAD / abs_delta
    b_reported = ETA_REPORTED_LEVEL / abs_delta
    return [
        {
            "bound_id": "BOUT3260_0_central_fit_product",
            "assumption": "DD-only EM residual; Delta eta_res=0; MICROSCOPE sign convention aligned with TA6V_minus_PtRh10",
            "formula": "B_alpha^MTS_fit = eta_central / DeltaQe_DD",
            "value": f"{b_central:.12e}",
            "units": "dimensionless product beta_source_alpha*b_alpha_EM*tau_WEP",
            "status": "CENTRAL_VALUE_NOT_DETECTION",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BOUT3260_1_stat_product_scale",
            "assumption": "DD-only EM residual",
            "formula": "sigma_stat(B_alpha)=eta_stat/|DeltaQe_DD|",
            "value": f"{b_stat:.12e}",
            "units": "dimensionless product",
            "status": "STAT_SCALE_ONLY",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BOUT3260_2_syst_product_scale",
            "assumption": "DD-only EM residual",
            "formula": "sigma_syst(B_alpha)=eta_syst/|DeltaQe_DD|",
            "value": f"{b_syst:.12e}",
            "units": "dimensionless product",
            "status": "SYST_SCALE_ONLY",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BOUT3260_3_quadrature_product_bound",
            "assumption": "DD-only EM residual and no cancellation by other composition channels",
            "formula": "|B_alpha^MTS| <= sqrt(eta_stat^2+eta_syst^2)/|DeltaQe_DD|",
            "value": f"{b_quad:.12e}",
            "units": "dimensionless product",
            "status": "NONCLAIM_BOUND_SCALE",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BOUT3260_4_reported_level_product_bound",
            "assumption": "DD-only EM residual and no cancellation by other composition channels",
            "formula": "|B_alpha^MTS| <= 2.7e-15/|DeltaQe_DD|",
            "value": f"{b_reported:.12e}",
            "units": "dimensionless product",
            "status": "REPORTED_LEVEL_BOUND_SCALE",
            "valid_for_claim": "false",
        },
    ]


def interpretation_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "GUARD3260_0_product_only",
            "statement": "The MICROSCOPE/DD calculation bounds only B_alpha^MTS=beta_source_alpha*b_alpha_EM*tau_WEP, not each factor separately.",
            "reason": "source normalization, alpha pullback, and WEP readout/tau are still not independently signed.",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "GUARD3260_1_no_cancellation",
            "statement": "The bound is meaningful only for the isolated EM/DD channel or with a no-cancellation theorem across channels.",
            "reason": "light-quark/surface/readout channels could cancel numerically unless parent identity forbids it.",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "GUARD3260_2_fixed_zero_preferred",
            "statement": "The cleaner GR route remains parent fixed-EM zero, not fitting B_alpha small.",
            "reason": "GR/Newton reduction wants derived universality; the bound branch is a fallback empirical leash.",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3260_0_fixed_zero",
            "gate": "fixed-EM owner zero theorem",
            "passed": "false",
            "reason": "no-counterterm/readout/no-extra-vertex clauses remain unsigned",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3260_1_real_WEP_bound_runner",
            "gate": "real MICROSCOPE/DD product bound computed",
            "passed": "true",
            "reason": "Ti/Pt eta source and DD DeltaQe source produce a finite product-bound scale",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3260_2_local_GR",
            "gate": "local GR/Newton/Maxwell claim",
            "passed": "false",
            "reason": "bound is product-only and nonclaim; fixed zero theorem remains unsigned",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3260_0",
            "verdict": "FIXED_ZERO_NOT_CLOSED_DD_BOUND_RUNNER_WORKS",
            "what_moved": "the EM alpha branch is now either a zero-theorem target or a real Ti/Pt WEP product bound at about 1.36e-12 for B_alpha^MTS",
            "meaning": "this does not prove MTS local GR, but it turns the alpha coupling from a vague gap into a testable product with a hard scale",
            "selected_next": "separate beta_source_alpha, b_alpha_EM, and tau_WEP or prove fixed-EM owner zero",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3260_0_3261",
            "selected": "primary",
            "target_doc": "3261-Y5-R2FR-factorize-B_alpha-product-or-sign-fixed-EM-no-counterterm-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3261_factorize_Balpha_product_or_sign_fixed_EM_no_counterterm.py",
            "objective": "Either split B_alpha^MTS into parent alpha pullback, source normalization, and WEP tau factors with real inputs, or close the no-counterterm fixed-EM theorem.",
            "guardrail": "Do not treat the 1.36e-12 product scale as a pass unless the local gate has a required threshold and no-cancellation/source factors are signed.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    source_rows = source_register()
    microscope_rows = microscope_evidence_rows()
    bound_outputs = bound_output_rows()
    reported_bound = next(row for row in bound_outputs if row["bound_id"] == "BOUT3260_4_reported_level_product_bound")
    validations = [
        {
            "check_id": "VAL3260_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3260_1_sources_parse",
            "check": "all cited source CSV/MD/TEX paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3260_2_MICROSCOPE_lines_found",
            "check": "MICROSCOPE evidence lines are found",
            "passed": bool_str(all(row["line_number"] != "NO_MATCH" for row in microscope_rows)),
            "detail": ";".join(f"{row['evidence_id']}:{row['line_number']}" for row in microscope_rows),
        },
        {
            "check_id": "VAL3260_3_outputs_parse",
            "check": "all 3260 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3260_4_bound_numeric",
            "check": "reported-level product bound is finite positive",
            "passed": bool_str(float_or_none(reported_bound["value"]) is not None and math.isfinite(float(reported_bound["value"])) and float(reported_bound["value"]) > 0),
            "detail": reported_bound["value"],
        },
        {
            "check_id": "VAL3260_5_claim_gates_false",
            "check": "no 3260 claim gate allows local-GR/WEP/Maxwell promotion",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3260_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3260_7_overall",
            "check": "3260 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3260_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    microscope = microscope_evidence_rows()
    zero_audit = fixed_zero_audit_rows()
    inputs = bound_input_rows()
    outputs = bound_output_rows()
    reported_bound = next(row for row in outputs if row["bound_id"] == "BOUT3260_4_reported_level_product_bound")
    guards = interpretation_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3260 - Fixed EM owner zero theorem or DD WEP bound runner under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- The fixed-EM zero theorem is still **not** closed: the no-counterterm/readout/no-extra-vertex clauses remain unsigned.
- The fallback DD branch now has a real MICROSCOPE Ti/Pt bound runner.
- With `DeltaQ'_e(TA6V-PtRh10)=-1.982376296670e-3` and the reported MICROSCOPE level `2.7e-15`, the isolated EM branch requires `|B_alpha^MTS| <= {reported_bound["value"]}`.
- This is not a pass/fail claim yet; it is a hard scale for the combined product `B_alpha^MTS=beta_source_alpha*b_alpha_EM*tau_WEP`.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## MICROSCOPE Evidence Lines
{md_table(microscope, ["evidence_id", "line_number", "text_excerpt", "role", "valid_for_claim"])}

## Fixed EM Zero-Theorem Audit
{md_table(zero_audit, ["zero_clause_id", "required_clause", "source_anchor", "current_status", "effect", "zero_signed", "valid_for_claim"])}

## Bound Inputs
{md_table(inputs, ["input_id", "quantity", "value", "units", "line_anchor", "valid_for_claim"])}

## Bound Outputs
{md_table(outputs, ["bound_id", "assumption", "formula", "value", "units", "status", "valid_for_claim"])}

## Interpretation Guards
{md_table(guards, ["guard_id", "statement", "reason", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "meaning", "selected_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_key = {
        "sources": source_register(),
        "microscope_evidence": microscope_evidence_rows(),
        "fixed_zero_audit": fixed_zero_audit_rows(),
        "bound_inputs": bound_input_rows(),
        "bound_outputs": bound_output_rows(),
        "interpretation": interpretation_rows(),
        "gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

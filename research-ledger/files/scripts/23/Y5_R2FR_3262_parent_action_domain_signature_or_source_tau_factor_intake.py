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

DOC = ROOT / "3262-Y5-R2FR-parent-action-domain-signature-or-source-tau-factor-intake-under-AX1090.md"

TAU_READOUT_CENTER = 1.0
TAU_READOUT_HALF_WIDTH = 2.0e-2

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3262_SOURCE_REGISTER.csv",
    "microscope_readout": OUT / "P8_Y5_R2FR_3262_MICROSCOPE_READOUT_FACTOR_EVIDENCE.csv",
    "tau_factorization": OUT / "P8_Y5_R2FR_3262_TAU_WEP_FACTORIZATION.csv",
    "reduced_bound": OUT / "P8_Y5_R2FR_3262_READOUT_REDUCED_PRODUCT_BOUND_NONCLAIM.csv",
    "action_domain": OUT / "P8_Y5_R2FR_3262_PARENT_ACTION_DOMAIN_SIGNATURE_AUDIT.csv",
    "remaining_inputs": OUT / "P8_Y5_R2FR_3262_REMAINING_SOURCE_TAU_INPUTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3262_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3262_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3262_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3262_VALIDATION.csv",
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


def product_bound() -> float:
    path = OUT / "P8_Y5_R2FR_3260_DD_WEP_BOUND_OUTPUT_NONCLAIM.csv"
    for row in read_csv(path):
        if row.get("bound_id") == "BOUT3260_4_reported_level_product_bound":
            value = float_or_none(row.get("value"))
            if value is None:
                raise ValueError("missing product bound value")
            return value
    raise ValueError("missing BOUT3260_4_reported_level_product_bound")


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3262_3261_handoff",
            ROOT / "3261-Y5-R2FR-factorize-B_alpha-product-or-sign-fixed-EM-no-counterterm-under-AX1090.md",
            "3261 selected parent action domain or source tau factor intake",
            ["NEXT3261_0_3262", "tau_WEP", "B_alpha^MTS"],
        ),
        (
            "SRC3262_3261_factor_inputs",
            OUT / "P8_Y5_R2FR_3261_REQUIRED_FACTOR_INPUTS.csv",
            "required factor inputs after product factorization",
            ["REQ3261_2_tau_WEP", "REQ3261_1_beta_source_map"],
        ),
        (
            "SRC3262_3260_bound",
            OUT / "P8_Y5_R2FR_3260_DD_WEP_BOUND_OUTPUT_NONCLAIM.csv",
            "MICROSCOPE/DD product bound",
            ["BOUT3260_4_reported_level_product_bound", "1.362001757454e-12"],
        ),
        (
            "SRC3262_MICROSCOPE_tex",
            MICROSCOPE_TEX,
            "MICROSCOPE measurement model and readout factor source",
            ["delta_x=", "tilde{a}_{c11}", "2\\times{}10^{-2}"],
        ),
        (
            "SRC3262_1228_tau_gate",
            OUT / "P8_Y5_R10_1228_ACCEPTANCE_GATE_MATRIX.csv",
            "official tau gate remains blocked",
            ["ACCEPT1228_4_tau_WEP"],
        ),
        (
            "SRC3262_1899_wep_pack",
            OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
            "source/readout/tau WEP input pack",
            ["WIP1899_5_force_map", "WIP1899_6_tau_wep"],
        ),
        (
            "SRC3262_1397_unique_F2",
            OUT / "P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv",
            "parent action domain/no-counterterm audit",
            ["UMF1397_2_operator_basis_uniqueness", "UMF1397_7_current_verdict"],
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


def microscope_readout_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "MRF3262_0_delta_eta",
            "\\delta(2,1)=m_{\\rm{G_2}}/m_{\\rm{I_2}}",
            "MICROSCOPE identifies the differential mass-ratio parameter with the Eotvos parameter up to sign convention.",
        ),
        (
            "MRF3262_1_x_readout",
            "\\delta_x=\\tilde{a}_{c11} \\delta \\simeq \\delta",
            "MICROSCOPE X-axis estimated readout is the calibrated factor multiplying the Eotvos parameter.",
        ),
        (
            "MRF3262_2_readout_tolerance",
            "\\vert\\tilde{a}_{c11}-1\\vert <2\\times{}10^{-2}",
            "readout calibration factor is within two percent of unity.",
        ),
        (
            "MRF3262_3_corrected_model",
            "\\Gamma^{(d)}_{x, {\\rm corr}}=\\tilde{b}_x^{'(d)}+\\delta_x g_x",
            "corrected differential acceleration model carries delta_x as the EP coefficient.",
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


def tau_factorization_rows() -> list[dict[str, Any]]:
    tau_min = TAU_READOUT_CENTER - TAU_READOUT_HALF_WIDTH
    tau_max = TAU_READOUT_CENTER + TAU_READOUT_HALF_WIDTH
    return [
        {
            "tau_id": "TAU3262_0_decomposition",
            "factor": "tau_WEP",
            "formula": "tau_WEP = tau_readout_X * tau_source_profile * tau_channel_projection",
            "source_status": "DECOMPOSITION_DEFINED",
            "numeric_status": "tau_readout_X bounded; source_profile/channel_projection missing",
            "valid_for_claim": "false",
        },
        {
            "tau_id": "TAU3262_1_readout_X",
            "factor": "tau_readout_X",
            "formula": "tau_readout_X = tilde(a)_c11",
            "source_status": "MICROSCOPE_SOURCE_BACKED",
            "numeric_status": f"{tau_min:.12e} <= tau_readout_X <= {tau_max:.12e}",
            "valid_for_claim": "false",
        },
        {
            "tau_id": "TAU3262_2_source_profile",
            "factor": "tau_source_profile",
            "formula": "projection of MTS source residual onto Earth/orbit/source-worldtube profile",
            "source_status": "WIP1899_1/2/5 remain missing",
            "numeric_status": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "tau_id": "TAU3262_3_channel_projection",
            "factor": "tau_channel_projection",
            "formula": "projection of selected EM/DD residual onto the MICROSCOPE fitted EP channel after nuisance/correction model",
            "source_status": "official arrays or exact parent reduction still required",
            "numeric_status": "MISSING",
            "valid_for_claim": "false",
        },
    ]


def reduced_bound_rows() -> list[dict[str, Any]]:
    bound = product_bound()
    tau_min = TAU_READOUT_CENTER - TAU_READOUT_HALF_WIDTH
    tau_max = TAU_READOUT_CENTER + TAU_READOUT_HALF_WIDTH
    remaining_bound_worst = bound / tau_min
    remaining_bound_center = bound / TAU_READOUT_CENTER
    return [
        {
            "bound_id": "RB3262_0_full_product",
            "quantity": "|beta_source_alpha*b_alpha_EM*tau_WEP|",
            "formula": "from 3260 MICROSCOPE/DD runner",
            "value": f"{bound:.12e}",
            "status": "REAL_PRODUCT_BOUND",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "RB3262_1_readout_factor",
            "quantity": "tau_readout_X",
            "formula": "0.98 <= tau_readout_X <= 1.02",
            "value": f"[{tau_min:.12e},{tau_max:.12e}]",
            "status": "SOURCE_BACKED_READOUT_SUBFACTOR",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "RB3262_2_remaining_product_worst",
            "quantity": "|beta_source_alpha*b_alpha_EM*tau_source_profile*tau_channel_projection|",
            "formula": "B_bound/min(|tau_readout_X|)",
            "value": f"{remaining_bound_worst:.12e}",
            "status": "READOUT_REDUCED_PRODUCT_BOUND",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "RB3262_3_remaining_product_center",
            "quantity": "center readout normalization",
            "formula": "B_bound/1",
            "value": f"{remaining_bound_center:.12e}",
            "status": "DEBUG_CENTER_NOT_CLAIM",
            "valid_for_claim": "false",
        },
    ]


def action_domain_rows() -> list[dict[str, Any]]:
    return [
        {
            "domain_id": "ADS3262_0_parent_only_domain",
            "signature_target": "forbid quotient-only Maxwell counterterm",
            "exact_condition": "S_parent is varied upstairs and Allowed_2der(parent,U(1)_Q) contains only parent curvature-norm subblocks",
            "current_status": "CONDITIONAL_FROM_1397_NOT_SIGNED",
            "if_signed": "lambda_A=0, advancing fixed-EM zero route",
            "valid_for_claim": "false",
        },
        {
            "domain_id": "ADS3262_1_readout_boundary_silence",
            "signature_target": "readout/coframe/Hodge cannot generate F_Q^2 coefficient drift",
            "exact_condition": "quotient-fixed readout and boundary projection add no independent Maxwell kinetic density",
            "current_status": "CONDITIONAL_UNSIGNED",
            "if_signed": "rho_readout=0 for alpha branch",
            "valid_for_claim": "false",
        },
        {
            "domain_id": "ADS3262_2_current_verdict",
            "signature_target": "fixed EM no-counterterm chain",
            "exact_condition": "ADS3262_0 and ADS3262_1 plus fixed N_Q/C_P",
            "current_status": "NOT_CLOSED_USE_TAU_INTAKE_PROGRESS",
            "if_signed": "b_alpha_EM=0; DD bound branch becomes unnecessary for EM local residual",
            "valid_for_claim": "false",
        },
    ]


def remaining_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "RIN3262_0_source_profile",
            "missing_piece": "tau_source_profile",
            "needed_source": "Earth/source stress, mass-density, or parent theorem reducing source to calibrated point-source profile",
            "current_anchor": "WIP1899_1_source_worldtube_profile;WIP1899_2_source_composition",
            "status": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "input_id": "RIN3262_1_channel_projection",
            "missing_piece": "tau_channel_projection",
            "needed_source": "official MICROSCOPE arrays or exact equivalent showing fitted EP channel projection",
            "current_anchor": "WIP1899_4_readout_arrays;ACCEPT1228_4_tau_WEP",
            "status": "PARTIAL_READOUT_FACTOR_ONLY",
            "valid_for_claim": "false",
        },
        {
            "input_id": "RIN3262_2_beta_source",
            "missing_piece": "beta_source_alpha",
            "needed_source": "same-owner current/source theorem or numeric force normalization",
            "current_anchor": "PAC990_4_source_charge;REM1400_4_beta_source_alpha",
            "status": "MISSING",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3262_0_readout_subfactor",
            "gate": "MICROSCOPE readout subfactor sourced",
            "passed": "true",
            "reason": "tilde(a)_c11 is sourced within 2 percent of unity",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3262_1_full_tau",
            "gate": "full tau_WEP sourced",
            "passed": "false",
            "reason": "source_profile and channel_projection factors remain missing",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3262_2_parent_action_domain",
            "gate": "parent action domain forbids quotient-only F_Q^2 counterterm",
            "passed": "false",
            "reason": "operator-domain signature remains conditional",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3262_3_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "one readout subfactor does not close source coupling or fixed EM theorem",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3262_0",
            "verdict": "READOUT_SUBFACTOR_SOURCED_FULL_TAU_NOT_CLOSED",
            "what_moved": "tau_WEP is no longer a single black box: tau_readout_X is sourced as 0.98..1.02 from MICROSCOPE",
            "new_bound": "remaining product |beta_source_alpha*b_alpha_EM*tau_source_profile*tau_channel_projection| <= 1.389797711688e-12",
            "best_next": "fill source_profile/channel_projection or sign parent action no-counterterm domain",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3262_0_3263",
            "selected": "primary",
            "target_doc": "3263-Y5-R2FR-source-profile-channel-projection-or-parent-domain-lock-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3263_source_profile_channel_projection_or_parent_domain_lock.py",
            "objective": "Either source the MICROSCOPE source_profile/channel_projection tau factors, or lock the parent-only action domain that removes lambda_A.",
            "guardrail": "Do not promote the 0.98..1.02 readout subfactor to full tau_WEP.",
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
    readout_rows = microscope_readout_rows()
    reduced = reduced_bound_rows()
    worst = next(row for row in reduced if row["bound_id"] == "RB3262_2_remaining_product_worst")
    expected = product_bound() / (TAU_READOUT_CENTER - TAU_READOUT_HALF_WIDTH)
    validations = [
        {
            "check_id": "VAL3262_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3262_1_sources_parse",
            "check": "all cited source CSV/MD/TEX paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3262_2_readout_lines_found",
            "check": "MICROSCOPE readout evidence lines are found",
            "passed": bool_str(all(row["line_number"] != "NO_MATCH" for row in readout_rows)),
            "detail": ";".join(f"{row['evidence_id']}:{row['line_number']}" for row in readout_rows),
        },
        {
            "check_id": "VAL3262_3_outputs_parse",
            "check": "all 3262 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3262_4_reduced_bound_numeric",
            "check": "readout-reduced remaining product bound matches B/0.98",
            "passed": bool_str(abs(float(worst["value"]) - expected) <= expected * 1e-12),
            "detail": worst["value"],
        },
        {
            "check_id": "VAL3262_5_claim_gates_false",
            "check": "no 3262 claim gate allows local-GR/WEP/Maxwell promotion",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3262_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3262_7_overall",
            "check": "3262 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3262_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    readout = microscope_readout_rows()
    tau_rows = tau_factorization_rows()
    bounds = reduced_bound_rows()
    action_domain = action_domain_rows()
    remaining = remaining_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    worst_bound = next(row for row in bounds if row["bound_id"] == "RB3262_2_remaining_product_worst")["value"]
    content = f"""# 3262 - Parent action domain signature or source tau factor intake under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3262` sources a real MICROSCOPE readout subfactor: `tau_readout_X = tilde(a)_c11`, with `0.98 <= tau_readout_X <= 1.02`.
- This does **not** close full `tau_WEP`; it splits it into `tau_readout_X * tau_source_profile * tau_channel_projection`.
- Using the sourced lower bound `tau_readout_X >= 0.98`, the remaining product obeys `|beta_source_alpha*b_alpha_EM*tau_source_profile*tau_channel_projection| <= {worst_bound}`.
- Parent action domain/no-counterterm is still conditional; the fixed-EM zero route remains the cleanest theorem path.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## MICROSCOPE Readout Evidence
{md_table(readout, ["evidence_id", "line_number", "text_excerpt", "role", "valid_for_claim"])}

## Tau WEP Factorization
{md_table(tau_rows, ["tau_id", "factor", "formula", "source_status", "numeric_status", "valid_for_claim"])}

## Readout-Reduced Product Bound
{md_table(bounds, ["bound_id", "quantity", "formula", "value", "status", "valid_for_claim"])}

## Parent Action Domain Signature Audit
{md_table(action_domain, ["domain_id", "signature_target", "exact_condition", "current_status", "if_signed", "valid_for_claim"])}

## Remaining Source/Tau Inputs
{md_table(remaining, ["input_id", "missing_piece", "needed_source", "current_anchor", "status", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "new_bound", "best_next", "valid_for_claim"])}

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
        "microscope_readout": microscope_readout_rows(),
        "tau_factorization": tau_factorization_rows(),
        "reduced_bound": reduced_bound_rows(),
        "action_domain": action_domain_rows(),
        "remaining_inputs": remaining_input_rows(),
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

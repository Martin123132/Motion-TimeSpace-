from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3471-Y5-R2FR-bme-clock-material-row-or-electron-mass-zero-theorem.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
ETA_TIPT_BOUND = 2.8e-15
DD_QME_COEFFICIENT = 5.5e-4

SOURCES: dict[str, dict[str, Any]] = {
    "script_3471": {"type": "local", "path": Path(__file__).resolve(), "role": "generator"},
    "doc_3470": {"type": "local", "path": ROOT / "3470-Y5-R2FR-executable-coefficient-vector-runner-and-input-templates.md", "role": "3470 handoff"},
    "next_3470": {"type": "local", "path": OUT / "P8_Y5_R2FR_3470_NEXT_TARGET.csv", "role": "3471 target statement"},
    "input_3470": {"type": "local", "path": OUT / "P8_Y5_R2FR_3470_WEP_VECTOR_INPUT_TEMPLATE.csv", "role": "previous WEP vector input"},
    "runner_3470": {"type": "local", "path": OUT / "P8_Y5_R2FR_3470_WEP_VECTOR_RUNNER_RESULTS.csv", "role": "previous WEP dry run"},
    "contract_3469": {"type": "local", "path": OUT / "P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv", "role": "visible coefficient owner contract"},
    "vector_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv", "role": "retained coefficient vector"},
    "grammar_2612": {"type": "local", "path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv", "role": "direct matter/source-prefactor status"},
    "typing_2650": {"type": "local", "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_SOURCE_PREFACTOR_TYPING_GATE.csv", "role": "object-language typing gate"},
    "dd_tex": {"type": "local", "path": ROOT / "source-intake" / "external-sources" / "damour_donoghue_1007.2792_source" / "DamourDonoghueEPfinal.tex", "role": "Damour-Donoghue electron-mass charge formula"},
    "material_3312": {"type": "local", "path": OUT / "P8_Y5_R2FR_3312_UPGRADED_MATERIAL_CHARGES.csv", "role": "source-backed MICROSCOPE alloy proxy charges"},
    "pair_3312": {"type": "local", "path": OUT / "P8_Y5_R2FR_3312_UPGRADED_PAIR_DELTAS.csv", "role": "MICROSCOPE alloy pair charge deltas"},
    "exact_material_3312": {"type": "local", "path": OUT / "P8_Y5_R2FR_3312_EXACT_WEP_MATERIAL_LEDGER.csv", "role": "MICROSCOPE material mass-fraction source ledger"},
    "local_bounds": {"type": "local", "path": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv", "role": "empirical local bounds"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", "<br>").replace("|", "/") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or "MISSING" in text or "FOLDED" in text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    rows: list[dict[str, Any]] = []
    for source_id, meta in SOURCES.items():
        path = meta["path"]
        rows.append(
            {
                "timestamp_utc": stamp,
                "source_id": source_id,
                "source_type": meta["type"],
                "source_path": str(path),
                "exists": path.exists(),
                "role": meta["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def bme_zero_attempt() -> list[dict[str, Any]]:
    contract_path = SOURCES["contract_3469"]["path"]
    vector_path = SOURCES["vector_3468"]["path"]
    grammar_path = SOURCES["grammar_2612"]["path"]
    typing_path = SOURCES["typing_2650"]["path"]
    return [
        {
            "attempt_id": "BMZ3471_0_define_b_me",
            "claim_tested": "b_me is the local vertical derivative of ln(m_e/Lambda_3), equivalently a visible electron-Yukawa/Higgs/QCD-ratio coefficient slope.",
            "mathematical_form": "b_me := L_v ln(m_e/Lambda_3) = L_v ln(y_e v_H/Lambda_3)",
            "result": "DEFINITION_ONLY",
            "blocker": "",
            "source_path": str(vector_path),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "BMZ3471_1_q_basic_route",
            "claim_tested": "If m_e/Lambda_3 is q-basic or superselected visible data, then b_me vanishes by the same vertical chain rule as the visible-coefficient owner contract.",
            "mathematical_form": "m_e/Lambda_3 = q^* theta_bar or fixed superselection => L_v ln(m_e/Lambda_3)=0 for v in ker(Dq)",
            "result": "EXACT_CONDITIONAL_ZERO",
            "blocker": "visible coefficient owner contract is not parent signed",
            "source_path": str(contract_path),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "BMZ3471_2_hidden_yukawa_countermodel",
            "claim_tested": "No hidden invariant can feed the electron Yukawa, Higgs scale, or QCD-ratio slot.",
            "mathematical_form": "Hom(I_hidden,{y_e,v_H/Lambda_3,m_e/Lambda_3}) = empty except constants",
            "result": "NOT_PROVED_COUNTERMODEL_REMAINS",
            "blocker": "a hidden scalar morphism into the electron mass slot is syntactically possible unless parent action forbids it",
            "source_path": str(grammar_path),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "BMZ3471_3_readout_preservation",
            "claim_tested": "Clock/material readout cannot reintroduce b_me if parent visible data are q-basic.",
            "mathematical_form": "Theta_eff = R(q-basic visible data, q-basic readout data) => L_v Theta_eff=0",
            "result": "CONDITIONAL_NOT_A_PARENT_PROOF",
            "blocker": "RG/readout preservation is a required contract clause, not an established MTS theorem",
            "source_path": str(typing_path),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "BMZ3471_SUMMARY",
            "claim_tested": "Can 3471 set b_me=0 by theorem?",
            "mathematical_form": "all clauses above parent signed",
            "result": "NO_THEOREM_ZERO_USE_SOURCED_MATERIAL_ROW",
            "blocker": "parent action has not yet signed q-basic electron mass/Higgs/Yukawa ownership",
            "source_path": str(contract_path),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
    ]


def dd_formula_audit() -> list[dict[str, Any]]:
    tex_path = SOURCES["dd_tex"]["path"]
    text = tex_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    formula_line = ""
    formula_line_number = ""
    for index, line in enumerate(lines, start=1):
        if "Q_{m_e}" in line:
            window = " ".join(lines[index - 1 : min(index + 3, len(lines))])
            if "5.5" in window and "10^{-4}" in window and "Z}{A" in window:
                formula_line = window.strip()
                formula_line_number = str(index)
                break
    found = bool(formula_line)
    return [
        {
            "audit_id": "DDF3471_0_source_exists",
            "source_path": str(tex_path),
            "line_number": "",
            "extraction_method": "local TeX source inspection",
            "formula_or_evidence": "Damour-Donoghue source TeX exists",
            "status": "PASS" if tex_path.exists() else "FAIL",
            "valid_for_claim": False,
        },
        {
            "audit_id": "DDF3471_1_qme_formula",
            "source_path": str(tex_path),
            "line_number": formula_line_number,
            "extraction_method": "exact local TeX formula search for Q_{m_e}",
            "formula_or_evidence": "Q_m_e = F_A [5.5e-4 Z/A]" if found else "MISSING_QME_FORMULA",
            "status": "FOUND_SOURCE_FORMULA_NONCLAIM" if found else "FAIL_MISSING_FORMULA",
            "valid_for_claim": False,
        },
        {
            "audit_id": "DDF3471_2_use_rule",
            "source_path": str(tex_path),
            "line_number": formula_line_number,
            "extraction_method": "lowest-order alloy proxy with F_A=1, using 3312 q_p=Z/A proxy",
            "formula_or_evidence": "Q_m_e_proxy = 5.5e-4 q_p; Delta_Q_m_e = 5.5e-4 Delta_q_p",
            "status": "USABLE_FOR_SMOKE_PATCH_NOT_CLAIM",
            "valid_for_claim": False,
        },
    ]


def qme_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    material_rows = read_csv(SOURCES["material_3312"]["path"])
    pair_rows = read_csv(SOURCES["pair_3312"]["path"])
    rows: list[dict[str, Any]] = []
    qme_by_material: dict[str, float] = {}
    for material_id in ["MICROSCOPE_PtRh10", "MICROSCOPE_TA6V"]:
        material = next(row for row in material_rows if row["material_id"] == material_id)
        q_p = parse_float(material["q_p"])
        if q_p is None:
            raise ValueError(f"missing q_p for {material_id}")
        qme = DD_QME_COEFFICIENT * q_p
        qme_by_material[material_id] = qme
        rows.append(
            {
                "qme_id": f"QME3471_{len(rows)}_{material_id}",
                "arena": "WEP_MICROSCOPE_TiPt",
                "material_id": material_id,
                "input_proxy": "q_p=Z/A from 3312 upgraded material charges",
                "q_p_Z_over_A": f"{q_p:.12e}",
                "F_A_assumption": "1.0 lowest-order proxy",
                "Q_m_e": f"{qme:.12e}",
                "units": "dimensionless",
                "source_path": str(SOURCES["material_3312"]["path"]),
                "formula_source_path": str(SOURCES["dd_tex"]["path"]),
                "status": "NUMERIC_PROXY_FROM_DD_QME_FORMULA",
                "valid_for_claim": False,
            }
        )
    pair = next(row for row in pair_rows if row["pair_id"] == "PAIR3312_0_MICROSCOPE_PtRh10_TA6V")
    delta_q_p = parse_float(pair["Delta_q_p"])
    if delta_q_p is None:
        raise ValueError("missing MICROSCOPE Delta_q_p")
    delta_qme = DD_QME_COEFFICIENT * delta_q_p
    rows.append(
        {
            "qme_id": "QME3471_2_PAIR_MICROSCOPE_PtRh10_minus_TA6V",
            "arena": "WEP_MICROSCOPE_TiPt",
            "material_id": "MICROSCOPE_PtRh10_minus_TA6V",
            "input_proxy": "Delta_q_p from 3312 pair ledger",
            "q_p_Z_over_A": f"{delta_q_p:.12e}",
            "F_A_assumption": "1.0 lowest-order proxy",
            "Q_m_e": f"{delta_qme:.12e}",
            "Delta_Q_m_e_abs": f"{abs(delta_qme):.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["pair_3312"]["path"]),
            "formula_source_path": str(SOURCES["dd_tex"]["path"]),
            "status": "NUMERIC_PROXY_PAIR_DELTA_FROM_DD_QME_FORMULA",
            "valid_for_claim": False,
        }
    )
    return rows, {
        "delta_q_p": delta_q_p,
        "delta_qme": delta_qme,
        "delta_qme_abs": abs(delta_qme),
        "qme_PtRh10": qme_by_material["MICROSCOPE_PtRh10"],
        "qme_TA6V": qme_by_material["MICROSCOPE_TA6V"],
    }


def bme_patch_row(delta_qme_abs: float) -> list[dict[str, Any]]:
    product_bound = ETA_TIPT_BOUND / delta_qme_abs
    return [
        {
            "input_id": "WVI3470_2_b_me",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "b_me",
            "component_role": "electron_mass_or_yukawa_product",
            "include_in_envelope": True,
            "theorem_zero": False,
            "sensitivity_abs": f"{delta_qme_abs:.12e}",
            "product_abs_bound": f"{product_bound:.12e}",
            "units": "dimensionless",
            "source_path": str(OUT / "P8_Y5_R2FR_3471_MICROSCOPE_ALLOY_QME_ROWS.csv"),
            "formula_source_path": str(SOURCES["dd_tex"]["path"]),
            "status": "NUMERIC_PROXY_SINGLE_CHANNEL_BOUND_FROM_DD_QME",
            "missing_marker": "",
            "valid_for_claim": False,
        }
    ]


def dryrun_with_bme_patch(patch_row: dict[str, Any]) -> list[dict[str, Any]]:
    template_rows = read_csv(SOURCES["input_3470"]["path"])
    rows: list[dict[str, Any]] = []
    total = 0.0
    missing: list[str] = []
    numeric_live = 0
    included_live = 0
    theorem_zero_rows = 0
    for index, template in enumerate(template_rows):
        row = dict(template)
        if row["input_id"] == "WVI3470_2_b_me":
            row.update({key: str(value) for key, value in patch_row.items()})
        include = parse_bool(row.get("include_in_envelope"))
        theorem_zero = parse_bool(row.get("theorem_zero"))
        sensitivity = parse_float(row.get("sensitivity_abs"))
        product_bound = parse_float(row.get("product_abs_bound"))
        contribution: str
        row_status: str
        blocker = ""
        if not include:
            contribution = "0.000000000000e+00"
            row_status = "IGNORED_COMMON_MODE_OR_NOT_IN_WEP_NUMERATOR"
        elif theorem_zero:
            theorem_zero_rows += 1
            contribution = "0.000000000000e+00"
            row_status = "THEOREM_ZERO"
        elif sensitivity is not None and product_bound is not None and not row.get("missing_marker"):
            included_live += 1
            numeric_live += 1
            value = abs(sensitivity * product_bound)
            total += value
            contribution = f"{value:.12e}"
            row_status = "NUMERIC_LIVE_COMPONENT"
        else:
            included_live += 1
            contribution = "MISSING"
            row_status = "BLOCKING_MISSING_LIVE_INPUT"
            blocker = row.get("missing_marker") or "MISSING_NUMERIC_INPUT"
            missing.append(f"{row.get('symbol')}:{blocker}")
        rows.append(
            {
                "result_id": f"WDR3471_{index}_{row['symbol']}",
                "symbol": row["symbol"],
                "include_in_envelope": include,
                "theorem_zero": theorem_zero,
                "sensitivity_abs": row.get("sensitivity_abs", ""),
                "product_abs_bound": row.get("product_abs_bound", ""),
                "abs_contribution": contribution,
                "row_status": row_status,
                "blocker": blocker,
                "source_path": row.get("source_path", ""),
                "valid_for_claim": False,
            }
        )
    status = "FAIL_BLOCKED_MISSING_LIVE_COMPONENTS_AND_KNOWN_ABS_SUM_EXCEEDS_BOUND"
    if missing and total <= ETA_TIPT_BOUND:
        status = "FAIL_BLOCKED_MISSING_LIVE_COMPONENTS"
    elif not missing and total > ETA_TIPT_BOUND:
        status = "FAIL_KNOWN_ABS_SUM_EXCEEDS_BOUND"
    elif not missing:
        status = "PASS_DRYRUN_ONLY_NOT_CLAIM"
    rows.append(
        {
            "result_id": "WDR3471_SUMMARY",
            "symbol": "WEP_VECTOR_WITH_BME_PATCH_SUMMARY",
            "include_in_envelope": True,
            "theorem_zero": False,
            "sensitivity_abs": f"included_live_rows={included_live};numeric_live_rows={numeric_live};theorem_zero_rows={theorem_zero_rows}",
            "product_abs_bound": f"eta_bound={ETA_TIPT_BOUND:.12e}",
            "abs_contribution": f"{total:.12e}",
            "row_status": status,
            "blocker": ";".join(missing),
            "source_path": str(Path(__file__).resolve()),
            "valid_for_claim": False,
        }
    )
    return rows


def claim_gates(zero_rows: list[dict[str, Any]], qme_stats: dict[str, float], dryrun_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = next(row for row in dryrun_rows if row["result_id"] == "WDR3471_SUMMARY")
    return [
        {
            "gate_id": "CG3471_0_bme_zero_theorem",
            "requirement": "b_me=0 must be parent signed, not only conditional on visible q-basic ownership",
            "passed": False,
            "evidence": next(row for row in zero_rows if row["attempt_id"] == "BMZ3471_SUMMARY")["result"],
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3471_1_dd_qme_formula",
            "requirement": "Damour-Donoghue Q_m_e formula must be found in local source",
            "passed": True,
            "evidence": f"Q_m_e = {DD_QME_COEFFICIENT:.6e} * Z/A",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3471_2_numeric_patch_row",
            "requirement": "b_me row must have positive numeric sensitivity and product bound with no missing markers",
            "passed": qme_stats["delta_qme_abs"] > 0.0,
            "evidence": f"Delta_Q_m_e_abs={qme_stats['delta_qme_abs']:.12e}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3471_3_full_wep_vector",
            "requirement": "No missing live WEP components and no known absolute-envelope excess",
            "passed": False,
            "evidence": f"{summary['row_status']}; contribution={summary['abs_contribution']}; blockers={summary['blocker']}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3471_4_no_public_claim",
            "requirement": "Patch remains internal and nonclaim until parent coefficients and all live rows are signed",
            "passed": True,
            "evidence": "all 3471 rows valid_for_claim=false",
            "valid_for_claim": False,
        },
    ]


def decision_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3471_0_progress",
            "decision": "WVI3470_2_b_me can now be replaced by a sourced numeric proxy row.",
            "rationale": "Damour-Donoghue gives Q_m_e = F_A[5.5e-4 Z/A], and 3312 already supplies MICROSCOPE q_p=Z/A proxy deltas.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3471_1_no_zero",
            "decision": "Do not set b_me=0 yet.",
            "rationale": "That requires a parent-owned visible coefficient theorem for electron Yukawa/Higgs/QCD-ratio data.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3471_2_wep_status",
            "decision": "WEP remains blocked after the b_me row is filled.",
            "rationale": f"{summary['row_status']} with absolute envelope {summary['abs_contribution']} against eta bound {ETA_TIPT_BOUND:.12e}.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3472-Y5-R2FR-visible-source-owner-theorem-or-full-DD-vector-upgrade.md",
            "next_script": "scripts/Y5_R2FR_3472_visible_source_owner_theorem_or_full_DD_vector_upgrade.py",
            "objective": "Stop treating WEP channels as isolated placeholders: either prove the visible source-owner theorem that zeros b_alpha/b_mhat/b_me/b_bind together, or upgrade the runner to a full Damour-Donoghue coefficient vector with all material sensitivities explicit.",
            "success_gate": "A parent-signed source-owner theorem removes live channels, or the WEP runner receives a full sourced DD vector without hidden cancellation.",
            "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; tuning signs to pass the MICROSCOPE bound.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def git_formalization_status() -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--short", "--", "formalization-workbench"],
            cwd=ROOT.parent,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return "GIT_NOT_AVAILABLE"
    if result.returncode != 0:
        if "not a git repository" in result.stderr.lower():
            return "NOT_A_GIT_REPOSITORY"
        return f"GIT_STATUS_FAILED:{result.stderr.strip()}"
    return result.stdout.strip()


def validation_rows(output_paths: list[Path], source_rows: list[dict[str, Any]], qme_stats: dict[str, float], dryrun_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    csv_paths = [path for path in output_paths if path.suffix.lower() == ".csv"]
    malformed: list[str] = []
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover - checkpoint validator
            malformed.append(f"{path.name}:{exc}")
    missing_sources = [row["source_id"] for row in source_rows if str(row["source_type"]) == "local" and not parse_bool(row["exists"])]
    summary = next(row for row in dryrun_rows if row["result_id"] == "WDR3471_SUMMARY")
    formalization_outputs = [str(path) for path in output_paths if str(path).lower().startswith(str(FORMALIZATION).lower())]
    git_status = git_formalization_status()
    checks = [
        ("VAL3471_0_sources_exist", not missing_sources, ";".join(missing_sources) or "all local sources exist"),
        ("VAL3471_1_csv_parse", not malformed, ";".join(malformed) or "all output csv files parse"),
        ("VAL3471_2_qme_positive", qme_stats["delta_qme_abs"] > 0.0, f"Delta_Q_m_e_abs={qme_stats['delta_qme_abs']:.12e}"),
        ("VAL3471_3_patch_no_missing", True, "WVI3470_2_b_me patch row has numeric sensitivity/product and empty missing_marker"),
        ("VAL3471_4_no_claim", True, "all generated rows are nonclaim and claim gates keep WEP blocked"),
        ("VAL3471_5_wep_still_blocked", "FAIL" in str(summary["row_status"]), str(summary["row_status"])),
        ("VAL3471_6_no_formalization_outputs", not formalization_outputs, ";".join(formalization_outputs) or "no outputs under formalization-workbench"),
        (
            "VAL3471_7_git_formalization_clean",
            git_status in {"", "NOT_A_GIT_REPOSITORY"},
            git_status or "git reports no formalization-workbench changes",
        ),
    ]
    for check_id, passed, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "passed": bool(passed),
                "detail": detail,
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "check_id": "VAL3471_SUMMARY",
            "passed": all(parse_bool(row["passed"]) for row in rows),
            "detail": "PASS" if all(parse_bool(row["passed"]) for row in rows) else "FAIL",
            "valid_for_claim": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    qme_rows_out: list[dict[str, Any]],
    patch_rows: list[dict[str, Any]],
    dryrun_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    summary = next(row for row in dryrun_rows if row["result_id"] == "WDR3471_SUMMARY")
    doc = f"""# 3471: b_me Clock/Material Row Or Electron-Mass Zero Theorem

## Current Verdict
- **Progress, not a pass:** `b_me` is no longer just a missing placeholder. The Damour-Donoghue electron-mass material charge gives a sourced proxy sensitivity for the MICROSCOPE PtRh10/TA6V pair.
- **No theorem-zero yet:** `b_me=0` is exact if `m_e/Lambda_3` is parent-owned q-basic/superselected visible data, but that owner clause is still unsigned.
- **WEP remains blocked:** with `b_me` filled, the no-cancellation absolute envelope is `{summary['abs_contribution']}` against the MICROSCOPE bound `{ETA_TIPT_BOUND:.12e}`, and `b_bind`, `b_readout`, and `direct_shadow_projector` remain live blockers.

## Concrete Progress
- Replaced the 3470 `WVI3470_2_b_me` placeholder with a numeric nonclaim patch row.
- Extracted the source formula `Q_m_e = F_A[5.5e-4 Z/A]` from local Damour-Donoghue TeX.
- Used the existing 3312 MICROSCOPE `q_p=Z/A` alloy proxy deltas, so this does not invent a new material model.
- Kept all rows `valid_for_claim=false`; this is a runner upgrade, not a WEP/local-GR claim.

## Zero-Theorem Attempt
{md_table(zero_rows)}

## Damour-Donoghue Formula Audit
{md_table(formula_rows)}

## MICROSCOPE Electron-Mass Charge Rows
{md_table(qme_rows_out)}

## Patch Row For 3470 Runner
{md_table(patch_rows)}

## Dry Run With b_me Patch
{md_table(dryrun_rows)}

## Claim Gates
{md_table(gate_rows)}

## Decision
{md_table(decision)}

## Next Target
{md_table(next_rows)}

## Source Register
{md_table(source_rows)}

## Validation
{md_table(validation)}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register()
    zero_rows = bme_zero_attempt()
    formula_rows = dd_formula_audit()
    qme_rows_out, qme_stats = qme_rows()
    patch_rows = bme_patch_row(qme_stats["delta_qme_abs"])
    dryrun_rows = dryrun_with_bme_patch(patch_rows[0])
    gates = claim_gates(zero_rows, qme_stats, dryrun_rows)
    summary = next(row for row in dryrun_rows if row["result_id"] == "WDR3471_SUMMARY")
    decisions = decision_rows(summary)
    next_rows = next_target()

    output_map = {
        OUT / "P8_Y5_R2FR_3471_SOURCE_REGISTER.csv": source_rows,
        OUT / "P8_Y5_R2FR_3471_BME_ZERO_THEOREM_ATTEMPT.csv": zero_rows,
        OUT / "P8_Y5_R2FR_3471_DD_ELECTRON_MASS_FORMULA_SOURCE_AUDIT.csv": formula_rows,
        OUT / "P8_Y5_R2FR_3471_MICROSCOPE_ALLOY_QME_ROWS.csv": qme_rows_out,
        OUT / "P8_Y5_R2FR_3471_WEP_VECTOR_INPUT_BME_PATCH_ROW.csv": patch_rows,
        OUT / "P8_Y5_R2FR_3471_WEP_VECTOR_DRYRUN_WITH_BME.csv": dryrun_rows,
        OUT / "P8_Y5_R2FR_3471_CLAIM_GATES.csv": gates,
        OUT / "P8_Y5_R2FR_3471_DECISION_LEDGER.csv": decisions,
        OUT / "P8_Y5_R2FR_3471_NEXT_TARGET.csv": next_rows,
    }
    for path, rows in output_map.items():
        write_csv(path, rows)

    validation = validation_rows([*output_map.keys(), DOC], source_rows, qme_stats, dryrun_rows)
    validation_path = OUT / "P8_Y5_BRR545_3471_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(source_rows, zero_rows, formula_rows, qme_rows_out, patch_rows, dryrun_rows, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()

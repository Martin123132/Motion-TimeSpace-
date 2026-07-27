from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3303-Y5-R2FR-universal-Hilbert-source-check-for-quadratic-amplitudes-under-AX1090.md"

SRC_3302_DOC = ROOT / "3302-Y5-R2FR-quadratic-curvature-finite-coefficient-extraction-and-bound-map-under-AX1090.md"
SRC_3302_MODE = OUT / "P8_Y5_R2FR_3302_LINEARIZED_MODE_MASS_MAP.csv"
SRC_3302_POTENTIAL = OUT / "P8_Y5_R2FR_3302_NEWTON_YUKAWA_POTENTIAL_TEMPLATE.csv"
SRC_3302_DECISION = OUT / "P8_Y5_R2FR_3302_DECISION_LEDGER.csv"
SRC_3302_NEXT = OUT / "P8_Y5_R2FR_3302_NEXT_TARGET.csv"
SRC_3302_VALIDATION = OUT / "P8_Y5_BRR545_3302_VALIDATION.csv"
SRC_3293_HILBERT = OUT / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv"
SRC_3293_LOCAL = OUT / "P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv"
SRC_3294_CONTRACT = OUT / "P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv"
SRC_3294_NEWTON = OUT / "P8_Y5_R2FR_3294_NEWTON_LIMIT_AND_COMMON_G_CALIBRATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3303_SOURCE_REGISTER.csv",
    "contract": OUT / "P8_Y5_R2FR_3303_AMPLITUDE_IMPORT_CONTRACT.csv",
    "evidence": OUT / "P8_Y5_R2FR_3303_HILBERT_SOURCE_EVIDENCE_SCORE.csv",
    "law": OUT / "P8_Y5_R2FR_3303_GENERALIZED_ALPHA_AMPLITUDE_LAW.csv",
    "requirements": OUT / "P8_Y5_R2FR_3303_SOURCE_PROJECTION_REQUIREMENTS.csv",
    "runner": OUT / "P8_Y5_R2FR_3303_AMPLITUDE_INHERITANCE_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3303_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3303_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3303_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3303_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 760) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered_needles):
            hits.append(f"L{line_number}:{compact(line, 400)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3302_DOC, "3302 finite quadratic map", ["Phi(r)", "alpha_0", "alpha_2"]),
        (SRC_3302_MODE, "3302 mode map", ["MODE3302_0_scalar", "MODE3302_1_spin2"]),
        (SRC_3302_POTENTIAL, "3302 potential templates", ["POT3302_0", "POT3302_1"]),
        (SRC_3302_DECISION, "3302 decision", ["DEC3302_1", "pure metric convention"]),
        (SRC_3302_NEXT, "3302 next target", ["universal-Hilbert-source-check", "quadratic amplitudes"]),
        (SRC_3302_VALIDATION, "3302 validation", ["VAL3302_11_overall", "true"]),
        (SRC_3293_HILBERT, "3293 Hilbert source theorem", ["HSSIG3293_0_target", "NOT_PARENT_SIGNED"]),
        (SRC_3293_LOCAL, "3293 local matter coupling", ["common coupling", "Maxwell_stress"]),
        (SRC_3294_CONTRACT, "3294 local GR contract", ["single public metric", "Hilbert source"]),
        (SRC_3294_NEWTON, "3294 Newton/common-G branch", ["G_cal", "Newton"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3303_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "AIC3303_0_pure_metric_branch",
            "clause": "local finite branch is pure metric quadratic gravity: one public metric, Einstein-Hilbert term, and quadratic curvature terms only",
            "needed_for": "import the projector residues that produce +1/3 and -4/3",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AIC3303_1_universal_Hilbert_source",
            "clause": "all matter couples through one Hilbert source T_H_mu_nu from one descended matter action with no post-variation source weights",
            "needed_for": "make scalar and spin-2 modes see the same source tensor as GR",
            "current_status": "EXACT_CONDITIONAL_FROM_3293_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AIC3303_2_same_readout_metric",
            "clause": "the observed metric used by rods, clocks, EM stress, and orbital motion is the same metric whose quadratic curvature operators are diagonalized",
            "needed_for": "avoid disformal/Weyl/readout factors multiplying alpha_0 and alpha_2",
            "current_status": "CONDITIONAL_FROM_3294_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AIC3303_3_canonical_mode_normalization",
            "clause": "linearized scalar and spin-2 modes have the same kinetic normalization and residue signs as the pure metric convention",
            "needed_for": "fix the numerical residues +1/3 and -4/3 rather than arbitrary alpha factors",
            "current_status": "MISSING_PARENT_COEFFICIENT_NORMALIZATION",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AIC3303_4_common_G_calibration",
            "clause": "the massless graviton residue defines the same measured G_cal used to normalize the Yukawa amplitudes",
            "needed_for": "make alpha_0 and alpha_2 dimensionless corrections relative to the Newtonian force",
            "current_status": "CALIBRATION_ALLOWED_NOT_PREDICTIVE",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AIC3303_5_no_screening_or_hidden_source_selector",
            "clause": "no local screening, hidden source selector, species weight, or environmental projector changes the finite-mode coupling relative to the massless graviton",
            "needed_for": "prevent MTS-specific coupling factors from replacing the pure metric amplitudes",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def evidence_score_rows() -> list[dict[str, Any]]:
    source_paths = {
        "AIC3303_0_pure_metric_branch": SRC_3302_DECISION,
        "AIC3303_1_universal_Hilbert_source": SRC_3293_HILBERT,
        "AIC3303_2_same_readout_metric": SRC_3294_CONTRACT,
        "AIC3303_3_canonical_mode_normalization": SRC_3302_DECISION,
        "AIC3303_4_common_G_calibration": SRC_3294_CONTRACT,
        "AIC3303_5_no_screening_or_hidden_source_selector": SRC_3293_LOCAL,
    }
    rows: list[dict[str, Any]] = []
    for contract in contract_rows():
        status = contract["current_status"]
        path = source_paths[contract["clause_id"]]
        passed = status in {"PARENT_SIGNED", "DERIVED_PARENT_SIGNED"}
        rows.append(
            {
                "clause_id": contract["clause_id"],
                "evidence_path": str(path),
                "evidence_status": status,
                "passed_for_amplitude_import": bool_str(passed),
                "evidence_excerpt": evidence_hits(path, ["NOT_PARENT_SIGNED", "G_cal", "Hilbert", "pure metric", "common coupling"]),
                "valid_for_claim": "false",
            }
        )
    return rows


def generalized_alpha_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "ALAW3303_0_scalar",
            "mode": "scalar_R2",
            "pure_metric_value": "+1/3",
            "mts_general_law": "alpha_0 = (1/3) * Z_0 * Xi_0 * U_0",
            "factor_meanings": "Z_0=scalar residue/normalization ratio; Xi_0=Hilbert-source projection overlap; U_0=observed-metric/readout overlap",
            "pure_limit": "Z_0=Xi_0=U_0=1",
            "current_status": "DERIVED_TEMPLATE_NOT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "law_id": "ALAW3303_1_spin2",
            "mode": "massive_spin2_Ricci_Weyl",
            "pure_metric_value": "-4/3",
            "mts_general_law": "alpha_2 = (-4/3) * Z_2 * Xi_2 * U_2",
            "factor_meanings": "Z_2=massive spin-2 residue/normalization ratio; Xi_2=Hilbert-source projection overlap; U_2=observed-metric/readout overlap",
            "pure_limit": "Z_2=Xi_2=U_2=1",
            "current_status": "DERIVED_TEMPLATE_NOT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "law_id": "ALAW3303_2_Newton_reference",
            "mode": "massless_graviton_reference",
            "pure_metric_value": "1",
            "mts_general_law": "G_cal is the measured massless spin-2 coupling; all finite-mode alphas are normalized relative to this reference",
            "factor_meanings": "common G calibration is allowed, but relative finite-mode residues are not hidden in G_cal",
            "pure_limit": "massless reference fixed by Newtonian calibration",
            "current_status": "CALIBRATION_REFERENCE_ONLY",
            "valid_for_claim": "false",
        },
    ]


def requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "REQ3303_0_Z_factors",
            "quantity": "Z_0, Z_2",
            "meaning": "mode residue/canonical normalization relative to pure metric quadratic gravity",
            "how_to_derive": "linearize the parent local kinetic action, diagonalize scalar and massive spin-2 sectors, normalize kinetic terms",
            "failure_mode": "using +1/3 or -4/3 without matching residue normalization",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "REQ3303_1_Xi_factors",
            "quantity": "Xi_0, Xi_2",
            "meaning": "source projection overlap between finite modes and the same Hilbert T_mu_nu that defines Newtonian mass",
            "how_to_derive": "vary the descended matter action with respect to the diagonalized finite modes or project T_H_mu_nu through the mode projectors",
            "failure_mode": "source-only weights, hidden labels, or non-Hilbert current owners modify the finite-mode force",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "REQ3303_2_U_factors",
            "quantity": "U_0, U_2",
            "meaning": "readout overlap from diagonal finite modes to the metric observed by rods, clocks, EM, and orbital matter",
            "how_to_derive": "derive the public metric/readout map and show no Weyl/disformal/screening factor changes the observed potential",
            "failure_mode": "field redefinitions or readout metric split change measured alpha values",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "REQ3303_3_lambdas",
            "quantity": "lambda_0, lambda_2",
            "meaning": "finite mode ranges from parent coefficients",
            "how_to_derive": "extract a_R2/b_Ric/b_W with units and compute m_0,m_2 in the chosen convention",
            "failure_mode": "amplitudes cannot be scored without ranges",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    evidence = evidence_score_rows()
    all_import_clauses = all(row["passed_for_amplitude_import"] == "true" for row in evidence)
    laws = generalized_alpha_law_rows()
    requirements = requirement_rows()
    return [
        {
            "runner_id": "RUN3303_0_import_fixed_amplitudes",
            "test": "all pure-metric import clauses passed",
            "result": "PASS_IMPORT" if all_import_clauses else "REFUSE_IMPORT_USE_GENERAL_ALPHA",
            "detail": ";".join(f"{row['clause_id']}={row['passed_for_amplitude_import']}" for row in evidence),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3303_1_general_law_ready",
            "test": "generalized alpha law contains scalar and spin-2 branches",
            "result": "PASS_NONCLAIM" if len(laws) >= 3 else "FAIL",
            "detail": ";".join(row["law_id"] for row in laws),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3303_2_projection_requirements_ready",
            "test": "Z/Xi/U/lambda requirements are listed before bound scoring",
            "result": "PASS_NONCLAIM" if len(requirements) == 4 else "FAIL",
            "detail": ";".join(row["quantity"] for row in requirements),
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    import_allowed = all(row["passed_for_amplitude_import"] == "true" for row in evidence_score_rows())
    return [
        {
            "gate_id": "GATE3303_0_import_plus_minus_amplitudes",
            "claim": "MTS inherits alpha_0=+1/3 and alpha_2=-4/3",
            "requirements": "all AIC3303 clauses parent-signed: pure metric branch, universal Hilbert source, same readout metric, canonical normalization, common G reference, and no hidden source selector",
            "current_evidence": "clauses remain conditional or missing",
            "passed": bool_str(import_allowed),
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3303_1_use_general_alpha_law",
            "claim": "MTS should use alpha_0=(1/3)Z_0Xi_0U_0 and alpha_2=(-4/3)Z_2Xi_2U_2 until pure limit is proven",
            "requirements": "law rows exist and keep amplitudes non-numeric/non-claim",
            "current_evidence": "ALAW3303 rows generated",
            "passed": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3303_2_score_bounds",
            "claim": "score finite quadratic branch against R10/PPN/orbital bounds",
            "requirements": "numeric Z/Xi/U/lambda values plus sourced bounds",
            "current_evidence": "requirements staged only",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    import_allowed = all(row["passed_for_amplitude_import"] == "true" for row in evidence_score_rows())
    return [
        {
            "decision_id": "DEC3303_0",
            "question": "Can MTS import +1/3 and -4/3 as its finite quadratic amplitudes?",
            "answer": "yes" if import_allowed else "no",
            "reason": "all import clauses are signed" if import_allowed else "Hilbert/source/readout/normalization clauses remain conditional or missing, so fixed amplitudes would be imported rather than derived",
            "next_action": "use pure metric amplitudes after review" if import_allowed else "derive or bound Z_0, Xi_0, U_0, Z_2, Xi_2, U_2",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3303_1",
            "question": "What is the mathematically safe MTS amplitude law?",
            "answer": "alpha_0=(1/3)Z_0Xi_0U_0 and alpha_2=(-4/3)Z_2Xi_2U_2",
            "reason": "pure metric values are recovered as the special case where residue, source projection, and readout overlaps are all unity",
            "next_action": "attack Xi source projection first because it links directly to the coupling problem",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3303_0_3304",
            "target_doc": "3304-Y5-R2FR-source-projection-overlap-law-for-alpha-factors-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3304_source_projection_overlap_law_for_alpha_factors.py",
            "objective": "derive or bound Xi_0 and Xi_2, the source-projection overlap factors that decide whether finite modes couple universally like Hilbert stress or produce WEP/source-weight residuals",
            "guardrails": "do not treat Xi_0=Xi_2=1 as default; prove it from the descended matter action or keep WEP/source residual rows alive",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    outputs_to_parse = [path for key, path in OUTPUTS.items() if key != "validation"]
    contracts = contract_rows()
    evidence = evidence_score_rows()
    laws = generalized_alpha_law_rows()
    requirements = requirement_rows()
    runners = runner_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3303_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3303_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3303_2_outputs_parse",
            "all 3303 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in outputs_to_parse),
            "",
        ),
        (
            "VAL3303_3_import_contract_complete",
            "amplitude import contract covers metric/source/readout/normalization/G/hidden-selector clauses",
            all(
                any(needle in row["clause_id"] for row in contracts)
                for needle in [
                    "pure_metric",
                    "universal_Hilbert",
                    "same_readout",
                    "canonical",
                    "common_G",
                    "no_screening",
                ]
            ),
            "",
        ),
        (
            "VAL3303_4_fixed_amplitudes_not_imported",
            "fixed amplitudes are refused unless all import clauses pass",
            any(row["result"] == "REFUSE_IMPORT_USE_GENERAL_ALPHA" for row in runners),
            ";".join(f"{row['clause_id']}={row['passed_for_amplitude_import']}" for row in evidence),
        ),
        (
            "VAL3303_5_general_alpha_law_complete",
            "general alpha law includes alpha_0 and alpha_2 with Z/Xi/U factors",
            any("alpha_0" in row["mts_general_law"] and "Z_0" in row["mts_general_law"] for row in laws)
            and any("alpha_2" in row["mts_general_law"] and "Z_2" in row["mts_general_law"] for row in laws),
            "",
        ),
        (
            "VAL3303_6_requirements_include_Z_Xi_U_lambda",
            "requirements include Z, Xi, U, and lambda quantities",
            all(
                any(token in row["quantity"] for row in requirements)
                for token in ["Z_", "Xi_", "U_", "lambda_"]
            ),
            "",
        ),
        (
            "VAL3303_7_claim_gates_safe",
            "no bound-scoring claim is allowed and all rows remain non-claim",
            all(row["valid_for_claim"] == "false" for row in gates)
            and any(row["gate_id"] == "GATE3303_2_score_bounds" and row["passed"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3303_8_next_target_Xi",
            "next target attacks source-projection overlap Xi factors",
            "source-projection-overlap" in next_rows[0]["target_doc"] and "Xi_0" in next_rows[0]["objective"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3303_9_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3303_10_overall",
            "3303 validation overall",
            overall,
            "all required checks passed" if overall else "one or more checks failed",
        )
    )

    return [
        {
            "check_id": check_id,
            "check": check,
            "passed": bool_str(passed),
            "detail": detail,
        }
        for check_id, check, passed, detail in checks
    ]


def render_doc() -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    contract_table = "\n".join(
        f"- `{row['clause_id']}`: {row['clause']} Status: `{row['current_status']}`."
        for row in contract_rows()
    )
    evidence_table = "\n".join(
        f"- `{row['clause_id']}`: passed={row['passed_for_amplitude_import']}; status={row['evidence_status']}; source=`{row['evidence_path']}`"
        for row in evidence_score_rows()
    )
    law_table = "\n".join(
        f"- `{row['law_id']}` `{row['mode']}`: `{row['mts_general_law']}`; pure limit: {row['pure_limit']}."
        for row in generalized_alpha_law_rows()
    )
    requirement_table = "\n".join(
        f"- `{row['requirement_id']}` `{row['quantity']}`: {row['how_to_derive']}"
        for row in requirement_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows()
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows()
    )
    next_row = next_target_rows()[0]

    return f"""# 3303 - Universal Hilbert-source check for quadratic amplitudes under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The coupling fork is now explicit.

MTS cannot yet import the pure metric quadratic amplitudes `+1/3` and `-4/3` as predictions, because the parent-owned source/readout/normalization clauses are not all signed. The safe finite-mode law is therefore

`alpha_0 = (1/3) Z_0 Xi_0 U_0`

and

`alpha_2 = (-4/3) Z_2 Xi_2 U_2`.

Pure metric quadratic gravity is recovered only when every factor equals one. That makes the next hard object the source-projection overlap `Xi`, not another vague missing coupling.

## Source Register

{source_table}

## Amplitude Import Contract

{contract_table}

## Evidence Score

{evidence_table}

## Generalized Amplitude Law

{law_table}

## Required Derivations

{requirement_table}

## Runner

{runner_table}

## Promotion Gates

{gate_table}

## Decision

{decision_table}

## Next Target

- `{next_row['target_doc']}`
- `{next_row['target_script']}`
- Objective: {next_row['objective']}
"""


def main() -> None:
    formalization_before = snapshot_tree(FW)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["contract"], contract_rows())
    write_csv(OUTPUTS["evidence"], evidence_score_rows())
    write_csv(OUTPUTS["law"], generalized_alpha_law_rows())
    write_csv(OUTPUTS["requirements"], requirement_rows())
    write_csv(OUTPUTS["runner"], runner_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))

    if PYCACHE.exists():
        for child in PYCACHE.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(PYCACHE.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        PYCACHE.rmdir()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

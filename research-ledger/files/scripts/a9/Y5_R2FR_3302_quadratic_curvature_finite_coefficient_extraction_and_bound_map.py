from __future__ import annotations

import csv
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3302-Y5-R2FR-quadratic-curvature-finite-coefficient-extraction-and-bound-map-under-AX1090.md"

SRC_3301_DOC = ROOT / "3301-Y5-R2FR-parent-curvature-linear-signature-hunt-or-quadratic-bound-fill-under-AX1090.md"
SRC_3301_DECISION = OUT / "P8_Y5_R2FR_3301_SIGNATURE_DECISION.csv"
SRC_3301_SCHEMA = OUT / "P8_Y5_R2FR_3301_QUADRATIC_BOUND_FILL_SCHEMA.csv"
SRC_3301_SCAN = OUT / "P8_Y5_R2FR_3301_PARENT_SIGNATURE_SCAN.csv"
SRC_3301_NEXT = OUT / "P8_Y5_R2FR_3301_NEXT_TARGET.csv"
SRC_3301_VALIDATION = OUT / "P8_Y5_BRR545_3301_VALIDATION.csv"
SRC_3300_YUKAWA = OUT / "P8_Y5_R2FR_3300_CURVATURE_SQUARED_YUKAWA_BASIS.csv"
SRC_3300_VARIATION = OUT / "P8_Y5_R2FR_3300_R2_RICCI2_VARIATION_AUDIT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3302_SOURCE_REGISTER.csv",
    "action_convention": OUT / "P8_Y5_R2FR_3302_QUADRATIC_ACTION_CONVENTION.csv",
    "mode_map": OUT / "P8_Y5_R2FR_3302_LINEARIZED_MODE_MASS_MAP.csv",
    "potential": OUT / "P8_Y5_R2FR_3302_NEWTON_YUKAWA_POTENTIAL_TEMPLATE.csv",
    "coefficient_scan": OUT / "P8_Y5_R2FR_3302_PARENT_COEFFICIENT_EXTRACTION_SCAN.csv",
    "test_inputs": OUT / "P8_Y5_R2FR_3302_TEST_INPUT_REQUIREMENTS.csv",
    "promotion": OUT / "P8_Y5_R2FR_3302_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3302_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3302_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3302_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

SCAN_ROOTS = [
    REPO / "core-mts-framework",
    REPO / "cosmology",
    REPO / "documents",
    REPO / "formalization-workbench",
    REPO / "mathematics",
    REPO / "orbital-dynamics",
    REPO / "quantum-particle-field",
]

TEXT_EXTENSIONS = {".md", ".txt", ".tex", ".csv", ".py", ".json", ".yaml", ".yml"}
SKIP_DIR_NAMES = {".git", "__pycache__", ".ipynb_checkpoints", "runs", "node_modules", ".venv", "venv"}

COEFFICIENT_PATTERNS = {
    "a_R2": [
        r"\ba_R2\b\s*[:=]",
        r"\bc_R2\b\s*[:=]",
        r"coefficient\s+of\s+R\^2",
        r"R\^2\s+coefficient",
        r"quadratic\s+curvature\s+coefficient",
    ],
    "b_Ric": [
        r"\bb_Ric\b\s*[:=]",
        r"\bc_Ric\b\s*[:=]",
        r"\bc_W\b\s*[:=]",
        r"Ricci\^2\s+coefficient",
        r"Weyl\^2\s+coefficient",
        r"coefficient\s+of\s+Ricci",
    ],
}


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
        (SRC_3301_DOC, "3301 parent signature hunt", ["Decision", "curvature-linear"]),
        (SRC_3301_DECISION, "3301 decision row", ["DEC3301_0_parent_signature", "fill finite"]),
        (SRC_3301_SCHEMA, "3301 finite schema", ["QBF3301_0_c_R2_scalar", "QBF3301_1_c_Ric_spin2"]),
        (SRC_3301_SCAN, "3301 scan evidence", ["promotes_curvature_squared_zero", "support_clauses"]),
        (SRC_3301_NEXT, "3301 next target", ["finite-coefficient-extraction", "bound-map"]),
        (SRC_3301_VALIDATION, "3301 validation", ["VAL3301_10_overall", "true"]),
        (SRC_3300_YUKAWA, "3300 Yukawa basis", ["alpha_0", "alpha_2"]),
        (SRC_3300_VARIATION, "3300 variation audit", ["R^2", "Ricci"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3302_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def safe_text_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    files: list[Path] = []
    for item in root.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in item.parts):
            continue
        if item.is_file() and item.suffix.lower() in TEXT_EXTENSIONS:
            try:
                if item.stat().st_size <= 2_000_000:
                    files.append(item)
            except OSError:
                continue
    return files


def line_evidence(text: str, patterns: list[str], limit: int = 4) -> str:
    compiled_patterns = [re.compile(pattern, flags=re.IGNORECASE) for pattern in patterns]
    snippets: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(pattern.search(line) for pattern in compiled_patterns):
            snippets.append(f"L{line_number}:{compact(line, 280)}")
        if len(snippets) >= limit:
            break
    return " | ".join(snippets) if snippets else "NO_LINE_EVIDENCE"


def action_convention_rows() -> list[dict[str, Any]]:
    return [
        {
            "convention_id": "ACT3302_0",
            "action_template": "S = (1/2 kappa) integral sqrt(-g) [R - 2 Lambda + a_R2 R^2 + b_Ric R_mu_nu R^mu_nu + b_W C_mu_nu_rho_sigma C^mu_nu_rho_sigma] + S_m",
            "normalization_warning": "a_R2, b_Ric, and b_W are convention placeholders; MTS must derive their exact normalization before scoring",
            "reason_for_template": "this is the finite fallback when c_R2/c_Ric are not zeroed by parent grammar",
            "valid_for_claim": "false",
        }
    ]


def mode_mass_rows() -> list[dict[str, Any]]:
    return [
        {
            "mode_id": "MODE3302_0_scalar",
            "source_operator": "a_R2 R^2 plus trace part of b_Ric R_mu_nu R^mu_nu",
            "mode_symbol": "m_0, lambda_0",
            "template_mass_relation": "m_0^2 ~ 1/[2(3 a_R2 + b_Ric)] in the displayed convention",
            "yukawa_amplitude_template": "alpha_0 = +1/3 for pure metric quadratic gravity with universal Hilbert source",
            "mts_caveat": "if MTS projection/source coupling differs, alpha_0 must be rederived rather than imported",
            "valid_for_claim": "false",
        },
        {
            "mode_id": "MODE3302_1_spin2",
            "source_operator": "b_Ric R_mu_nu R^mu_nu or b_W Weyl^2",
            "mode_symbol": "m_2, lambda_2",
            "template_mass_relation": "m_2^2 ~ -1/b_Ric or equivalent Weyl-normalized expression in the displayed convention",
            "yukawa_amplitude_template": "alpha_2 = -4/3 for pure metric quadratic gravity with universal Hilbert source",
            "mts_caveat": "sign/stability/ghost handling and exact source coupling must be parent-derived before using alpha_2",
            "valid_for_claim": "false",
        },
    ]


def potential_rows() -> list[dict[str, Any]]:
    return [
        {
            "potential_id": "POT3302_0",
            "branch": "pure_metric_quadratic_template",
            "formula": "Phi(r) = -G_cal M/r [1 + (1/3) exp(-r/lambda_0) - (4/3) exp(-r/lambda_2)]",
            "use_case": "finite fallback if parent action contains quadratic curvature with universal Hilbert source",
            "blocked_by": "missing MTS-owned a_R2/b_Ric/b_W normalization and source projection",
            "valid_for_claim": "false",
        },
        {
            "potential_id": "POT3302_1",
            "branch": "MTS_generalized_quadratic_template",
            "formula": "Phi(r) = -G_cal M/r [1 + alpha_0 exp(-r/lambda_0) + alpha_2 exp(-r/lambda_2)]",
            "use_case": "safe nonclaim scoring form when amplitudes/ranges are parent-derived but not necessarily pure metric",
            "blocked_by": "alpha_0, alpha_2, lambda_0, lambda_2 not yet sourced from parent coefficients",
            "valid_for_claim": "false",
        },
        {
            "potential_id": "POT3302_2_GR_limit",
            "branch": "infinite_mass_or_zero_coefficient_limit",
            "formula": "lambda_0,lambda_2 -> 0 or alpha_0=alpha_2=0 gives Phi(r) -> -G_cal M/r",
            "use_case": "local Newtonian limit recovered only if parent zero theorem or decoupling limit is derived",
            "blocked_by": "parent zero/decoupling proof not yet signed",
            "valid_for_claim": "false",
        },
    ]


def coefficient_scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in SCAN_ROOTS:
        for path in safe_text_files(root):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for coefficient, patterns in COEFFICIENT_PATTERNS.items():
                if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
                    rows.append(
                        {
                            "coefficient": coefficient,
                            "path": str(path),
                            "parent_owned": bool_str(ROOT not in path.parents),
                            "numeric_candidate": bool_str(bool(re.search(r"[-+]?\d+(\.\d+)?([eE][-+]?\d+)?", text))),
                            "evidence_lines": line_evidence(text, patterns),
                            "status": "CANDIDATE_NEEDS_MANUAL_REVIEW",
                            "valid_for_claim": "false",
                        }
                    )
    if not rows:
        rows.append(
            {
                "coefficient": "a_R2/b_Ric",
                "path": "NO_PARENT_COEFFICIENT_CANDIDATE",
                "parent_owned": "false",
                "numeric_candidate": "false",
                "evidence_lines": "NO_LINE_EVIDENCE",
                "status": "MISSING_PARENT_COEFFICIENT",
                "valid_for_claim": "false",
            }
        )
    rows.sort(key=lambda row: (row["parent_owned"] == "true", row["numeric_candidate"] == "true"), reverse=True)
    return rows[:60]


def test_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "TIN3302_0_R10",
            "arena": "R10_short_range_Yukawa",
            "needed_values": "lambda_0, alpha_0 and/or lambda_2, alpha_2 at laboratory ranges",
            "needed_bound_source": "real alpha(lambda) curve or sourced anchor rows with valid_for_claim=false until full curve exists",
            "current_status": "WAITING_ON_PARENT_COEFFICIENTS_AND_BOUND_CURVE",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TIN3302_1_PPN",
            "arena": "solar_system_PPN",
            "needed_values": "gamma(r)-1, beta(r)-1, light-bending residual from scalar/spin-2 modes",
            "needed_bound_source": "PPN gamma/beta and light-bending bounds with source paths",
            "current_status": "WAITING_ON_METRIC_PROJECTION",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TIN3302_2_orbital",
            "arena": "orbital_precession_ephemerides",
            "needed_values": "extra radial acceleration and perihelion/precession residual from finite lambda modes",
            "needed_bound_source": "orbital residual limits with units and body/system labels",
            "current_status": "WAITING_ON_RANGE_AND_ACCELERATION_MAP",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows(coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reviewed_numeric_parent_rows = [
        row
        for row in coefficient_rows
        if row["parent_owned"] == "true"
        and row["numeric_candidate"] == "true"
        and row["status"] == "PARENT_REVIEWED_NUMERIC_COEFFICIENT"
    ]
    return [
        {
            "gate_id": "GATE3302_0_use_pure_metric_amplitudes",
            "claim": "use +1/3 and -4/3 as MTS amplitudes",
            "requirements": "parent action must reduce to pure metric quadratic gravity with universal Hilbert source and matching normalization",
            "current_evidence": "template only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3302_1_use_parent_coefficients",
            "claim": "calculate lambda_0/lambda_2 from parent coefficients",
            "requirements": "reviewed numeric or algebraic parent coefficients with units for a_R2 and b_Ric/b_W",
            "current_evidence": f"reviewed_numeric_parent_rows={len(reviewed_numeric_parent_rows)}",
            "passed": bool_str(bool(reviewed_numeric_parent_rows)),
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3302_2_score_bounds",
            "claim": "score quadratic curvature branch against R10/PPN/orbital bounds",
            "requirements": "GATE3302_1 plus sourced bound tables and metric/orbital projection rows",
            "current_evidence": "not ready",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidate_count = sum(1 for row in coefficient_rows if row["path"] != "NO_PARENT_COEFFICIENT_CANDIDATE")
    return [
        {
            "decision_id": "DEC3302_0",
            "question": "Can the finite c_R2/c_Ric branch now be numerically tested?",
            "answer": "no",
            "reason": "the finite potential map is derived, but parent-owned coefficient normalization and bound-source rows are not yet claim-ready",
            "coefficient_candidate_count": candidate_count,
            "next_action": "review coefficient candidates if any; otherwise acquire bound curves and keep deriving parent coefficients",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3302_1",
            "question": "What changed mathematically?",
            "answer": "the finite branch now has a concrete two-mode Yukawa form with scalar amplitude +1/3 and spin-2 amplitude -4/3 in the pure metric convention",
            "reason": "this turns c_R2/c_Ric from an abstract residual into test quantities alpha_0/lambda_0 and alpha_2/lambda_2",
            "coefficient_candidate_count": candidate_count,
            "next_action": "decide whether MTS signs pure metric universal coupling or derives modified amplitudes",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3302_0_3303",
            "target_doc": "3303-Y5-R2FR-universal-Hilbert-source-check-for-quadratic-amplitudes-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3303_universal_Hilbert_source_check_for_quadratic_amplitudes.py",
            "objective": "check whether MTS can legitimately inherit the pure metric quadratic amplitudes +1/3 and -4/3, or must derive modified alpha_0/alpha_2 from its own source projection",
            "guardrails": "do not import Stelle-style amplitudes as an MTS prediction unless the source coupling and metric branch match; do not score bounds until lambda values are sourced",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(
    formalization_before: dict[str, tuple[int, int]],
    coefficient_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    outputs_to_parse = [path for key, path in OUTPUTS.items() if key != "validation"]
    mode_rows = mode_mass_rows()
    potential_template_rows = potential_rows()
    test_inputs = test_input_rows()
    gates = promotion_gate_rows(coefficient_rows)
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3302_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3302_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3302_2_outputs_parse",
            "all 3302 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in outputs_to_parse),
            "",
        ),
        (
            "VAL3302_3_mode_map_has_scalar_and_spin2",
            "mode map includes scalar and spin-2 branches",
            any(row["mode_id"] == "MODE3302_0_scalar" for row in mode_rows)
            and any(row["mode_id"] == "MODE3302_1_spin2" for row in mode_rows),
            "",
        ),
        (
            "VAL3302_4_potential_has_fixed_template_amplitudes",
            "potential template records +1/3 and -4/3 pure metric amplitudes",
            any("(1/3)" in row["formula"] and "- (4/3)" in row["formula"] for row in potential_template_rows),
            "",
        ),
        (
            "VAL3302_5_general_mts_alpha_template_present",
            "general MTS alpha_0/alpha_2 template is present separately from pure metric template",
            any("alpha_0" in row["formula"] and "alpha_2" in row["formula"] for row in potential_template_rows),
            "",
        ),
        (
            "VAL3302_6_coefficient_scan_safe",
            "coefficient scan rows remain non-claim",
            bool(coefficient_rows) and all(row["valid_for_claim"] == "false" for row in coefficient_rows),
            f"rows={len(coefficient_rows)}",
        ),
        (
            "VAL3302_7_test_inputs_cover_local_arenas",
            "test inputs cover R10, PPN, and orbital arenas",
            all(any(row["arena"].startswith(prefix) for row in test_inputs) for prefix in ["R10", "solar_system", "orbital"]),
            "",
        ),
        (
            "VAL3302_8_claim_gates_safe",
            "no scoring gate passes without reviewed parent coefficients and bounds",
            all(row["valid_for_claim"] == "false" for row in gates)
            and all(row["passed"] == "false" for row in gates if row["gate_id"] != "GATE3302_1_use_parent_coefficients"),
            "",
        ),
        (
            "VAL3302_9_next_target_source_amplitudes",
            "next target checks source coupling before importing fixed amplitudes",
            "universal-Hilbert-source-check" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3302_10_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3302_11_overall",
            "3302 validation overall",
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


def render_doc(coefficient_rows: list[dict[str, Any]]) -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    mode_table = "\n".join(
        f"- `{row['mode_id']}`: {row['template_mass_relation']}; amplitude template: {row['yukawa_amplitude_template']}"
        for row in mode_mass_rows()
    )
    potential_table = "\n".join(
        f"- `{row['potential_id']}` `{row['branch']}`: `{row['formula']}`"
        for row in potential_rows()
    )
    coefficient_table = "\n".join(
        f"- `{row['coefficient']}`: `{row['path']}`; status={row['status']}; evidence={row['evidence_lines']}"
        for row in coefficient_rows[:12]
    )
    input_table = "\n".join(
        f"- `{row['input_id']}` `{row['arena']}`: needs {row['needed_values']}; status={row['current_status']}"
        for row in test_input_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; evidence={row['current_evidence']}"
        for row in promotion_gate_rows(coefficient_rows)
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows(coefficient_rows)
    )
    next_row = next_target_rows()[0]

    return f"""# 3302 - Quadratic-curvature finite coefficient extraction and bound map under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

This checkpoint takes the finite route seriously.

If the curvature-squared coefficients are not zeroed by parent grammar, the local Newtonian potential has a concrete two-mode Yukawa structure. In the pure metric quadratic-gravity convention,

`Phi(r) = -G_cal M/r [1 + (1/3) exp(-r/lambda_0) - (4/3) exp(-r/lambda_2)]`.

That is not yet an MTS prediction. It becomes an MTS prediction only if MTS signs the same metric branch, source coupling, and coefficient normalization. Until then, the safe MTS form is

`Phi(r) = -G_cal M/r [1 + alpha_0 exp(-r/lambda_0) + alpha_2 exp(-r/lambda_2)]`.

## Source Register

{source_table}

## Action Convention

- `S = (1/2 kappa) integral sqrt(-g) [R - 2 Lambda + a_R2 R^2 + b_Ric R_mu_nu R^mu_nu + b_W C^2] + S_m`
- `a_R2`, `b_Ric`, and `b_W` are placeholders until MTS supplies parent-owned coefficients with units.

## Mode Mass Map

{mode_table}

## Potential Templates

{potential_table}

## Parent Coefficient Scan

{coefficient_table}

## Test Inputs

{input_table}

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
    coefficient_rows = coefficient_scan_rows()

    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["action_convention"], action_convention_rows())
    write_csv(OUTPUTS["mode_map"], mode_mass_rows())
    write_csv(OUTPUTS["potential"], potential_rows())
    write_csv(OUTPUTS["coefficient_scan"], coefficient_rows)
    write_csv(OUTPUTS["test_inputs"], test_input_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows(coefficient_rows))
    write_csv(OUTPUTS["decision"], decision_rows(coefficient_rows))
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(coefficient_rows), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before, coefficient_rows))

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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1943"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1943-Y5-R2FR-delta-gamma-R11-weak-field-solve-or-Cassini-bound-runner.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

CASSINI_GAMMA_CENTRAL = 2.1e-5
CASSINI_GAMMA_SIGMA = 2.3e-5

SOURCES = {
    "1942_doc": ROOT / "1942-Y5-R2FR-PPN-R11-residual-equations-or-solar-system-bound-ledger.md",
    "1942_validation": OUT / "P8_Y5_BRR545_1942_VALIDATION.csv",
    "1942_equations": OUT / "P8_Y5_PARENT_QLOC_1942_PPN_R11_EQUATION_MAP.csv",
    "1942_bounds": OUT / "P8_Y5_PARENT_QLOC_1942_SOLAR_SYSTEM_BOUND_LEDGER.csv",
    "1942_acceptance": OUT / "P8_Y5_PARENT_QLOC_1942_RESIDUAL_ACCEPTANCE_GATE.csv",
    "1942_claims": OUT / "P8_Y5_PARENT_QLOC_1942_CLAIM_GATE.csv",
    "1942_next": OUT / "P8_Y5_PARENT_QLOC_1942_NEXT_TARGET.csv",
    "1939_r11": OUT / "P8_Y5_PARENT_QLOC_1939_R11_RESIDUAL_NEWTONIAN_LAW.csv",
}

NEEDLES = {
    "1942_doc": ["EQ1942_1_gamma", "BND1942_0_Cassini_gamma", "VAL1942_OVERALL"],
    "1942_validation": ["VAL1942_OVERALL", "PASS"],
    "1942_equations": ["EQ1942_1_gamma", "delta_gamma"],
    "1942_bounds": ["BND1942_0_Cassini_gamma", "2.3e-05"],
    "1942_acceptance": ["ACC1942_0_gamma", "RULE_RECORDED_NONCLAIM"],
    "1942_claims": ["CG1942_2_numeric_residuals", "FAIL_BLOCKED"],
    "1942_next": ["NEXT1942_0_primary", "delta-gamma"],
    "1939_r11": ["R111939_2_Newtonian_projection", "R111939_4_PPN_projection"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1943_SOURCE_REGISTER.csv",
    "delta_gamma_derivation": OUT / "P8_Y5_PARENT_QLOC_1943_DELTA_GAMMA_R11_DERIVATION.csv",
    "cassini_bound_runner": OUT / "P8_Y5_PARENT_QLOC_1943_CASSINI_GAMMA_BOUND_RUNNER.csv",
    "missing_input_ledger": OUT / "P8_Y5_PARENT_QLOC_1943_DELTA_GAMMA_MISSING_INPUT_LEDGER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1943_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1943_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1943_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1943_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1943_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_delta_gamma": SOURCE_WEIGHT_DOCS / "DELTA_GAMMA_R11_CASSINI_GATE_1943_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1943_CLAIM_GATE_NONCLAIM.csv",
    "cassini_queue": QUEUE / "JR1943_DELTA_GAMMA_R11_CASSINI_BOUND_RUNNER_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1943_CLAIM_GATE.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_key, source_path in SOURCES.items():
        path_exists = source_path.exists()
        source_text = read_text(source_path) if path_exists else ""
        missing_needles = [needle for needle in NEEDLES[source_key] if needle not in source_text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "needed_for": "1943 delta-gamma R11 weak-field solve or Cassini bound runner",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def delta_gamma_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "DG1943_0_metric_potentials",
            "statement": "Write the weak static isotropic observed metric as g_00=-(1+2 Phi/c^2), g_ij=(1+2 Psi/c^2)delta_ij.",
            "result": "WEAK_FIELD_SETUP",
            "formula": "gamma = Psi/Phi",
            "claim_blocker": "Phi and Psi must be solved from the MTS/R11 weak-field equations",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "DG1943_1_residual_split",
            "statement": "Split Phi=U+Phi_R11 and Psi=U+Psi_R11 where U is the GR/Newton potential.",
            "result": "RESIDUAL_PARAMETERIZATION",
            "formula": "gamma_R11 = (U+Psi_R11)/(U+Phi_R11)",
            "claim_blocker": "Phi_R11 and Psi_R11 are not yet derived or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "DG1943_2_delta_gamma_exact",
            "statement": "The exact residual expression relative to GR is delta_gamma_R11=gamma_R11-1.",
            "result": "EXACT_SYMBOLIC_EXPRESSION",
            "formula": "delta_gamma_R11 = (Psi_R11-Phi_R11)/(U+Phi_R11)",
            "claim_blocker": "requires nonzero denominator and residual potential definitions",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "DG1943_3_linear_limit",
            "statement": "If |Phi_R11|,|Psi_R11| << |U|, then delta_gamma_R11 is the anisotropic spatial/time potential difference over U.",
            "result": "CONTROLLED_LINEAR_LIMIT",
            "formula": "delta_gamma_R11 ~= (Psi_R11-Phi_R11)/U",
            "claim_blocker": "small-residual condition must be proved or checked for any numeric comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "DG1943_4_cassini_target",
            "statement": "Cassini constrains the same gamma residual once the observable mapping and confidence convention are fixed.",
            "result": "BOUND_TARGET_READY_INPUTS_MISSING",
            "formula": f"delta_gamma_R11 compare to gamma-1 = {CASSINI_GAMMA_CENTRAL:.3e} +/- {CASSINI_GAMMA_SIGMA:.3e}",
            "claim_blocker": "numeric Phi_R11/Psi_R11 or theorem-zero residual is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def cassini_bound_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1943_0_cassini_schema",
            "observable": "gamma_minus_one",
            "bound_central": CASSINI_GAMMA_CENTRAL,
            "bound_sigma": CASSINI_GAMMA_SIGMA,
            "prediction_symbolic": "delta_gamma_R11=(Psi_R11-Phi_R11)/(U+Phi_R11)",
            "linear_prediction_symbolic": "delta_gamma_R11~=(Psi_R11-Phi_R11)/U",
            "numeric_prediction": "MISSING_NUMERIC_R11_POTENTIALS",
            "comparison_rule": "blocked until confidence convention and numeric/theorem-zero prediction exist",
            "runner_status": "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED",
            "source_ref": "BND1942_0_Cassini_gamma",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def missing_input_rows() -> list[dict[str, Any]]:
    rows = [
        ("MISS1943_0_U", "U", "GR/Newton potential normalization in observed frame", "MISSING_OBSERVED_FRAME_NORMALIZATION"),
        ("MISS1943_1_Phi_R11", "Phi_R11", "time-time weak-field residual potential", "MISSING_R11_00_SOLVE"),
        ("MISS1943_2_Psi_R11", "Psi_R11", "spatial isotropic weak-field residual potential", "MISSING_R11_IJ_SOLVE"),
        ("MISS1943_3_anisotropy", "anisotropic spatial residual", "non-isotropic pieces must be projected into PPN preferred-frame/tidal observables", "MISSING_ANISOTROPIC_PROJECTION"),
        ("MISS1943_4_small_residual", "|Phi_R11|,|Psi_R11| << |U|", "linear limit control", "MISSING_SMALL_RESIDUAL_PROOF"),
        ("MISS1943_5_confidence", "Cassini acceptance convention", "1-sigma/2-sigma/model-comparison rule", "MISSING_CONFIDENCE_POLICY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": input_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for input_id, symbol, meaning, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1943_0_symbolic_delta_gamma", "symbolic delta_gamma_R11 expression exists", "PASS_NONCLAIM", "exact and linear expressions recorded"),
        ("CG1943_1_cassini_runner", "Cassini bound runner schema exists", "PASS_NONCLAIM", "runner remains blocked until numeric residuals exist"),
        ("CG1943_2_numeric_prediction", "MTS predicts numeric delta_gamma_R11", "FAIL_BLOCKED", "Phi_R11 and Psi_R11 missing"),
        ("CG1943_3_cassini_pass", "MTS passes Cassini gamma", "FAIL_BLOCKED", "no numeric/theorem-zero delta_gamma_R11"),
        ("CG1943_4_local_gr_ppn", "MTS derives local GR/PPN", "FAIL_BLOCKED", "remaining PPN residuals unresolved"),
        ("CG1943_5_public_claim", "1943 is public-ready Cassini proof", "FAIL_BLOCKED", "private symbolic/bound-runner checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1943_0_delta_gamma_status",
            "decision": "DELTA_GAMMA_SYMBOLICALLY_DERIVED_NUMERICALLY_BLOCKED",
            "rationale": "Cassini comparison now has the exact residual expression, but MTS has not solved Phi_R11/Psi_R11.",
            "next_action": "derive weak-field R11 potential equations for Phi_R11 and Psi_R11",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1943_1_next_route",
            "decision": "ATTACK_R11_WEAK_FIELD_POTENTIALS_NEXT",
            "rationale": "The next bottleneck is not more bounds; it is the actual R11 00/ij weak-field solve.",
            "next_action": "derive Phi_R11/Psi_R11 from the residual operator or demote R11 to coefficient placeholders",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1943_0_primary",
            "selection_status": "selected",
            "target_doc": "1944-Y5-R2FR-R11-weak-field-potential-equations-or-coefficient-placeholder-ledger.md",
            "target_script": "scripts/Y5_R2FR_R11_weak_field_potential_equations_or_coefficients_1944.py",
            "objective": "derive weak-field equations for Phi_R11 and Psi_R11 from the R11/residual operator, or create coefficient placeholders that keep Cassini/local-GR claims blocked",
            "success_condition": "symbolic Phi_R11/Psi_R11 equations tied to R11 operator coefficients, or explicit missing-coefficient ledger with claim=false",
            "do_not": "do not claim Cassini/local GR pass without numeric or theorem-zero residual potentials; do not modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1943_0_project_position",
            "status": "DELTA_GAMMA_SYMBOLIC_GATE_READY_NUMERIC_R11_POTENTIALS_MISSING",
            "summary": "1943 derives the symbolic Cassini gamma residual in terms of Phi_R11 and Psi_R11 and builds a nonclaim bound runner.",
            "strongest_result": "delta_gamma_R11=(Psi_R11-Phi_R11)/(U+Phi_R11), linearized as (Psi_R11-Phi_R11)/U",
            "missing_piece": "derive or source Phi_R11 and Psi_R11 from the R11 weak-field operator",
            "claim_position": "Cassini/local-GR/PPN claims remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_delta_gamma"], rows_by_name["delta_gamma_derivation"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["cassini_queue"], rows_by_name["cassini_bound_runner"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1943*") if artifact.is_file())


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation_rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        validation_rows.append(
            {
                "validation_id": validation_id,
                "status": "PASS" if status else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL1943_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1943_01_derivation", any(row["result"] == "EXACT_SYMBOLIC_EXPRESSION" for row in rows_by_name["delta_gamma_derivation"]) and any(row["result"] == "CONTROLLED_LINEAR_LIMIT" for row in rows_by_name["delta_gamma_derivation"]), "exact and linear delta_gamma expressions recorded")
    runner = rows_by_name["cassini_bound_runner"][0]
    add("VAL1943_02_runner", runner["runner_status"] == "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED" and float(runner["bound_sigma"]) > 0, "Cassini runner schema ready and blocked")
    add("VAL1943_03_missing_inputs", len(rows_by_name["missing_input_ledger"]) == 6 and all(str(row["status"]).startswith("MISSING_") for row in rows_by_name["missing_input_ledger"]), "missing inputs explicitly listed")
    add("VAL1943_04_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only nonclaim gates pass; all claim flags false")
    add("VAL1943_05_decision", any(row["decision"] == "ATTACK_R11_WEAK_FIELD_POTENTIALS_NEXT" for row in rows_by_name["decision"]), "R11 weak-field potentials selected next")
    add("VAL1943_06_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1944-Y5-R2FR-R11-weak-field"), "1944 R11 weak-field target selected")
    add("VAL1943_07_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1943_08_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1943_09_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1943_10_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1943_11_formalization_untouched", formalization_count == 0, f"formalization_1943_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1943_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1943 delta-gamma R11 weak-field solve or Cassini bound runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1943 Y5 R2FR: Delta-Gamma R11 Weak-Field Solve or Cassini Bound Runner",
        "",
        "## Verdict",
        "",
        "1943 derives the symbolic Cassini-facing residual: `delta_gamma_R11=(Psi_R11-Phi_R11)/(U+Phi_R11)`, with the controlled small-residual limit `delta_gamma_R11≈(Psi_R11-Phi_R11)/U`.",
        "",
        "This is useful but still nonclaim. The bound runner is ready, but MTS has not solved or bounded `Phi_R11` and `Psi_R11`, so there is no Cassini pass.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Delta-Gamma R11 Derivation",
        "",
        markdown_table(rows_by_name["delta_gamma_derivation"]),
        "",
        "## Cassini Gamma Bound Runner",
        "",
        markdown_table(rows_by_name["cassini_bound_runner"]),
        "",
        "## Missing Input Ledger",
        "",
        markdown_table(rows_by_name["missing_input_ledger"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "source_register": source_register_rows(),
        "delta_gamma_derivation": delta_gamma_derivation_rows(),
        "cassini_bound_runner": cassini_bound_runner_rows(),
        "missing_input_ledger": missing_input_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

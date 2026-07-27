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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1942"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1942-Y5-R2FR-PPN-R11-residual-equations-or-solar-system-bound-ledger.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1941_doc": ROOT / "1941-Y5-R2FR-Lovelock-assumption-signature-audit-or-PPN-residual-vector.md",
    "1941_validation": OUT / "P8_Y5_BRR545_1941_VALIDATION.csv",
    "1941_ppn_vector": OUT / "P8_Y5_PARENT_QLOC_1941_PPN_R11_RESIDUAL_VECTOR.csv",
    "1941_solar_gate": OUT / "P8_Y5_PARENT_QLOC_1941_SOLAR_SYSTEM_TEST_GATE.csv",
    "1941_claims": OUT / "P8_Y5_PARENT_QLOC_1941_CLAIM_GATE.csv",
    "1941_next": OUT / "P8_Y5_PARENT_QLOC_1941_NEXT_TARGET.csv",
    "1939_r11": OUT / "P8_Y5_PARENT_QLOC_1939_R11_RESIDUAL_NEWTONIAN_LAW.csv",
}

NEEDLES = {
    "1941_doc": ["PPN1941_1_gamma_residual", "SS1941_5_acceptance_rule", "VAL1941_OVERALL"],
    "1941_validation": ["VAL1941_OVERALL", "PASS"],
    "1941_ppn_vector": ["PPN1941_0_newtonian_residual", "PPN1941_7_shapiro"],
    "1941_solar_gate": ["SS1941_0_Cassini_gamma", "SS1941_5_acceptance_rule"],
    "1941_claims": ["CG1941_4_local_gr_claim", "FAIL_BLOCKED"],
    "1941_next": ["NEXT1941_0_primary", "PPN-R11-residual"],
    "1939_r11": ["R111939_2_Newtonian_projection", "R111939_4_PPN_projection"],
}

WEB_SOURCES = [
    {
        "web_source_id": "WEB1942_0_CASSINI_GAMMA",
        "title": "A test of general relativity using radio links with the Cassini spacecraft",
        "url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
        "doi": "https://doi.org/10.1038/nature01997",
        "used_for": "source-backed gamma-1 bound anchor",
        "extraction": "gamma = 1 + (2.1 +/- 2.3)e-5 from PubMed abstract",
        "confidence": "high",
    },
    {
        "web_source_id": "WEB1942_1_WILL_LRR_2014",
        "title": "The Confrontation between General Relativity and Experiment",
        "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
        "doi": "https://doi.org/10.12942/lrr-2014-4",
        "used_for": "PPN framework and review-bound extraction target",
        "extraction": "review source for beta, preferred-frame, Nordtvedt and conservation bounds; primary extraction still needed for claims",
        "confidence": "review_source_nonclaim",
    },
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1942_SOURCE_REGISTER.csv",
    "web_source_register": OUT / "P8_Y5_PARENT_QLOC_1942_WEB_SOURCE_REGISTER.csv",
    "ppn_equation_map": OUT / "P8_Y5_PARENT_QLOC_1942_PPN_R11_EQUATION_MAP.csv",
    "solar_bound_ledger": OUT / "P8_Y5_PARENT_QLOC_1942_SOLAR_SYSTEM_BOUND_LEDGER.csv",
    "residual_acceptance": OUT / "P8_Y5_PARENT_QLOC_1942_RESIDUAL_ACCEPTANCE_GATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1942_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1942_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1942_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1942_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1942_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_ppn": SOURCE_WEIGHT_DOCS / "PPN_R11_RESIDUAL_BOUND_LEDGER_1942_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1942_CLAIM_GATE_NONCLAIM.csv",
    "bound_queue": QUEUE / "JR1942_SOLAR_SYSTEM_BOUND_EXTRACTION_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1942_CLAIM_GATE.csv",
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
                "needed_for": "1942 PPN/R11 residual equation and bound ledger",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def web_source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **source,
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for source in WEB_SOURCES
    ]


def ppn_equation_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("EQ1942_0_newtonian", "Xi_N", "nabla^2 U = -4*pi*G*rho - Xi_N", "U potential / effective G", "must vanish or be bounded by inverse-square/ephemeris tests"),
        ("EQ1942_1_gamma", "delta_gamma", "g_ij=(1+2(1+delta_gamma)U/c^2)delta_ij", "light deflection and Shapiro delay", "Cassini gamma bound applies after mapping"),
        ("EQ1942_2_beta", "delta_beta", "g_00=-1+2U/c^2-2(1+delta_beta)U^2/c^4", "perihelion/nonlinear superposition", "requires beta bound extraction"),
        ("EQ1942_3_alpha1", "alpha1_R11", "g_0i preferred-frame vector term proportional to alpha1_R11", "preferred-frame orbital polarization", "requires alpha1 bound extraction"),
        ("EQ1942_4_alpha2", "alpha2_R11", "preferred-frame anisotropy term proportional to alpha2_R11", "spin/orbital anisotropy", "requires alpha2 bound extraction"),
        ("EQ1942_5_zeta", "zeta_R11", "nonconservation residual in PPN zeta_i sector", "momentum/conservation tests", "requires divergence/exchange law"),
        ("EQ1942_6_light", "Delta_theta_R11", "Delta theta = Delta theta_GR + F_gamma(delta_gamma)+F_extra(R11)", "light bending", "needs observable map"),
        ("EQ1942_7_shapiro", "Delta_t_R11", "Delta t = Delta t_GR + F_gamma(delta_gamma)+F_extra(R11)", "time delay", "Cassini-style observable map needed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "equation_id": equation_id,
            "residual_symbol": residual_symbol,
            "symbolic_equation": symbolic_equation,
            "observable_link": observable_link,
            "acceptance_need": acceptance_need,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for equation_id, residual_symbol, symbolic_equation, observable_link, acceptance_need in rows
    ]


def solar_bound_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("BND1942_0_Cassini_gamma", "delta_gamma", "gamma-1", 2.1e-5, 2.3e-5, "dimensionless", "SOURCE_BACKED_NUMERIC_NONCLAIM", "WEB1942_0_CASSINI_GAMMA"),
        ("BND1942_1_beta_review", "delta_beta", "beta-1", "TO_EXTRACT", "TO_EXTRACT", "dimensionless", "REVIEW_SOURCE_RECORDED_PRIMARY_EXTRACTION_NEEDED", "WEB1942_1_WILL_LRR_2014"),
        ("BND1942_2_alpha1_review", "alpha1_R11", "alpha1", "TO_EXTRACT", "TO_EXTRACT", "dimensionless", "REVIEW_SOURCE_RECORDED_PRIMARY_EXTRACTION_NEEDED", "WEB1942_1_WILL_LRR_2014"),
        ("BND1942_3_alpha2_review", "alpha2_R11", "alpha2", "TO_EXTRACT", "TO_EXTRACT", "dimensionless", "REVIEW_SOURCE_RECORDED_PRIMARY_EXTRACTION_NEEDED", "WEB1942_1_WILL_LRR_2014"),
        ("BND1942_4_zeta_review", "zeta_R11", "zeta_i", "TO_EXTRACT", "TO_EXTRACT", "dimensionless", "REVIEW_SOURCE_RECORDED_PRIMARY_EXTRACTION_NEEDED", "WEB1942_1_WILL_LRR_2014"),
        ("BND1942_5_XiN_ephemeris", "Xi_N", "Newtonian residual", "TO_DERIVE", "TO_DERIVE", "1/s^2 or mapped dimensionless", "MTS_EQUATION_AND_BOUND_MAPPING_NEEDED", "local_ephemeris_future_source"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": bound_id,
            "residual_symbol": residual_symbol,
            "ppn_parameter": ppn_parameter,
            "central_or_value": central_or_value,
            "sigma_or_bound_scale": sigma_or_bound_scale,
            "units": units,
            "status": status,
            "source_ref": source_ref,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for bound_id, residual_symbol, ppn_parameter, central_or_value, sigma_or_bound_scale, units, status, source_ref in rows
    ]


def residual_acceptance_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACC1942_0_gamma", "delta_gamma", "numeric MTS delta_gamma and Cassini mapping", "abs(delta_gamma_pred - 2.1e-5) <= declared confidence scale; nonclaim until convention fixed"),
        ("ACC1942_1_beta", "delta_beta", "numeric MTS delta_beta and beta bound extraction", "abs(delta_beta_pred) <= sourced bound"),
        ("ACC1942_2_preferred_frame", "alpha1_R11,alpha2_R11", "preferred-frame residual solve", "each residual theorem-zero or below sourced bound"),
        ("ACC1942_3_newtonian", "Xi_N", "dimensionful-to-observable map", "Xi_N must be zero/bounded in solar-system regime"),
        ("ACC1942_4_all", "all residuals", "complete PPN residual vector", "local GR claim only when every row is theorem-zero or sourced below bound"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acceptance_id": acceptance_id,
            "residuals": residuals,
            "needed_input": needed_input,
            "acceptance_rule": acceptance_rule,
            "status": "RULE_RECORDED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for acceptance_id, residuals, needed_input, acceptance_rule in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1942_0_equation_map", "symbolic PPN/R11 residual equation map exists", "PASS_NONCLAIM", "equation-to-observable rows recorded"),
        ("CG1942_1_gamma_bound", "Cassini gamma bound source row exists", "PASS_NONCLAIM", "source-backed numeric gamma row recorded"),
        ("CG1942_2_numeric_residuals", "MTS predicts numeric PPN residuals", "FAIL_BLOCKED", "delta_gamma, delta_beta, alpha residuals unsolved"),
        ("CG1942_3_full_bound_ledger", "all solar-system bounds are primary-source extracted", "FAIL_BLOCKED", "only gamma is numeric; others need extraction"),
        ("CG1942_4_local_gr_ppn", "MTS passes local GR/PPN", "FAIL_BLOCKED", "residuals not theorem-zero or bounded"),
        ("CG1942_5_public_claim", "1942 is public-ready PPN proof", "FAIL_BLOCKED", "private nonclaim bound/equation checkpoint"),
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
            "decision_id": "DEC1942_0_ppn_status",
            "decision": "PPN_R11_EQUATION_MAP_CREATED_GAMMA_BOUND_ANCHORED",
            "rationale": "The local-GR test branch now has symbolic residual equations and one source-backed numeric bound.",
            "next_action": "derive delta_gamma from R11 weak-field coefficients or extract remaining primary solar-system bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1942_1_next_route",
            "decision": "ATTACK_DELTA_GAMMA_FIRST",
            "rationale": "Cassini gamma is the cleanest first numeric local-GR gate; solve/bound delta_gamma before broad PPN expansion.",
            "next_action": "derive delta_gamma_R11 from weak-field spatial metric residual or keep gamma comparison blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1942_0_primary",
            "selection_status": "selected",
            "target_doc": "1943-Y5-R2FR-delta-gamma-R11-weak-field-solve-or-Cassini-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_delta_gamma_R11_weak_field_solve_or_Cassini_bound_runner_1943.py",
            "objective": "derive delta_gamma_R11 from the weak-field spatial metric residual or build a Cassini gamma bound runner that remains blocked until numeric MTS residuals exist",
            "success_condition": "a symbolic delta_gamma_R11 expression tied to R11 coefficients, or a Cassini bound runner schema with claim=false",
            "do_not": "do not claim local GR/PPN or Cassini pass without numeric residuals and source-backed confidence convention; do not modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1942_0_project_position",
            "status": "PPN_RESIDUAL_EQUATION_MAP_AND_FIRST_BOUND_ANCHOR_CREATED",
            "summary": "1942 gives the local-GR branch its first symbolic PPN/R11 residual equation map and a source-backed Cassini gamma bound row.",
            "strongest_result": "delta_gamma is now the first concrete solar-system gate",
            "missing_piece": "derive numeric R11 residuals, especially delta_gamma_R11, or keep Cassini/local-GR comparison blocked",
            "claim_position": "local-GR/PPN public claims remain blocked",
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
    write_csv(BRANCH_COPIES["source_weight_ppn"], rows_by_name["solar_bound_ledger"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["bound_queue"], rows_by_name["solar_bound_ledger"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1942*") if artifact.is_file())


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

    add("VAL1942_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1942_01_web_sources", len(rows_by_name["web_source_register"]) == 2 and all(str(row["url"]).startswith("https://") for row in rows_by_name["web_source_register"]), "web sources recorded")
    add("VAL1942_02_equation_map", len(rows_by_name["ppn_equation_map"]) == 8 and any(row["residual_symbol"] == "delta_gamma" for row in rows_by_name["ppn_equation_map"]), "PPN residual equation map includes delta_gamma")
    gamma_rows = [row for row in rows_by_name["solar_bound_ledger"] if row["bound_id"] == "BND1942_0_Cassini_gamma"]
    add("VAL1942_03_gamma_bound", len(gamma_rows) == 1 and float(gamma_rows[0]["sigma_or_bound_scale"]) > 0, "Cassini gamma numeric bound row recorded")
    add("VAL1942_04_bound_ledger_nonclaim", len(rows_by_name["solar_bound_ledger"]) == 6 and all(str(row["valid_for_claim"]) == "False" for row in rows_by_name["solar_bound_ledger"]), "solar-system bound ledger remains nonclaim")
    add("VAL1942_05_acceptance", len(rows_by_name["residual_acceptance"]) == 5 and all(row["status"] == "RULE_RECORDED_NONCLAIM" for row in rows_by_name["residual_acceptance"]), "acceptance rules recorded nonclaim")
    add("VAL1942_06_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only nonclaim gates pass; all claim flags false")
    add("VAL1942_07_decision", any(row["decision"] == "ATTACK_DELTA_GAMMA_FIRST" for row in rows_by_name["decision"]), "delta_gamma selected first")
    add("VAL1942_08_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1943-Y5-R2FR-delta-gamma"), "1943 delta-gamma target selected")
    add("VAL1942_09_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1942_10_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1942_11_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1942_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1942_13_formalization_untouched", formalization_count == 0, f"formalization_1942_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1942_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1942 PPN R11 residual equations or solar-system bound ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1942 Y5 R2FR: PPN R11 Residual Equations or Solar-System Bound Ledger",
        "",
        "## Verdict",
        "",
        "1942 turns the local-GR residual problem into a concrete PPN testing object. The residual vector now maps into symbolic metric/observable equations, and the first source-backed numeric solar-system anchor is the Cassini `gamma-1` result.",
        "",
        "This is still nonclaim: MTS has not produced numeric `delta_gamma`, `delta_beta`, preferred-frame, or Newtonian residuals. The next best strike is `delta_gamma_R11`, because Cassini provides the clean first bound.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Web Source Register",
        "",
        markdown_table(rows_by_name["web_source_register"]),
        "",
        "## PPN/R11 Equation Map",
        "",
        markdown_table(rows_by_name["ppn_equation_map"]),
        "",
        "## Solar-System Bound Ledger",
        "",
        markdown_table(rows_by_name["solar_bound_ledger"]),
        "",
        "## Residual Acceptance Gate",
        "",
        markdown_table(rows_by_name["residual_acceptance"]),
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
        "web_source_register": web_source_register_rows(),
        "ppn_equation_map": ppn_equation_map_rows(),
        "solar_bound_ledger": solar_bound_ledger_rows(),
        "residual_acceptance": residual_acceptance_rows(),
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

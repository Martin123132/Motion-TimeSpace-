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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1940"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1939_doc": ROOT / "1939-Y5-R2FR-parent-gravity-operator-EH-or-R11-residual-Newtonian-law.md",
    "1939_validation": OUT / "P8_Y5_BRR545_1939_VALIDATION.csv",
    "1939_action": OUT / "P8_Y5_PARENT_QLOC_1939_GRAVITY_ACTION_CANDIDATE.csv",
    "1939_eh": OUT / "P8_Y5_PARENT_QLOC_1939_EH_NEWTONIAN_THEOREM.csv",
    "1939_r11": OUT / "P8_Y5_PARENT_QLOC_1939_R11_RESIDUAL_NEWTONIAN_LAW.csv",
    "1939_decision": OUT / "P8_Y5_PARENT_QLOC_1939_OPERATOR_DECISION_MATRIX.csv",
    "1939_claims": OUT / "P8_Y5_PARENT_QLOC_1939_CLAIM_GATE.csv",
    "1939_next": OUT / "P8_Y5_PARENT_QLOC_1939_NEXT_TARGET.csv",
    "1938_blockers": OUT / "P8_Y5_PARENT_QLOC_1938_GRAVITY_OPERATOR_BLOCKERS.csv",
}

NEEDLES = {
    "1939_doc": ["GAC1939_0_EH_minimal", "EH1939_2_Poisson", "VAL1939_OVERALL"],
    "1939_validation": ["VAL1939_OVERALL", "PASS"],
    "1939_action": ["GAC1939_0_EH_minimal", "GAC1939_4_residual_retained_branch"],
    "1939_eh": ["EH1939_2_Poisson", "EH1939_3_verdict"],
    "1939_r11": ["R111939_0_field_equation", "R111939_4_PPN_projection"],
    "1939_decision": ["ODM1939_1_EH_derived", "SELECTED_NEXT_DERIVATION_TARGET"],
    "1939_claims": ["CG1939_1_parent_EH_derivation", "FAIL_BLOCKED"],
    "1939_next": ["NEXT1939_0_primary", "EH-uniqueness"],
    "1938_blockers": ["GOB1938_0_operator_owner", "GOB1938_5_PPN_map"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1940_SOURCE_REGISTER.csv",
    "lovelock_assumption_gate": OUT / "P8_Y5_PARENT_QLOC_1940_LOVELOCK_ASSUMPTION_GATE.csv",
    "eh_uniqueness_theorem": OUT / "P8_Y5_PARENT_QLOC_1940_EH_UNIQUENESS_THEOREM.csv",
    "r11_residual_operator": OUT / "P8_Y5_PARENT_QLOC_1940_R11_RESIDUAL_OPERATOR_LEDGER.csv",
    "local_gr_readiness": OUT / "P8_Y5_PARENT_QLOC_1940_LOCAL_GR_READINESS_MATRIX.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1940_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1940_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1940_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1940_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1940_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_lovelock": SOURCE_WEIGHT_DOCS / "EH_UNIQUENESS_LOVELOCK_GATE_1940_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1940_CLAIM_GATE_NONCLAIM.csv",
    "operator_queue": QUEUE / "JR1940_LOVELOCK_ASSUMPTIONS_OR_R11_OPERATOR_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1940_CLAIM_GATE.csv",
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
                "needed_for": "1940 EH uniqueness Lovelock gate or R11 residual operator",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def lovelock_assumption_rows() -> list[dict[str, Any]]:
    assumptions = [
        ("LOV1940_0_dimension", "observed local spacetime is 4D", "needed because Lovelock uniqueness changes in higher dimensions", "ASSUMED_NOT_PARENT_DERIVED"),
        ("LOV1940_1_metric_only", "field variable is only g_obs/coframe equivalent with no independent connection/torsion/nonmetricity", "excludes scalar-tensor, metric-affine, torsion and vector operators", "ASSUMED_NOT_PARENT_DERIVED"),
        ("LOV1940_2_locality", "field equation is local and built from finite derivatives of g_obs", "excludes nonlocal memory kernels as part of the local operator", "ASSUMED_NOT_PARENT_DERIVED"),
        ("LOV1940_3_second_order", "metric field equations contain no derivatives higher than second order", "excludes generic R^2, f(R), and higher-curvature local terms", "ASSUMED_NOT_PARENT_DERIVED"),
        ("LOV1940_4_divergence_free", "left-hand side is identically divergence-free", "matches Hilbert source conservation", "CONDITIONALLY_SUPPORTED_BY_BIANCHI"),
        ("LOV1940_5_symmetric_rank2", "operator is a symmetric rank-2 tensor built naturally from g_obs", "targets the gravitational field equation source slot", "ASSUMED_NOT_PARENT_DERIVED"),
        ("LOV1940_6_boundary_topological", "4D Gauss-Bonnet/topological terms do not alter local bulk equations", "keeps EH+Lambda as the local bulk operator", "STANDARD_CONDITIONAL"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "assumption_id": assumption_id,
            "assumption": assumption,
            "why_needed": why_needed,
            "status": status,
            "if_unsigned": "R11/residual operator branch remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for assumption_id, assumption, why_needed, status in assumptions
    ]


def eh_uniqueness_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHU1940_0_lovelock_form",
            "statement": "Under 4D, local, metric-only, second-order, divergence-free symmetric tensor assumptions, the bulk gravitational operator is G_mn+Lambda g_mn.",
            "proof_status": "STANDARD_CONDITIONAL_UNIQUENESS",
            "formula": "E_mn = a G_mn + b g_mn",
            "remaining_debt": "the MTS parent has not signed all assumptions as mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHU1940_1_kappa_normalization",
            "statement": "The overall coefficient is fixed by matching the Newtonian Poisson equation.",
            "proof_status": "EXACT_CONDITIONAL_NORMALIZATION",
            "formula": "kappa=8*pi*G/c^4",
            "remaining_debt": "G remains an empirical normalization unless derived by deeper MTS units/scale setting",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHU1940_2_local_GR_branch",
            "statement": "If all Lovelock assumptions are parent-signed and R11 residual is zero/silent, the local operator reduces to EH/GR.",
            "proof_status": "CONDITIONAL_LOCAL_GR_OPERATOR_BRANCH",
            "formula": "G_mn+Lambda g_mn=kappa T_mn",
            "remaining_debt": "R11 zero/silence and observed-frame PPN map remain to be signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHU1940_3_verdict",
            "statement": "MTS derives EH uniqueness as a parent theorem.",
            "proof_status": "NOT_DERIVED_AS_PARENT_CLAIM",
            "formula": "EH is conditionally forced, not unconditionally derived",
            "remaining_debt": "sign the Lovelock assumptions from MTS parent geometry or carry R11 residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def r11_residual_operator_rows() -> list[dict[str, Any]]:
    residuals = [
        ("R111940_0_extra_dimension_or_memory", "operator depends on hidden/memory/extra-dimensional structure", "violates metric-only/local Lovelock assumptions", "DEFINE_OR_BOUND"),
        ("R111940_1_higher_derivative_curvature", "R^2, f(R), Weyl^2, or higher-curvature effective terms", "violates second-order assumption unless degenerate/topological", "DEFINE_OR_BOUND"),
        ("R111940_2_nonlocal_kernel", "nonlocal memory kernel in gravitational operator", "violates locality assumption", "DEFINE_OR_BOUND"),
        ("R111940_3_metric_affine_torsion", "independent connection/torsion/nonmetricity residual", "violates metric-only assumption", "DEFINE_OR_BOUND"),
        ("R111940_4_stress_exchange", "nonzero divergence balanced by exchange current", "requires conservation law beyond Hilbert source", "DEFINE_OR_BOUND"),
        ("R111940_5_ppn_residual", "weak-field residual vector affecting gamma,beta/preferred-frame terms", "needed for local solar-system gate", "DEFINE_OR_BOUND"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "residual_family": residual_family,
            "why_lovelock_does_not_kill_it": why_lovelock_does_not_kill_it,
            "required_action": required_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for residual_id, residual_family, why_lovelock_does_not_kill_it, required_action in residuals
    ]


def local_gr_readiness_rows() -> list[dict[str, Any]]:
    rows = [
        ("READY1940_0_matter_source", "universal Hilbert matter source", "READY_CONDITIONALLY", "1937/1938 candidate matter source"),
        ("READY1940_1_conservation", "Ward/Bianchi matter conservation", "READY_CONDITIONALLY", "1938 conservation theorem"),
        ("READY1940_2_EH_operator", "EH operator under Lovelock assumptions", "READY_CONDITIONALLY", "1940 conditional uniqueness"),
        ("READY1940_3_kappa", "Newtonian normalization", "READY_CONDITIONALLY", "matched to G; not deeper-derived"),
        ("READY1940_4_assumption_signature", "MTS parent signs Lovelock assumptions", "BLOCKED", "assumptions not parent-derived"),
        ("READY1940_5_R11_silence", "R11/residual operator zero or bounded", "BLOCKED", "residual families live"),
        ("READY1940_6_PPN_map", "gamma,beta and preferred-frame residual map", "BLOCKED", "not yet derived"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "readiness_id": readiness_id,
            "criterion": criterion,
            "status": status,
            "basis_or_blocker": basis_or_blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for readiness_id, criterion, status, basis_or_blocker in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1940_0_EH_uniqueness_conditional", "Lovelock assumptions force EH+Lambda", "PASS_NONCLAIM", "conditional uniqueness theorem recorded"),
        ("CG1940_1_kappa_conditional", "kappa normalization gives Newtonian Poisson law", "PASS_NONCLAIM", "conditional normalization recorded"),
        ("CG1940_2_parent_assumptions", "MTS parent signs all Lovelock assumptions", "FAIL_BLOCKED", "assumptions are not parent-derived"),
        ("CG1940_3_R11_silence", "R11/residual branch is zero or bounded locally", "FAIL_BLOCKED", "residual families require definition/bounds"),
        ("CG1940_4_local_GR_PPN", "local GR/PPN is derived", "FAIL_BLOCKED", "PPN map and residual vector missing"),
        ("CG1940_5_public_claim", "1940 is public-ready EH/local-GR proof", "FAIL_BLOCKED", "private conditional theorem checkpoint only"),
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
            "decision_id": "DEC1940_0_eh_status",
            "decision": "EH_FORCED_ONLY_UNDER_LOVELOCK_ASSUMPTIONS",
            "rationale": "This is a strong conditional route to GR, but not a parent MTS derivation until assumptions are signed.",
            "next_action": "audit which Lovelock assumptions MTS can truly derive from motion/time/space parent principles",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1940_1_residual_status",
            "decision": "R11_REMAINS_THE_EXPLICIT_NOVELTY_BRANCH",
            "rationale": "Any violation of metric-only/local/second-order assumptions belongs in a named residual family.",
            "next_action": "pick either assumption-signature audit or PPN residual vector construction",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1940_0_primary",
            "selection_status": "selected",
            "target_doc": "1941-Y5-R2FR-Lovelock-assumption-signature-audit-or-PPN-residual-vector.md",
            "target_script": "scripts/Y5_R2FR_Lovelock_assumption_signature_audit_or_PPN_residual_vector_1941.py",
            "objective": "audit whether MTS parent principles sign 4D, metric-only, local, second-order, divergence-free assumptions; if not, construct the first PPN/R11 residual vector ledger",
            "success_condition": "a signed assumption subset sufficient for EH/local-GR branch, or a PPN residual vector with claims blocked",
            "do_not": "do not claim EH/local GR unless assumptions and residual silence are signed; do not modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1940_0_project_position",
            "status": "EH_CONDITIONAL_ROUTE_SHARP_R11_BRANCH_ACTIVE",
            "summary": "1940 makes the GR route precise: if MTS signs Lovelock assumptions, EH+Lambda is forced locally; if not, every violation becomes an R11 residual family.",
            "strongest_result": "conditional EH uniqueness and Newtonian normalization are now explicit",
            "missing_piece": "parent signature of Lovelock assumptions, R11 silence/bounds, and PPN residual map",
            "claim_position": "local-GR/Newton public claims remain blocked",
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
    write_csv(BRANCH_COPIES["source_weight_lovelock"], rows_by_name["eh_uniqueness_theorem"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["operator_queue"], rows_by_name["lovelock_assumption_gate"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1940*") if artifact.is_file())


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

    add("VAL1940_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1940_01_assumptions", len(rows_by_name["lovelock_assumption_gate"]) == 7 and any(row["status"] == "ASSUMED_NOT_PARENT_DERIVED" for row in rows_by_name["lovelock_assumption_gate"]), "Lovelock assumptions explicit and not over-promoted")
    add("VAL1940_02_eh_uniqueness", any(row["proof_status"] == "STANDARD_CONDITIONAL_UNIQUENESS" for row in rows_by_name["eh_uniqueness_theorem"]) and any(row["proof_status"] == "NOT_DERIVED_AS_PARENT_CLAIM" for row in rows_by_name["eh_uniqueness_theorem"]), "EH uniqueness conditional and not claimed as parent-derived")
    add("VAL1940_03_r11_residuals", len(rows_by_name["r11_residual_operator"]) == 6 and all(row["required_action"] == "DEFINE_OR_BOUND" for row in rows_by_name["r11_residual_operator"]), "R11 residual families require define-or-bound treatment")
    add("VAL1940_04_readiness", any(row["status"] == "READY_CONDITIONALLY" for row in rows_by_name["local_gr_readiness"]) and any(row["status"] == "BLOCKED" for row in rows_by_name["local_gr_readiness"]), "readiness matrix separates conditional ready pieces from blockers")
    add("VAL1940_05_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only nonclaim gates pass; all claim flags false")
    add("VAL1940_06_decision", any(row["decision"] == "EH_FORCED_ONLY_UNDER_LOVELOCK_ASSUMPTIONS" for row in rows_by_name["decision"]), "EH conditional status decision recorded")
    add("VAL1940_07_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1941-Y5-R2FR-Lovelock-assumption"), "1941 assumption audit/PPN residual target selected")
    add("VAL1940_08_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1940_09_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1940_10_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1940_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1940_12_formalization_untouched", formalization_count == 0, f"formalization_1940_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1940_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1940 EH uniqueness Lovelock gate or R11 residual operator",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1940 Y5 R2FR: EH Uniqueness Lovelock Gate or R11 Residual Operator",
        "",
        "## Verdict",
        "",
        "1940 makes the GR route precise. Under the Lovelock-style assumptions — 4D, metric-only, local, second-order, symmetric divergence-free field equations — the local bulk operator is forced to EH plus Lambda. That gives a strong conditional route to local GR/Newton.",
        "",
        "But the assumptions are not yet parent-signed by MTS. Therefore EH is conditionally forced, not unconditionally derived. Every violation of those assumptions is now routed into an explicit R11 residual family that must be defined or bounded before any local-GR claim.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Lovelock Assumption Gate",
        "",
        markdown_table(rows_by_name["lovelock_assumption_gate"]),
        "",
        "## EH Uniqueness Theorem",
        "",
        markdown_table(rows_by_name["eh_uniqueness_theorem"]),
        "",
        "## R11 Residual Operator Ledger",
        "",
        markdown_table(rows_by_name["r11_residual_operator"]),
        "",
        "## Local GR Readiness Matrix",
        "",
        markdown_table(rows_by_name["local_gr_readiness"]),
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
        "lovelock_assumption_gate": lovelock_assumption_rows(),
        "eh_uniqueness_theorem": eh_uniqueness_theorem_rows(),
        "r11_residual_operator": r11_residual_operator_rows(),
        "local_gr_readiness": local_gr_readiness_rows(),
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

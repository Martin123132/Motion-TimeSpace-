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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1941"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1941-Y5-R2FR-Lovelock-assumption-signature-audit-or-PPN-residual-vector.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1940_doc": ROOT / "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md",
    "1940_validation": OUT / "P8_Y5_BRR545_1940_VALIDATION.csv",
    "1940_assumptions": OUT / "P8_Y5_PARENT_QLOC_1940_LOVELOCK_ASSUMPTION_GATE.csv",
    "1940_eh": OUT / "P8_Y5_PARENT_QLOC_1940_EH_UNIQUENESS_THEOREM.csv",
    "1940_r11": OUT / "P8_Y5_PARENT_QLOC_1940_R11_RESIDUAL_OPERATOR_LEDGER.csv",
    "1940_readiness": OUT / "P8_Y5_PARENT_QLOC_1940_LOCAL_GR_READINESS_MATRIX.csv",
    "1940_claims": OUT / "P8_Y5_PARENT_QLOC_1940_CLAIM_GATE.csv",
    "1940_next": OUT / "P8_Y5_PARENT_QLOC_1940_NEXT_TARGET.csv",
    "1939_r11": OUT / "P8_Y5_PARENT_QLOC_1939_R11_RESIDUAL_NEWTONIAN_LAW.csv",
    "1938_pass": OUT / "P8_Y5_PARENT_QLOC_1938_CANDIDATE_PASS_MATRIX.csv",
}

NEEDLES = {
    "1940_doc": ["EHU1940_0_lovelock_form", "READY1940_4_assumption_signature", "VAL1940_OVERALL"],
    "1940_validation": ["VAL1940_OVERALL", "PASS"],
    "1940_assumptions": ["LOV1940_0_dimension", "LOV1940_6_boundary_topological"],
    "1940_eh": ["EHU1940_0_lovelock_form", "EHU1940_3_verdict"],
    "1940_r11": ["R111940_0_extra_dimension_or_memory", "R111940_5_ppn_residual"],
    "1940_readiness": ["READY1940_4_assumption_signature", "READY1940_6_PPN_map"],
    "1940_claims": ["CG1940_4_local_GR_PPN", "FAIL_BLOCKED"],
    "1940_next": ["NEXT1940_0_primary", "PPN-residual"],
    "1939_r11": ["R111939_2_Newtonian_projection", "R111939_4_PPN_projection"],
    "1938_pass": ["PASS1938_5_local_GR_PPN", "BLOCKED_DOWNSTREAM"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1941_SOURCE_REGISTER.csv",
    "assumption_signature_audit": OUT / "P8_Y5_PARENT_QLOC_1941_LOVELOCK_ASSUMPTION_SIGNATURE_AUDIT.csv",
    "signed_subset": OUT / "P8_Y5_PARENT_QLOC_1941_SIGNED_SUBSET_AND_FAILURES.csv",
    "ppn_residual_vector": OUT / "P8_Y5_PARENT_QLOC_1941_PPN_R11_RESIDUAL_VECTOR.csv",
    "solar_system_gate": OUT / "P8_Y5_PARENT_QLOC_1941_SOLAR_SYSTEM_TEST_GATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1941_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1941_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1941_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1941_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1941_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_assumptions": SOURCE_WEIGHT_DOCS / "LOVELOCK_ASSUMPTION_SIGNATURE_AUDIT_1941_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1941_CLAIM_GATE_NONCLAIM.csv",
    "ppn_queue": QUEUE / "JR1941_PPN_R11_RESIDUAL_VECTOR_ACQUISITION_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1941_CLAIM_GATE.csv",
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
                "needed_for": "1941 Lovelock assumption signature audit or PPN residual vector",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def assumption_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("AUD1941_0_dimension", "4D observed local spacetime", "PARTIALLY_SIGNABLE_AS_EFFECTIVE_OBSERVED_ARENA", "corpus uses 4D local tests but parent derivation of dimension is not closed", "PPN branch may assume observed 4D as test arena only"),
        ("AUD1941_1_metric_only", "only g_obs/coframe field, no independent connection/torsion/nonmetricity", "NOT_PARENT_SIGNED", "MTS hidden/memory/flow structure may create extra geometric variables", "R11 metric-affine/torsion/nonmetric residual remains live"),
        ("AUD1941_2_locality", "local finite-derivative gravitational equation", "NOT_PARENT_SIGNED", "memory/cosmology branches allow nonlocal or history-dependent structure", "R11 nonlocal kernel residual remains live"),
        ("AUD1941_3_second_order", "second-order metric equations", "NOT_PARENT_SIGNED", "higher-curvature/effective corrections are not parent-forbidden", "R11 higher-derivative residual remains live"),
        ("AUD1941_4_divergence_free", "divergence-free left-hand side", "CONDITIONALLY_SIGNABLE", "Bianchi compatibility required by Hilbert source conservation", "residual branch needs divergence law or exchange current"),
        ("AUD1941_5_symmetric_rank2", "symmetric rank-2 metric source slot", "CONDITIONALLY_SIGNABLE", "Hilbert source is symmetric rank-2 if metric/coframe action is adopted", "extra fields still project into residual vector"),
        ("AUD1941_6_boundary_topological", "topological/boundary terms do not affect local bulk equations", "CONDITIONALLY_SIGNABLE_FOR_BULK_ONLY", "bulk local tests can ignore pure boundary terms only if projection maps are silent", "boundary/local projection residual remains live"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "assumption": assumption,
            "signature_status": signature_status,
            "reason": reason,
            "consequence": consequence,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for audit_id, assumption, signature_status, reason, consequence in rows
    ]


def signed_subset_rows() -> list[dict[str, Any]]:
    rows = [
        ("SUB1941_0_ready_conditionally", "Hilbert matter source + conservation + symmetric stress tensor", "CONDITIONAL_SUBSET", "supports source side of local GR"),
        ("SUB1941_1_arena_assumption", "4D observed weak-field test arena", "TEST_ARENA_ASSUMPTION_ONLY", "usable for PPN testing but not parent derivation"),
        ("SUB1941_2_failed_parent_signature", "metric-only/local/second-order operator", "FAILED_PARENT_SIGNATURE", "prevents unconditional EH derivation"),
        ("SUB1941_3_residual_requirement", "R11 residual vector must absorb every failed assumption", "ACTIVE_REQUIREMENT", "prevents hidden deviations from being lost"),
        ("SUB1941_4_verdict", "signed subset sufficient for full EH/local-GR branch", "NO", "not sufficient until metric-only/local/second-order and R11 silence are signed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "subset_id": subset_id,
            "item": item,
            "status": status,
            "effect": effect,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for subset_id, item, status, effect in rows
    ]


def ppn_residual_vector_rows() -> list[dict[str, Any]]:
    rows = [
        ("PPN1941_0_newtonian_residual", "Xi_N", "nabla^2 Phi = 4*pi*G*rho + Xi_N", "captures R11 Newtonian source correction", "MISSING_RESIDUAL_PROJECTION"),
        ("PPN1941_1_gamma_residual", "delta_gamma", "gamma = 1 + delta_gamma", "spatial curvature per unit Newtonian potential", "MISSING_PPN_SOLVE"),
        ("PPN1941_2_beta_residual", "delta_beta", "beta = 1 + delta_beta", "nonlinear superposition/self-interaction residual", "MISSING_PPN_SOLVE"),
        ("PPN1941_3_preferred_frame_alpha1", "alpha1_R11", "alpha1 = alpha1_R11", "preferred-frame/vector/flow residual", "MISSING_FRAME_MAP"),
        ("PPN1941_4_preferred_frame_alpha2", "alpha2_R11", "alpha2 = alpha2_R11", "preferred-frame anisotropy residual", "MISSING_FRAME_MAP"),
        ("PPN1941_5_nonconservation_zeta", "zeta_R11", "zeta_i residuals", "stress exchange/nonconservation residual if R11 divergence is not zero", "MISSING_DIVERGENCE_LAW"),
        ("PPN1941_6_light_deflection", "Delta_theta_R11", "theta = theta_GR + Delta_theta_R11", "observable lensing/deflection residual", "MISSING_OBSERVABLE_MAP"),
        ("PPN1941_7_shapiro", "Delta_t_R11", "Delta t = Delta t_GR + Delta_t_R11", "time-delay residual", "MISSING_OBSERVABLE_MAP"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for residual_id, symbol, definition, meaning, status in rows
    ]


def solar_system_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("SS1941_0_Cassini_gamma", "delta_gamma", "must be near zero at solar-system scale", "BOUND_SOURCE_NEEDED"),
        ("SS1941_1_ephemeris_beta", "delta_beta", "must be near zero in planetary dynamics", "BOUND_SOURCE_NEEDED"),
        ("SS1941_2_preferred_frame", "alpha1_R11, alpha2_R11", "must be bounded by preferred-frame tests", "BOUND_SOURCE_NEEDED"),
        ("SS1941_3_lunar_laser", "eta_Nordtvedt_R11", "strong-equivalence/material self-energy residual", "BOUND_SOURCE_NEEDED"),
        ("SS1941_4_clock_shapiro", "Delta_t_R11", "time-delay/redshift consistency", "BOUND_SOURCE_NEEDED"),
        ("SS1941_5_acceptance_rule", "all residuals", "local GR only if every residual is theorem-zero or below sourced bound", "RULE_RECORDED_NONCLAIM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": test_id,
            "residual_symbol": residual_symbol,
            "acceptance_need": acceptance_need,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for test_id, residual_symbol, acceptance_need, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1941_0_assumption_audit", "Lovelock assumption audit completed", "PASS_NONCLAIM", "signed subset and failures recorded"),
        ("CG1941_1_ppn_vector", "first PPN/R11 residual vector exists", "PASS_NONCLAIM", "residual symbols and observable slots recorded"),
        ("CG1941_2_eh_parent_signature", "MTS signs all EH/Lovelock assumptions", "FAIL_BLOCKED", "metric-only/local/second-order not parent-signed"),
        ("CG1941_3_r11_silence", "R11 residual vector is theorem-zero or bounded", "FAIL_BLOCKED", "PPN residuals lack solve/bounds"),
        ("CG1941_4_local_gr_claim", "MTS derives local GR/PPN", "FAIL_BLOCKED", "needs residual zero/bounds and PPN map"),
        ("CG1941_5_public_claim", "1941 is public-ready local-GR proof", "FAIL_BLOCKED", "private residual-vector checkpoint only"),
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
            "decision_id": "DEC1941_0_assumption_status",
            "decision": "LOVELOCK_ASSUMPTIONS_NOT_FULLY_PARENT_SIGNED",
            "rationale": "Only conservation/symmetric-source pieces are conditionally ready; metric-only, locality, and second-order are still assumptions.",
            "next_action": "stop treating EH as derived; carry PPN/R11 residual vector until assumptions or bounds close it",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1941_1_next_route",
            "decision": "BUILD_PPN_RESIDUAL_SOLVER_OR_BOUND_RUNNER_NEXT",
            "rationale": "The residual vector makes local-GR testing concrete; next step is solve/bound delta_gamma, delta_beta, preferred-frame and Newtonian residuals.",
            "next_action": "construct symbolic PPN residual equations or source solar-system bounds without claiming a pass",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1941_0_primary",
            "selection_status": "selected",
            "target_doc": "1942-Y5-R2FR-PPN-R11-residual-equations-or-solar-system-bound-ledger.md",
            "target_script": "scripts/Y5_R2FR_PPN_R11_residual_equations_or_solar_system_bound_ledger_1942.py",
            "objective": "derive symbolic equations for Xi_N, delta_gamma, delta_beta, alpha1_R11, alpha2_R11, and related R11/PPN residuals, or source the first solar-system bound ledger with claims blocked",
            "success_condition": "a symbolic residual-equation map to PPN observables, or a source-backed bound ledger with all local-GR claims still blocked",
            "do_not": "do not claim local GR/PPN unless residuals are theorem-zero or bounded; do not modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1941_0_project_position",
            "status": "LOVELOCK_ASSUMPTIONS_PARTIAL_PPN_RESIDUAL_VECTOR_CREATED",
            "summary": "1941 shows MTS has a conditional EH route but has not parent-signed the assumptions; the first explicit PPN/R11 residual vector is now available.",
            "strongest_result": "local-GR blockers are now concrete residuals rather than vague caveats",
            "missing_piece": "derive or bound Xi_N, delta_gamma, delta_beta, preferred-frame and observable residual maps",
            "claim_position": "local-GR/Newton/PPN public claims remain blocked",
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
    write_csv(BRANCH_COPIES["source_weight_assumptions"], rows_by_name["assumption_signature_audit"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["ppn_queue"], rows_by_name["ppn_residual_vector"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1941*") if artifact.is_file())


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

    add("VAL1941_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1941_01_assumption_audit", len(rows_by_name["assumption_signature_audit"]) == 7 and any(row["signature_status"] == "NOT_PARENT_SIGNED" for row in rows_by_name["assumption_signature_audit"]), "assumption audit identifies unsigned Lovelock assumptions")
    add("VAL1941_02_signed_subset", any(row["status"] == "FAILED_PARENT_SIGNATURE" for row in rows_by_name["signed_subset"]) and any(row["status"] == "NO" for row in rows_by_name["signed_subset"]), "signed subset not sufficient for local GR claim")
    add("VAL1941_03_ppn_vector", len(rows_by_name["ppn_residual_vector"]) == 8 and all(str(row["status"]).startswith("MISSING_") for row in rows_by_name["ppn_residual_vector"]), "PPN/R11 residual vector created and unresolved")
    add("VAL1941_04_solar_system_gate", len(rows_by_name["solar_system_gate"]) == 6 and all(str(row["status"]).endswith("NEEDED") or str(row["status"]).startswith("RULE_") for row in rows_by_name["solar_system_gate"]), "solar-system bound needs recorded")
    add("VAL1941_05_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only nonclaim gates pass; all claim flags false")
    add("VAL1941_06_decision", any(row["decision"] == "BUILD_PPN_RESIDUAL_SOLVER_OR_BOUND_RUNNER_NEXT" for row in rows_by_name["decision"]), "PPN residual solver/bound runner selected next")
    add("VAL1941_07_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1942-Y5-R2FR-PPN-R11-residual"), "1942 PPN residual target selected")
    add("VAL1941_08_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1941_09_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1941_10_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1941_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1941_12_formalization_untouched", formalization_count == 0, f"formalization_1941_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1941_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1941 Lovelock assumption signature audit or PPN residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1941 Y5 R2FR: Lovelock Assumption Signature Audit or PPN Residual Vector",
        "",
        "## Verdict",
        "",
        "1941 finds that MTS has a strong conditional EH route but not a fully parent-signed Lovelock route. The source/conservation side is in decent shape; metric-only, locality, and second-order operator assumptions are still not parent-derived.",
        "",
        "The forward move is concrete: the first PPN/R11 residual vector is now named. Local-GR testing is no longer a vague missing step; it is `Xi_N`, `delta_gamma`, `delta_beta`, preferred-frame residuals, nonconservation residuals, and observable light/time-delay residuals.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Lovelock Assumption Signature Audit",
        "",
        markdown_table(rows_by_name["assumption_signature_audit"]),
        "",
        "## Signed Subset and Failures",
        "",
        markdown_table(rows_by_name["signed_subset"]),
        "",
        "## PPN/R11 Residual Vector",
        "",
        markdown_table(rows_by_name["ppn_residual_vector"]),
        "",
        "## Solar-System Test Gate",
        "",
        markdown_table(rows_by_name["solar_system_gate"]),
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
        "assumption_signature_audit": assumption_audit_rows(),
        "signed_subset": signed_subset_rows(),
        "ppn_residual_vector": ppn_residual_vector_rows(),
        "solar_system_gate": solar_system_gate_rows(),
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

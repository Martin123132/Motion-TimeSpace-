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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1936"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1935_doc": ROOT / "1935-Y5-R2FR-MTS-WEP-eta-projection-map-or-material-charge-ledger.md",
    "1935_validation": OUT / "P8_Y5_BRR545_1935_VALIDATION.csv",
    "1935_eta_theorem": OUT / "P8_Y5_PARENT_QLOC_1935_WEP_ETA_PROJECTION_THEOREM.csv",
    "1935_contract": OUT / "P8_Y5_PARENT_QLOC_1935_MTS_WEP_PROJECTION_CONTRACT.csv",
    "1935_product": OUT / "P8_Y5_PARENT_QLOC_1935_WEP_PRODUCT_BOUND_TARGET.csv",
    "1935_material": OUT / "P8_Y5_PARENT_QLOC_1935_MATERIAL_CHARGE_LEDGER.csv",
    "1935_claims": OUT / "P8_Y5_PARENT_QLOC_1935_CLAIM_GATE.csv",
    "1935_next": OUT / "P8_Y5_PARENT_QLOC_1935_NEXT_TARGET.csv",
    "1931_signature": OUT / "P8_Y5_PARENT_QLOC_1931_PARENT_SIGNATURE_LEDGER.csv",
}

NEEDLES = {
    "1935_doc": ["ETA1935_4_mts_source_weight_form", "MAT1935_6_universality_theorem", "VAL1935_OVERALL"],
    "1935_validation": ["VAL1935_OVERALL", "PASS"],
    "1935_eta_theorem": ["ETA1935_3_universal_part_cancels", "ETA1935_4_mts_source_weight_form"],
    "1935_contract": ["CON1935_1_material_weight_difference", "CON1935_3_transfer_factor"],
    "1935_product": ["PB1935_0_linear_WEP_product_target", "PB1935_1_exact_WEP_product_contract"],
    "1935_material": ["MAT1935_0_Ti_alloy", "MAT1935_6_universality_theorem"],
    "1935_claims": ["CG1935_5_local_GR_Newton", "FAIL_BLOCKED"],
    "1935_next": ["NEXT1935_0_primary", "source-weight-universality"],
    "1931_signature": ["SIG1931_4_source_weight_exclusion", "SIG1931_10_verdict"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1936_SOURCE_REGISTER.csv",
    "universality_attempt": OUT / "P8_Y5_PARENT_QLOC_1936_SOURCE_WEIGHT_UNIVERSALITY_ATTEMPT.csv",
    "hilbert_contract": OUT / "P8_Y5_PARENT_QLOC_1936_HILBERT_SOURCE_CONTRACT.csv",
    "tipt_material_ledger": OUT / "P8_Y5_PARENT_QLOC_1936_TIPT_MATERIAL_CHARGE_LEDGER.csv",
    "wep_implication": OUT / "P8_Y5_PARENT_QLOC_1936_WEP_ETA_IMPLICATION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1936_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1936_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1936_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1936_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1936_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_universality": SOURCE_WEIGHT_DOCS / "SOURCE_WEIGHT_UNIVERSALITY_CONTRACT_1936_NONCLAIM.csv",
    "microscope_material": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1936_TIPT_MATERIAL_CHARGE_LEDGER_NONCLAIM.csv",
    "hilbert_queue": QUEUE / "JR1936_PARENT_HILBERT_SOURCE_COUPLING_SIGNATURE_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1936_CLAIM_GATE.csv",
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
                "needed_for": "1936 source-weight universality theorem or Ti/Pt material charge ledger",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def universality_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "UNIV1936_0_target",
            "claim": "ordinary matter has universal source weight, DeltaW_AB=0",
            "formal_condition": "all ordinary matter couples to one observed metric/coframe through the same Hilbert stress-energy source",
            "result": "TARGET_NOT_PARENT_SIGNED",
            "proof_or_obstruction": "1931 still marks source-weight exclusion as conditional/unsigned",
            "wep_effect": "would kill composition residuals for MICROSCOPE if signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "UNIV1936_1_hilbert_source_theorem",
            "claim": "universal Hilbert coupling implies no species-dependent gravitational source weight in the test-body limit",
            "formal_condition": "S_matter=sum_A S_A[psi_A,g_obs,theta_A] with no independent w_A coefficient and source T_mn=-2/sqrt(-g) delta S_matter/delta g^mn",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "the same metric variation defines the gravitational source for all ordinary sectors; composition enters inertial/internal energy, not a separate free-fall charge",
            "wep_effect": "DeltaW_AB=0 if all nonmetric coefficients are absent",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "UNIV1936_2_common_shift_cancels",
            "claim": "a universal source rescaling can be absorbed into measured GM but not a composition difference",
            "formal_condition": "W_A=W_univ for all A",
            "result": "EXACT_WEP_CANCELLATION",
            "proof_or_obstruction": "eta_AB depends on epsilon_A-epsilon_B, so the common term cancels",
            "wep_effect": "measured-G shift is not a WEP violation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "UNIV1936_3_nonmetric_counterterms",
            "claim": "ordinary covariance alone forbids species-dependent source weights",
            "formal_condition": "allow w_A(I_hid) T_A or species labels inside source coupling",
            "result": "FALSE_WITH_CURRENT_ASSUMPTIONS",
            "proof_or_obstruction": "scalar source weights remain ordinary-covariant unless parent object-language forbids them",
            "wep_effect": "Ti/Pt material charge ledger remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "UNIV1936_4_verdict",
            "claim": "MTS currently derives DeltaW_AB=0 for ordinary matter",
            "formal_condition": "parent-signed universal Hilbert source coupling plus no nonmetric/material coefficients",
            "result": "UNIVERSALITY_NOT_DERIVED",
            "proof_or_obstruction": "conditional theorem is strong, but its parent hypotheses are still unsigned",
            "wep_effect": "no WEP/local-GR claim; move to parent Hilbert source signature or finite material-charge rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def hilbert_contract_rows() -> list[dict[str, Any]]:
    clauses = [
        ("HIL1936_0_single_observed_metric", "all ordinary matter sees the same g_obs or coframe e_obs", "MISSING_PARENT_SIGNATURE"),
        ("HIL1936_1_stress_energy_owner", "the gravitational source is T_mn from Hilbert variation of the same matter action", "MISSING_PARENT_SIGNATURE"),
        ("HIL1936_2_no_species_weight", "no independent species/material coefficient w_A multiplies source coupling", "MISSING_NO_SOURCE_WEIGHT_THEOREM"),
        ("HIL1936_3_binding_included", "rest mass, kinetic energy, pressure, and binding energy enter the same T_mn source", "MISSING_BINDING_SOURCE_CONTRACT"),
        ("HIL1936_4_test_body_limit", "self-field and finite-size corrections are negligible or explicitly bounded for MICROSCOPE", "MISSING_ARENA_LIMIT"),
        ("HIL1936_5_readout_boundary_preservation", "projection/readout/boundary maps do not reintroduce species weights", "MISSING_PRESERVATION_THEOREM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "required_clause": required_clause,
            "status": status,
            "if_signed": "supports DeltaW_AB=0 and WEP/source universality",
            "if_unsigned": "retain Ti/Pt finite material-charge ledger and claim=false",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for clause_id, required_clause, status in clauses
    ]


def tipt_material_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("TIPT1936_0_Ti_weight", "W_Ti", "Ti alloy source weight", "MISSING_THEOREM_OR_SOURCE"),
        ("TIPT1936_1_Pt_weight", "W_Pt", "Pt alloy source weight", "MISSING_THEOREM_OR_SOURCE"),
        ("TIPT1936_2_universal_branch", "W_Ti=W_Pt=W_univ", "conditional if HIL1936 clauses are signed", "CONDITIONAL_ONLY_NOT_CLAIM"),
        ("TIPT1936_3_delta_branch", "DeltaW_TiPt=W_Ti-W_Pt", "finite residual if universality fails", "MISSING_NUMERIC_ROW"),
        ("TIPT1936_4_tau_source_product", "P_WEP=tau_WEP*S_Earth", "transfer from source weight to acceleration residual", "MISSING_TRANSFER_PRODUCT"),
        ("TIPT1936_5_eta_target", "eta_TiPt=2P DeltaW/(2+P SigmaW)", "MICROSCOPE comparison formula from 1935", "FORMULA_READY_INPUTS_MISSING"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "valid_for_numeric_comparison": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for row_id, symbol, meaning, status in rows
    ]


def wep_implication_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "implication_id": "IMP1936_0_universality_to_eta_zero",
            "premise": "DeltaW_TiPt=0",
            "formula": "eta_TiPt=2P*0/(2+P*SigmaW)=0",
            "status": "EXACT_CONDITIONAL_IMPLICATION",
            "claim_blocker": "DeltaW_TiPt=0 is not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "implication_id": "IMP1936_1_finite_residual_bound",
            "premise": "DeltaW_TiPt not proven zero",
            "formula": "|P_WEP*DeltaW_TiPt| <= 2.7e-15 in the linear residual regime",
            "status": "NONCLAIM_BOUND_TARGET",
            "claim_blocker": "P_WEP and DeltaW_TiPt missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1936_0_hilbert_conditional", "universal Hilbert coupling implies DeltaW_AB=0", "PASS_NONCLAIM", "conditional theorem recorded"),
        ("CG1936_1_parent_signature", "MTS parent signs universal Hilbert source coupling", "FAIL_BLOCKED", "required HIL1936 clauses unsigned"),
        ("CG1936_2_source_weight_zero", "DeltaW_TiPt is theorem-zero", "FAIL_BLOCKED", "universality theorem not parent-signed"),
        ("CG1936_3_material_charge_numeric", "Ti/Pt material charges are numeric", "FAIL_BLOCKED", "W_Ti and W_Pt missing"),
        ("CG1936_4_wep_pass", "MTS passes MICROSCOPE WEP", "FAIL_BLOCKED", "eta_pred still not numeric or theorem-zero"),
        ("CG1936_5_local_GR_Newton", "local GR/Newton source coupling is derived", "FAIL_BLOCKED", "source universality is necessary but not yet signed"),
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
            "decision_id": "DEC1936_0_universality_status",
            "decision": "SOURCE_UNIVERSALITY_CONDITIONAL_NOT_PARENT_SIGNED",
            "rationale": "Universal Hilbert coupling gives the desired WEP result, but MTS has not signed the parent clauses.",
            "next_action": "attack the parent Hilbert source-coupling signature directly",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1936_1_fallback",
            "decision": "TIPT_MATERIAL_CHARGE_LEDGER_REMAINS_ACTIVE",
            "rationale": "If the source-coupling theorem fails, MICROSCOPE testing needs actual W_Ti, W_Pt, and P_WEP rows.",
            "next_action": "do not run numeric WEP comparison until either theorem-zero or finite rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1936_0_primary",
            "selection_status": "selected",
            "target_doc": "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md",
            "target_script": "scripts/Y5_R2FR_parent_Hilbert_source_coupling_or_nonmetric_source_coefficients_1937.py",
            "objective": "prove the parent action signs universal Hilbert source coupling for ordinary matter, or demote WEP/source universality to a nonmetric source-coefficient ledger",
            "success_condition": "a parent-signed Hilbert source-coupling clause sufficient for DeltaW_AB=0, or explicit nonmetric coefficients with WEP/local-GR claims blocked",
            "do_not": "do not claim WEP pass, absorb composition dependence into measured G, set tau_WEP=1, invent material charges, claim local GR, or modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1936_0_project_position",
            "status": "SOURCE_UNIVERSALITY_REDUCED_TO_HILBERT_SIGNATURE",
            "summary": "1936 shows the WEP/source route is clean if ordinary matter has universal Hilbert coupling, but that parent signature remains unsigned.",
            "strongest_result": "universal source weight gives DeltaW_TiPt=0 and hence eta_TiPt=0 exactly",
            "missing_piece": "parent-signed single-metric Hilbert source coupling with no species/material source coefficient",
            "fallback": "Ti/Pt material-charge ledger remains active for finite nonclaim testing",
            "claim_position": "WEP/local-GR/Newton claims remain blocked",
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
    write_csv(BRANCH_COPIES["source_weight_universality"], rows_by_name["universality_attempt"])
    write_csv(BRANCH_COPIES["microscope_material"], rows_by_name["tipt_material_ledger"])
    write_csv(BRANCH_COPIES["hilbert_queue"], rows_by_name["hilbert_contract"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1936*") if artifact.is_file())


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

    add("VAL1936_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1936_01_universality_attempt", any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_by_name["universality_attempt"]) and any(row["result"] == "UNIVERSALITY_NOT_DERIVED" for row in rows_by_name["universality_attempt"]), "conditional Hilbert theorem retained without promotion")
    add("VAL1936_02_hilbert_contract", len(rows_by_name["hilbert_contract"]) == 6 and all(str(row["status"]).startswith("MISSING_") for row in rows_by_name["hilbert_contract"]), "Hilbert source contract blockers named")
    add("VAL1936_03_tipt_ledger", len(rows_by_name["tipt_material_ledger"]) == 6 and all(str(row["status"]) != "NUMERIC_CLAIM_READY" for row in rows_by_name["tipt_material_ledger"]), "Ti/Pt material ledger remains nonnumeric")
    add("VAL1936_04_wep_implication", any(row["status"] == "EXACT_CONDITIONAL_IMPLICATION" for row in rows_by_name["wep_implication"]) and any(row["status"] == "NONCLAIM_BOUND_TARGET" for row in rows_by_name["wep_implication"]), "eta-zero implication and finite bound target both recorded")
    add("VAL1936_05_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only conditional theorem gate passes as nonclaim; all claim flags false")
    add("VAL1936_06_decision", any(row["decision"] == "SOURCE_UNIVERSALITY_CONDITIONAL_NOT_PARENT_SIGNED" for row in rows_by_name["decision"]), "source universality remains conditional")
    add("VAL1936_07_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1937-Y5-R2FR-parent-Hilbert-source"), "1937 parent Hilbert source target selected")
    add("VAL1936_08_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1936_09_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1936_10_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1936_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1936_12_formalization_untouched", formalization_count == 0, f"formalization_1936_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1936_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1936 source-weight universality theorem or Ti/Pt material charge ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1936 Y5 R2FR: Source-Weight Universality Theorem or Ti/Pt Material Charge Ledger",
        "",
        "## Verdict",
        "",
        "1936 gets the WEP/source-coupling branch into a much cleaner shape. If ordinary matter is coupled through one universal Hilbert stress-energy source, then the composition source-weight difference vanishes: `DeltaW_AB=0`, and the MICROSCOPE eta residual is exactly zero. That is the GR/Newton-compatible route.",
        "",
        "But the current MTS branch still has not parent-signed the universal Hilbert source-coupling clauses. So this remains a conditional theorem, not a WEP pass or local-GR derivation.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Source-Weight Universality Attempt",
        "",
        markdown_table(rows_by_name["universality_attempt"]),
        "",
        "## Hilbert Source Contract",
        "",
        markdown_table(rows_by_name["hilbert_contract"]),
        "",
        "## Ti/Pt Material Charge Ledger",
        "",
        markdown_table(rows_by_name["tipt_material_ledger"]),
        "",
        "## WEP Eta Implication",
        "",
        markdown_table(rows_by_name["wep_implication"]),
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
        "universality_attempt": universality_attempt_rows(),
        "hilbert_contract": hilbert_contract_rows(),
        "tipt_material_ledger": tipt_material_ledger_rows(),
        "wep_implication": wep_implication_rows(),
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

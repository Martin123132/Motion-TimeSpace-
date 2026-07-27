from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3490-Y5-R2FR-species-blind-measure-current-owner-or-product-bound-upgrade.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3490": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3489": {
        "path": ROOT / "3489-Y5-R2FR-connected-matter-category-certificate-or-Jspurion-bound-source.md",
        "role": "3489 handoff",
    },
    "measure_1452": {
        "path": ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients" / "common_measure_current_theorem_attempt_1452.csv",
        "role": "common measure/current theorem attempt",
    },
    "signature_1462": {
        "path": ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients" / "common_measure_current_signature_attempt_1462.csv",
        "role": "common measure/current signature attempt",
    },
    "owner_1687": {
        "path": ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals" / "R2FR_common_action_measure_current_owner_proof_attempt_1687.csv",
        "role": "common action/measure/current owner proof attempt",
    },
    "audit_1594": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1594_COMMON_MEASURE_CURRENT_AUDIT.csv",
        "role": "common measure/current audit",
    },
    "finite_3488": {
        "path": OUT / "P8_Y5_R2FR_3488_FINITE_JSPURION_COEFFICIENT_ROWS.csv",
        "role": "finite fallback coefficients including epsilon_species_measure",
    },
    "updates_3489": {
        "path": OUT / "P8_Y5_R2FR_3489_FINITE_COEFFICIENT_UPDATES.csv",
        "role": "J_spurion product-bound update",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "WEP rows with empirical eta bounds",
    },
    "leakage_3134": {
        "path": OUT / "P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv",
        "role": "leakage heads including J_nonH",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(meta["path"]),
            "exists": str(Path(meta["path"]).exists()),
            "role": meta["role"],
            "valid_for_claim": "False",
        }
        for source_id, meta in SOURCES.items()
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "MEAS3490_0_common_owner_target",
            "statement": "A common parent measure/current owner would remove species measure Jacobians and current-rescaling slots.",
            "derivation": "S_parent/hbar_parent contains sum_A S_A with one measure, one action scale, and Hilbert source varied before readout.",
            "source_path": str(SOURCES["owner_1687"]["path"]),
            "status": "TARGET_EXACT_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "MEAS3490_1_classical_EOM_no_go",
            "statement": "Classical equations of motion cannot erase species action weights.",
            "derivation": "delta(w_A S_A)/delta psi_A may share roots with delta S_A/delta psi_A, but source variation gives delta(w_A S_A)/delta e_obs = w_A T_A.",
            "source_path": str(SOURCES["measure_1452"]["path"]),
            "status": "NO_GO_EXACT",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "MEAS3490_2_single_hbar_route",
            "statement": "A single parent hbar/path-measure route would forbid independent hbar_A or J_A measure weights.",
            "derivation": "Independent exp(i w_A S_A/hbar_parent) factors require extra parent coefficients; they are illegal only if the parent measure/statistical grammar excludes them.",
            "source_path": str(SOURCES["signature_1462"]["path"]),
            "status": "CONDITIONAL_ROUTE_CLEAN_NOT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "MEAS3490_3_hilbert_current_subtheorem",
            "statement": "Once common S_matter is fixed, Hilbert variation gives a unique post-variation source current.",
            "derivation": "T_mu_nu := delta S_matter/delta e_obs before readout; post-variation selectors are illegal.",
            "source_path": str(SOURCES["owner_1687"]["path"]),
            "status": "EXACT_SUBTHEOREM_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "MEAS3490_4_countermodel_retention",
            "statement": "Species Jacobian, current rescaling, and non-Hilbert bypass countermodels survive without parent signature.",
            "derivation": "Dmu_parent=product_A J_A Dpsi_A, J_src=sum_A c_A J_A, and J_src=kappa T_H+sum_A zeta_A J_NH,A remain covariant-shaped unless forbidden.",
            "source_path": str(SOURCES["measure_1452"]["path"]),
            "status": "COUNTERMODELS_SURVIVE",
            "valid_for_claim": "False",
        },
    ]


def residual_coefficient_rows() -> list[dict[str, Any]]:
    leakage = {row["symbol"]: row for row in read_csv(SOURCES["leakage_3134"]["path"])}
    return [
        {
            "coefficient_id": "MEAS3490_0_species_measure",
            "symbol": "epsilon_species_measure",
            "definition": "sup_A |partial_q ln J_A| for species-dependent measure Jacobian",
            "residual_slot": "R_matter_glue",
            "source_basis": "CMT1452_3 species Jacobian countermodel; 3488 finite row",
            "old_status": "MISSING_THEOREM_ZERO_OR_SOURCE_BOUND",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "MEAS3490_1_current_rescaling",
            "symbol": "epsilon_current_rescaling",
            "definition": "sup_A,B |partial_q ln c_A - partial_q ln c_B| for source-current normalization contrast",
            "residual_slot": "R_matter_glue + R_readout_PPN",
            "source_basis": "CMT1452_4 current normalization countermodel",
            "old_status": "MISSING_THEOREM_ZERO_OR_SOURCE_BOUND",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "MEAS3490_2_nonhilbert_current",
            "symbol": "epsilon_nonHilbert_current",
            "definition": "source-normalized envelope for species-dependent non-Hilbert source bypass",
            "residual_slot": "R_visible_coeff + R_readout_PPN",
            "source_basis": leakage.get("J_nonH", {}).get("row_id", "QLEAK3134_COEF2970_6_J_nonH"),
            "old_status": leakage.get("J_nonH", {}).get("candidate_value", "MISSING_SOURCE_BACKED_UPPER_BOUND"),
            "valid_for_claim": "False",
        },
    ]


def product_bound_rows(coefficients: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matrix = read_csv(SOURCES["matrix_3475"]["path"])
    wep_rows = [row for row in matrix if row["row_type"] == "WEP_material_difference"]
    rows: list[dict[str, Any]] = []
    for coeff in coefficients:
        for index, wep in enumerate(wep_rows):
            rows.append(
                {
                    "product_bound_id": f"MEASB3490_{coeff['symbol']}_{index}_{wep['aug_row_id']}",
                    "coefficient_symbol": coeff["symbol"],
                    "arena": wep["arena"],
                    "observable_row": wep["aug_row_id"],
                    "product_symbol": f"abs(S_E^q) * abs(Delta_{coeff['symbol']}_AB)",
                    "bound_value": wep["bound"],
                    "bound_units": wep["bound_units"],
                    "derivation": "Measure/current residual contrast contributes to eta as a source product; WEP eta bound limits the product but not the isolated coefficient.",
                    "source_path": wep["source_path"],
                    "isolates_coefficient": "False",
                    "missing_for_isolation": "parent-owned lower bound on abs(S_E^q), or theorem-zero/common measure-current owner",
                    "valid_for_claim": "False",
                }
            )
    return rows


def status_update_rows(coefficients: list[dict[str, Any]], product_bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for coeff in coefficients:
        bounds = [row["product_bound_id"] for row in product_bounds if row["coefficient_symbol"] == coeff["symbol"]]
        rows.append(
            {
                "coefficient_id": coeff["coefficient_id"],
                "symbol": coeff["symbol"],
                "old_status": coeff["old_status"],
                "new_status": "PRODUCT_BOUNDED_NOT_ISOLATED" if bounds else "STILL_MISSING",
                "bound_source": ";".join(bounds),
                "meaning": "residual is finite-product-bounded by WEP rows, but isolated coefficient needs source-amplitude ownership or theorem-zero",
                "valid_for_claim": "False",
            }
        )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3490_0_common_owner_theorem",
            "requirement": "single parent action-scale/measure/current owner is parent signed",
            "passed": "False",
            "evidence": "1687/1462 say target exact but owner not derived",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3490_1_classical_EOM_shortcut_blocked",
            "requirement": "do not use classical EOM equivalence to erase source weights",
            "passed": "True",
            "evidence": "1452/1462 exact no-go rows",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3490_2_species_jacobian_excluded",
            "requirement": "species measure Jacobian is theorem-zero or source-bounded",
            "passed": "False",
            "evidence": "species Jacobian countermodel survives; product bounds only",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3490_3_nonHilbert_bypass_excluded",
            "requirement": "non-Hilbert source bypass is theorem-zero or source-bounded",
            "passed": "False",
            "evidence": "non-Hilbert bypass remains open; product bounds only",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3490_4_product_bounds_created",
            "requirement": "measure/current residuals have finite product-bound rows",
            "passed": "True",
            "evidence": "WEP eta rows applied to epsilon_species_measure, epsilon_current_rescaling, epsilon_nonHilbert_current",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3490_0_common_measure_owner_conditional",
            "statement": "A single parent action-scale, species-blind measure, and Hilbert current owner would zero species measure/current source residuals up to common calibration.",
            "proof": "With one S_matter/hbar_parent and one variation-before-readout Hilbert source, species-dependent J_A, c_A, and zeta_A are not admissible parent arguments.",
            "result": "conditional theorem target sharpened, not parent-signed",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3490_1_EOM_no_go",
            "statement": "Classical EOM equivalence cannot erase measure/current source weights.",
            "proof": "Multiplying a sector action by w_A may leave field-equation roots unchanged but rescales the Hilbert/source variation.",
            "result": "pre-action weights must be owned, bounded, or forbidden",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3490_2_product_bound_upgrade",
            "statement": "Surviving species measure/current residuals are now finite-product-bounded by WEP rows.",
            "proof": "Each residual contrast enters eta multiplied by S_E^q; empirical eta bounds constrain that product.",
            "result": "epsilon_species_measure/current/nonHilbert move from missing-only to product-bounded-not-isolated",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3490_0_measure_owner_status",
            "decision": "Do not sign the common measure/current theorem yet.",
            "rationale": "The parent action-scale/statistical measure owner is still a contract and species Jacobian/non-Hilbert countermodels survive.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3490_1_residual_upgrade",
            "decision": "Upgrade species measure/current residuals to product-bounded-not-isolated.",
            "rationale": "This is stronger than missing rows and keeps the residual empirically tethered without pretending to isolate epsilon.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3490_2_best_next_attack",
            "decision": "Attack non-Hilbert source bypass and readout-order silence next.",
            "rationale": "Common Hilbert current is conditionally clean; the biggest remaining loopholes are zeta_A J_NH and readout/boundary reentry.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3491-Y5-R2FR-nonHilbert-current-bypass-or-readout-order-silence.md",
            "next_script": "scripts/Y5_R2FR_3491_nonHilbert_current_bypass_or_readout_order_silence.py",
            "objective": "Try to prove non-Hilbert source bypass and readout-order source reentry are silent; if not, keep them as product-bounded residuals in R_bridge.",
            "success_gate": "J_nonH/readout reentry theorem-zero, or source-backed product bounds plus explicit projection/readout residual map",
            "forbidden_shortcuts": "equating Hilbert conditional theorem with total source proof; ignoring boundary/readout selectors; isolating epsilon without source amplitude",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], product_bounds: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({"check_id": "VAL3490_0_sources_exist", "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()), "detail": "all cited local sources exist", "valid_for_claim": "False"})
    parse_ok = True
    details = []
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{name}:ERROR:{exc}")
    rows.append({"check_id": "VAL3490_1_csv_parse", "passed": parse_ok, "detail": "; ".join(details), "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3490_2_product_bounds_created", "passed": len(product_bounds) >= 6, "detail": f"product_bounds={len(product_bounds)}", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3490_3_parent_claim_blocked", "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates), "detail": "common-owner gates remain blocked", "valid_for_claim": "False"})
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append({"check_id": "VAL3490_4_no_claim", "passed": all(row.get("valid_for_claim") == "False" for row in all_rows), "detail": "all generated rows valid_for_claim=false", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3490_5_no_formalization_outputs", "passed": all(FORMALIZATION not in path.parents for path in outputs.values()), "detail": "outputs are under post-checkpoint-work/source-intake only", "valid_for_claim": "False"})
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append({"check_id": "VAL3490_SUMMARY", "passed": passed, "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep] + body)


def write_doc(
    attempts: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    product_bounds: list[dict[str, Any]],
    updates: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3490: Species-Blind Measure Current Owner Or Product-Bound Upgrade",
                "",
                "## Current Verdict",
                "- **No shortcut:** classical equations of motion cannot erase species action/measure weights because source variation still sees them.",
                "- **Conditional clean route:** one parent action-scale, species-blind measure, and Hilbert current owner would kill these residuals.",
                "- **Current corpus status:** that owner is not parent-signed; species Jacobian and non-Hilbert current countermodels survive.",
                "- **Concrete progress:** `epsilon_species_measure`, `epsilon_current_rescaling`, and `epsilon_nonHilbert_current` now have WEP product-bound rows.",
                "- **No claim:** no local-GR/source-coupling pass is claimed.",
                "",
                "## Theorem Attempts",
                md_table(attempts, ["attempt_id", "statement", "derivation", "status", "valid_for_claim"]),
                "",
                "## Residual Coefficients",
                md_table(coefficients, ["coefficient_id", "symbol", "definition", "residual_slot", "old_status", "valid_for_claim"]),
                "",
                "## Product Bounds",
                md_table(product_bounds, ["product_bound_id", "coefficient_symbol", "arena", "product_symbol", "bound_value", "bound_units", "isolates_coefficient", "valid_for_claim"]),
                "",
                "## Status Updates",
                md_table(updates, ["coefficient_id", "symbol", "old_status", "new_status", "bound_source", "meaning", "valid_for_claim"]),
                "",
                "## Theorems",
                md_table(theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"]),
                "",
                "## Gates",
                md_table(gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"]),
                "",
                "## Decisions",
                md_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"_Generated: {now()}_",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    attempts = theorem_attempt_rows()
    coefficients = residual_coefficient_rows()
    product_bounds = product_bound_rows(coefficients)
    updates = status_update_rows(coefficients, product_bounds)
    gates = gate_rows()
    theorems = theorem_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3490_SOURCE_REGISTER.csv",
        "attempts": OUT / "P8_Y5_R2FR_3490_MEASURE_CURRENT_THEOREM_ATTEMPTS.csv",
        "coefficients": OUT / "P8_Y5_R2FR_3490_RESIDUAL_COEFFICIENT_ROWS.csv",
        "product_bounds": OUT / "P8_Y5_R2FR_3490_MEASURE_CURRENT_PRODUCT_BOUNDS.csv",
        "updates": OUT / "P8_Y5_R2FR_3490_STATUS_UPDATES.csv",
        "theorems": OUT / "P8_Y5_R2FR_3490_THEOREM_LEDGER.csv",
        "gates": OUT / "P8_Y5_R2FR_3490_GATES.csv",
        "decisions": OUT / "P8_Y5_R2FR_3490_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3490_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["attempts"], attempts, ["attempt_id", "statement", "derivation", "source_path", "status", "valid_for_claim"])
    write_csv(outputs["coefficients"], coefficients, ["coefficient_id", "symbol", "definition", "residual_slot", "source_basis", "old_status", "valid_for_claim"])
    write_csv(outputs["product_bounds"], product_bounds, ["product_bound_id", "coefficient_symbol", "arena", "observable_row", "product_symbol", "bound_value", "bound_units", "derivation", "source_path", "isolates_coefficient", "missing_for_isolation", "valid_for_claim"])
    write_csv(outputs["updates"], updates, ["coefficient_id", "symbol", "old_status", "new_status", "bound_source", "meaning", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, product_bounds, gates)
    validation_path = OUT / "P8_Y5_BRR545_3490_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(attempts, coefficients, product_bounds, updates, theorems, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()

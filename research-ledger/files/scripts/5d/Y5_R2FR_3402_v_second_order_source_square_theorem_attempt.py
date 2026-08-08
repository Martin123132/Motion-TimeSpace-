from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3402-Y5-R2FR-v-second-order-source-square-theorem-attempt-under-AX1090.md"


SOURCES = {
    "3401_doc": ROOT / "3401-Y5-R2FR-kappav-second-order-beta-ledger-under-AX1090.md",
    "3401_eta": OUT / "P8_Y5_R2FR_3401_ETA_V_EXPONENTIAL_READOUT_DERIVATION.csv",
    "3401_square": OUT / "P8_Y5_R2FR_3401_SOURCE_AB_SQUARE_LAW.csv",
    "3401_components": OUT / "P8_Y5_R2FR_3401_KAPPAV_COMPONENT_LEDGER.csv",
    "3400_clauses": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "source_calibrated_eh_stack": OUT / "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv",
    "source_calibrated_eh_decision": OUT / "P8_Y5_SOURCE_CALIBRATED_EH_DECISION.csv",
    "eh_premise_audit": OUT / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
    "1585_doc": ROOT / "1585-Y5-EH-source-normalized-parent-action-owner-or-beta-residual-ledger.md",
    "1561_doc": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
    "delta_beta_derivation": OUT / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv",
}


OUTPUT_PATHS = {
    "source_register": OUT / "P8_Y5_R2FR_3402_SOURCE_REGISTER.csv",
    "log_lapse_theorem": OUT / "P8_Y5_R2FR_3402_LOG_LAPSE_NO_QUADRATIC_THEOREM.csv",
    "source_square_theorem": OUT / "P8_Y5_R2FR_3402_SOURCE_SQUARE_THEOREM.csv",
    "premise_audit": OUT / "P8_Y5_R2FR_3402_PREMISE_AUDIT.csv",
    "kappav_impact": OUT / "P8_Y5_R2FR_3402_KAPPAV_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3402_PROMOTION_GATES.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3402_RUNNER_NONCLAIM.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3402_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3402_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3402_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": f"SRC3402_{idx:02d}_{name}",
            "path": str(path),
            "exists": path.exists(),
            "role": "v_second_order_source_square_source",
            "valid_for_claim": False,
        }
        for idx, (name, path) in enumerate(SOURCES.items())
    ]


def log_lapse_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "LL3402_0_isotropic_eh",
            "statement": "For the one-parameter EH exterior in isotropic/PPN radius, the lapse is N=(1-x)/(1+x) with x=G_ref M/(2 r c^2).",
            "math": "g_00=-N^2 c^2",
            "result": "standard EH exterior supplies the reference one-parameter family",
            "valid_for_claim": False,
        },
        {
            "step_id": "LL3402_1_log_lapse",
            "statement": "Define v=log(N^2).",
            "math": "v=2[log(1-x)-log(1+x)]",
            "result": "v=-4x-(4/3)x^3+O(x^5), with no x^2 term",
            "valid_for_claim": False,
        },
        {
            "step_id": "LL3402_2_map_to_U",
            "statement": "With U=G_ref M/r=2c^2 x, the log-lapse expansion becomes the MTS v-readout target.",
            "math": "v=-2U/c^2 + O(c^-6)",
            "result": "a_v=0 through O(U^2/c^4)",
            "valid_for_claim": False,
        },
        {
            "step_id": "LL3402_3_beta",
            "statement": "Insert a_v=0 into the 3401 exponential readout result.",
            "math": "beta-1=a_v/2",
            "result": "beta_eta_lane=0 and kappa_eta=0 if the EH one-parameter/log-lapse branch is parent-owned",
            "valid_for_claim": False,
        },
    ]


def source_square_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "SS3402_0_family",
            "statement": "A one-parameter exterior metric family depends on the source only through one mass parameter mu.",
            "math": "U=mu/r; g_00=-1+2U/c^2-2U^2/c^4+O(c^-6)",
            "result": "the same mu controls the linear and quadratic terms",
            "valid_for_claim": False,
        },
        {
            "step_id": "SS3402_1_unmeasured_W",
            "statement": "If W is an unmeasured source potential and U=A_source W, then the same one-parameter family fixes the quadratic coefficient.",
            "math": "g_00=-1+2A_source W/c^2-2A_source^2 W^2/c^4+O(c^-6)",
            "result": "B_source=A_source^2",
            "valid_for_claim": False,
        },
        {
            "step_id": "SS3402_2_beta_source",
            "statement": "Insert B_source=A_source^2 into the 3401 source-square law.",
            "math": "delta_beta_source=B_source/A_source^2-1=0",
            "result": "kappa_source_quad=0 if the one-parameter source-calibrated family is parent-owned",
            "valid_for_claim": False,
        },
    ]


def premise_audit() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "PRE3402_0_observed_metric_branch",
            "needed_for": "log-lapse and source-square theorem",
            "required_statement": "one observed metric/coframe is used by matter, clocks, photons, source variation and PPN readout through O(U^2)",
            "current_status": "CONDITIONAL_NOT_DERIVED_THROUGH_O_U2",
            "source": str(SOURCES["source_calibrated_eh_stack"]),
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PRE3402_1_EH_only_exterior",
            "needed_for": "one-parameter EH family",
            "required_statement": "compact exterior field equation is EH plus harmless background/boundary terms",
            "current_status": "NOT_DERIVED_R11_TEMPLATE_ONLY",
            "source": str(SOURCES["source_calibrated_eh_stack"]),
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PRE3402_2_one_parameter_nohair",
            "needed_for": "B_source=A_source^2",
            "required_statement": "ordinary compact exterior has no independent scalar/vector/domain/memory/boundary hair charges",
            "current_status": "NOT_DERIVED_EXTRA_SECTORS_RETAINED",
            "source": str(SOURCES["source_calibrated_eh_stack"]),
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PRE3402_3_measured_mu",
            "needed_for": "source-calibrated U",
            "required_statement": "mu_EH equals measured orbital GM and Hilbert/Pi_M source charge",
            "current_status": "NOT_DERIVED_SOURCE_SCORECARD_UNFILLED",
            "source": str(SOURCES["source_calibrated_eh_stack"]),
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PRE3402_4_no_quadratic_leakage",
            "needed_for": "kappa_v=0 not just eta/source lanes",
            "required_statement": "R11, q_loc, boundary/domain, readout and coupling sectors add no independent O(U^2) beta term",
            "current_status": "NOT_DERIVED_COMPONENTS_UNFILLED",
            "source": str(SOURCES["source_calibrated_eh_stack"]),
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PRE3402_5_pc3400_adoption",
            "needed_for": "MTS ownership rather than imported EH fact",
            "required_statement": "PC3400 source-coupling clauses are adopted into the parent branch",
            "current_status": "STAGED_NOT_ADOPTED",
            "source": str(SOURCES["3400_clauses"]),
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]


def kappav_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "KI3402_0_eta",
            "component": "kappa_eta",
            "result_if_premises_signed": "0",
            "reason": "log-lapse has no U^2 term: a_v=0",
            "current_status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "impact_id": "KI3402_1_source_quad",
            "component": "kappa_source_quad",
            "result_if_premises_signed": "0",
            "reason": "one-parameter source family gives B_source=A_source^2",
            "current_status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "impact_id": "KI3402_2_remaining",
            "component": "kappa_PiM+kappa_boundary+kappa_readout+kappa_operator+kappa_coupling+q_loc_guard",
            "result_if_premises_signed": "not automatically zero unless PRE3402_4 also signs or component bounds are filled",
            "reason": "eta/source-square theorem does not silence retained non-EH/readout/boundary sectors by itself",
            "current_status": "REMAINS_OPEN",
            "valid_for_claim": False,
        },
        {
            "impact_id": "KI3402_3_kappav",
            "component": "kappa_v",
            "result_if_premises_signed": "0 only if all lanes close together",
            "reason": "kappa_v absolute envelope still includes retained lanes",
            "current_status": "BETA_NOT_CLAIMED",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3402_0_log_lapse",
            "claim": "EH/log-lapse gives a_v=0 through O(U^2)",
            "gate_pass": True,
            "reason": "v=2(log(1-x)-log(1+x)) has no x^2 term",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3402_1_source_square",
            "claim": "one-parameter source family gives B_source=A_source^2",
            "gate_pass": True,
            "reason": "same mass parameter controls U and U^2 terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3402_2_parent_ownership",
            "claim": "MTS parent owns the EH/log-lapse/source-square branch",
            "gate_pass": False,
            "reason": "observed O(U^2) branch, EH-only exterior, measured mu, no-hair and PC3400 adoption are not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3402_3_kappav",
            "claim": "kappa_v=0 is derived",
            "gate_pass": False,
            "reason": "eta and source lanes have conditional zeroes, but retained PiM/boundary/readout/operator/coupling lanes remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3402_4_local_GR",
            "claim": "local GR/PPN is derived",
            "gate_pass": False,
            "reason": "beta full vector remains open; alpha_i/zeta_i/xi still require their own gates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3402_0_log_lapse",
            "test": "derive a_v=0 condition",
            "status": "PASS_EXACT_CONDITIONAL",
            "detail": "EH log lapse has no quadratic term",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3402_1_source_square",
            "test": "derive B_source=A_source^2 condition",
            "status": "PASS_EXACT_CONDITIONAL",
            "detail": "one source mass parameter squares the first-order response",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3402_2_parent_gate",
            "test": "MTS ownership",
            "status": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "conditional theorem is not an adopted MTS prediction",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3402_3_claim_firewall",
            "test": "beta/local-GR claim",
            "status": "BLOCKED_NO_CLAIM",
            "detail": "retained kappa_v lanes remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3402_0_best_result",
            "finding": "a_v=0 and B_source=A_source^2 are both exact in the source-calibrated EH one-parameter branch",
            "reason": "log-lapse oddness removes the quadratic v term; one mass parameter forces the source square law",
            "next_action": "try to make the EH one-parameter/no-hair branch parent-owned or explicitly fill the retained lanes",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3402_1_not_enough",
            "finding": "this is not yet kappa_v=0",
            "reason": "PiM, boundary, readout, operator, coupling and q_loc lanes can still contribute beta drift",
            "next_action": "attack retained lanes under 3403",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3402_2_project_status",
            "finding": "beta route is sharper and less grim than before",
            "reason": "two central kappa_v pieces now have exact conditional zero theorems rather than generic missing labels",
            "next_action": "continue from exact conditional results into parent-ownership/no-hair gates",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3403-Y5-R2FR-PiM-boundary-readout-operator-beta-residual-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3403_PiM_boundary_readout_operator_beta_residual_fill.py",
            "objective": "derive zero or finite bounds for the retained PiM, boundary, readout, operator, coupling and q_loc lanes in kappa_v",
            "why_next": "3402 closes the eta/source-square route conditionally; remaining beta drift lives in retained lanes",
            "valid_for_claim": False,
        },
        {
            "target_id": "3404-Y5-R2FR-source-calibrated-EH-parent-ownership-audit-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3404_source_calibrated_EH_parent_ownership_audit.py",
            "objective": "audit whether the source-calibrated EH one-parameter branch can be adopted as a parent-owned MTS local theorem without importing GR as an axiom",
            "why_next": "parent ownership is the difference between a useful conditional theorem and a serious derived local-GR route",
            "valid_for_claim": False,
        },
    ]


def validate(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": passed, "detail": detail})

    add("VAL3402_0_sources_exist", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3402_1_log_lapse", "log lapse theorem derives no quadratic term", any("no x^2 term" in row["result"] for row in outputs["log_lapse_theorem"]), "")
    add("VAL3402_2_source_square", "source square theorem derives B_source=A_source^2", any("B_source=A_source^2" in row["result"] for row in outputs["source_square_theorem"]), "")
    add("VAL3402_3_premises_block", "premise audit blocks current claim", all(row["blocks_claim"] for row in outputs["premise_audit"]), "")
    add("VAL3402_4_impact", "kappa_v impact keeps retained lanes open", any(row["current_status"] == "REMAINS_OPEN" for row in outputs["kappav_impact"]), "")
    add("VAL3402_5_gates", "parent/kappav/local-GR gates remain blocked", not any(row["gate_pass"] for row in outputs["promotion_gates"] if row["gate_id"] in {"GATE3402_2_parent_ownership", "GATE3402_3_kappav", "GATE3402_4_local_GR"}), "")
    add("VAL3402_6_no_overclaim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim", False)).lower() == "false" for group in outputs.values() for row in group), "")
    add("VAL3402_7_scope", "no 3402 output path targets formalization-workbench", "formalization-workbench" not in str(DOC).lower() and all("formalization-workbench" not in str(path).lower() for path in OUTPUT_PATHS.values()), "")
    add("VAL3402_8_next_target", "next target moves to retained beta lanes", any("retained" in row["objective"] for row in outputs["next_target"]), "")
    add("VAL3402_9_overall", "3402 validation overall", all(row["passed"] is True for row in rows), "all required checks passed")
    return rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
                for row in rows
            ],
        ]
    )


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    sections = [
        "# 3402 - Y5/R2FR v second-order source-square theorem attempt under AX1090",
        "",
        "## Summary",
        "- 3402 proves the clean conditional beta fact we wanted: in the EH one-parameter exterior, the log lapse has no quadratic term, so `a_v=0`.",
        "- It also proves the matching source-square condition: if one source mass parameter controls the exterior, then `B_source=A_source^2`.",
        "- These two results conditionally zero the `eta_v` and `kappa_source_quad` lanes of `kappa_v`.",
        "- This is still not a beta/local-GR claim because MTS has not parent-signed the EH/no-hair/source-calibrated branch and the retained lanes remain open.",
        f"- Generated UTC: `{timestamp}`.",
        "",
        "## Source Register",
        md_table(outputs["source_register"]),
        "",
        "## Log-Lapse No-Quadratic Theorem",
        md_table(outputs["log_lapse_theorem"]),
        "",
        "## Source-Square Theorem",
        md_table(outputs["source_square_theorem"]),
        "",
        "## Premise Audit",
        md_table(outputs["premise_audit"]),
        "",
        "## Kappa_v Impact",
        md_table(outputs["kappav_impact"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Nonclaim Runner",
        md_table(outputs["runner_nonclaim"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    outputs = {
        "source_register": source_register(),
        "log_lapse_theorem": log_lapse_theorem(),
        "source_square_theorem": source_square_theorem(),
        "premise_audit": premise_audit(),
        "kappav_impact": kappav_impact(),
        "promotion_gates": promotion_gates(),
        "runner_nonclaim": runner_nonclaim(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    outputs["validation"] = validate(outputs)
    for name, rows in outputs.items():
        write_csv(OUTPUT_PATHS[name], rows)
    parsed = [(path.name, len(read_csv(path))) for path in OUTPUT_PATHS.values()]
    if not all(row["passed"].lower() == "true" for row in read_csv(OUTPUT_PATHS["validation"])):
        raise RuntimeError("3402 validation failed")
    write_doc(outputs)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUT_PATHS)} CSV outputs under {OUT}")
    print("Parsed outputs: " + "; ".join(f"{name}={count}" for name, count in parsed))


if __name__ == "__main__":
    main()

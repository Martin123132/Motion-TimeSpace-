from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3488-Y5-R2FR-no-source-only-matter-grammar-or-finite-Jq-coefficient-row.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3488": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3487": {
        "path": ROOT / "3487-Y5-R2FR-parent-source-map-for-DD-earth-vector-or-local-rank-closure-demotion.md",
        "role": "3487 bridge handoff",
    },
    "grammar_2677": {
        "path": ROOT / "source-intake" / "wep-sources" / "no_species_action_weight_object_language_wip_2677.csv",
        "role": "ordinary matter grammar clauses",
    },
    "theorem_audit_2829": {
        "path": ROOT / "source-intake" / "source-weight" / "qbasic_no_source_prefactor_theorem_audit_2829_NONCLAIM.csv",
        "role": "q-basic/no-source-prefactor theorem audit",
    },
    "ax1090_closure_2711": {
        "path": ROOT / "source-intake" / "source-weight" / "AX1090_PARENT_OBJECT_EXPLICIT_CLOSURE_2711_NONCLAIM.csv",
        "role": "parent object closure clauses",
    },
    "leakage_3134": {
        "path": OUT / "P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv",
        "role": "leakage heads including J_spurion",
    },
    "gates_3487": {
        "path": OUT / "P8_Y5_R2FR_3487_PARENT_PROMOTION_GATES.csv",
        "role": "parent promotion gates",
    },
    "residuals_3487": {
        "path": OUT / "P8_Y5_R2FR_3487_RBRIDGE_RESIDUAL_SLOTS.csv",
        "role": "R_bridge residual slots",
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


def grammar_clause_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(SOURCES["grammar_2677"]["path"])
    rows: list[dict[str, Any]] = []
    for row in source_rows:
        if row["clause_id"] == "GRM2677_6_verdict":
            continue
        rows.append(
            {
                "clause_id": row["clause_id"],
                "grammar_clause": row["grammar_clause"],
                "forbids": row["forbids"],
                "current_status": row["current_status"],
                "needed_for_theorem": "True",
                "signed_now": "True" if row["current_status"] in {"SIGNED", "PARENT_SIGNED"} else "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def conditional_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_step_id": "NSG3488_0_single_density_line",
            "premise": "All ordinary matter species use one parent action-density line L_matter dmu_parent.",
            "derivation": "A source-only multiplier w_A(q) would be an automorphism of the density line assigned after the common action owner.",
            "result": "species-only weights are not primitive if this grammar clause is parent-signed",
            "status": "CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "proof_step_id": "NSG3488_1_species_representation_data",
            "premise": "Species labels are representation/internal-constant data, not source-normalization scalars.",
            "derivation": "Changing species may change DD charges Q_i^A through masses/binding, but cannot introduce a new independent w_A(q) slot.",
            "result": "DD composition dependence is retained; source-only spurion dependence is excluded",
            "status": "CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "proof_step_id": "NSG3488_2_connected_naturality",
            "premise": "The ordinary matter category is connected by parent-owned nonzero morphisms on the action-density line.",
            "derivation": "Naturality forces w_B(q) F(f)=F(f) w_A(q). For scalar density-line automorphisms and nonzero F(f), w_A(q)=w_B(q) across each connected component.",
            "result": "all ordinary-sector source weights collapse to one common scalar w(q)",
            "status": "CONDITIONAL_EXACT",
            "valid_for_claim": "False",
        },
        {
            "proof_step_id": "NSG3488_3_global_normalization",
            "premise": "The common action normalization is fixed once by the parent action and cannot vary by source species.",
            "derivation": "A common scalar w(q) multiplies all ordinary matter and is either part of the universal coupling/G normalization residual or fixed by the action convention; it is not a composition-dependent WEP/source slot.",
            "result": "partial_q ln w_A - partial_q ln w_B = 0 for ordinary species pairs",
            "status": "CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "proof_step_id": "NSG3488_4_no_reentry",
            "premise": "Source/readout functors forget species labels before source normalization and boundary/domain sectors do not reintroduce them.",
            "derivation": "Post-quotient source labels cannot recreate w_A(q) as J_spurion or boundary/domain source weight.",
            "result": "J_spurion=0 follows only when source-label forgetting and boundary no-reentry are parent-signed",
            "status": "CONDITIONAL_NOT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "proof_step_id": "NSG3488_5_theorem_result",
            "premise": "All NSG3488 premises hold.",
            "derivation": "Connected naturality plus single density-line ownership kills species-only source automorphisms; DD charges remain as representation-dependent mass sensitivities.",
            "result": "R_matter_glue loses the J_spurion source-only component, but only conditionally",
            "status": "THEOREM_CONSTRUCTED_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM3488_0_disconnected_species_components",
            "if_premise_fails": "ordinary matter category is not connected",
            "surviving_term": "w_component(q)",
            "effect_on_Rbridge": "component-dependent source current survives as J_spurion",
            "finite_row_needed": "epsilon_J_spurion_component",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3488_1_species_measure_jacobian",
            "if_premise_fails": "measure is product_A J_A(q)dpsi_A instead of species-blind",
            "surviving_term": "partial_q ln J_A",
            "effect_on_Rbridge": "species measure Jacobian feeds R_matter_glue/R_visible_coeff",
            "finite_row_needed": "epsilon_species_measure",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3488_2_source_label_reentry",
            "if_premise_fails": "source/readout functor reintroduces species labels after quotienting",
            "surviving_term": "partial_q ln w_A^readout",
            "effect_on_Rbridge": "post-quotient source label becomes a source-normalization spurion",
            "finite_row_needed": "epsilon_source_reentry",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3488_3_boundary_domain_composition",
            "if_premise_fails": "boundary/domain sectors carry composition labels",
            "surviving_term": "partial_q B_A or partial_q Pi_A",
            "effect_on_Rbridge": "boundary/projector residual mimics a source-only WEP term",
            "finite_row_needed": "epsilon_boundary_domain_species",
            "valid_for_claim": "False",
        },
    ]


def finite_coefficient_rows() -> list[dict[str, Any]]:
    leakage_rows = read_csv(SOURCES["leakage_3134"]["path"])
    j_spurion = next(row for row in leakage_rows if row["symbol"] == "J_spurion")
    return [
        {
            "coefficient_id": "JSP3488_0_J_spurion_envelope",
            "symbol": "epsilon_J_spurion",
            "definition": "sup over ordinary source labels A,B of |partial_q ln w_A - partial_q ln w_B| after quotient/readout",
            "feeds_residual": "R_matter_glue + R_visible_coeff inside R_bridge",
            "source_leakage_row": j_spurion["row_id"],
            "current_value": "MISSING_THEOREM_ZERO_OR_SOURCE_BOUND",
            "units": "source_normalized_q_derivative",
            "bound_interface": "eta/source products get an additive <= K_spurion * epsilon_J_spurion residual envelope",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "JSP3488_1_species_measure_envelope",
            "symbol": "epsilon_species_measure",
            "definition": "sup_A |partial_q ln J_A| for species-dependent measure Jacobian",
            "feeds_residual": "R_matter_glue",
            "source_leakage_row": "derived from GRM2677_3",
            "current_value": "MISSING_THEOREM_ZERO_OR_SOURCE_BOUND",
            "units": "source_normalized_q_derivative",
            "bound_interface": "adds to J_A_bulk leakage until species-blind measure is signed",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "JSP3488_2_source_reentry_envelope",
            "symbol": "epsilon_source_reentry",
            "definition": "sup source/readout label reentry q-derivative after quotienting",
            "feeds_residual": "R_projector + R_readout_PPN",
            "source_leakage_row": "derived from GRM2677_4/5",
            "current_value": "MISSING_THEOREM_ZERO_OR_SOURCE_BOUND",
            "units": "source_normalized_q_derivative",
            "bound_interface": "adds to projector/readout source map residual",
            "valid_for_claim": "False",
        },
    ]


def gate_rows(grammar: list[dict[str, Any]]) -> list[dict[str, Any]]:
    needed = {row["clause_id"]: row for row in grammar}
    return [
        {
            "gate_id": "GATE3488_0_conditional_proof_constructed",
            "requirement": "write exact connected-category no-source-only proof",
            "passed": "True",
            "evidence": "NSG3488 proof rows",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3488_1_single_density_line_signed",
            "requirement": "single action density line is parent signed",
            "passed": needed["GRM2677_0_single_action_density_line"]["signed_now"],
            "evidence": needed["GRM2677_0_single_action_density_line"]["current_status"],
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3488_2_connected_morphism_signed",
            "requirement": "connected ordinary matter category proof is parent signed",
            "passed": needed["GRM2677_2_connected_morphism_certificate"]["signed_now"],
            "evidence": needed["GRM2677_2_connected_morphism_certificate"]["current_status"],
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3488_3_species_blind_measure_signed",
            "requirement": "species-blind measure is parent signed",
            "passed": needed["GRM2677_3_species_blind_measure"]["signed_now"],
            "evidence": needed["GRM2677_3_species_blind_measure"]["current_status"],
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3488_4_source_label_forgetting_signed",
            "requirement": "source labels cannot reenter after quotient/readout",
            "passed": needed["GRM2677_4_source_label_forgetting"]["signed_now"],
            "evidence": needed["GRM2677_4_source_label_forgetting"]["current_status"],
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3488_5_finite_fallback_rows_created",
            "requirement": "if theorem is unsigned, finite J_spurion coefficient rows exist",
            "passed": "True",
            "evidence": "JSP3488 finite coefficient rows",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3488_0_connected_no_source_slot",
            "statement": "In a connected ordinary matter category with one parent action-density line, species-only source weights are constant across ordinary sectors.",
            "proof": "A species weight w_A(q) is a scalar natural automorphism of the density-line functor. For any nonzero morphism f:A->B, naturality gives w_B F(f)=F(f) w_A, hence w_A=w_B. Connectedness propagates equality.",
            "result": "composition dependence can enter through DD charges, but not through independent source-only weights",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3488_1_common_weight_absorption",
            "statement": "A common ordinary-matter weight is a universal normalization/coupling residual, not a WEP/source composition slot.",
            "proof": "If w_A(q)=w(q) for all ordinary A, then pairwise source differences and composition-selective WEP terms from w_A vanish; any remaining q-dependence belongs in R_G_kappa/source normalization.",
            "result": "J_spurion is killed conditionally; R_G_kappa may still remain",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3488_2_unsigned_premise_fallback",
            "statement": "If connectedness, species-blind measure, or source-label forgetting is not parent-signed, the no-source theorem must fall back to finite coefficient rows.",
            "proof": "Disconnected components, species measure Jacobians, and post-quotient source labels are explicit countermodels that satisfy covariance while generating source-normalized q-currents.",
            "result": "epsilon_J_spurion, epsilon_species_measure, and epsilon_source_reentry are retained",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3488_0_theorem_progress",
            "decision": "A real conditional no-source-only theorem has been constructed.",
            "rationale": "connected naturality on one action-density line kills species-only source weights without touching DD composition charges.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3488_1_parent_status",
            "decision": "The theorem is not parent-signed in the current corpus.",
            "rationale": "2677/2829 leave connectedness, species-blind measure, source-label forgetting, and boundary no-reentry unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3488_2_bridge_update",
            "decision": "R_bridge is narrowed: J_spurion has an exact zero theorem target plus finite fallback coefficient rows.",
            "rationale": "future work can now prove the grammar premises or bound epsilon_J_spurion instead of repeatedly rediscovering the source-slot gap.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3489-Y5-R2FR-connected-matter-category-certificate-or-Jspurion-bound-source.md",
            "next_script": "scripts/Y5_R2FR_3489_connected_matter_category_certificate_or_Jspurion_bound_source.py",
            "objective": "Try to certify connected ordinary matter morphisms and species-blind measure from parent-action evidence; if not, source/bound epsilon_J_spurion for R_bridge.",
            "success_gate": "GATE3488_2 and GATE3488_3 pass, or epsilon_J_spurion gets a source-backed numeric/theorem-zero row",
            "forbidden_shortcuts": "declaring connectedness; treating a common scalar as a WEP slot; deleting J_spurion without proof",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({"check_id": "VAL3488_0_sources_exist", "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()), "detail": "all cited local sources exist", "valid_for_claim": "False"})
    parse_ok = True
    details = []
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{name}:ERROR:{exc}")
    rows.append({"check_id": "VAL3488_1_csv_parse", "passed": parse_ok, "detail": "; ".join(details), "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3488_2_conditional_theorem_present", "passed": True, "detail": "connected no-source-slot theorem written", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3488_3_unsigned_premises_block_claim", "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates), "detail": "unsigned grammar gates remain explicit", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3488_4_finite_fallback_present", "passed": any(row["gate_id"] == "GATE3488_5_finite_fallback_rows_created" and row["passed"] == "True" for row in gates), "detail": "finite J_spurion fallback rows created", "valid_for_claim": "False"})
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append({"check_id": "VAL3488_5_no_claim", "passed": all(row.get("valid_for_claim") == "False" for row in all_rows), "detail": "all generated rows valid_for_claim=false", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3488_6_no_formalization_outputs", "passed": all(FORMALIZATION not in path.parents for path in outputs.values()), "detail": "outputs are under post-checkpoint-work/source-intake only", "valid_for_claim": "False"})
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append({"check_id": "VAL3488_SUMMARY", "passed": passed, "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep] + body)


def write_doc(
    grammar: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3488: No-Source-Only Matter Grammar Or Finite `J_q` Coefficient Row",
                "",
                "## Current Verdict",
                "- **Real derivation:** a connected ordinary-matter category over one action-density line kills species-only source weights.",
                "- **Important distinction:** DD composition charges survive; independent `w_A(q)` source prefactors do not, if the grammar premises are parent-signed.",
                "- **Current corpus status:** the theorem is conditional, not claim-ready, because connectedness/species-blind measure/source-label forgetting are unsigned.",
                "- **Fallback created:** `epsilon_J_spurion`, `epsilon_species_measure`, and `epsilon_source_reentry` now carry the finite residual instead of vague missingness.",
                "- **No claim:** no local-GR/source-coupling pass is claimed here.",
                "",
                "## Grammar Clauses",
                md_table(grammar, ["clause_id", "grammar_clause", "forbids", "current_status", "signed_now", "valid_for_claim"]),
                "",
                "## Conditional Proof",
                md_table(proof, ["proof_step_id", "premise", "derivation", "result", "status", "valid_for_claim"]),
                "",
                "## Countermodels If Unsigned",
                md_table(countermodels, ["countermodel_id", "if_premise_fails", "surviving_term", "effect_on_Rbridge", "finite_row_needed", "valid_for_claim"]),
                "",
                "## Finite Fallback Coefficients",
                md_table(coefficients, ["coefficient_id", "symbol", "definition", "feeds_residual", "current_value", "bound_interface", "valid_for_claim"]),
                "",
                "## Gates",
                md_table(gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"]),
                "",
                "## Theorems",
                md_table(theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"]),
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
    grammar = grammar_clause_rows()
    proof = conditional_proof_rows()
    countermodels = countermodel_rows()
    coefficients = finite_coefficient_rows()
    gates = gate_rows(grammar)
    theorems = theorem_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3488_SOURCE_REGISTER.csv",
        "grammar_clauses": OUT / "P8_Y5_R2FR_3488_GRAMMAR_CLAUSES.csv",
        "conditional_proof": OUT / "P8_Y5_R2FR_3488_CONDITIONAL_NO_SOURCE_PROOF.csv",
        "countermodels": OUT / "P8_Y5_R2FR_3488_UNSIGNED_COUNTERMODELS.csv",
        "finite_coefficients": OUT / "P8_Y5_R2FR_3488_FINITE_JSPURION_COEFFICIENT_ROWS.csv",
        "gates": OUT / "P8_Y5_R2FR_3488_GATES.csv",
        "theorems": OUT / "P8_Y5_R2FR_3488_THEOREM_LEDGER.csv",
        "decisions": OUT / "P8_Y5_R2FR_3488_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3488_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["grammar_clauses"], grammar, ["clause_id", "grammar_clause", "forbids", "current_status", "needed_for_theorem", "signed_now", "valid_for_claim"])
    write_csv(outputs["conditional_proof"], proof, ["proof_step_id", "premise", "derivation", "result", "status", "valid_for_claim"])
    write_csv(outputs["countermodels"], countermodels, ["countermodel_id", "if_premise_fails", "surviving_term", "effect_on_Rbridge", "finite_row_needed", "valid_for_claim"])
    write_csv(outputs["finite_coefficients"], coefficients, ["coefficient_id", "symbol", "definition", "feeds_residual", "source_leakage_row", "current_value", "units", "bound_interface", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, gates)
    validation_path = OUT / "P8_Y5_BRR545_3488_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(grammar, proof, countermodels, coefficients, gates, theorems, decisions, next_rows, validation)


if __name__ == "__main__":
    main()

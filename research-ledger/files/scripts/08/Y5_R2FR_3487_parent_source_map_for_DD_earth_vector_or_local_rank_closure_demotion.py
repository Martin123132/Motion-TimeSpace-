from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3487-Y5-R2FR-parent-source-map-for-DD-earth-vector-or-local-rank-closure-demotion.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3487": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3486": {
        "path": ROOT / "3486-Y5-R2FR-earth-Qdelta-source-stability-or-parent-kernel-exclusion.md",
        "role": "3486 DD-proxy Qdelta stability handoff",
    },
    "source_leg_2444": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv",
        "role": "formal S_E^q source leg contract",
    },
    "jq_attempt_2445": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv",
        "role": "J_q extraction attempt and visible coefficient route",
    },
    "residual_pack_2446": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv",
        "role": "MTS residual-current families blocking S_Eq",
    },
    "proof_matrix_3134": {
        "path": OUT / "P8_Y5_R2FR_3134_PROOF_REDUCTION_MATRIX.csv",
        "role": "quotient/matter descent proof statuses",
    },
    "leakage_3134": {
        "path": OUT / "P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv",
        "role": "finite leakage heads after quotient proof",
    },
    "dd_formula_3472": {
        "path": OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_FORMULA_AUDIT.csv",
        "role": "source-backed DD four-charge formulas",
    },
    "earth_vector_3482": {
        "path": OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv",
        "role": "bulk Earth DD source proxy vector",
    },
    "rank_3485": {
        "path": OUT / "P8_Y5_R2FR_3485_RANK_AND_CONDITION_LEDGER.csv",
        "role": "conditional rank closure through hyperfine/isotope rows",
    },
    "qdelta_3486": {
        "path": OUT / "P8_Y5_R2FR_3486_QDELTA_POSITIVITY_BOUNDS.csv",
        "role": "Q_delta_m_Earth stability proof in DD proxy",
    },
    "stress_3486": {
        "path": OUT / "P8_Y5_R2FR_3486_RANK_STRESS_TESTS.csv",
        "role": "rank stress tests for Q_delta_m_Earth",
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
            "source_id": key,
            "path": str(meta["path"]),
            "exists": str(Path(meta["path"]).exists()),
            "role": meta["role"],
            "valid_for_claim": "False",
        }
        for key, meta in SOURCES.items()
    ]


def earth_vector_text() -> str:
    row = read_csv(SOURCES["earth_vector_3482"]["path"])[0]
    return (
        "("
        + ", ".join(
            [
                row["Q_hatm_full_Earth"],
                row["Q_delta_m_Earth"],
                row["Q_m_e_Earth"],
                row["Q_e_full_Earth"],
            ]
        )
        + ")"
    )


def bridge_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "BRIDGE3487_0_parent_source_definition",
            "claim": "The owned source leg must be a projected parent current, not a chosen normalizer.",
            "derivation": "S_E^q[x] := P_arena[ integral G_q(x,y) J_q^E(y) dmu_y ] / N_E, with J_q^E := delta S_matter,E / delta q.",
            "input_source": str(SOURCES["source_leg_2444"]["path"]),
            "status": "CONTRACT_DEFINED_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BRIDGE3487_1_body_action_chain_rule",
            "claim": "If ordinary matter descends through observed variables and dimensionless constants theta_i(q), then the q-current has a DD-like chain-rule term.",
            "derivation": "delta_q ln M_E = sum_i (partial ln M_E/partial ln theta_i)(partial ln theta_i/partial q) + R_action.",
            "input_source": str(SOURCES["proof_matrix_3134"]["path"]),
            "status": "FORMAL_CHAIN_RULE_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BRIDGE3487_2_DD_charge_identification",
            "claim": "For theta=(mhat/Lambda_QCD, delta_m/Lambda_QCD, m_e/Lambda_QCD, alpha), DD gives partial ln M_A/partial ln theta_i = Q_i^A.",
            "derivation": "Use the 3472 source-backed DD formulas for Q_hatm, Q_delta_m, Q_me, and Q_e.",
            "input_source": str(SOURCES["dd_formula_3472"]["path"]),
            "status": "DD_FORMULA_SOURCE_BACKED_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BRIDGE3487_3_Earth_composition_average",
            "claim": "For the bulk Earth proxy, Q_i^E = sum_a f_a Q_i^a.",
            "derivation": "3482 computed the mass-fraction weighted DD vector Q_Earth = " + earth_vector_text() + ".",
            "input_source": str(SOURCES["earth_vector_3482"]["path"]),
            "status": "NUMERIC_DD_PROXY_BUILT",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BRIDGE3487_4_parent_bridge_equation",
            "claim": "The actual parent bridge is S_E^q = Q_Earth dot C + R_bridge.",
            "derivation": "C_i := partial ln theta_i/partial q in the parent q-normalization; R_bridge collects descent, source-weight, projection, boundary, readout, and non-DD sector defects.",
            "input_source": str(SOURCES["residual_pack_2446"]["path"]),
            "status": "DERIVED_CONDITIONAL_BRIDGE_WITH_RESIDUAL",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BRIDGE3487_5_closure_implication",
            "claim": "If R_bridge=0 and the parent q-normalization matches the coefficient basis, then 3485-3486 promote from DD-proxy closure to parent-owned local source closure.",
            "derivation": "3485 closes rank with sourced hyperfine/isotope rows; 3486 proves Q_delta_m_Earth remains positive in the DD proxy.",
            "input_source": str(SOURCES["rank_3485"]["path"]) + ";" + str(SOURCES["qdelta_3486"]["path"]),
            "status": "CONDITIONAL_PROMOTION_PATH_IDENTIFIED",
            "valid_for_claim": "False",
        },
    ]


def residual_bridge_rows() -> list[dict[str, Any]]:
    pack = read_csv(SOURCES["residual_pack_2446"]["path"])
    rows: list[dict[str, Any]] = []
    mapping = {
        "RCS2446_0_reference_boundary": "R_boundary",
        "RCS2446_1_extra_nonEH": "R_extra_nonEH",
        "RCS2446_2_projector_domain": "R_projector",
        "RCS2446_3_matter_source_glue": "R_matter_glue",
        "RCS2446_4_coupling_constant": "R_G_kappa",
        "RCS2446_5_readout_PPN_tail": "R_readout_PPN",
        "RCS2446_6_EM_clock_mass_coupling_guard": "R_visible_coeff",
    }
    for row in pack:
        residual_id = row["residual_id"]
        if residual_id not in mapping:
            continue
        rows.append(
            {
                "bridge_residual_id": mapping[residual_id],
                "source_residual_id": residual_id,
                "bridge_formula_slot": "R_bridge includes " + mapping[residual_id],
                "current_status": row["current_status"],
                "required_zero_or_bound": row["required_zero_or_bound"],
                "blocks_parent_promotion": "True",
                "source_path": str(SOURCES["residual_pack_2446"]["path"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def parent_gate_rows() -> list[dict[str, Any]]:
    proof = read_csv(SOURCES["proof_matrix_3134"]["path"])
    proof_by_clause = {row["clause"]: row for row in proof}
    leakage = read_csv(SOURCES["leakage_3134"]["path"])
    missing_leaks = [row["symbol"] for row in leakage if "MISSING" in row.get("candidate_value", "") or "REQUIRED" in row.get("candidate_value", "")]
    gates = [
        {
            "gate_id": "GATE3487_0_parent_source_definition",
            "requirement": "explicit parent q and J_q^E = delta S_matter,E/delta q are supplied",
            "evidence": "2444/2445 define the contract but say target not extracted",
            "passed": "False",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3487_1_chain_rule_shape",
            "requirement": "chain-rule descent shape exists",
            "evidence": proof_by_clause["chain_rule_variation"]["proof_status"],
            "passed": "True",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3487_2_matter_functor_owned",
            "requirement": "ordinary matter functor over observed variables is parent signed",
            "evidence": proof_by_clause["q_basic_matter_functor"]["proof_status"],
            "passed": "False",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3487_3_no_source_only_slot",
            "requirement": "no independent source/species prefactor bypasses DD composition weights",
            "evidence": proof_by_clause["no_source_only_slot"]["proof_status"],
            "passed": "False",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3487_4_DD_formula_source_backing",
            "requirement": "DD charge formulas exist for all four channels",
            "evidence": "3472 formula audit found four formulas",
            "passed": "True",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3487_5_residual_zero_or_bound",
            "requirement": "all R_bridge residual slots are zero-derived or source-bounded",
            "evidence": "open leakage heads: " + ";".join(missing_leaks),
            "passed": "False",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3487_6_rank_closure_proxy_stable",
            "requirement": "DD proxy rank closure exists and Q_delta_m_Earth stability survives stress tests",
            "evidence": "3485 closing rows plus 3486 positive lower-bound and forced-zero rank-fail",
            "passed": "True",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]
    return gates


def bridge_status_rows(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocking = [row["gate_id"] for row in gates if row["blocks_claim"] == "True" and row["passed"] != "True"]
    return [
        {
            "status_id": "STATUS3487_0_bridge_equation",
            "status": "CONDITIONAL_BRIDGE_DERIVED",
            "meaning": "The exact promotion equation is S_E^q = Q_Earth dot C + R_bridge.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STATUS3487_1_parent_ownership",
            "status": "NOT_PARENT_OWNED_YET",
            "meaning": "R_bridge cannot be set to zero and J_q is not extracted from a parent matter action.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STATUS3487_2_demote_or_promote",
            "status": "DD_PROXY_EVIDENCE_RETAINED_NOT_DEMOTED_TO_NOTHING",
            "meaning": "3485-3486 remain useful conditional evidence, but cannot be advertised as local-GR/source-coupling closure.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STATUS3487_3_blocking_gates",
            "status": "BLOCKED_FOR_CLAIM_BY_" + ";".join(blocking),
            "meaning": "Parent promotion requires closing these exact gates, not rerunning WEP fits.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3487_0_parent_to_DD_bridge",
            "statement": "If the parent matter action descends to ordinary body masses M_A(theta(q)) and has no source-only bypass, then the parent q-source leg equals the DD charge vector contracted with parent coefficient slopes, up to explicit residuals.",
            "proof": "Apply the chain rule to ln M_A(theta(q)); identify partial ln M_A/partial ln theta_i with DD charges; average over Earth composition; collect every unsatisfied parent/projection/source clause into R_bridge.",
            "result": "S_E^q = Q_Earth dot C + R_bridge",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3487_1_no_smuggling_condition",
            "statement": "Setting R_bridge=0 is equivalent to proving parent source ownership, not a convention.",
            "proof": "R_bridge contains source-current, matter-functor, source-weight, boundary, projector, coupling-normalization, and readout residuals explicitly listed in 2446/3134.",
            "result": "No local coefficient or local-GR claim is allowed while any blocking residual lacks a zero theorem or bound.",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3487_2_best_forward_route",
            "statement": "The shortest route forward is to close R_matter_glue/no-source-slot/source-current ownership before chasing more WEP rows.",
            "proof": "3485-3486 already supply a proxy-stable rank closure; remaining failure is parent ownership of the source map.",
            "result": "Next target should attack matter functor/source slot theorem or source-current coefficient extraction.",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3487_0_main_result",
            "decision": "Keep the local source-coupling branch alive as a conditional bridge, not a claim.",
            "rationale": "The bridge equation is derived with an explicit R_bridge; proxy rank closure is stable but parent source ownership is unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3487_1_not_a_dead_end",
            "decision": "Do not throw away 3485-3486.",
            "rationale": "They establish that the DD proxy has the right algebraic structure and a stable neutron-excess component; the remaining issue is ownership, not rank existence.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3487_2_best_next_attack",
            "decision": "Derive the no-source-only ordinary matter grammar or extract a finite parent source-current coefficient row.",
            "rationale": "That closes the largest bridge residual rather than circling WEP evidence.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3488-Y5-R2FR-no-source-only-matter-grammar-or-finite-Jq-coefficient-row.md",
            "next_script": "scripts/Y5_R2FR_3488_no_source_only_matter_grammar_or_finite_Jq_coefficient_row.py",
            "objective": "Try to prove the ordinary-matter grammar forbids independent source/species prefactors; if not, construct the first finite parent J_q coefficient row feeding R_bridge.",
            "success_gate": "GATE3487_2 and GATE3487_3 close by theorem, or R_matter_glue/R_visible_coeff get source-backed finite bounds",
            "forbidden_shortcuts": "setting R_bridge=0 by declaration; using DD proxy as parent-owned; running more WEP rank rows instead of attacking source ownership",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "check_id": "VAL3487_0_sources_exist",
            "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()),
            "detail": "all cited local sources exist",
            "valid_for_claim": "False",
        }
    )
    parse_ok = True
    details = []
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{name}:ERROR:{exc}")
    rows.append({"check_id": "VAL3487_1_csv_parse", "passed": parse_ok, "detail": "; ".join(details), "valid_for_claim": "False"})
    rows.append(
        {
            "check_id": "VAL3487_2_bridge_equation_present",
            "passed": True,
            "detail": "S_E^q = Q_Earth dot C + R_bridge written in bridge derivation and theorem ledger",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3487_3_parent_claim_blocked",
            "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates),
            "detail": "blocking parent gates remain explicit",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3487_4_proxy_evidence_retained",
            "passed": any(row["passed"] == "True" and row["gate_id"] == "GATE3487_6_rank_closure_proxy_stable" for row in gates),
            "detail": "3485-3486 proxy closure is retained as conditional evidence",
            "valid_for_claim": "False",
        }
    )
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append({"check_id": "VAL3487_5_no_claim", "passed": all(row.get("valid_for_claim") == "False" for row in all_rows), "detail": "all generated rows valid_for_claim=false", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3487_6_no_formalization_outputs", "passed": all(FORMALIZATION not in path.parents for path in outputs.values()), "detail": "outputs are under post-checkpoint-work/source-intake only", "valid_for_claim": "False"})
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append({"check_id": "VAL3487_SUMMARY", "passed": passed, "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep] + body)


def write_doc(
    bridge: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3487: Parent Source Map For DD Earth Vector Or Local Rank Closure Demotion",
                "",
                "## Current Verdict",
                "- **Actual bridge derived:** `S_E^q = Q_Earth · C + R_bridge`.",
                "- **Good news:** 3485-3486 are not junk; they are a proxy-stable conditional source-coupling closure.",
                "- **Hard guard:** this is not parent-owned until `R_bridge` is zero-derived or bounded from the parent action.",
                "- **Best next attack:** ordinary-matter grammar / no-source-only slot, because that is the biggest remaining source-map loophole.",
                "- **No claim:** no local-GR, Newton, WEP, Maxwell/EM, or calibrated source-coupling pass is claimed here.",
                "",
                "## Bridge Derivation",
                md_table(bridge, ["step_id", "claim", "derivation", "status", "valid_for_claim"]),
                "",
                "## Residual Bridge Slots",
                md_table(residuals, ["bridge_residual_id", "source_residual_id", "bridge_formula_slot", "current_status", "required_zero_or_bound", "blocks_parent_promotion", "valid_for_claim"]),
                "",
                "## Parent Promotion Gates",
                md_table(gates, ["gate_id", "requirement", "evidence", "passed", "blocks_claim", "valid_for_claim"]),
                "",
                "## Status Ledger",
                md_table(statuses, ["status_id", "status", "meaning", "claim_allowed", "valid_for_claim"]),
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
    bridge = bridge_derivation_rows()
    residuals = residual_bridge_rows()
    gates = parent_gate_rows()
    statuses = bridge_status_rows(gates)
    theorems = theorem_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3487_SOURCE_REGISTER.csv",
        "bridge_derivation": OUT / "P8_Y5_R2FR_3487_PARENT_TO_DD_BRIDGE_DERIVATION.csv",
        "residual_slots": OUT / "P8_Y5_R2FR_3487_RBRIDGE_RESIDUAL_SLOTS.csv",
        "parent_gates": OUT / "P8_Y5_R2FR_3487_PARENT_PROMOTION_GATES.csv",
        "status_ledger": OUT / "P8_Y5_R2FR_3487_STATUS_LEDGER.csv",
        "theorems": OUT / "P8_Y5_R2FR_3487_THEOREM_LEDGER.csv",
        "decisions": OUT / "P8_Y5_R2FR_3487_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3487_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["bridge_derivation"], bridge, ["step_id", "claim", "derivation", "input_source", "status", "valid_for_claim"])
    write_csv(outputs["residual_slots"], residuals, ["bridge_residual_id", "source_residual_id", "bridge_formula_slot", "current_status", "required_zero_or_bound", "blocks_parent_promotion", "source_path", "valid_for_claim"])
    write_csv(outputs["parent_gates"], gates, ["gate_id", "requirement", "evidence", "passed", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["status_ledger"], statuses, ["status_id", "status", "meaning", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, gates)
    validation_path = OUT / "P8_Y5_BRR545_3487_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(bridge, residuals, gates, statuses, theorems, decisions, next_rows, validation)


if __name__ == "__main__":
    main()

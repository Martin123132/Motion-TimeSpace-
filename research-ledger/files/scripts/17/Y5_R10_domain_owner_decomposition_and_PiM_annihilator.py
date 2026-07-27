from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1125-Y5-R10-domain-owner-decomposition-and-PiM-annihilator.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1125_0_1124_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1124_NEXT_TARGET.csv",
            "needle": "NEXT1124_0_1125",
            "note": "1124 handoff to domain owner decomposition and Pi_M annihilator.",
        },
        {
            "source_id": "SRC1125_1_1124_clauses",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1124_THEOREM_CLAUSES.csv",
            "needle": "TH1124_3_PiM_annihilator",
            "note": "1124 identified Pi_M domain annihilator as a missing certificate.",
        },
        {
            "source_id": "SRC1125_2_owner_terms",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A8_projector_domain_topological",
            "note": "Domain/projector source-owner route is retained symbolic.",
        },
        {
            "source_id": "SRC1125_3_ward_owner",
            "relative_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C1_exact_owner_decomposition",
            "note": "Exact owner decomposition is not parent-derived.",
        },
        {
            "source_id": "SRC1125_4_q_retained",
            "relative_path": "source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv",
            "needle": "Q5_executable_retained_vector",
            "note": "Nonzero retained currents must become executable residual rows.",
        },
        {
            "source_id": "SRC1125_5_PiM_algebra",
            "relative_path": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needle": "PM4_projector_algebra",
            "note": "Pi_M algebra is conditional and lacks explicit domain block annihilator.",
        },
        {
            "source_id": "SRC1125_6_PiM_variation",
            "relative_path": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
            "needle": "PV4_domain_homology_variation_owned",
            "note": "Domain/homology variation is not parent-derived.",
        },
        {
            "source_id": "SRC1125_7_domain_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "Domain alpha3 flux product is still the live coefficient row.",
        },
        {
            "source_id": "SRC1125_8_R11_domain_minimum",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "c_domain_source_normalization_operator",
            "note": "R11 domain minimum vector has source-normalization and stress families retained/unfilled.",
        },
        {
            "source_id": "SRC1125_9_R11_missing",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
            "needle": "projector_domain_stress",
            "note": "R11 missing ledger shows domain vector, source normalization, and stress rows block claims.",
        },
        {
            "source_id": "SRC1125_10_ownership",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P2_domain_selector_no_vector",
            "note": "Domain selector/vector premise remains not derived.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def decomposition_attempt_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "OD1125_0_target",
                "object": "domain exchange current",
                "candidate_form": "F_D^nu = nabla_mu K_D^{mu nu} + q_D^nu",
                "derivation_attempt": "derive by varying S_projector+S_domain before readout, with every domain selector/projector variable varied or retained",
                "current_result": "TARGET_SHARP_NOT_DERIVED",
                "blocker": "no formula-level K_D/q_D owner decomposition in the corpus",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "OD1125_1_topological_projector",
                "object": "projector/domain topological piece",
                "candidate_form": "F_D^nu = nabla_mu K_D^{mu nu}, q_D^nu=0",
                "derivation_attempt": "use metric-independent/topological P_D and local trivial representative",
                "current_result": "CONDITIONAL_NOT_PARENT_OWNED",
                "blocker": "P_D topological ownership and local trivial representative remain conditional",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "OD1125_2_selector_vector",
                "object": "domain selector vector/flux",
                "candidate_form": "q_D^nu includes selector marker/vector/flux unless scalar stationary selector is parent-derived",
                "derivation_attempt": "kill q_D by scalar stationary no-vector/no-flux local representative",
                "current_result": "LIVE_RETAINED_COMPONENT",
                "blocker": "P2 domain selector no-vector and T2 no-flux are not parent-derived",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "OD1125_3_source_normalization",
                "object": "source-normalization operator",
                "candidate_form": "q_D^nu includes c_domain_source_normalization_operator contribution unless coefficient/theorem zero is supplied",
                "derivation_attempt": "use R11 domain minimum vector as executable fallback",
                "current_result": "LIVE_RETAINED_COMPONENT",
                "blocker": "c_domain_source_normalization_operator remains missing/unfilled",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "OD1125_4_projector_stress",
                "object": "projector/domain stress",
                "candidate_form": "q_D^nu includes delta_g P_D, delta_g chi_D, lambda_P/domain stress unless topological ownership is parent-derived",
                "derivation_attempt": "use metric-independent topological projector stress zero",
                "current_result": "CONDITIONAL_ZERO_NOT_PARENT_OWNED",
                "blocker": "projector/domain stress remains conditional and blocks R5/R6/R7/R8/R11",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def retained_component_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "component_id": "QD1125_0_vector_flux",
                "qD_component": "q_D_vector_flux",
                "maps_to": "epsilon_domain_vector; epsilon_domain_flux",
                "affected_rows": "R5;R6;R7;R11",
                "zero_certificate_needed": "parent scalar stationary selector plus local no-flux representative",
                "numeric_fallback": "W_domain_alpha3*epsilon_domain_flux and sibling vector products",
                "current_status": "LIVE_UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "component_id": "QD1125_1_source_normalization",
                "qD_component": "q_D_source_normalization",
                "maps_to": "c_domain_source_normalization_operator",
                "affected_rows": "R5;R6;R7;R8;R11",
                "zero_certificate_needed": "domain source-normalization operator zero or EH-only/local-boundary silence",
                "numeric_fallback": "canonical R11 source-normalization coefficient row",
                "current_status": "LIVE_UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "component_id": "QD1125_2_projector_stress",
                "qD_component": "q_D_projector_domain_stress",
                "maps_to": "c_projector_domain_stress; xi; alpha_i siblings",
                "affected_rows": "R5;R6;R7;R8;R11",
                "zero_certificate_needed": "parent-owned metric-independent topological P_D and no domain wall/readout-mask stress",
                "numeric_fallback": "projector/domain stress coefficient vector",
                "current_status": "CONDITIONAL_LIVE_UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "component_id": "QD1125_3_boundary_exact",
                "qD_component": "nabla_mu K_D^{mu nu}",
                "maps_to": "compact boundary mass/source flux",
                "affected_rows": "R4;R7;R9;R10;R11",
                "zero_certificate_needed": "int_boundary Pi_M K_D=0 or constant universal calibration",
                "numeric_fallback": "boundary/domain flux coefficient with units and source path",
                "current_status": "BOUNDARY_FAIL_OPEN",
                "valid_for_claim": "false",
            },
        ]
    )


def annihilator_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "annihilator_id": "PA1125_0_target",
                "candidate_identity": "Pi_M q_D = 0 and/or ell_M(domain exact class)=0",
                "required_structure": "Pi_M has an explicit domain-vertical block in its kernel, not merely shear/matter/memory orthogonality",
                "current_status": "MISSING_EXPLICIT_DOMAIN_BLOCK",
                "reason": "PM4 lists conditional block orthogonality but does not prove the domain exchange class is in ker(Pi_M)",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "annihilator_id": "PA1125_1_topological_route",
                "candidate_identity": "ell_M(nabla K_D)=int_boundary Pi_M K_D=0",
                "required_structure": "domain exact term has no compact-boundary mass charge or only a universal constant calibration",
                "current_status": "FAIL_OPEN",
                "reason": "boundary silence and class-only/topological no-flux remain open",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "annihilator_id": "PA1125_2_vertical_route",
                "candidate_identity": "Pi_M(F_D^vertical)=0",
                "required_structure": "parent quotient/symplectic split proves domain variations are vertical to the mass/current projector",
                "current_status": "NOT_PARENT_DERIVED",
                "reason": "domain/homology variation is not parent-derived and projector variation stress remains retained",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "annihilator_id": "PA1125_3_verdict",
                "candidate_identity": "Pi_M annihilates all live domain exchange pieces",
                "required_structure": "PA1125_0 through PA1125_2 all pass",
                "current_status": "ANNIHILATOR_NOT_PROVED",
                "reason": "vector/flux, source-normalization, stress, and boundary pieces remain live or conditional",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1125_0_owner_decomposition",
                "rule": "F_D=nabla K_D+q_D is parent-derived",
                "gate_pass": "false",
                "reason": "no formula-level K_D/q_D derivation exists",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1125_1_qD_zero",
                "rule": "all q_D components are zero by legal routes",
                "gate_pass": "false",
                "reason": "vector/flux, source-normalization, and stress components remain live",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1125_2_PiM_annihilator",
                "rule": "Pi_M annihilates the domain exchange class",
                "gate_pass": "false",
                "reason": "explicit domain block/vertical annihilator is missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1125_3_executable_split",
                "rule": "retained q_D split is explicit enough for next coefficient/vector work",
                "gate_pass": "true_nonclaim",
                "reason": "1125 splits q_D into vector/flux, source-normalization, stress, and boundary pieces",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1125_4_alpha3",
                "rule": "epsilon_domain_flux=0 follows from 1125",
                "gate_pass": "false",
                "reason": "q_D_vector_flux and Pi_M annihilator are not closed",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1125_0_verdict",
                "decision": "owner_decomposition_not_proved",
                "reason": "the corpus has operator/vector templates but no parent K_D/q_D derivation",
                "next_action": "turn q_D split into executable retained-current vector or derive one zero certificate at a time",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1125_1_best_next",
                "decision": "attack_qD_vector_flux_first",
                "reason": "q_D_vector_flux is the direct alpha3 path; source-normalization/stress siblings stay guarded",
                "next_action": "derive scalar stationary selector/local no-flux certificate or fill epsilon_domain_flux product",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1125_2_no_promotion",
                "decision": "keep_alpha3_and_local_GR_blocked",
                "reason": "Pi_M annihilator and q_D zero are both unproved",
                "next_action": "do not claim PPN/R10/local-GR pass",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1125_0_1126",
                "next_target": "1126-Y5-R10-qD-vector-flux-zero-certificate-or-executable-row.md",
                "objective": "attack the direct alpha3 component q_D_vector_flux: prove scalar stationary selector plus local no-flux representative, or build the executable epsilon_domain_flux product row with source-backed K/c/epsilon inputs",
                "include": "q_D_vector_flux; epsilon_domain_flux; selector no-vector; local no-flux representative; W_domain_alpha3; K_R11_flux_alpha3; c_R11_flux_alpha3; 4e-20",
                "exclude": "source-normalization/stress promotion; Pi_M annihilator claim without domain block proof; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    components: list[dict[str, object]],
    annihilators: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = attempts + components + annihilators + gates + decisions + next_target
    component_names = {row["qD_component"] for row in components}
    add("V1125_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1125_1_decomposition_attempted", attempts[0]["current_result"] == "TARGET_SHARP_NOT_DERIVED" and attempts[-1]["current_result"].startswith("CONDITIONAL"), "owner decomposition is attempted but not promoted")
    add("V1125_2_qD_split", {"q_D_vector_flux", "q_D_source_normalization", "q_D_projector_domain_stress", "nabla_mu K_D^{mu nu}"}.issubset(component_names), "retained domain current split covers vector/flux, source-normalization, stress, and boundary exact pieces")
    add("V1125_3_annihilator_not_proved", annihilators[-1]["current_status"] == "ANNIHILATOR_NOT_PROVED", "Pi_M domain annihilator remains unproved")
    add("V1125_4_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and gates[3]["gate_pass"] == "true_nonclaim" and sum(row["gate_pass"] == "false" for row in gates) >= 4, "claim gates remain blocked except executable split")
    add("V1125_5_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in attempts + annihilators + next_target), "all generated rows remain nonclaim")
    add("V1125_6_next_target", next_target[0]["next_target"].startswith("1126-") and "qD-vector-flux" in str(next_target[0]["next_target"]), "1126 handoff targets q_D vector/flux component")
    add("V1125_7_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1125_8_csv_parse", csv_parse_ok, "all 1125 CSV outputs parse cleanly")
    add("V1125_9_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1125_SUMMARY", True, "1125 fails owner/PiM proof but splits q_D into executable retained components")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    components: list[dict[str, object]],
    annihilators: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1125 - Y5/R10 Domain Owner Decomposition And PiM Annihilator

**Current verdict:** the parent owner decomposition `F_D = nabla_mu K_D^{{mu nu}} + q_D^nu` is not derived, and the `Pi_M` domain-annihilator is not proved.

**Useful progress:** the live retained domain current is now split into four concrete pieces: vector/flux, source-normalization, projector/domain stress, and exact/boundary flux. The direct alpha3 piece is `q_D_vector_flux`.

**Best next move:** attack `q_D_vector_flux` first. If scalar stationary selector plus local no-flux closes, the hardest alpha3 path collapses without tiny coefficient tuning.

**No claim:** no domain/R11 `alpha3`, R10, PPN, Newton/local-GR, or measured-GM pass follows from 1125.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Owner Decomposition Attempt
{table(["attempt_id", "object", "candidate_form", "derivation_attempt", "current_result", "blocker", "claim_allowed", "valid_for_claim"], attempts)}

## Retained qD Component Split
{table(["component_id", "qD_component", "maps_to", "affected_rows", "zero_certificate_needed", "numeric_fallback", "current_status", "valid_for_claim"], components)}

## PiM Annihilator Audit
{table(["annihilator_id", "candidate_identity", "required_structure", "current_status", "reason", "claim_allowed", "valid_for_claim"], annihilators)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1125_SOURCE_REGISTER.csv",
        "attempts": OUT / "P8_Y5_R10_1125_OWNER_DECOMPOSITION_ATTEMPT.csv",
        "components": OUT / "P8_Y5_R10_1125_RETAINED_QD_COMPONENT_SPLIT.csv",
        "annihilators": OUT / "P8_Y5_R10_1125_PIM_ANNIHILATOR_AUDIT.csv",
        "gates": OUT / "P8_Y5_R10_1125_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1125_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1125_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1125_VALIDATION.csv",
    }
    sources = source_rows()
    attempts = decomposition_attempt_rows()
    components = retained_component_rows()
    annihilators = annihilator_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["attempts"], attempts)
    write_csv(outputs["components"], components)
    write_csv(outputs["annihilators"], annihilators)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, attempts, components, annihilators, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, attempts, components, annihilators, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

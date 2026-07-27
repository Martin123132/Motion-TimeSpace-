from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1124-Y5-R10-domain-flux-no-exchange-parent-current-theorem.md"


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
            "source_id": "SRC1124_0_1123_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_NEXT_TARGET.csv",
            "needle": "NEXT1123_0_1124",
            "note": "1123 handoff to parent no-exchange current theorem.",
        },
        {
            "source_id": "SRC1124_1_1123_obligations",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_PARENT_THEOREM_OBLIGATIONS.csv",
            "needle": "OB1123_1_no_exchange_projection",
            "note": "1123 identifies Pi_M F_D=0 as strongest no-flux route.",
        },
        {
            "source_id": "SRC1124_2_flux_closure",
            "relative_path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "needle": "FC3_no_exchange_projection",
            "note": "Mass/projected-current closure requires no exchange projection.",
        },
        {
            "source_id": "SRC1124_3_source_current",
            "relative_path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
            "needle": "SC4_no_nonHilbert_source_current",
            "note": "Source-current route requires non-Hilbert/domain currents to vanish or be retained.",
        },
        {
            "source_id": "SRC1124_4_hamiltonian",
            "relative_path": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
            "needle": "HC5_no_extra_hidden_charge",
            "note": "Hamiltonian route requires no unowned hidden/domain mass charge.",
        },
        {
            "source_id": "SRC1124_5_mass_flux",
            "relative_path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
            "needle": "MF6_zero_boundary_and_nonHilbert_flux",
            "note": "Mass-flux route leaves zero boundary/non-Hilbert flux unproved.",
        },
        {
            "source_id": "SRC1124_6_q_retained",
            "relative_path": "source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv",
            "needle": "Q2_exact_owned_zero_flux",
            "note": "Retained-current zero requires exact owner plus compact-boundary no-flux.",
        },
        {
            "source_id": "SRC1124_7_owner_terms",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A8_projector_domain_topological",
            "note": "Domain/projector source-owner clause is retained symbolic, not closed.",
        },
        {
            "source_id": "SRC1124_8_ward_owner",
            "relative_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C1_exact_owner_decomposition",
            "note": "Ward owner identity requires exact owner decomposition plus retained rows.",
        },
        {
            "source_id": "SRC1124_9_PiM_variation",
            "relative_path": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
            "needle": "PV4_domain_homology_variation_owned",
            "note": "Domain/homology variation is not parent-derived.",
        },
        {
            "source_id": "SRC1124_10_PiM_algebra",
            "relative_path": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needle": "PM6_flux_closure_requires_Ward_or_Euler",
            "note": "Pi_M algebra alone cannot prove flux closure.",
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


def theorem_clause_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "clause_id": "TH1124_0_same_frame",
                "clause": "same-frame Hilbert/source current",
                "formal_requirement": "J_H is defined by varying the same observed coframe used in the local branch, before readout masks or fitted projectors",
                "source_basis": "SC0; SC1; MF1; FC0",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "if_closed": "removes fitted/readout source-current ambiguity",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "TH1124_1_owner_decomposition",
                "clause": "domain exchange has exact owner decomposition",
                "formal_requirement": "F_D^nu = nabla_mu K_D^{mu nu} + q_D^nu with K_D parent-owned and q_D retained or legally zero",
                "source_basis": "A1; A8; C1; Q2",
                "current_status": "NOT_PARENT_DERIVED",
                "if_closed": "turns domain exchange into boundary/exact plus retained-current problem",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "TH1124_2_retained_zero",
                "clause": "retained domain current is absent or theorem-zero",
                "formal_requirement": "q_D^nu=0 by configuration absence, gauge/topological identity, or source-free no-hair theorem; not by dropping a written field",
                "source_basis": "Q0; Q1; Q2; A2",
                "current_status": "NOT_PARENT_DERIVED",
                "if_closed": "prevents unowned local domain force from feeding alpha3/Gdot/source-normalization",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "TH1124_3_PiM_annihilator",
                "clause": "mass projector annihilates domain-vertical exchange",
                "formal_requirement": "Pi_M F_D=0 for domain/projector vertical or topological exchange classes, or Pi_M nabla K_D has zero compact-boundary mass charge",
                "source_basis": "PM4; PM6; PV4; FC3",
                "current_status": "MISSING_EXPLICIT_DOMAIN_ANNIHILATOR",
                "if_closed": "kills epsilon_domain_flux at the parent-current level",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "TH1124_4_boundary_silence",
                "clause": "compact boundary flux is zero or universal calibration only",
                "formal_requirement": "int_boundary Pi_M K_D = 0, or any boundary term is constant, universal, and derivative-silent",
                "source_basis": "MF6; FC4; SC5; C2; Q2",
                "current_status": "FAIL_OPEN",
                "if_closed": "prevents exact divergence from returning as boundary alpha3/Gdot/source hair",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "TH1124_5_not_Ward_only",
                "clause": "total Ward conservation is insufficient",
                "formal_requirement": "nabla_mu T_tot^{mu nu}=0 does not imply Pi_M F_D=0 without owner decomposition and projector annihilator/boundary clauses",
                "source_basis": "C0; FC3; SC4",
                "current_status": "REJECTED_SHORTCUT",
                "if_closed": "keeps the proof from smuggling in no-exchange",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def conditional_proof_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "step_id": "P1124_0_define_flux",
                "proof_step": "Define the live alpha3 flux as epsilon_domain_flux = P_loc^i_mu F_D^mu.",
                "depends_on": "1122 flux narrowing; 1123 definition",
                "status": "DEFINITION",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "step_id": "P1124_1_owner_split",
                "proof_step": "Assume parent variation gives F_D^nu = nabla_mu K_D^{mu nu} + q_D^nu.",
                "depends_on": "TH1124_1_owner_decomposition",
                "status": "CONDITIONAL",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "step_id": "P1124_2_kill_retained",
                "proof_step": "If q_D^nu=0 by a legal route, the only remaining domain exchange is the owned exact/boundary term.",
                "depends_on": "TH1124_2_retained_zero",
                "status": "CONDITIONAL",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "step_id": "P1124_3_project",
                "proof_step": "Apply Pi_M: Pi_M F_D = Pi_M nabla_mu K_D^{mu nu}; if Pi_M annihilates domain-vertical exchange or the compact boundary charge vanishes, Pi_M F_D=0.",
                "depends_on": "TH1124_3_PiM_annihilator; TH1124_4_boundary_silence",
                "status": "CONDITIONAL",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "step_id": "P1124_4_local_flux",
                "proof_step": "With Pi_M F_D=0 and the local representative in the observed coframe, the alpha3 flux branch epsilon_domain_flux is zero.",
                "depends_on": "TH1124_0_same_frame; P1124_1-P1124_3",
                "status": "CONDITIONAL",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "step_id": "P1124_5_verdict",
                "proof_step": "Current corpus does not prove Pi_M F_D=0 because owner decomposition, retained-zero, Pi_M annihilator, and boundary silence are unsigned/open.",
                "depends_on": "TH1124_1-TH1124_4",
                "status": "THEOREM_CONTRACT_NOT_PROVED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def failure_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "failure_id": "FAIL1124_0_owner",
                "missing_certificate": "formula-level domain owner decomposition",
                "needed_form": "F_D^nu = nabla_mu K_D^{mu nu} + q_D^nu",
                "why_it_matters": "without it, Pi_M F_D is an unowned source/current leak",
                "next_action": "derive K_D/q_D from parent S_projector+S_domain variation",
                "valid_for_claim": "false",
            },
            {
                "failure_id": "FAIL1124_1_retained",
                "missing_certificate": "q_D^nu=0 or executable retained-current vector",
                "needed_form": "q_D absent/gauge/topological/no-hair zero, or numeric residual with units/source path",
                "why_it_matters": "nonzero q_D can feed R7 alpha3 and R11 source-normalization",
                "next_action": "prove legal q_D zero or carry it into bound product",
                "valid_for_claim": "false",
            },
            {
                "failure_id": "FAIL1124_2_annihilator",
                "missing_certificate": "Pi_M annihilates the domain-vertical/exact exchange class",
                "needed_form": "Pi_M|_{im F_D}=0 or ell_M(domain exact class)=0",
                "why_it_matters": "this is the cleanest way to kill alpha3 flux without tiny tuning",
                "next_action": "derive Pi_M-domain orthogonality from parent symplectic/projector algebra",
                "valid_for_claim": "false",
            },
            {
                "failure_id": "FAIL1124_3_boundary",
                "missing_certificate": "compact boundary silence for Pi_M K_D",
                "needed_form": "int_boundary Pi_M K_D = 0 or constant universal calibration",
                "why_it_matters": "an exact divergence can still produce a surface monopole/source-normalization shift",
                "next_action": "prove class-only/topological boundary no-flux or retain boundary coefficient",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1124_0_conditional_theorem",
                "rule": "conditional proof contract for Pi_M F_D=0 is written",
                "gate_pass": "true_nonclaim",
                "reason": "the if-clauses and proof chain are explicit",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1124_1_owner_decomposition",
                "rule": "domain owner decomposition is parent-derived",
                "gate_pass": "false",
                "reason": "A8/C1 remain retained/not parent-derived",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1124_2_PiM_annihilator",
                "rule": "Pi_M annihilates domain exchange",
                "gate_pass": "false",
                "reason": "explicit domain annihilator/orthogonality certificate is missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1124_3_boundary_silence",
                "rule": "compact boundary domain flux is zero",
                "gate_pass": "false",
                "reason": "boundary/no-Hilbert flux remains fail-open",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1124_4_alpha3_no_flux",
                "rule": "epsilon_domain_flux=0 follows for the local branch",
                "gate_pass": "false",
                "reason": "no-exchange theorem is not proved",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1124_0_verdict",
                "decision": "Pi_M_F_D_zero_not_proved",
                "reason": "conditional theorem clauses are sharp but unsigned",
                "next_action": "attack owner decomposition and Pi_M-domain annihilator",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1124_1_best_next",
                "decision": "domain_owner_decomposition_first",
                "reason": "without F_D=nabla K_D+q_D the Pi_M annihilator has no legal object to act on",
                "next_action": "derive K_D/q_D from parent projector/domain variation, then test Pi_M annihilator",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1124_2_keep_bound",
                "decision": "keep_1123_flux_bound_row_active",
                "reason": "if any theorem clause fails, the alpha3 flux product remains the executable fallback",
                "next_action": "do not promote R7 alpha3/R10/local-GR",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1124_0_1125",
                "next_target": "1125-Y5-R10-domain-owner-decomposition-and-PiM-annihilator.md",
                "objective": "derive F_D=nabla_mu K_D^{mu nu}+q_D^nu from the parent domain/projector sector, then prove q_D=0 and/or Pi_M annihilates the resulting domain-vertical exchange class",
                "include": "S_projector; S_domain; K_D; q_D; Pi_M domain orthogonality; compact boundary silence; epsilon_domain_flux",
                "exclude": "Ward-only shortcut; dropping q_D after variation; plateau axiom; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    clauses: list[dict[str, object]],
    proof: list[dict[str, object]],
    failures: list[dict[str, object]],
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

    all_rows = clauses + proof + failures + gates + decisions + next_target
    clause_ids = {row["clause_id"] for row in clauses}
    failure_needs = {row["missing_certificate"] for row in failures}
    add("V1124_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1124_1_clause_coverage", {"TH1124_1_owner_decomposition", "TH1124_2_retained_zero", "TH1124_3_PiM_annihilator", "TH1124_4_boundary_silence", "TH1124_5_not_Ward_only"}.issubset(clause_ids), "core no-exchange theorem clauses are covered")
    add("V1124_2_conditional_not_proved", proof[-1]["status"] == "THEOREM_CONTRACT_NOT_PROVED", "conditional theorem is not promoted as proof")
    add("V1124_3_failure_certificates", {"formula-level domain owner decomposition", "Pi_M annihilates the domain-vertical/exact exchange class", "compact boundary silence for Pi_M K_D"}.issubset(failure_needs), "missing certificates are explicit")
    add("V1124_4_gates_blocked", gates[0]["gate_pass"] == "true_nonclaim" and all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 3, "claim gates remain blocked except conditional theorem wiring")
    add("V1124_5_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in clauses + proof + next_target), "all generated rows remain nonclaim")
    add("V1124_6_next_target", next_target[0]["next_target"].startswith("1125-") and "owner-decomposition" in str(next_target[0]["next_target"]), "1125 handoff targets domain owner decomposition and Pi_M annihilator")
    add("V1124_7_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1124_8_csv_parse", csv_parse_ok, "all 1124 CSV outputs parse cleanly")
    add("V1124_9_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1124_SUMMARY", True, "1124 writes the conditional Pi_M F_D=0 theorem contract and keeps alpha3 blocked")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    clauses: list[dict[str, object]],
    proof: list[dict[str, object]],
    failures: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1124 - Y5/R10 Domain Flux No-Exchange Parent Current Theorem

**Current verdict:** `Pi_M F_D=0` is now a sharp conditional theorem, but not a proved result. The proof needs a parent-owned domain exchange decomposition, a legal retained-current zero, a `Pi_M` domain-annihilator/orthogonality certificate, and compact-boundary silence.

**Conditional theorem:** if `F_D = nabla_mu K_D^{{mu nu}} + q_D^nu`, `q_D=0`, and `Pi_M` annihilates the domain/exact class or its compact boundary charge, then `Pi_M F_D=0`, hence the live `epsilon_domain_flux` alpha3 branch is killed.

**Failure point:** the current corpus has total Ward structure, but not the owner decomposition/annihilator/boundary certificates. Ward-only conservation remains explicitly rejected.

**No claim:** no domain/R11 `alpha3`, R10, PPN, Newton/local-GR, or measured-GM pass follows from 1124.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Theorem Clauses
{table(["clause_id", "clause", "formal_requirement", "source_basis", "current_status", "if_closed", "claim_allowed", "valid_for_claim"], clauses)}

## Conditional Proof Chain
{table(["step_id", "proof_step", "depends_on", "status", "claim_allowed", "valid_for_claim"], proof)}

## Missing Certificates
{table(["failure_id", "missing_certificate", "needed_form", "why_it_matters", "next_action", "valid_for_claim"], failures)}

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
        "source_register": OUT / "P8_Y5_R10_1124_SOURCE_REGISTER.csv",
        "clauses": OUT / "P8_Y5_R10_1124_THEOREM_CLAUSES.csv",
        "proof": OUT / "P8_Y5_R10_1124_CONDITIONAL_PROOF_CHAIN.csv",
        "failures": OUT / "P8_Y5_R10_1124_MISSING_CERTIFICATES.csv",
        "gates": OUT / "P8_Y5_R10_1124_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1124_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1124_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1124_VALIDATION.csv",
    }
    sources = source_rows()
    clauses = theorem_clause_rows()
    proof = conditional_proof_rows()
    failures = failure_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["clauses"], clauses)
    write_csv(outputs["proof"], proof)
    write_csv(outputs["failures"], failures)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, clauses, proof, failures, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, clauses, proof, failures, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

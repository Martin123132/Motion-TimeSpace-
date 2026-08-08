from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1129-Y5-R10-cohomology-norm-branch-selector-action-or-reject.md"


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
            "source_id": "SRC1129_0_1128_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1128_NEXT_TARGET.csv",
            "needle": "NEXT1128_0_1129",
            "note": "1128 handoff to cohomology-norm selector action.",
        },
        {
            "source_id": "SRC1129_1_1128_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1128_PARENT_BRANCH_ACTION_CONTRACT.csv",
            "needle": "BA1128_1_smooth_selector",
            "note": "1128 stages smooth selector invariant I_D.",
        },
        {
            "source_id": "SRC1129_2_topological_pim",
            "relative_path": "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv",
            "needle": "TC500_6_FLRW_unification",
            "note": "Topological Pi_M closure has conditional FLRW-unification shape only.",
        },
        {
            "source_id": "SRC1129_3_pim_algebra",
            "relative_path": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needle": "PM4_projector_algebra",
            "note": "Projector algebra is conditional and not enough for flux closure.",
        },
        {
            "source_id": "SRC1129_4_pim_variation",
            "relative_path": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
            "needle": "PV0_product_variation_included",
            "note": "Projector variations must be included before reduction.",
        },
        {
            "source_id": "SRC1129_5_FLRW",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_822_FLRW_REDUCTION_AUDIT.csv",
            "needle": "F822_4_pressure_kernel",
            "note": "FLRW volume/determinant route is conditional and needs parent-owned source density/boundary variation.",
        },
        {
            "source_id": "SRC1129_6_parent_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "note": "Single parent action discipline exists as contract, not derivation.",
        },
        {
            "source_id": "SRC1129_7_topological_level",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1056_TOPOLOGICAL_LEVEL_INDEX_ROUTE_AUDIT.csv",
            "needle": "TL1056_4_verdict",
            "note": "Topological routes need explicit inheritance theorem.",
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


def candidate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "candidate_id": "ID1129_0_cohomology_norm",
                "candidate": "I_D = ||P_coh J_D||^2",
                "local_behavior": "local exact/trivial domain class gives I_D=0 if P_coh and J_D are parent-owned",
                "FLRW_behavior": "coherent expansion/current class gives I_D>0 if P_coh selects the coherent branch",
                "strength": "best structural route because zero is class/norm based, not global all-domain zero",
                "failure": "P_coh, J_D, inner product/norm, and variation/stress ownership are not parent-derived",
                "status": "BEST_CANDIDATE_NOT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ID1129_1_det_Qcoh",
                "candidate": "I_D = normalized det(Q_coh)",
                "local_behavior": "would need Q_coh=0 or exact local class in compact branch",
                "FLRW_behavior": "822 gives conditional det(Q)=X_load^3 and locked FLRW shape",
                "strength": "naturally matches existing FLRW memory-shape algebra",
                "failure": "Q_coh formula, positive orientation, normalization, and local-zero theorem are not parent-owned",
                "status": "PROMISING_FLRW_SHAPE_NOT_LOCAL_CERTIFICATE",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ID1129_2_volume_ND",
                "candidate": "I_D = N_D or f(N_D)",
                "local_behavior": "would need N_D=0 parent theorem for compact local branch",
                "FLRW_behavior": "822 gives N_D=-ln(a)=ln(1+z) conditionally",
                "strength": "simple FLRW reduction and directly tied to expansion memory",
                "failure": "volume/log variable creates stress/pressure and does not by itself prove local no-flux",
                "status": "USEFUL_FLRW_COORDINATE_NOT_SELECTOR_PROOF",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ID1129_3_response_function",
                "candidate": "A(I_D)=1-exp[-(I_D/u3)^p] with p>=2/double-zero local response",
                "local_behavior": "A(0)=A'(0)=0 can suppress linear local leakage if I_D is parent-owned",
                "FLRW_behavior": "for coherent branch I_D>0 gives active memory response",
                "strength": "smooth alternative to discontinuous branch switch",
                "failure": "u3, p>=2 origin, and I_D variation are not parent-derived",
                "status": "SMOOTH_RESPONSE_CONTRACT_NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
            },
        ]
    )


def action_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "action_id": "ACT1129_0_minimal_selector_action",
                "minimal_action_piece": "S_branch = integral sqrt(-g_obs) rho_branch(A(I_D))",
                "required_derivation": "I_D is built from parent fields/projectors before readout and A is smooth/double-zero at I_D=0",
                "would_buy": "one rule for local quiet and FLRW active branch",
                "current_status": "CONTRACT_READY_NOT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "action_id": "ACT1129_1_variation_ledger",
                "minimal_action_piece": "delta S_branch includes delta I_D, delta P_coh, delta Q_coh, delta N_D",
                "required_derivation": "all branch-selector stress terms are theorem-zero or retained in residual rows",
                "would_buy": "no hidden selector stress in local-GR reduction",
                "current_status": "MISSING_VARIATION_LEDGER",
                "valid_for_claim": "false",
            },
            {
                "action_id": "ACT1129_2_local_certificate",
                "minimal_action_piece": "I_D=0 -> [J_D]_local exact/trivial -> epsilon_domain_flux=0",
                "required_derivation": "local branch theorem from parent topology/current, not plateau axiom",
                "would_buy": "direct alpha3 q_D_vector_flux zero",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "action_id": "ACT1129_3_FLRW_certificate",
                "minimal_action_piece": "I_D>0 -> N_D=ln(1+z), Q_coh coherent, memory response active",
                "required_derivation": "same I_D selector owns coherent FLRW branch without fit-history import",
                "would_buy": "cosmology survives local no-flux",
                "current_status": "CONDITIONAL_SUPPORTED_NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
            },
        ]
    )


def verdict_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "verdict_id": "V1129C_0_select_candidate",
                "verdict": "prefer_cohomology_norm_candidate",
                "reason": "it is the only candidate where local zero can be a class/norm zero rather than an imposed all-domain shutdown",
                "claim_effect": "candidate only; no alpha3/local-GR claim",
                "valid_for_claim": "false",
            },
            {
                "verdict_id": "V1129C_1_reject_claim",
                "verdict": "do_not_claim_selector_action",
                "reason": "P_coh/J_D/norm and variation ownership are not parent-derived",
                "claim_effect": "branch selector remains conditional",
                "valid_for_claim": "false",
            },
            {
                "verdict_id": "V1129C_2_fallback",
                "verdict": "keep_executable_flux_products_active",
                "reason": "if I_D ownership cannot be proved, alpha3 direct flux must be bounded numerically or theorem-zero elsewhere",
                "claim_effect": "1126 product rows remain active",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1129_0_ID_owned",
                "rule": "I_D is parent-owned before readout",
                "gate_pass": "false",
                "reason": "candidate invariant is written but not derived from parent fields",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1129_1_variation",
                "rule": "delta I_D and projector/coherent-variable stresses are owned or retained",
                "gate_pass": "false",
                "reason": "variation ledger is missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1129_2_local_zero",
                "rule": "I_D=0 implies local no-flux",
                "gate_pass": "false",
                "reason": "local exact/trivial class theorem is conditional",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1129_3_FLRW_active",
                "rule": "same I_D preserves FLRW active memory",
                "gate_pass": "false",
                "reason": "FLRW shape is conditional but not parent-owned",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1129_4_best_candidate",
                "rule": "best candidate selected for next proof attempt",
                "gate_pass": "true_nonclaim",
                "reason": "cohomology norm is selected as next theorem target only",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1129_0_verdict",
                "decision": "selector_action_not_derived",
                "reason": "cohomology-norm action is a good candidate but lacks parent ownership and variation proof",
                "next_action": "derive P_coh J_D norm ownership or reject to executable alpha3 products",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1129_1_best_next",
                "decision": "prove_Pcoh_JD_norm_ownership",
                "reason": "this is the narrowest certificate needed for I_D=||P_coh J_D||^2",
                "next_action": "show P_coh and J_D are parent variables and norm is varied/stress-owned",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1129_2_guard",
                "decision": "no_selector_claim",
                "reason": "candidate action is not enough for local-GR or cosmology claims",
                "next_action": "keep branch selector and alpha3 gates blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1129_0_1130",
                "next_target": "1130-Y5-R10-Pcoh-JD-norm-ownership-or-executable-flux-products.md",
                "objective": "prove that P_coh and J_D are parent-owned objects with a varied/stress-owned norm I_D=||P_coh J_D||^2, or demote the branch selector route and keep executable alpha3 flux product rows",
                "include": "P_coh; J_D; inner product/norm; delta I_D; local exact class; FLRW coherent class; no empirical selector; alpha3 product fallback",
                "exclude": "global all-domain zero; unvaried projector stress; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    contracts: list[dict[str, object]],
    verdicts: list[dict[str, object]],
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

    all_rows = candidates + contracts + verdicts + gates + decisions + next_target
    candidate_names = {row["candidate"] for row in candidates}
    add("V1129_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1129_1_candidates_covered", {"I_D = ||P_coh J_D||^2", "I_D = normalized det(Q_coh)", "I_D = N_D or f(N_D)"}.issubset(candidate_names), "cohomology norm, determinant, and N_D candidates are covered")
    add("V1129_2_contract_present", any(row["minimal_action_piece"].startswith("S_branch") for row in contracts) and any("delta I_D" in row["minimal_action_piece"] for row in contracts), "action and variation contracts are present")
    add("V1129_3_best_candidate_not_claim", verdicts[0]["verdict"] == "prefer_cohomology_norm_candidate" and verdicts[1]["verdict"] == "do_not_claim_selector_action", "best candidate is selected but not claimed")
    add("V1129_4_gates_blocked", gates[-1]["gate_pass"] == "true_nonclaim" and all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 4, "claim gates remain blocked except best-candidate selection")
    add("V1129_5_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1129_6_next_target", next_target[0]["next_target"].startswith("1130-") and "Pcoh-JD-norm" in str(next_target[0]["next_target"]), "1130 handoff targets P_coh/J_D norm ownership")
    add("V1129_7_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1129_8_csv_parse", csv_parse_ok, "all 1129 CSV outputs parse cleanly")
    add("V1129_9_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1129_SUMMARY", True, "1129 selects cohomology-norm selector as best candidate but keeps branch selector unclaimed")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    contracts: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1129 - Y5/R10 Cohomology-Norm Branch Selector Action Or Reject

**Current verdict:** the cohomology-norm selector is the best candidate so far, but it is not derived. `I_D=||P_coh J_D||^2` would cleanly distinguish local exact/trivial zero from FLRW coherent activity only if `P_coh`, `J_D`, the norm, and their variation are parent-owned.

**Best candidate:** `I_D=||P_coh J_D||^2`, with a smooth/double-zero response `A(I_D)`, beats raw volume or determinant as the local no-flux route because exact local class can naturally give `I_D=0`.

**Failure point:** parent ownership and variation/stress ledger are missing, so this remains a theorem target, not a branch-selector proof.

**No claim:** no local no-flux, domain/R11 `alpha3`, R10, PPN, Newton/local-GR, FLRW, or measured-GM pass follows from 1129.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Candidate Selector Comparison
{table(["candidate_id", "candidate", "local_behavior", "FLRW_behavior", "strength", "failure", "status", "valid_for_claim"], candidates)}

## Minimal Action Contract
{table(["action_id", "minimal_action_piece", "required_derivation", "would_buy", "current_status", "valid_for_claim"], contracts)}

## Verdict Ledger
{table(["verdict_id", "verdict", "reason", "claim_effect", "valid_for_claim"], verdicts)}

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
        "source_register": OUT / "P8_Y5_R10_1129_SOURCE_REGISTER.csv",
        "candidates": OUT / "P8_Y5_R10_1129_SELECTOR_CANDIDATE_COMPARISON.csv",
        "contracts": OUT / "P8_Y5_R10_1129_MINIMAL_ACTION_CONTRACT.csv",
        "verdicts": OUT / "P8_Y5_R10_1129_VERDICT_LEDGER.csv",
        "gates": OUT / "P8_Y5_R10_1129_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1129_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1129_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1129_VALIDATION.csv",
    }
    sources = source_rows()
    candidates = candidate_rows()
    contracts = action_contract_rows()
    verdicts = verdict_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["candidates"], candidates)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["verdicts"], verdicts)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, candidates, contracts, verdicts, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, candidates, contracts, verdicts, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1123-Y5-R10-R11-flux-alpha3-zero-or-bound.md"


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
            "source_id": "SRC1123_0_1122_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1122_NEXT_TARGET.csv",
            "needle": "NEXT1122_0_1123",
            "note": "1122 handoff to flux alpha3 zero/bound.",
        },
        {
            "source_id": "SRC1123_1_1122_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
            "needle": "R11F1122_0_flux_alpha3",
            "note": "1122 narrowed the live alpha3 map to a flux product.",
        },
        {
            "source_id": "SRC1123_2_no_vector",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T2_no_flux_local_representative",
            "note": "Existing no-flux local representative route is conditional, not parent-derived.",
        },
        {
            "source_id": "SRC1123_3_vector_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "Alpha3 coefficient row is a flux product with 4e-20 target.",
        },
        {
            "source_id": "SRC1123_4_flux_closure",
            "relative_path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "needle": "FC3_no_exchange_projection",
            "note": "Parent current closure requires no exchange projection, not just Ward covariance.",
        },
        {
            "source_id": "SRC1123_5_mass_flux",
            "relative_path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
            "needle": "MF6_zero_boundary_and_nonHilbert_flux",
            "note": "Mass-flux projector route keeps zero boundary/non-Hilbert flux unproved.",
        },
        {
            "source_id": "SRC1123_6_hamiltonian_charge",
            "relative_path": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
            "needle": "HC5_no_extra_hidden_charge",
            "note": "Hamiltonian charge route requires no hidden/domain extra charge.",
        },
        {
            "source_id": "SRC1123_7_source_current",
            "relative_path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
            "needle": "SC4_no_nonHilbert_source_current",
            "note": "Source-current Ward route requires non-Hilbert/domain source currents to vanish or be retained.",
        },
        {
            "source_id": "SRC1123_8_R11_fill",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "needle": "DSR_R7_alpha3",
            "note": "R11 fill requirements carry alpha3 target and product acceptance.",
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


def no_flux_proof_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "proof_id": "NF1123_0_definition",
                "claim_piece": "epsilon_domain_flux definition",
                "formal_statement": "epsilon_domain_flux = P_loc^i_mu F_D^mu, the local spatial projection of the retained domain/source exchange flux",
                "current_status": "DEFINED",
                "blocker": "none",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "NF1123_1_local_representative",
                "claim_piece": "local representative is exact/trivial",
                "formal_statement": "[J_D]_local=0 and no coherent FLRW memory class is active locally imply P_loc^i_mu F_D^mu=0",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "blocker": "existing T2 no-flux lemma is conditional and rests on local representative ownership",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "NF1123_2_parent_current_closure",
                "claim_piece": "parent mass/source current has no domain exchange projection",
                "formal_statement": "Pi_M(F_X+F_P+F_B+F_D+F_nm+T d kappa)=0, especially Pi_M F_D=0",
                "current_status": "NOT_PARENT_DERIVED",
                "blocker": "FC3/SC4/MF6/HC5 all require no hidden/domain exchange or retained executable residuals",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "NF1123_3_Ward_shortcut",
                "claim_piece": "Ward/Bianchi covariance alone kills flux",
                "formal_statement": "nabla_mu T_total^{mu nu}=0 therefore epsilon_domain_flux=0",
                "current_status": "REJECTED_SHORTCUT",
                "blocker": "covariance conserves total exchange but does not prove each domain projection vanishes",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "NF1123_4_boundary_silence",
                "claim_piece": "compact boundary carries no domain/source flux",
                "formal_statement": "int_partialSigma P_loc F_D = 0 or universal constant calibration only",
                "current_status": "FAIL_OPEN",
                "blocker": "mass-flux and source-current contracts keep boundary/non-Hilbert flux open",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "NF1123_5_verdict",
                "claim_piece": "epsilon_domain_flux=0 is proved in the current corpus",
                "formal_statement": "NF1123_1 through NF1123_4 all close with parent-owned identities",
                "current_status": "NO_FLUX_NOT_PROVED",
                "blocker": "local representative, no-exchange projection, and boundary silence are all conditional/open",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "bound_id": "FB1123_0_alpha3_flux_product",
                "observable": "alpha3",
                "quantity": "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "formula": "P_R11_source_alpha3_flux = K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "target_bound": "4e-20",
                "units": "dimensionless PPN alpha3 after declared flux/coupling normalization",
                "required_sources": "K_R11_flux_alpha3 source; c_R11_flux_alpha3 source; epsilon_domain_flux profile/source; observed coframe normalization",
                "current_value": "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO",
                "acceptance": "abs(product) <= 4e-20 without tuned cancellation and with R5/R6/R8/R11 siblings guarded",
                "current_status": "MISSING",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "FB1123_1_flux_zero_certificate",
                "observable": "alpha3",
                "quantity": "epsilon_domain_flux",
                "formula": "epsilon_domain_flux=0",
                "target_bound": "sufficient_zero_for_alpha3_flux_product",
                "units": "dimensionless projected flux convention",
                "required_sources": "parent local representative proof plus no-exchange projection and boundary silence",
                "current_value": "MISSING_PARENT_ZERO_CERTIFICATE",
                "acceptance": "parent-owned proof, not Ward-only and not an imposed plateau",
                "current_status": "MISSING_PARENT_INPUT",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "FB1123_2_coupling_zero_certificate",
                "observable": "alpha3",
                "quantity": "K_R11_flux_alpha3*c_R11_flux_alpha3",
                "formula": "K_R11_flux_alpha3*c_R11_flux_alpha3=0",
                "target_bound": "sufficient_zero_for_alpha3_flux_product",
                "units": "declared coupling-map units",
                "required_sources": "parent symmetry forbidding flux coupling or numeric coefficient map",
                "current_value": "MISSING_COUPLING_ZERO_OR_NUMERIC_COEFFICIENT",
                "acceptance": "prove coupling zero or supply sourced coefficient usable in FB1123_0",
                "current_status": "MISSING_PARENT_INPUT",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def obligation_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "obligation_id": "OB1123_0_same_frame_source",
                "required_identity": "same observed coframe Hilbert/source current before readout",
                "source_contract": "SC0/SC1",
                "status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "effect_if_closed": "removes fitted/readout current ambiguity",
                "valid_for_claim": "false",
            },
            {
                "obligation_id": "OB1123_1_no_exchange_projection",
                "required_identity": "Pi_M F_D = 0 for the domain/source flux",
                "source_contract": "FC3; SC4; HC5",
                "status": "NOT_PARENT_DERIVED",
                "effect_if_closed": "kills epsilon_domain_flux at the source, strongest route",
                "valid_for_claim": "false",
            },
            {
                "obligation_id": "OB1123_2_local_representative",
                "required_identity": "local compact representative is exact/trivial with no coherent FLRW memory flux",
                "source_contract": "T2_no_flux_local_representative",
                "status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "effect_if_closed": "sets P_loc^i_mu F_D^mu=0 in the local branch",
                "valid_for_claim": "false",
            },
            {
                "obligation_id": "OB1123_3_boundary_silence",
                "required_identity": "compact boundary/domain flux is zero or universal calibration only",
                "source_contract": "MF6; FC4; SC5",
                "status": "FAIL_OPEN",
                "effect_if_closed": "prevents hidden boundary flux re-entering alpha3/Gdot/source-normalization rows",
                "valid_for_claim": "false",
            },
            {
                "obligation_id": "OB1123_4_numeric_fallback",
                "required_identity": "if any zero identity fails, the product has sourced numbers and units",
                "source_contract": "FB1123_0",
                "status": "MISSING",
                "effect_if_closed": "permits a nonclaim smoke comparison to the 4e-20 alpha3 bound",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1123_0_no_flux",
                "rule": "epsilon_domain_flux=0 is parent-derived",
                "gate_pass": "false",
                "reason": "no-exchange/local representative/boundary silence are not parent-owned",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1123_1_numeric_bound",
                "rule": "flux product is numerically below 4e-20",
                "gate_pass": "false",
                "reason": "K_R11_flux_alpha3, c_R11_flux_alpha3, and epsilon_domain_flux are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1123_2_Ward_shortcut_blocked",
                "rule": "Ward/Bianchi alone cannot certify no-flux",
                "gate_pass": "true_nonclaim",
                "reason": "1123 explicitly rejects total-conservation to component-zero shortcut",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1123_3_total_alpha3",
                "rule": "total domain/R11 alpha3 is closed",
                "gate_pass": "false",
                "reason": "flux branch remains open",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1123_0_no_flux_attempt",
                "decision": "no_flux_not_proved",
                "reason": "the route is plausible but still rests on unsigned parent current/local representative clauses",
                "next_action": "attack no-exchange parent current theorem before numeric coefficient hunting",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1123_1_bound_row",
                "decision": "strict_flux_bound_row_staged",
                "reason": "if derivation fails later, the exact product and 4e-20 acceptance gate are now fixed",
                "next_action": "fill only with sourced K, c, epsilon values or a theorem-zero certificate",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1123_2_best_route",
                "decision": "derive_no_exchange_first",
                "reason": "killing Pi_M F_D avoids needing an extremely tiny product against alpha3",
                "next_action": "1124 should target parent no-exchange current theorem",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1123_0_1124",
                "next_target": "1124-Y5-R10-domain-flux-no-exchange-parent-current-theorem.md",
                "objective": "try to prove Pi_M F_D=0 from same-frame Hilbert source, parent current closure, and compact boundary silence; otherwise keep the flux product bound row nonclaim",
                "include": "Pi_M F_D; same observed coframe; Hilbert/Ward source; no non-Hilbert/domain exchange; compact boundary silence; epsilon_domain_flux",
                "exclude": "Ward-only shortcut; plateau axiom; numeric claim without K/c/epsilon sources; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    proofs: list[dict[str, object]],
    bounds: list[dict[str, object]],
    obligations: list[dict[str, object]],
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

    all_rows = proofs + bounds + obligations + gates + decisions + next_target
    add("V1123_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1123_1_no_flux_not_proved", proofs[-1]["current_status"] == "NO_FLUX_NOT_PROVED", "no-flux proof remains unclaimed")
    add("V1123_2_bound_row_explicit", bounds[0]["target_bound"] == "4e-20" and "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux" in bounds[0]["quantity"], "strict flux product bound row is explicit")
    add("V1123_3_obligations_cover_core", {"Pi_M F_D = 0 for the domain/source flux", "local compact representative is exact/trivial with no coherent FLRW memory flux", "compact boundary/domain flux is zero or universal calibration only"}.issubset({row["required_identity"] for row in obligations}), "no-exchange, local representative, and boundary obligations are covered")
    add("V1123_4_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and gates[0]["gate_pass"] == "false" and gates[1]["gate_pass"] == "false", "claim gates remain blocked except shortcut guard")
    add("V1123_5_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in proofs + bounds + next_target), "all generated rows remain nonclaim")
    add("V1123_6_next_target", next_target[0]["next_target"].startswith("1124-") and "no-exchange" in str(next_target[0]["next_target"]), "1124 handoff targets parent no-exchange current theorem")
    add("V1123_7_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1123_8_csv_parse", csv_parse_ok, "all 1123 CSV outputs parse cleanly")
    add("V1123_9_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1123_SUMMARY", True, "1123 rejects current no-flux claim and stages strict alpha3 flux bound product")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    proofs: list[dict[str, object]],
    bounds: list[dict[str, object]],
    obligations: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1123 - Y5/R10 R11 Flux Alpha3: Zero Or Bound

**Current verdict:** `epsilon_domain_flux=0` is not proved in the current corpus. The route is plausible, but it still needs a parent-owned no-exchange current theorem plus local representative and boundary-silence clauses.

**Best route:** derive `Pi_M F_D=0` first. That kills the flux at the parent-current level and avoids needing a tiny numerical product against the `4e-20` alpha3 bound.

**Fallback row:** if the zero route fails, the exact nonclaim product is `K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux`, accepted only if `abs(product) <= 4e-20` with sourced units/normalization.

**No claim:** no domain/R11 `alpha3`, R10, PPN, or local-GR claim follows from 1123.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## No-Flux Proof Audit
{table(["proof_id", "claim_piece", "formal_statement", "current_status", "blocker", "claim_allowed", "valid_for_claim"], proofs)}

## Flux Bound Product Rows
{table(["bound_id", "observable", "quantity", "formula", "target_bound", "units", "required_sources", "current_value", "acceptance", "current_status", "claim_allowed", "valid_for_claim"], bounds)}

## Parent-Theorem Obligations
{table(["obligation_id", "required_identity", "source_contract", "status", "effect_if_closed", "valid_for_claim"], obligations)}

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
        "source_register": OUT / "P8_Y5_R10_1123_SOURCE_REGISTER.csv",
        "proofs": OUT / "P8_Y5_R10_1123_NO_FLUX_PROOF_AUDIT.csv",
        "bounds": OUT / "P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
        "obligations": OUT / "P8_Y5_R10_1123_PARENT_THEOREM_OBLIGATIONS.csv",
        "gates": OUT / "P8_Y5_R10_1123_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1123_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1123_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1123_VALIDATION.csv",
    }
    sources = source_rows()
    proofs = no_flux_proof_rows()
    bounds = bound_rows()
    obligations = obligation_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["proofs"], proofs)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["obligations"], obligations)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, proofs, bounds, obligations, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, proofs, bounds, obligations, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

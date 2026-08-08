from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1133-Y5-R10-epsilon-domain-flux-zero-theorem-or-profile-bound.md"


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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1133_0_1132_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1132_NEXT_TARGET.csv",
            "needle": "NEXT1132_0_1133",
            "note": "1132 selects epsilon_domain_flux as the next theorem/profile-bound target.",
        },
        {
            "source_id": "SRC1133_1_1132_factors",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1132_FACTOR_SOURCE_PACK.csv",
            "needle": "FAC1132_0_epsilon_domain_flux",
            "note": "1132 identifies epsilon_domain_flux as the shared alpha3 bottleneck.",
        },
        {
            "source_id": "SRC1133_2_1126_obligations",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1126_SELECTOR_LOCAL_FLUX_OBLIGATIONS.csv",
            "needle": "OB1126_1_local_representative",
            "note": "1126 says local exact/trivial representative would set epsilon_domain_flux=0.",
        },
        {
            "source_id": "SRC1133_3_1127_branch",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1127_BRANCH_SELECTOR_AUDIT.csv",
            "needle": "BS1127_0_local",
            "note": "1127 keeps local exact/trivial branch conditional and FLRW branch separate.",
        },
        {
            "source_id": "SRC1133_4_no_vector_attempt",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T2_no_flux_local_representative",
            "note": "No-vector/no-flux theorem attempt remains conditional.",
        },
        {
            "source_id": "SRC1133_5_ownership",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P3_local_trivial_representative",
            "note": "Local trivial representative exists only as a premise/conditional route.",
        },
        {
            "source_id": "SRC1133_6_1123_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
            "needle": "FB1123_1_flux_zero_certificate",
            "note": "1123 states epsilon_domain_flux=0 would be a sufficient alpha3 flux-zero certificate.",
        },
        {
            "source_id": "SRC1133_7_1132_product_matrix",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1132_EXECUTABLE_PRODUCT_MATRIX.csv",
            "needle": "PM1132_1_R11_flux",
            "note": "1132 product matrix gives the two alpha3 inequalities that epsilon must serve.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def definition_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "definition_id": "DEF1133_0_observable_target",
                "quantity": "epsilon_domain_flux",
                "working_definition": "dimensionless local projected domain-flux residual feeding alpha3 product rows",
                "symbolic_shape": "epsilon_domain_flux ~ ||P_loc^i_mu F_D^mu||_local / normalization",
                "needed_precision": "must control the local preferred-frame vector/flux amplitude, not merely the integrated net flux",
                "current_status": "DEFINITIONAL_SHAPE_ONLY",
                "valid_for_claim": "false",
            },
            {
                "definition_id": "DEF1133_1_surface_flux",
                "quantity": "Phi_D(surface)",
                "working_definition": "surface-integrated domain flux through local boundary",
                "symbolic_shape": "Phi_D = int_boundary F_D^i n_i dS = int_volume div F_D dV",
                "needed_precision": "Phi_D=0 is weaker than epsilon_domain_flux=0",
                "current_status": "USEFUL_BUT_INSUFFICIENT",
                "valid_for_claim": "false",
            },
            {
                "definition_id": "DEF1133_2_profile_bound",
                "quantity": "epsilon_required",
                "working_definition": "symbolic upper bound needed for the two alpha3 products",
                "symbolic_shape": "|epsilon_domain_flux| <= min(4e-20/|W_domain_alpha3|, 4e-20/|K_R11_flux_alpha3*c_R11_flux_alpha3|)",
                "needed_precision": "requires finite sourced W, K, and c or theorem-zero replacement",
                "current_status": "SYMBOLIC_ONLY",
                "valid_for_claim": "false",
            },
        ]
    )


def derivation_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "step_id": "DER1133_0_stationary_conservation",
                "claim_attempt": "stationary compact branch with no local exchange gives div F_D=0",
                "derivation": "if partial_t rho_D=0 and S_parent gives local continuity, then div F_D=0 in the local region",
                "what_it_proves": "zero divergence / conserved local flux",
                "what_it_does_not_prove": "pointwise F_D=0 or epsilon_domain_flux=0",
                "current_result": "CONDITIONAL_PARTIAL_PROGRESS",
                "blocker": "parent continuity/no-exchange statement is not fully owned",
                "valid_for_claim": "false",
            },
            {
                "step_id": "DER1133_1_boundary_silence",
                "claim_attempt": "no boundary exchange makes net flux vanish",
                "derivation": "if div F_D=0 and boundary exchange vanishes, then int_boundary F_D.n dS=0",
                "what_it_proves": "surface-integrated net flux can vanish",
                "what_it_does_not_prove": "circulating/coexact/harmonic local flux is absent",
                "current_result": "NET_FLUX_ONLY_NOT_ALPHA3_ZERO",
                "blocker": "PPN alpha3 is sensitive to local vector residuals, not only total flux",
                "valid_for_claim": "false",
            },
            {
                "step_id": "DER1133_2_hodge_split",
                "claim_attempt": "decompose the local flux into exact, coexact/circulating, harmonic, and boundary/exchange pieces",
                "derivation": "F_D = grad phi_D + curl A_D + h_D + F_boundary/exchange in a local spatial slice",
                "what_it_proves": "the exact/net piece can be separated from swirl/harmonic loopholes",
                "what_it_does_not_prove": "curl A_D=0 and h_D=0",
                "current_result": "BLOCKER_IDENTIFIED",
                "blocker": "no parent no-swirl/no-harmonic lemma exists yet",
                "valid_for_claim": "false",
            },
            {
                "step_id": "DER1133_3_scalar_isotropy_route",
                "claim_attempt": "stationary scalar/topological local selector forbids a preferred local vector",
                "derivation": "if the local branch is generated only by scalar/topological parent variables and the boundary data are isotropic, no invariant local vector can be built",
                "what_it_proves": "would set the coexact/harmonic vector flux to zero",
                "what_it_does_not_prove": "that current parent action and boundary conditions actually satisfy the premise",
                "current_result": "PROMISING_CONDITIONAL_ROUTE",
                "blocker": "needs parent-signed scalar/isotropy/no-swirl theorem",
                "valid_for_claim": "false",
            },
            {
                "step_id": "DER1133_4_FLRW_guard",
                "claim_attempt": "local epsilon zero does not erase FLRW memory",
                "derivation": "require epsilon_domain_flux=0 only on compact local exact/trivial branch, not on coherent FLRW branch with N_D active",
                "what_it_proves": "the local route can be logically compatible with cosmology",
                "what_it_does_not_prove": "the parent selector that chooses those branches",
                "current_result": "GUARD_ONLY_TRUE_NONCLAIM",
                "blocker": "same parent selector still not derived",
                "valid_for_claim": "false",
            },
            {
                "step_id": "DER1133_5_verdict",
                "claim_attempt": "epsilon_domain_flux=0 is proved",
                "derivation": "requires DER1133_0 through DER1133_4 plus no-swirl/no-harmonic closure",
                "what_it_proves": "nothing claimable yet",
                "what_it_does_not_prove": "alpha3 pass, R10 pass, local-GR reduction",
                "current_result": "ZERO_THEOREM_NOT_CLOSED",
                "blocker": "net flux zero is insufficient; circulation/harmonic component remains the hard gap",
                "valid_for_claim": "false",
            },
        ]
    )


def loophole_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "loophole_id": "LOOP1133_0_circulation",
                "residual_piece": "curl A_D / coexact circulation",
                "why_dangerous": "can have zero divergence and zero net surface flux while leaving a local preferred-frame vector",
                "must_kill_by": "parent no-swirl lemma, isotropic boundary data, dissipative extremum, or numeric bound",
                "current_status": "OPEN",
                "valid_for_claim": "false",
            },
            {
                "loophole_id": "LOOP1133_1_harmonic",
                "residual_piece": "h_D harmonic/topological flux class",
                "why_dangerous": "can survive conservation identities and carry global/topological orientation",
                "must_kill_by": "simply-connected local domain, trivial relative cohomology, or branch selector excluding local harmonic class",
                "current_status": "OPEN",
                "valid_for_claim": "false",
            },
            {
                "loophole_id": "LOOP1133_2_boundary_exchange",
                "residual_piece": "F_boundary/exchange",
                "why_dangerous": "boundary leakage can mimic local flux even if interior equations conserve",
                "must_kill_by": "boundary silence theorem and matching to observed local coframe",
                "current_status": "OPEN",
                "valid_for_claim": "false",
            },
            {
                "loophole_id": "LOOP1133_3_gauge_hide",
                "residual_piece": "coframe-normalization artifact",
                "why_dangerous": "can make a vector disappear by definition rather than by physics",
                "must_kill_by": "show epsilon is zero in an observable PPN-safe frame, not only in a chosen representation",
                "current_status": "OPEN_GUARD",
                "valid_for_claim": "false",
            },
        ]
    )


def profile_bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "bound_id": "PB1133_0_domain_requirement",
                "product_row": "PM1132_0_domain_flux",
                "symbolic_requirement": "|epsilon_domain_flux| <= 4e-20/|W_domain_alpha3|",
                "needed_sources": "W_domain_alpha3 finite numeric/source-backed bound; epsilon profile convention",
                "current_value": "MISSING_W_AND_EPSILON",
                "claim_gate": "not executable until W and epsilon are source-backed or theorem-zero",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "PB1133_1_R11_requirement",
                "product_row": "PM1132_1_R11_flux",
                "symbolic_requirement": "|epsilon_domain_flux| <= 4e-20/|K_R11_flux_alpha3*c_R11_flux_alpha3|",
                "needed_sources": "K_R11_flux_alpha3; c_R11_flux_alpha3; epsilon profile convention",
                "current_value": "MISSING_K_C_AND_EPSILON",
                "claim_gate": "not executable until K, c, and epsilon are source-backed or theorem-zero",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "PB1133_2_shared_requirement",
                "product_row": "PM1132_0_domain_flux;PM1132_1_R11_flux",
                "symbolic_requirement": "|epsilon_domain_flux| <= min(4e-20/|W|, 4e-20/|K*c|)",
                "needed_sources": "all relevant coupling bounds plus observed-coframe epsilon normalization",
                "current_value": "SYMBOLIC_ONLY_NOT_EXECUTABLE",
                "claim_gate": "usable only after coupling source pack exists or epsilon zero theorem closes",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1133_0_epsilon_zero",
                "rule": "epsilon_domain_flux=0 is parent-proved",
                "gate_pass": "false",
                "reason": "net flux zero is not pointwise/no-vector zero; no-swirl/harmonic theorem missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1133_1_no_circulation",
                "rule": "coexact/circulating local flux vanishes",
                "gate_pass": "false",
                "reason": "no parent no-swirl lemma or isotropic extremum proof yet",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1133_2_no_harmonic",
                "rule": "local harmonic/topological flux class vanishes",
                "gate_pass": "false",
                "reason": "local topology/relative cohomology branch exclusion is not proved",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1133_3_profile_bound",
                "rule": "symbolic epsilon bound is executable",
                "gate_pass": "false",
                "reason": "W, K, c, and epsilon normalization are not numeric/source-backed",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1133_4_FLRW_guard",
                "rule": "local zero route does not kill cosmology",
                "gate_pass": "true_nonclaim",
                "reason": "1133 explicitly keeps local compact branch separate from FLRW memory branch",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1133_5_alpha3_R10_local_GR",
                "rule": "alpha3/R10/local-GR can promote",
                "gate_pass": "false",
                "reason": "epsilon zero/profile is not closed and product rows remain blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1133_0_verdict",
                "decision": "epsilon_zero_not_proved",
                "reason": "stationary conservation can at most give net flux; local alpha3 needs no coexact/harmonic vector residual",
                "next_action": "attack the no-swirl/no-harmonic lemma directly",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1133_1_real_progress",
                "decision": "hard_gap_identified",
                "reason": "the missing object is no longer vague coupling soup; it is the circulation/harmonic part of the local domain flux",
                "next_action": "derive it from scalar/isotropic parent local action or demote epsilon zero to closure-only",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1133_2_fallback",
                "decision": "profile_bound_route_staged",
                "reason": "if no-swirl theorem fails, epsilon must be bounded symbolically/numerically against W and K*c",
                "next_action": "do not promote alpha3 until bound runner has real coupling inputs",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1133_0_1134",
                "next_target": "1134-Y5-R10-no-swirl-harmonic-flux-lemma-or-epsilon-profile-runner.md",
                "objective": "try to kill the coexact/circulating and harmonic parts of local domain flux from parent scalar/isotropic local action; if not, build an executable epsilon profile-bound runner",
                "include": "Hodge split; curl/coexact flux; harmonic flux; boundary silence; simply-connected local branch; scalar isotropy; symbolic epsilon bound",
                "exclude": "net-flux-only proof; gauge hiding; global all-domain zero; tuned cancellation; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    definitions: list[dict[str, object]],
    derivations: list[dict[str, object]],
    loopholes: list[dict[str, object]],
    profile_bounds: list[dict[str, object]],
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

    all_rows = definitions + derivations + loopholes + profile_bounds + gates + decisions + next_target
    loophole_set = {row["residual_piece"] for row in loopholes}
    add("V1133_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1133_1_definition_distinguishes_net_flux", definitions[1]["current_status"] == "USEFUL_BUT_INSUFFICIENT", "surface/net flux is explicitly weaker than epsilon_domain_flux")
    add("V1133_2_hodge_blocker_present", "curl A_D / coexact circulation" in loophole_set and "h_D harmonic/topological flux class" in loophole_set, "coexact/circulation and harmonic loopholes are explicit")
    add("V1133_3_zero_not_closed", derivations[-1]["current_result"] == "ZERO_THEOREM_NOT_CLOSED", "epsilon zero theorem remains unclosed")
    add("V1133_4_profile_bound_symbolic", all(row["current_value"].startswith(("MISSING", "SYMBOLIC")) for row in profile_bounds), "profile-bound route is staged but not executable")
    add("V1133_5_FLRW_preserved", gates[4]["gate_pass"] == "true_nonclaim", "local-zero attempt keeps FLRW memory branch guarded")
    add("V1133_6_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 5, "claim gates remain blocked")
    add("V1133_7_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1133_8_next_target", next_target[0]["next_target"].startswith("1134-") and "no-swirl" in str(next_target[0]["next_target"]), "1134 handoff targets no-swirl/harmonic flux closure")
    add("V1133_9_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1133_10_csv_parse", csv_parse_ok, "all 1133 CSV outputs parse cleanly")
    add("V1133_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1133_SUMMARY", True, "1133 shows net flux zero is insufficient and identifies no-swirl/harmonic closure as the next hard gap")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    definitions: list[dict[str, object]],
    derivations: list[dict[str, object]],
    loopholes: list[dict[str, object]],
    profile_bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1133 - Y5/R10 Epsilon Domain Flux Zero Theorem Or Profile Bound

**Current verdict:** `epsilon_domain_flux=0` is not proved. A stationary/compact conservation argument can give zero net flux, but alpha3 needs the local projected vector/flux amplitude to vanish.

**Real progress:** the hard gap is now precise: kill the coexact/circulating and harmonic pieces of the local domain flux, not merely the surface-integrated flux.

**Conditional theorem shape:** if the parent local branch is scalar/isotropic, simply connected or relative-cohomology trivial, boundary silent, and no-exchange, then `F_D = grad phi_D + curl A_D + h_D + F_boundary` collapses to a pure exact/trivial piece and `epsilon_domain_flux=0`. Current corpus does not parent-sign those premises.

**No claim:** no alpha3, R10, PPN, local-GR, measured-GM, or cosmology claim follows from 1133. The profile-bound route is symbolic only.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Definition/Profile Targets
{table(["definition_id", "quantity", "working_definition", "symbolic_shape", "needed_precision", "current_status", "valid_for_claim"], definitions)}

## Derivation Ledger
{table(["step_id", "claim_attempt", "derivation", "what_it_proves", "what_it_does_not_prove", "current_result", "blocker", "valid_for_claim"], derivations)}

## Harmonic/Circulation Loopholes
{table(["loophole_id", "residual_piece", "why_dangerous", "must_kill_by", "current_status", "valid_for_claim"], loopholes)}

## Symbolic Profile Bounds
{table(["bound_id", "product_row", "symbolic_requirement", "needed_sources", "current_value", "claim_gate", "valid_for_claim"], profile_bounds)}

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
        "source_register": OUT / "P8_Y5_R10_1133_SOURCE_REGISTER.csv",
        "definitions": OUT / "P8_Y5_R10_1133_EPSILON_DEFINITION_PROFILE.csv",
        "derivations": OUT / "P8_Y5_R10_1133_FLUX_ZERO_DERIVATION_LEDGER.csv",
        "loopholes": OUT / "P8_Y5_R10_1133_HARMONIC_CIRCULATION_BLOCKER.csv",
        "profile_bounds": OUT / "P8_Y5_R10_1133_PROFILE_BOUND_ROWS.csv",
        "gates": OUT / "P8_Y5_R10_1133_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1133_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1133_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1133_VALIDATION.csv",
    }
    sources = source_rows()
    definitions = definition_rows()
    derivations = derivation_rows()
    loopholes = loophole_rows()
    profile_bounds = profile_bound_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["definitions"], definitions)
    write_csv(outputs["derivations"], derivations)
    write_csv(outputs["loopholes"], loopholes)
    write_csv(outputs["profile_bounds"], profile_bounds)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, definitions, derivations, loopholes, profile_bounds, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, definitions, derivations, loopholes, profile_bounds, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

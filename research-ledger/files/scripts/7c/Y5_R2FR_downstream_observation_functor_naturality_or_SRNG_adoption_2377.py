from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_DOWNSTREAM_OBSERVATION_FUNCTOR_OR_SRNG_ADOPTION_2377"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2377-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2377_2376_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2376_NEXT_TARGET.csv", "NEXT2376_0_selected", "2376 selected downstream observation functor route"),
        ("SRC2377_2376_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2376_VALIDATION.csv", "VAL2376_OVERALL", "2376 validation"),
        ("SRC2377_2376_certificate", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2376_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv", "SRNG2376_6_verdict", "2376 SRNG certificate"),
        ("SRC2377_2336_naturality", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2336_DOWNSTREAM_NATURALITY_DERIVATION_AUDIT.csv", "DNF2336_7_verdict", "2336 downstream naturality audit"),
        ("SRC2377_2336_contract", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2336_OBSERVATION_FUNCTOR_CONTRACT.csv", "OFC2336_5_status", "2336 observation functor contract"),
        ("SRC2377_2336_adoption", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2336_SRNG_ADOPTION_DECISION_MATRIX.csv", "ADM2336_3_decision", "2336 adoption decision"),
        ("SRC2377_2336_p4", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2336_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv", "P4A2336_4_reduced_total", "2336 P4 status after private SRNG"),
        ("SRC2377_2336_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2336_NEXT_TARGET.csv", "NEXT2336_0", "2336 boundary/projective next target"),
        ("SRC2377_2336_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2336_VALIDATION.csv", "VAL2336_OVERALL", "2336 validation"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def downstream_naturality_audit() -> list[dict[str, object]]:
    rows = [
        (
            "DNF2377_0_target",
            "derive SRNG from downstream observation functor naturality",
            "If observations are natural functors O_i: Sol(Q_obs)->Readout_i evaluated after the variational problem, then O_i cannot add Gamma_ind to S_parent.",
            "TARGET_SHARPENED",
            "turns readout silence from a clause into functorial bookkeeping",
            "must prove readouts are not hidden action/source terms",
        ),
        (
            "DNF2377_1_quotient_domain",
            "observed quotient domain",
            "q: Phi_parent -> Q_obs is fixed before readout, and e_obs/g_obs/omega_LC[e_obs] are functors of Q_obs.",
            "CONDITIONAL_FROM_PRIOR_CONTRACTS",
            "readouts can depend on observed fields without depending on representative/Gamma slots",
            "q and full observed coframe descent remain not parent-signed in active corpus",
        ),
        (
            "DNF2377_2_downstream_separation",
            "action/readout separation",
            "S_parent is varied over dynamical fields first; O_clock, O_light, O_orbit and detector readouts are maps on solutions, not extra action terms.",
            "EXACT_IF_PARENT_OBSERVATION_POLICY_SIGNED",
            "delta O_i/delta Gamma_ind is irrelevant to hypermomentum because O_i is not in S_parent",
            "instrument backreaction and marker/domain selection must be included as ordinary matter or residuals",
        ),
        (
            "DNF2377_3_naturality",
            "naturality under vertical/gauge maps",
            "For v in ker(Dq), O_i(q(Phi)) is invariant: delta_v O_i = D O_i[Dq(v)] = 0.",
            "EXACT_CONDITIONAL_CHAIN_RULE",
            "kills fake readout-frame dependence without fitting",
            "actual MTS vertical directions and no-shadow-frame clauses are still conditional",
        ),
        (
            "DNF2377_4_source_selector",
            "source/worldtube selector",
            "W_source=closure(supp J_H[tau]) is legal only when selected from the same Hilbert/coframe matter current before readout.",
            "CONDITIONAL_NOT_CLOSED",
            "prevents measured GM/source support from becoming a post-readout mask",
            "compactness, M_H_ref, tau/frame lock, boundary/reference and coupling descent are unsigned",
        ),
        (
            "DNF2377_5_orbit_readout",
            "test-body and orbit readout",
            "A trajectory readout is admissible only as a downstream limit of the same matter action; an independent autoparallel Gamma_ind law is a new coupling.",
            "EXACT_CONDITIONAL_FILTER",
            "blocks importing GR geodesics by words while keeping a derivable route",
            "finite-body marker/domain and test-body limit not yet written as parent data",
        ),
        (
            "DNF2377_6_boundary_projective_limit",
            "boundary and projective limitation",
            "Downstream functor naturality does not itself kill boundary/improvement flux or projective trace coupling.",
            "LIMIT_EXPLICIT",
            "stops SRNG from eating a separate residual channel",
            "Delta_boundary and Delta_projective require their own zero proof or P4 policy",
        ),
        (
            "DNF2377_7_verdict",
            "derive SRNG now",
            "DNF2377_1 through DNF2377_5 would derive SRNG for source/readout sectors if parent-signed together.",
            "PARTIAL_DERIVATION_NOT_CORPUS_CLOSED",
            "SRNG is grounded in a precise downstream-functor theorem shape",
            "current corpus has contracts and conditional lemmas, not full parent observation policy",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "derivation_piece": piece,
            "formal_statement": statement,
            "status": status,
            "proof_gain": gain,
            "obstruction": obstruction,
        }
        for row_id, piece, statement, status, gain, obstruction in rows
    ]


def observation_functor_contract() -> list[dict[str, object]]:
    rows = [
        ("OFC2377_0_domain", "observation functor domain", "Readouts are maps O_i: Sol(Q_obs, boundary data, theta)->Reported_i.", "readouts depend on solved observed fields, not hidden parent representatives", "CONTRACT_WRITTEN_NONCLAIM"),
        ("OFC2377_1_action_separation", "no readout in parent variation", "O_i is not an argument of S_parent and contributes no Euler-Lagrange or hypermomentum current.", "clock/light/orbit readout cannot create Delta_i unless promoted to apparatus matter or residual", "CONTRACT_WRITTEN_NONCLAIM"),
        ("OFC2377_2_vertical_invariance", "vertical invariance", "If Dq(v)=0, then delta_v O_i=0 for all ordinary readouts.", "readout frame dependence is forbidden unless it descends through Q_obs or is residualized", "EXACT_IF_Q_NATURALITY_SIGNED"),
        ("OFC2377_3_no_gamma_slot", "no independent Gamma in readout", "O_i may use g_obs/e_obs and omega_LC[e_obs], but not Gamma_ind as an independent probe variable.", "turns SRNG into a consequence of observation object language", "CONTRACT_WRITTEN_NONCLAIM"),
        ("OFC2377_4_apparatus_backreaction", "apparatus backreaction rule", "If an instrument changes the source, it is included in ordinary matter/source action before variation; if not, it remains downstream.", "prevents sneaking source-current physics into a measurement map", "CONTRACT_WRITTEN_NONCLAIM"),
        ("OFC2377_5_status", "contract status", "OFC2377 is suitable as a private working parent-observation clause, not as a public derivation.", "supports disciplined local-branch development while retaining proof debt", "PRIVATE_CONTRACT_READY_NOT_DERIVED"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "contract_piece": piece,
            "clause": clause,
            "effect": effect,
            "status": status,
        }
        for row_id, piece, clause, effect, status in rows
    ]


def adoption_decision_matrix() -> list[dict[str, object]]:
    rows = [
        (
            "ADM2377_0_derivation_route",
            "derive SRNG from q-natural downstream observation",
            "BEST_ROUTE_BUT_NOT_CLOSED",
            "requires parent-signed q, observation policy, same-frame/tau/source selector and no-shadow clauses",
            "future theorem target only",
        ),
        (
            "ADM2377_1_private_adoption",
            "adopt SRNG/OFC as private working parent-action/observation clause",
            "RECOMMENDED_PRIVATE_WORKING_CLAUSE",
            "it is minimal, non-fitted, and blocks Gamma/readout leakage without altering data by hand",
            "internal local-branch calculations with explicit nonclaim label",
        ),
        (
            "ADM2377_2_reject_or_unresolved",
            "do not adopt SRNG",
            "FALLBACK_TO_P4_COMPONENT_BOUNDS",
            "then Delta_source/clock/light/orbit must be bounded with units and projection maps",
            "P4 residual row fill only",
        ),
        (
            "ADM2377_3_decision",
            "dual track",
            "PRIVATE_ADOPTION_PLUS_DERIVATION_AUDIT",
            "use SRNG internally as a named clause while continuing to derive it; never count it as public GR/Newton proof",
            "next checkpoint may use SRNG-gated branch and separately attack boundary/projective residuals",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "option": option,
            "status": status,
            "reason": reason,
            "allowed_use": allowed,
        }
        for row_id, option, status, reason, allowed in rows
    ]


def p4_status_after_srng_adoption() -> list[dict[str, object]]:
    rows = [
        ("P4A2377_0_SRNG_effect", "Delta_source+Delta_clock+Delta_light+Delta_orbit", "THEOREM_ZERO_INSIDE_PRIVATE_BRANCH_ONLY", "REQUIRES_P4_BOUNDS", "false_inside_private_branch_true_publicly"),
        ("P4A2377_1_spin", "Delta_spin", "UNCHANGED", "UNCHANGED", "true"),
        ("P4A2377_2_boundary", "Delta_boundary", "STILL_REQUIRES_BOUNDARY_CERTIFICATE", "STILL_REQUIRES_BOUNDARY_CERTIFICATE", "true"),
        ("P4A2377_3_projective", "Delta_projective", "STILL_REQUIRES_PROJECTIVE_POLICY", "STILL_REQUIRES_PROJECTIVE_POLICY", "true"),
        ("P4A2377_4_reduced_total", "Delta_abs_private_SRNG_branch", "Delta_abs -> Delta_matter/private + Delta_spin + Delta_boundary + Delta_projective", "full Delta_abs component queue retained", "true"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "component": component,
            "status_if_private_SRNG_used": private_status,
            "status_if_SRNG_rejected": rejected_status,
            "still_live": still_live,
        }
        for row_id, component, private_status, rejected_status, still_live in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2377_0_naturality_derived", "downstream observation naturality derived from parent MTS", "FAIL", "conditional theorem only"),
        ("CG2377_1_SRNG_public", "SRNG is public active theorem", "FAIL", "private working clause only"),
        ("CG2377_2_source_readout_zero_public", "Delta_source/clock/light/orbit zero for public claim", "FAIL", "zero only inside private adopted branch"),
        ("CG2377_3_boundary_projective_closed", "boundary/projective residuals closed", "FAIL", "still live"),
        ("CG2377_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "connection subgate improved but not complete"),
        ("CG2377_5_github", "safe public evidence update", "FAIL", "no GitHub evidence update"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "gate_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2377_0_private_as_public", "private SRNG adoption proves local GR publicly", "false", "private adoption is a named working clause, not a derivation from parent MTS"),
        ("REF2377_1_readout_backreaction_ignored", "all measurement apparatus is downstream by definition", "false", "apparatus that changes the source must be included as matter/source before variation or residualized"),
        ("REF2377_2_boundary_eaten_by_SRNG", "SRNG removes boundary and projective terms", "false", "downstream observation naturality does not kill integration-boundary or projective trace channels"),
        ("REF2377_3_import_orbits", "orbit equations can be imported from GR geodesics", "false", "orbit readout must come from the Hilbert/coframe test-body limit or remain a P4 residual"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, allowed, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2377_0_selected",
            "2378-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md",
            "scripts/Y5_R2FR_boundary_projective_residual_split_under_private_SRNG_2378.py",
            "with SRNG available as a private working clause, split remaining connection residuals into spin, boundary/improvement and projective trace",
            "retain each as explicit P4 residual unless zero/projected-silent/gauge policy closes",
        ),
        (
            "NEXT2377_1_parallel",
            "2378b-Y5-R2FR-parent-observation-policy-derivation.md",
            "scripts/Y5_R2FR_parent_observation_policy_derivation_2378b.py",
            "try to parent-sign q-natural downstream observation instead of private adoption",
            "if not closed, keep SRNG/OFC private-only",
        ),
        (
            "NEXT2377_2_fallback",
            "2378c-Y5-R2FR-P4-source-readout-component-bounds-if-SRNG-rejected.md",
            "scripts/Y5_R2FR_P4_source_readout_component_bounds_if_SRNG_rejected_2378c.py",
            "fill Delta_source/clock/light/orbit units and bounds if SRNG is rejected",
            "keep nonclaim until sourced and same-frame",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "next_file": file_name,
            "next_script": script_name,
            "success_condition": success,
            "fallback_condition": fallback,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, file_name, script_name, success, fallback in rows
    ]


def all_output_files() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2377_SOURCE_REGISTER.csv",
        "naturality_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2377_DOWNSTREAM_NATURALITY_DERIVATION_AUDIT.csv",
        "observation_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_2377_OBSERVATION_FUNCTOR_CONTRACT.csv",
        "adoption_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_2377_SRNG_ADOPTION_DECISION_MATRIX.csv",
        "p4_status": RESIDUALS / "P8_Y5_PARENT_QLOC_2377_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2377_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2377_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2377_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2377_VALIDATION.csv",
    }


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    sensitive = {
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
        "local_gr_claim",
        "epsilon_zero_active",
        "vector_complete",
    }
    positive_values = {"true", "pass", "passed", "ready", "yes", "1"}
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in sensitive and str(value).strip().lower() in positive_values:
                    return False
    return True


def validation_rows(outputs: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(outputs["source_register"])
    generated_paths = [path for key, path in outputs.items() if key != "validation"]
    parsed_ok = True
    for path in generated_paths:
        try:
            parsed_ok = parsed_ok and bool(read_csv(path))
        except Exception:
            parsed_ok = False

    audit = read_csv(outputs["naturality_audit"])
    contract = read_csv(outputs["observation_contract"])
    adoption = read_csv(outputs["adoption_matrix"])
    p4 = read_csv(outputs["p4_status"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])

    checks = [
        ("VAL2377_00_required_sources_exist", all(row["path_exists"] == "true" for row in source_rows), "all required source paths exist"),
        ("VAL2377_01_required_needles_found", all(row["needle_found"] == "true" for row in source_rows), "all source needles found"),
        ("VAL2377_02_outputs_exist", all(path.exists() for path in generated_paths), "all 2377 output files written"),
        ("VAL2377_03_csv_parse", parsed_ok, "all generated CSV files parse and contain rows"),
        (
            "VAL2377_04_naturality_not_closed",
            any(row["row_id"] == "DNF2377_7_verdict" and row["status"] == "PARTIAL_DERIVATION_NOT_CORPUS_CLOSED" for row in audit),
            "downstream naturality remains conditional",
        ),
        (
            "VAL2377_05_observation_contract_written",
            any(row["row_id"] == "OFC2377_5_status" and row["status"] == "PRIVATE_CONTRACT_READY_NOT_DERIVED" for row in contract),
            "observation functor contract written as private nonclaim",
        ),
        (
            "VAL2377_06_private_adoption_selected",
            any(row["row_id"] == "ADM2377_3_decision" and row["status"] == "PRIVATE_ADOPTION_PLUS_DERIVATION_AUDIT" for row in adoption),
            "private SRNG/OFC adoption selected with derivation audit",
        ),
        (
            "VAL2377_07_boundary_projective_still_live",
            any(row["row_id"] == "P4A2377_2_boundary" and row["still_live"] == "true" for row in p4)
            and any(row["row_id"] == "P4A2377_3_projective" and row["still_live"] == "true" for row in p4),
            "boundary and projective residuals remain live",
        ),
        (
            "VAL2377_08_local_claims_block",
            any(row["row_id"] == "CG2377_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
            "local GR/Newton claim gate remains false",
        ),
        (
            "VAL2377_09_next_boundary_projective",
            any(row["row_id"] == "NEXT2377_0_selected" for row in next_rows),
            "boundary/projective residual split selected next",
        ),
        (
            "VAL2377_10_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2377_11_formalization_untouched",
            not any(FORMALIZATION_WORKBENCH in path.parents for path in generated_paths),
            "generator writes only under post-checkpoint-work",
        ),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2377_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2377 valid: downstream observation naturality remains conditional, SRNG/OFC private adoption selected, boundary/projective residuals remain live"
            if overall_ok
            else "2377 validation failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    audit = read_csv(outputs["naturality_audit"])
    contract = read_csv(outputs["observation_contract"])
    adoption = read_csv(outputs["adoption_matrix"])
    p4 = read_csv(outputs["p4_status"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    generated = [rel(path) for path in outputs.values()]

    text = f"""# 2377 - Downstream Observation Functor Naturality Or SRNG Adoption

## Result

The downstream observation route is now cleanly framed:

`O_i: Sol(Q_obs) -> Readout_i`

If clocks, light, orbits and detector readouts are natural functors of solved observed fields, evaluated after variation, they cannot add an independent `Gamma_ind` source to `S_parent`.

That is an excellent theorem shape, but it is not parent-signed in the active corpus.  So the disciplined move is dual-track:

1. use `SRNG/OFC` as a private working observation clause, and
2. keep trying to derive it from q-natural downstream observation.

Inside the private SRNG branch, `Delta_source+Delta_clock+Delta_light+Delta_orbit` are switched off by contract only.  Publicly, they remain proof debt.  Boundary/improvement and projective trace remain live either way.

## Downstream Naturality Derivation Audit

{md_table(audit, ["row_id", "derivation_piece", "status", "obstruction"])}

## Observation Functor Contract

{md_table(contract, ["row_id", "contract_piece", "status", "effect"])}

## SRNG Adoption Decision Matrix

{md_table(adoption, ["row_id", "option", "status", "allowed_use"])}

## P4 Residual Status After SRNG Adoption

{md_table(p4, ["row_id", "component", "status_if_private_SRNG_used", "still_live"])}

## Claim Gates

{md_table(gates, ["row_id", "gate", "gate_status", "claim_effect"])}

## Next Target

{md_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition"])}

## Generated Files

"""
    text += "\n".join(f"- `{path}`" for path in generated)
    text += """

## Practical Status

This is a useful branch-control result.  We can now calculate inside a private SRNG/OFC branch without pretending it is public proof.  The live public residuals are sharper: spin, boundary/improvement, and projective trace, with boundary/projective selected next.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["naturality_audit"], downstream_naturality_audit())
    write_csv(outputs["observation_contract"], observation_functor_contract())
    write_csv(outputs["adoption_matrix"], adoption_decision_matrix())
    write_csv(outputs["p4_status"], p4_status_after_srng_adoption())
    write_csv(outputs["claim_gates"], claim_gates())
    write_csv(outputs["refusal_runner"], refusal_runner())
    write_csv(outputs["next_target"], next_target())
    write_csv(outputs["validation"], validation_rows(outputs))
    write_doc(outputs)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()

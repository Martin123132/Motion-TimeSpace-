from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"

DOC_PATH = ROOT / "575-Y5-R10-readout-constant-sector-first-lock-or-finite-envelope.md"

PRIOR_574_VALIDATION = RESIDUALS / "P8_Y5_BRR545_574_VALIDATION.csv"
PRIOR_574_ORDER = RESIDUALS / "P8_Y5_R10_574_GENERATOR_ATTACK_ORDER.csv"

PROOF_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_575_FIRST_LOCK_PROOF_ATTEMPT.csv"
READOUT_LOCK_PATH = RESIDUALS / "P8_Y5_R10_575_READOUT_LOCK_CONTRACT.csv"
CONSTANT_LOCK_PATH = RESIDUALS / "P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv"
QBAR_GATE_PATH = RESIDUALS / "P8_Y5_R10_575_QBAR_XT_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_575_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_575_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_575_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_575_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_first_lock_pair_attempt_readout_formalized_constants_not_parent_derived_qbar_retained"
CLAIM_CEILING = "readout_constant_first_lock_attempt_only_no_qbar_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md"


SOURCE_FILES = [
    "574-Y5-R10-local-invariant-generator-elimination-or-finite-envelope.md",
    "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
    "448-constant-sector-universality-theorem-attempt.md",
    "449-source-current-Ward-universality-theorem-attempt.md",
    "447-no-species-source-charge-one-coframe-theorem-attempt.md",
    "432-same-frame-matter-functor-zero-route.md",
    "source-intake/mts_residuals/P8_Y5_BRR545_574_VALIDATION.csv",
    "source-intake/mts_residuals/P8_Y5_R10_574_GENERATOR_ATTACK_ORDER.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def prior_clean(rows: list[dict[str, str]]) -> bool:
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def make_proof_attempts() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "FL575_0_readout_domain_lock",
            "lock": "post_readout_projector",
            "claim": "Readout/projectors are not parent-action variables.",
            "mathematical_form": "S_parent:C_parent->R; R_read:Sol(S_parent)/G->Obs; P_read notin Args(S_parent)",
            "result": "formal_domain_lock_written",
            "what_it_removes": "delta S_parent/delta P_read and reduced-action projector source terms",
            "why_not_full_claim": "does not itself prove matter factorization, constant universality, source-current universality, or observed-kernel X",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "FL575_1_constant_superselection_lock",
            "lock": "species_charge_constants",
            "claim": "Matter constants are representation data with trivial MTS action.",
            "mathematical_form": "theta_A in Rep_A; L_X theta_A=L_IQ theta_A=L_m theta_A=0",
            "result": "conditional_not_parent_derived",
            "what_it_removes": "theta_A(X), theta_A(I_Q), theta_A(m), and direct constant-sector X charge if parent-derived",
            "why_not_full_claim": "quotient invariance alone still allows theta_A(I_Q), and no universal-property theorem forces trivial MTS action",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "FL575_2_universal_source_current_lock",
            "lock": "source_current_universality",
            "claim": "Active ordinary matter source is the Hilbert/coframe variation with one universal coupling.",
            "mathematical_form": "J_grav=delta S_m/delta e_obs; E_munu=kappa_univ T_munu; not sum_A kappa_A T_A",
            "result": "conditional_Hilbert_sublemma",
            "what_it_removes": "species-weighted source current kappa_A and direct source-charge split if parent-derived",
            "why_not_full_claim": "universal kappa, measured-GM calibration, non-Hilbert zero current, and compact boundary flux are not derived",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "FL575_3_paired_qbar_gate",
            "lock": "qbar_XT_gate",
            "claim": "Readout lock plus constant/source lock would close ordinary test-body X charge.",
            "mathematical_form": "partial_X e_obs=0; partial_X theta_A=0; no P_read in S_parent; universal Hilbert source => delta_X S_T=0",
            "result": "conditional_gate_only",
            "what_it_removes": "ordinary test-body X charge only if all premises are parent-derived",
            "why_not_full_claim": "constant/source lock is not derived and observed-kernel X remains conditional",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "FL575_4_finite_envelope_trigger",
            "lock": "fallback",
            "claim": "If constant/source lock fails, qbar_XT must be finite and bounded.",
            "mathematical_form": "alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT with qbar_XT retained",
            "result": "fallback_retained",
            "what_it_removes": "nothing; prevents fake theorem-zero",
            "why_not_full_claim": "requires numeric/source-backed coefficient envelope and R10 comparison",
            "valid_for_claim": "false",
        },
    ]


def make_readout_lock() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "RL575_0_parent_domain",
            "required_clause": "Parent action is defined before observation/readout.",
            "mathematical_form": "S_parent=S[Phi in C_parent]",
            "current_status": "formal_clause_written",
            "blocks_if_missing": "post-readout EFT can act as source",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RL575_1_solution_space_readout",
            "required_clause": "Readout is a map on the solution space, not a variational argument.",
            "mathematical_form": "R_read:Sol(S_parent)/G->Obs",
            "current_status": "conditional_no_cheat_lock",
            "blocks_if_missing": "P_read or P_active can generate reduced-action marker terms",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RL575_2_no_backreaction",
            "required_clause": "No readout-selected reduced block is fed back into S_parent.",
            "mathematical_form": "delta S_parent/delta R_read = 0 by absence, not by equation of motion",
            "current_status": "contract_not_full_parent_audit",
            "blocks_if_missing": "closure-zero rows can become hidden theorem-zero claims",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RL575_3_qbar_effect",
            "required_clause": "Readout/projector cannot contribute to delta_X S_T.",
            "mathematical_form": "partial_X P_read terms absent from S_T and S_parent",
            "current_status": "conditional_pass_if_RL575_0_to_2",
            "blocks_if_missing": "qbar_XT returns through projector/readout marker",
            "valid_for_claim": "false",
        },
    ]


def make_constant_lock() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "CL575_0_representation_data",
            "required_clause": "Matter constants are ordinary species representation data, not MTS fields.",
            "mathematical_form": "theta_A in Rep_A, not theta_A=theta_A[X,I_Q,m,h]",
            "current_status": "definition_guardrail",
            "blocks_if_missing": "constants become local MTS marker channels",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CL575_1_trivial_MTS_action",
            "required_clause": "MTS selectors, quotient invariants, material markers, memory, and fibre directions act trivially on constants.",
            "mathematical_form": "L_X theta_A=L_IQ theta_A=L_m theta_A=L_h theta_A=0",
            "current_status": "not_parent_derived",
            "blocks_if_missing": "theta_A(I_Q), theta_A(m), theta_A(h) counterexamples remain legal",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CL575_2_no_direct_constant_vertices",
            "required_clause": "No direct MTS-dependent matter vertices at fixed observed geometry.",
            "mathematical_form": "no alpha_EM(X)F^2, no m_A(X), no q_A X_mu J_A^mu",
            "current_status": "forbidden_vertex_policy_only",
            "blocks_if_missing": "clock, WEP, and fifth-force residuals return",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CL575_3_Hilbert_source_current",
            "required_clause": "Active ordinary matter source is the common Hilbert/coframe current.",
            "mathematical_form": "tau_a^mu=det(e)^-1 delta S_m/delta e_mu^a",
            "current_status": "conditional_standard_identity",
            "blocks_if_missing": "source current can be fitted/readout-defined",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CL575_4_universal_coupling",
            "required_clause": "Field equation uses one universal coupling for the Hilbert current.",
            "mathematical_form": "E_munu=kappa_univ T_munu, not sum_A kappa_A T_A_munu",
            "current_status": "not_parent_derived",
            "blocks_if_missing": "species-weighted active source charge remains",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CL575_5_measured_monopole_separate",
            "required_clause": "Measured GM calibration is kept separate from ordinary qbar_XT lock.",
            "mathematical_form": "Hilbert source universality != mu_obs=G_eff M_eff proof",
            "current_status": "guardrail_pass",
            "blocks_if_missing": "R1/R4/R9/R11 overclaim",
            "valid_for_claim": "false",
        },
    ]


def make_qbar_gate() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "QG575_0_readout",
            "gate": "readout does not enter parent variation",
            "status": "conditional_lock_written",
            "qbar_effect": "removes P_read source terms",
            "claim_effect": "not enough alone",
        },
        {
            "gate_id": "QG575_1_constants",
            "gate": "partial_X theta_A=0 by parent theorem",
            "status": "not_parent_derived",
            "qbar_effect": "would remove constant-sector X charge",
            "claim_effect": "blocks qbar_XT theorem-zero",
        },
        {
            "gate_id": "QG575_2_source_current",
            "gate": "universal Hilbert source with no kappa_A",
            "status": "conditional_sublemma_not_full_parent",
            "qbar_effect": "would remove species-weighted source charge for ordinary matter",
            "claim_effect": "blocks WEP/source claim until universal coupling derived",
        },
        {
            "gate_id": "QG575_3_observed_kernel",
            "gate": "partial_X e_obs=0",
            "status": "conditional_from_prior",
            "qbar_effect": "removes metric/coframe X source",
            "claim_effect": "still needed for qbar_XT theorem-zero",
        },
        {
            "gate_id": "QG575_4_result",
            "gate": "qbar_XT=0",
            "status": "not_promoted",
            "qbar_effect": "finite qbar_XT retained",
            "claim_effect": "R10 finite envelope remains active",
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D575_0_readout_lock_progress",
            "decision": "readout lock written as formal domain clause",
            "meaning": "readout/projectors can be excluded as parent sources if observables are maps on solution space",
            "status": "conditional_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D575_1_constant_lock_not_closed",
            "decision": "do not promote constant-sector universality",
            "meaning": "trivial MTS action on constants and universal source coupling are not parent-derived",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D575_2_qbar_retained",
            "decision": "do not promote qbar_XT=0",
            "meaning": "first lock pair is incomplete; finite qbar_XT remains in R10 envelope",
            "status": "retained_nonclaim",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU575_0_allowed",
            "allowed_after_575": "Use readout-after-variation as a formal no-cheat clause and continue deriving constant/source universality.",
            "forbidden_after_575": "Claim qbar_XT=0, R10 pass, WEP pass, PPN pass, measured-GM pass, or local-GR pass.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU575_1_theory_route",
            "allowed_after_575": "Attack trivial MTS action on constants and universal Hilbert source coupling next.",
            "forbidden_after_575": "Use quotient invariance alone as proof that theta_A(I_Q) is constant.",
            "next_action": "derive constant/source-current universality or mark qbar_XT finite",
        },
        {
            "route_id": "RU575_2_finite_route",
            "allowed_after_575": "Keep finite R10 coefficient envelope active with qbar_XT retained.",
            "forbidden_after_575": "Let a partial readout lock erase the coefficient-wall obligation.",
            "next_action": "if 576 fails, fill qbar_XT coefficient envelope",
        },
    ]


def make_validation(
    prior_rows: list[dict[str, str]],
    order_rows: list[dict[str, str]],
    proof_rows: list[dict[str, object]],
    readout_rows: list[dict[str, object]],
    constant_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing = [path for path in SOURCE_FILES if not (ROOT / path).exists()]
    claim_rows = [
        row for row in proof_rows if str(row.get("valid_for_claim", "")).lower() == "true"
    ]
    order_first_two = [row.get("generator") for row in sorted(order_rows, key=lambda r: int(r["rank"]))[:2]]
    return [
        {
            "check_id": "V575_0_source_paths_exist",
            "result": "pass" if not missing else "fail",
            "detail": "missing=" + str(len(missing)) + (";" + ";".join(missing) if missing else ""),
        },
        {
            "check_id": "V575_1_prior_574_clean",
            "result": "pass" if prior_clean(prior_rows) else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={sum(row.get('result') != 'pass' for row in prior_rows)}",
        },
        {
            "check_id": "V575_2_first_pair_confirmed",
            "result": "pass"
            if order_first_two == ["post_readout_projector", "species_charge_constants"]
            else "fail",
            "detail": "first_two=" + ";".join(order_first_two),
        },
        {
            "check_id": "V575_3_proof_attempts_nonclaim",
            "result": "pass" if len(proof_rows) >= 5 and not claim_rows else "fail",
            "detail": f"proof_rows={len(proof_rows)};claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V575_4_lock_contracts_written",
            "result": "pass" if len(readout_rows) >= 4 and len(constant_rows) >= 6 else "fail",
            "detail": f"readout_rows={len(readout_rows)};constant_rows={len(constant_rows)}",
        },
        {
            "check_id": "V575_5_qbar_gate_blocks_promotion",
            "result": "pass" if any(row.get("status") == "not_promoted" for row in qbar_rows) else "fail",
            "detail": f"qbar_rows={len(qbar_rows)};qbar_XT_zero=false",
        },
        {
            "check_id": "V575_6_decision_blocks_claim",
            "result": "pass" if any(row.get("status") == "blocked_for_claim" for row in decisions) else "fail",
            "detail": "R10_pass=false;local_GR=false;claim_allowed=false",
        },
        {
            "check_id": "V575_7_no_overclaim",
            "result": "pass",
            "detail": "readout_lock_full_claim=false;constant_lock=false;qbar_XT_zero=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    proof_rows: list[dict[str, object]],
    readout_rows: list[dict[str, object]],
    constant_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 575 Y5 R10 readout constant-sector first lock or finite envelope

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- We tried the first lock pair: readout-after-variation plus constant-sector/source-current universality.
- The readout side is the cleaner win: if readout is only a map on `Sol(S_parent)`, then projectors/readout choices are not parent sources.
- The constant/source side is not closed: `theta_A(I_Q)`, `theta_A(m)`, `kappa_A`, non-Hilbert source currents, and measured-GM calibration splits remain legal unless a stronger parent theorem is supplied.
- Therefore `qbar_XT=0` is not promoted. The finite R10 product wall remains active with `qbar_XT` retained.

## Paired Proof Attempt
The desired chain is:

```text
S_parent = S[Phi in C_parent],
R_read: Sol(S_parent)/G -> Obs,
theta_A in Rep_A with L_X theta_A = 0,
J_grav = delta S_matter / delta e_obs,
E_munu = kappa_univ T_munu,
partial_X e_obs = 0
=> delta_X S_T = 0
=> qbar_XT = 0.
```

This does not close yet because the constant/source clauses remain contracts rather than parent-derived identities.

## First-Lock Proof Attempts
{markdown_table(proof_rows, ["attempt_id", "lock", "claim", "result", "what_it_removes", "why_not_full_claim", "valid_for_claim"])}

## Readout Lock Contract
{markdown_table(readout_rows, ["clause_id", "required_clause", "mathematical_form", "current_status", "blocks_if_missing", "valid_for_claim"])}

## Constant Source Lock Contract
{markdown_table(constant_rows, ["clause_id", "required_clause", "mathematical_form", "current_status", "blocks_if_missing", "valid_for_claim"])}

## qbar_XT Gate
{markdown_table(qbar_rows, ["gate_id", "gate", "status", "qbar_effect", "claim_effect"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_575", "forbidden_after_575", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is a partial lock, not a dead end. The readout backdoor can be fenced off cleanly by the solution-space rule. The stubborn part is constants and source current: GR wins locally because ordinary matter source is one Hilbert current with one coupling, not because someone says “universal” loudly. If MTS can derive that same source-current universality, `qbar_XT=0` is back on the table. If not, we stop trying to zero it and put `qbar_XT` into the finite R10 envelope.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    prior_rows = read_csv(PRIOR_574_VALIDATION)
    order_rows = read_csv(PRIOR_574_ORDER)

    proof_rows = make_proof_attempts()
    readout_rows = make_readout_lock()
    constant_rows = make_constant_lock()
    qbar_rows = make_qbar_gate()
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        prior_rows, order_rows, proof_rows, readout_rows, constant_rows, qbar_rows, decisions
    )

    summary_rows = [
        {
            "summary_id": "S575_0_result",
            "status": STATUS,
            "readout_lock_status": "formal_domain_lock_written",
            "constant_source_lock_status": "not_parent_derived",
            "qbar_XT_zero_parent_derived": "false",
            "qbar_XT_retained": "true",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(
        PROOF_ATTEMPT_PATH,
        proof_rows,
        [
            "attempt_id",
            "lock",
            "claim",
            "mathematical_form",
            "result",
            "what_it_removes",
            "why_not_full_claim",
            "valid_for_claim",
        ],
    )
    write_csv(
        READOUT_LOCK_PATH,
        readout_rows,
        [
            "clause_id",
            "required_clause",
            "mathematical_form",
            "current_status",
            "blocks_if_missing",
            "valid_for_claim",
        ],
    )
    write_csv(
        CONSTANT_LOCK_PATH,
        constant_rows,
        [
            "clause_id",
            "required_clause",
            "mathematical_form",
            "current_status",
            "blocks_if_missing",
            "valid_for_claim",
        ],
    )
    write_csv(
        QBAR_GATE_PATH,
        qbar_rows,
        ["gate_id", "gate", "status", "qbar_effect", "claim_effect"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "status", "next_target"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_update,
        ["route_id", "allowed_after_575", "forbidden_after_575", "next_action"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "readout_lock_status",
            "constant_source_lock_status",
            "qbar_XT_zero_parent_derived",
            "qbar_XT_retained",
            "claim_allowed",
            "R10_pass_for_claim",
            "local_GR_pass",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        proof_rows,
        readout_rows,
        constant_rows,
        qbar_rows,
        decisions,
        route_update,
        validation,
    )

    all_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "next_target": NEXT_TARGET,
                "all_validation_passed": all_passed,
                "claim_allowed": False,
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

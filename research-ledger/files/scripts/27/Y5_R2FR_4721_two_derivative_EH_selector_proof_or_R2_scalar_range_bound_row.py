from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4721"
CLAIM_ID = "L-563"
MARKER = "PPC4161_TWO_DERIVATIVE_EH_SELECTOR_PROOF_OR_R2_SCALAR_RANGE_BOUND_4721"
PACKET_MARKER = "PPC4161_PACKET_TWO_DERIVATIVE_EH_SELECTOR_PROOF_OR_R2_SCALAR_RANGE_BOUND_4721"
DECISION = "TWO_DERIVATIVE_EH_SELECTOR_PROVED_CONDITIONAL_COVARIANCE_ALONE_REJECTED_R2_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4722-Y5-R2FR-parent-two-derivative-signature-insertion-or-R2-alpha-lambda-runner.md"

DOC_PATH = POST / "4721-Y5-R2FR-two-derivative-EH-selector-proof-or-R2-scalar-range-bound-row.md"
FORMAL_PATH = FORMAL / "737-PPC4161-two-derivative-EH-selector-proof-or-R2-scalar-range-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_SOURCE_REGISTER.csv"
PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_TWO_DERIVATIVE_EH_SELECTOR_PROOF_ROWS.csv"
FAILURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_SELECTOR_FAILURE_MODE_ROWS.csv"
R2_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_R2_SCALAR_RANGE_BOUND_ROW.csv"
PROJECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_R2_GAMMA_BETA_R10_PROJECTION_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4721_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4721_VALIDATION.csv"


SOURCE_SPECS = [
    {
        "source_id": "SRC4721_0",
        "path": "P8_Y5_R2FR_4720_EH_SELECTOR_THEOREM_ROWS.csv",
        "needle": "EHS4720_0_selector_theorem",
        "role": "4720 conditional EH selector theorem to sharpen.",
    },
    {
        "source_id": "SRC4721_1",
        "path": "P8_Y5_R2FR_4720_PARENT_EH_SIGNATURE_CLAUSES.csv",
        "needle": "EHSC4720_2_two_derivative_IR",
        "role": "Two-derivative IR clause whose proof/rejection is the target.",
    },
    {
        "source_id": "SRC4721_2",
        "path": "P8_Y5_R2FR_4720_NONEH_OPERATOR_COEFFICIENT_MATRIX.csv",
        "needle": "NEH4720_0_R2_fR_scalar",
        "role": "R2/f(R) fallback row selected if two-derivative selector is unsigned.",
    },
    {
        "source_id": "SRC4721_3",
        "path": "P8_Y5_R2FR_4720_NONEH_PROJECTION_KERNEL_ROWS.csv",
        "needle": "PROJ4720_4_R10",
        "role": "R10 projection contract for range-dependent scalar fallback.",
    },
    {
        "source_id": "SRC4721_4",
        "path": "P8_Y5_R2FR_4719_PPN_RESIDUAL_VECTOR_ROWS.csv",
        "needle": "PPNV4719_0_gamma",
        "role": "Gamma PPN residual row that R2 scalar feeds.",
    },
    {
        "source_id": "SRC4721_5",
        "path": "P8_Y5_R2FR_4719_PPN_RESIDUAL_VECTOR_ROWS.csv",
        "needle": "PPNV4719_1_beta",
        "role": "Beta PPN residual row that R2 scalar can feed at nonlinear order.",
    },
    {
        "source_id": "SRC4721_6",
        "path": "P8_Y5_R2FR_4719_POISSON_RESIDUAL_BOUND_ROWS.csv",
        "needle": "PB4719_1_fractional_density_region",
        "role": "Poisson residual bound that non-EH scalar source modifies.",
    },
    {
        "source_id": "SRC4721_7",
        "path": "R11_nonEH_operator_vector_executable.csv",
        "needle": "R2_fR_scalar_mode",
        "role": "Existing skeleton row for R2/f(R) scalar coefficient, currently nonclaim.",
    },
    {
        "source_id": "SRC4721_8",
        "path": "P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv",
        "needle": "nonEH_operator_potential",
        "role": "Scorecard rows showing non-EH potential feeds gamma/beta/R10/R11.",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    path.write_text(existing + separator + block.rstrip() + "\n", encoding="utf-8", newline="\n")


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = SOURCE_DIR / spec["path"]
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(path),
                "exists": path.exists(),
                "needle": spec["needle"],
                "needle_found": spec["needle"] in text,
                "role": spec["role"],
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def proof_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "TDEH4721_0_object_language",
            "statement": "Assume the local visible geometry object language contains exactly one observed coframe/metric, a compatible connection that is algebraic or Levi-Civita in the compact spinless branch, the volume form, constants, and fixed boundary/topological data.",
            "proof_step": "This removes second metrics, independent scalar/vector slots, source labels, memory kernels and post-readout objects from the bulk local action before variation.",
            "result": "operator_domain_restricted",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "TDEH4721_1_two_derivative_count",
            "statement": "At two bulk derivatives, the only parity-even scalar density built from the metric/coframe and compatible connection that contributes to second-order metric equations is sqrt(-g)R, plus a zeroth-order Lambda density and fixed boundary/topological terms.",
            "proof_step": "R contains two derivatives of the metric through the connection. R^2, Ricci^2, Weyl^2 and f_extra(R) contain four or more derivatives in the equations or introduce an extra scalar mode; torsion/nonmetricity invariants require independent connection components; scalar/vector/disformal terms require extra fields.",
            "result": "EH_principal_block_forced_if_two_derivative_selector_signed",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "TDEH4721_2_Palatini_to_EH",
            "statement": "The first-order EC/Palatini form collapses to the EH metric equation when the connection equation is algebraic and torsion/nonmetricity vanish or are separately bounded.",
            "proof_step": "Variation with respect to the connection imposes metric compatibility/torsion silence in the compact spinless branch. Substituting the solved connection into the coframe equation gives the EH Einstein tensor plus retained connection residuals if the silence clauses fail.",
            "result": "Palatini_selector_reduces_to_EH_conditionally",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "TDEH4721_3_covariance_alone_rejected",
            "statement": "Diffeomorphism covariance alone does not prove EH.",
            "proof_step": "A covariant action may include R^2, Ricci^2, Weyl^2, scalar-tensor, vector, torsion/nonmetricity, boundary, nonlocal or memory operators. These are legal unless the two-derivative/no-extra-slot selector is parent-signed.",
            "result": "exact_EH_not_derived_from_covariance_alone",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "TDEH4721_4_verdict",
            "statement": "The two-derivative EH selector is proved as a sufficient theorem, but the existing parent action has not yet signed every premise.",
            "proof_step": "Therefore the honest branch is: sign the parent selector, or retain the first fallback R2/f(R) scalar range row with gamma/beta/R10 projection contracts.",
            "result": "conditional_proof_plus_R2_fallback",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def failure_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("FAIL4721_0_R2_fR", "four-derivative curvature scalar allowed", "R2/f(R) scalar finite-range mode", "R2_scalar_row"),
        ("FAIL4721_1_Ricci_Weyl", "quadratic spin-2/tidal curvature operators allowed", "gamma/xi/wave-sector residual", "Ricci_Weyl_matrix_row"),
        ("FAIL4721_2_torsion_Q", "connection has independent propagating torsion/nonmetricity", "preferred-frame/clock/WEP residual", "torsion_nonmetricity_row"),
        ("FAIL4721_3_scalar_vector_slot", "parent admits independent scalar/vector selector", "R10/Gdot/alpha_i/xi residual", "scalar_vector_rows"),
        ("FAIL4721_4_disformal_metric", "matter/source sees second metric or disformal slot", "WEP/gamma/clock residual", "c_D_bdis_row"),
        ("FAIL4721_5_memory_nonlocal", "local collar admits Gamma/memory/nonlocal kernel", "range/local leakage residual", "c_Gamma_row"),
        ("FAIL4721_6_boundary_source", "boundary/corner data creates source-dependent bulk charge", "source normalization/orbital/alpha3 residual", "c_bdy_row"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "failure_id": failure_id,
            "unsigned_clause": clause,
            "surviving_operator": operator,
            "fallback_route": route,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for failure_id, clause, operator, route in rows
    ]


def r2_row(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R2F4721_0_scalaron_contract",
            "operator_family": "R2_fR_scalar_mode",
            "parent_operator": "S_geo=(M_EH^2/2) int sqrt(-g)[R + a_R2 R^2 + ...]",
            "canonical_parameters": "m_R^2=1/(6 a_R2) for the pure metric R+a_R2 R^2 normalization; lambda_R=hbar/(m_R c); alpha_R=1/3 for pure universal f(R), or alpha_R=(1/3) zeta_R^2 if parent source normalization weakens the scalar charge.",
            "weak_field_potential": "Phi(r)=-G_eff M/r [1 + alpha_R exp(-r/lambda_R)]",
            "gamma_projection": "gamma(r)-1=-2 alpha_R exp(-r/lambda_R)/(1+alpha_R exp(-r/lambda_R)) approx -2 alpha_R exp(-r/lambda_R)",
            "beta_projection": "beta-1 requires nonlinear scalar self-interaction/source-normalization row; do not infer beta from the first-order Yukawa row.",
            "R10_projection": "for every lambda_R row: abs(alpha_R_predicted(lambda_R)) <= alpha_bound(lambda_R), using full source-backed bound curve, not anchor-only.",
            "required_inputs": "a_R2 or m_R; alpha_R or zeta_R; units; source path; normalization convention; full alpha_bound(lambda) curve; gamma/beta projection convention",
            "status": "fallback_contract_staged_not_filled",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def projection_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("R2P4721_0_R10_curve", "R10_fifth_force", "lambda_R, alpha_R", "abs(alpha_R)<=alpha_bound(lambda_R)", "full digitized/source-backed curve required; no anchor-only claim"),
        ("R2P4721_1_gamma_slip", "gamma_minus_1", "alpha_R exp(-r/lambda_R) at Solar/local scale", "abs(gamma-1) below gamma bound in same PPN convention", "screening/range/profile must be stated, not assumed"),
        ("R2P4721_2_beta_nonlinear", "beta_minus_1", "nonlinear scalar source coefficient beta_R", "abs(beta-1) below beta bound", "separate second-order source-normalized row required"),
        ("R2P4721_3_Poisson_source", "epsilon_N_density", "E00_R2/(kappa_eff rho c^2)", "fractional source residual below Newton/Poisson tolerance", "density-region normalization and boundary terms required"),
        ("R2P4721_4_orbital_range", "orbital_precession_or_inverse_square", "alpha_R, lambda_R, source radius/profile", "range-dependent acceleration residual below orbital bound", "finite-size/shell profile required"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "projection_id": projection_id,
            "observable": observable,
            "inputs": inputs,
            "pass_contract": contract,
            "blocking_note": note,
            "status": "projection_contract_only",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for projection_id, observable, inputs, contract, note in rows
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("GATE4721_0_parent_selector_signed", "Parent action explicitly signs the object-language and two-derivative IR selector premises.", "PARENT_SELECTOR_UNSIGNED"),
        ("GATE4721_1_covariance_not_enough", "No promotion from covariance alone; every higher-derivative/extra-slot term is excluded or retained.", "COVARIANCE_ONLY_REJECTED"),
        ("GATE4721_2_R2_row_filled", "R2/f(R) fallback row has numeric/theorem-zero m_R, alpha_R, units and source paths.", "R2_NUMERIC_OR_ZERO_MISSING"),
        ("GATE4721_3_R10_curve_available", "R10 alpha(lambda) bound curve is full/source-backed and row-compatible.", "R10_FULL_CURVE_REQUIRED"),
        ("GATE4721_4_gamma_beta_same_convention", "Gamma and beta projections use the same observed-frame/source-normalized PPN convention.", "PPN_CONVENTION_UNFILLED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "requirement": requirement,
            "passed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, requirement, blocker in rows
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4721_0_no_covariance_shortcut",
            "rule": "Do not claim EH from covariance alone.",
            "reason": "Covariant higher-derivative and extra-field operators survive unless the two-derivative/no-extra-slot selector is signed.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4721_1_no_R2_anchor_claim",
            "rule": "Do not claim an R10 pass from a single alpha=1 threshold or anchor-only bound.",
            "reason": "The R2/f(R) scalar is range-dependent and needs alpha(lambda) across the relevant curve.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4721_2_no_beta_from_gamma",
            "rule": "Do not infer beta from the first-order Yukawa/gamma projection.",
            "reason": "Beta is a second-order nonlinear source-normalization row.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4721_0",
            "decision": DECISION,
            "meaning": "The exact EH path is viable only as a signed two-derivative/no-extra-slot parent selector theorem; covariance alone is rejected. The first fallback is now a concrete R2/f(R) scalaron contract with R10/gamma/beta projections.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4721_0",
            "status": "private_nonclaim_EH_selector_proof_plus_R2_contract",
            "summary": "Two-derivative EH selector proved conditionally, covariance-alone proof rejected, R2/f(R) scalar range fallback row staged.",
            "claim_allowed": False,
            "timestamp_utc": ts,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4721_0",
            "next_target": NEXT_TARGET,
            "why": "The next concrete move is either to insert/sign the parent two-derivative signature, or execute the R2 alpha(lambda) fallback row against the existing R10 machinery.",
            "derive_first": "write the parent geometry signature with no R2/f(R), Ricci/Weyl2, torsion, scalar, vector, disformal or memory coefficient targets and test whether current MTS parent clauses can sign it",
            "fallback": "generate an R2 alpha(lambda) runner input with placeholder-invalid rows until m_R, alpha_R, source paths and bound curve are sourced",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def write_docs(
    ts: str,
    sources: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    r2: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    source_lines = "\n".join(
        f"- `{r['source_id']}`: `{r['source_path']}`; exists={r['exists']}; needle_found={r['needle_found']}; role={r['role']}"
        for r in sources
    )
    proof_lines = "\n".join(f"- `{r['proof_id']}`: {r['statement']} Result: `{r['result']}`." for r in proof)
    failure_lines = "\n".join(f"- `{r['failure_id']}`: {r['unsigned_clause']} -> {r['surviving_operator']} -> `{r['fallback_route']}`." for r in failures)
    r2_lines = "\n".join(f"- `{r['row_id']}`: `{r['weak_field_potential']}`; R10: `{r['R10_projection']}`." for r in r2)
    projection_lines = "\n".join(f"- `{r['projection_id']}` / `{r['observable']}`: {r['pass_contract']} Blocker: {r['blocking_note']}." for r in projections)
    gate_lines = "\n".join(f"- `{r['gate_id']}`: passed={r['passed']}; blocker=`{r['blocker']}`." for r in gates)

    write_text(
        DOC_PATH,
        f"""# 4721 - Two-Derivative EH Selector Proof or R2 Scalar Range Bound Row

Generated: `{ts}`

## Purpose

4720 sharpened the local left-hand problem to an EH-selector fork. 4721 tries the proof first and refuses the cheap version:

- covariance alone does not derive EH;
- the strict two-derivative/no-extra-slot IR selector does force EH;
- if that selector is not parent-signed, the first fallback is an `R2/f(R)` scalar finite-range row.

## Proof Result

The conditional proof works:

If the parent local geometry object language has one observed metric/coframe, local covariant parity-even bulk terms, a two-derivative IR selector, algebraic/silent torsion/nonmetricity, and no scalar/vector/disformal/memory/source coefficient targets, the bulk principal operator is EH plus `Lambda`, topological and boundary terms.

The unconditional proof fails:

Diffeomorphism covariance by itself allows `R^2`, `R_mu_nu R^mu_nu`, `C^2`, scalar-tensor terms, vector selectors, torsion/nonmetricity, nonlocal/memory kernels and source-boundary terms.

So the exact route is not dead, but it must be signed as a parent object-language theorem.

## Proof Rows

{proof_lines}

## Failure Modes

{failure_lines}

## R2 / f(R) Scalar Fallback

{r2_lines}

For pure metric `R+a_R2 R^2`, use the scalaron contract:

`m_R^2 = 1/(6 a_R2)`, `lambda_R = hbar/(m_R c)`, and `Phi(r)=-G_eff M/r [1+alpha_R exp(-r/lambda_R)]`.

For the pure universal case `alpha_R=1/3`; for a general parent source normalization, keep `alpha_R=(1/3) zeta_R^2` until `zeta_R` is derived or bounded.

## Projection Contracts

{projection_lines}

## Gates

{gate_lines}

## Source Register

{source_lines}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
""",
    )

    write_text(
        FORMAL_PATH,
        f"""# PPC4161 4721 - Two-Derivative EH Selector Proof / R2 Scalar Range Row

Generated: `{ts}`

## Formal Result

The EH selector is a sufficient parent theorem:

`single geometry + local covariant parity-even 4-form + two-derivative IR order + algebraic/silent connection + no extra scalar/vector/disformal/memory/source target`

implies:

`S_geo,IR = (M_EH^2/2) int sqrt(-g) R - int sqrt(-g) Lambda + S_top + S_boundary`.

Covariance alone is rejected because it admits non-EH covariant operators.

## First Fallback Row

If `R+a_R2 R^2` is retained:

`m_R^2=1/(6a_R2)`, `lambda_R=hbar/(m_R c)`, and

`Phi(r)=-G_eff M/r [1+alpha_R exp(-r/lambda_R)]`.

Pure universal metric `f(R)` has `alpha_R=1/3`; general parent-normalized rows must source `alpha_R`.

## Nonclaim Boundary

No EH/local-GR/R10/PPN claim fires. The parent selector is unsigned and the R2 row is contract-only until theorem-zero or numeric source-backed inputs are supplied.

## Decision

`{DECISION}`

## Next

`{NEXT_TARGET}`
""",
    )


def update_claims(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if CLAIM_ID in {row.get("claim_id", "") for row in rows}:
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4721 proves the two-derivative EH selector as a conditional parent theorem, rejects covariance-alone EH derivation, and stages the R2/f(R) scalar range fallback row.",
        "current_evidence": "Generated source register, proof rows, failure-mode rows, R2 scalar range row, projection rows, gates, firewalls, decision, status, next target and validation.",
        "status": "conditional_EH_selector_proof_R2_fallback_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating covariance alone as an EH proof or treating the R2 scalar fallback as passing R10/PPN without numeric/source-backed curve rows.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "Two-derivative EH selector proof or R2 scalar range bound row",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=fieldnames).writerow(new_row)


def update_resume(ts: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`4721-Y5-R2FR-two-derivative-EH-selector-proof-or-R2-scalar-range-bound-row.md`

## Decision

`{DECISION}`

## What moved forward

- The two-derivative EH selector has been proved as a conditional parent theorem.
- The covariance-alone route has been explicitly rejected.
- The first fallback is no longer vague: `R2/f(R)` maps to a scalaron with `m_R^2=1/(6a_R2)`, `lambda_R=hbar/(m_R c)`, and a Yukawa correction `alpha_R exp(-r/lambda_R)`.
- No local-GR/R10/PPN claim fires until the parent selector is signed or the R2 row gets numeric/theorem-zero inputs.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def validation_rows(
    ts: str,
    sources: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    r2: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4721_sources_exist", all(r["exists"] for r in sources), "all cited local source paths exist"),
        ("VAL4721_needles_found", all(r["needle_found"] for r in sources), "all cited source needles found"),
        ("VAL4721_selector_proof", any(r["proof_id"] == "TDEH4721_1_two_derivative_count" for r in proof), "two-derivative proof row present"),
        ("VAL4721_covariance_rejected", any(r["proof_id"] == "TDEH4721_3_covariance_alone_rejected" for r in proof), "covariance-alone rejection present"),
        ("VAL4721_failure_modes", len(failures) >= 7 and any(r["failure_id"] == "FAIL4721_0_R2_fR" for r in failures), "selector failure modes present"),
        ("VAL4721_R2_row", len(r2) == 1 and "Phi(r)" in r2[0]["weak_field_potential"], "R2/f(R) scalar row present"),
        ("VAL4721_projection_rows", len(projections) >= 5 and any(r["projection_id"] == "R2P4721_0_R10_curve" for r in projections), "R2 projection rows present"),
        ("VAL4721_gates_not_passing", not all(bool(r["passed"]) for r in gates), "promotion gates not all passing"),
        ("VAL4721_no_claim_allowed", all(not bool(r.get("valid_for_claim")) for r in sources + proof + failures + r2 + projections + gates), "no row allows a claim"),
        ("VAL4721_doc_written", DOC_PATH.exists() and DOC_PATH.stat().st_size > 1000, "checkpoint document written"),
        ("VAL4721_formal_written", FORMAL_PATH.exists() and FORMAL_PATH.stat().st_size > 500, "formal packet document written"),
        ("VAL4721_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "passed": passed,
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4721_OVERALL",
            "passed": overall,
            "detail": "4721 artifacts validate as private nonclaim EH selector proof/R2 fallback checkpoint",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()

    sources = source_register(ts)
    proof = proof_rows(ts)
    failures = failure_rows(ts)
    r2 = r2_row(ts)
    projections = projection_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(PROOF_CSV, proof)
    write_csv(FAILURE_CSV, failures)
    write_csv(R2_ROW_CSV, r2)
    write_csv(PROJECTION_CSV, projections)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    write_docs(ts, sources, proof, failures, r2, projections, gates)
    update_claims(ts)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: the two-derivative EH selector is proved conditionally; covariance-alone EH derivation is rejected.
- Fallback staged: `R2/f(R)` scalaron row with `m_R^2=1/(6a_R2)`, `lambda_R=hbar/(m_R c)`, Yukawa `alpha_R exp(-r/lambda_R)` and R10/gamma/beta contracts.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: sharpens the EH selector proof and stages the first concrete non-EH scalar range fallback row.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    update_resume(ts)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    write_csv(VALIDATION_CSV, validation_rows(ts, sources, proof, failures, r2, projections, gates))


if __name__ == "__main__":
    main()

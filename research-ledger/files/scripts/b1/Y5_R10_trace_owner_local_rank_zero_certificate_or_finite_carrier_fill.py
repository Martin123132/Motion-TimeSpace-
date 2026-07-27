from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_901_trace_owner_certificate_failed_parent_unit_and_pairing_missing_finite_carrier_fill_staged_nonclaim"
CLAIM_CEILING = "trace_owner_certificate_and_finite_fill_only_no_parent_Ptr_no_rank_zero_no_trace_zero_no_R10_PPN_WEP_clock_orbital_or_local_GR_claim"
NEXT_TARGET = "902-Y5-R10-finite-trace-carrier-minimum-source-runner-or-Qtr-zero-proof.md"

CERTIFICATE_RULE = (
    "Trace-owner local-rank-zero certificate passes only if Q_trace/Q_* is a parent-owned boundary readout, "
    "K_parent raises ell_tr to v_tr on the full quotient tangent space, P_tr is source-at-zero/readout-only, "
    "q_loc[U] excludes boundary classes on compact local domains, boundary tails vanish, and matter has no trace marker."
)

SOURCE_SPECS = [
    {
        "source_id": "900_doc",
        "path": ROOT / "900-Y5-R10-trace-residual-vector-priority-source-acquisition-or-theorem-zero-reopen.md",
        "needle": "best next move is not data",
        "role": "immediate trace-owner priority handoff",
    },
    {
        "source_id": "900_validation",
        "path": OUT / "P8_Y5_BRR545_900_VALIDATION.csv",
        "needle": "V900_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "900_parent_signature",
        "path": OUT / "P8_Y5_R10_900_PARENT_SIGNATURE_TEST.csv",
        "needle": "PST900_0_Qtrace_Qstar",
        "role": "parent-owner blocker rows",
    },
    {
        "source_id": "900_source_plan",
        "path": OUT / "P8_Y5_R10_900_SOURCE_ACQUISITION_PLAN.csv",
        "needle": "SAP900_0_Ztr",
        "role": "finite-carrier source acquisition rows",
    },
    {
        "source_id": "880_endpoint_action",
        "path": ROOT / "880-Y5-R10-minimal-Qtrace-Qstar-Kparent-action-contract-or-retained-cT-bound.md",
        "needle": "oriented endpoint action",
        "role": "endpoint action and positive endpoint Hessian candidate",
    },
    {
        "source_id": "881_qstar_audit",
        "path": ROOT / "881-Y5-R10-Qstar-Ward-normalization-and-oriented-boundary-signature-or-retained-cT-bound-runner.md",
        "needle": "boundary sign has a plausible parent-geometry route",
        "role": "Qstar Ward normalization blocker",
    },
    {
        "source_id": "885_charge_lattice",
        "path": ROOT / "885-Y5-R10-parent-charge-lattice-or-Htr-P0-zero-pole-source-fill.md",
        "needle": "charge-unit route was attempted",
        "role": "Qstar charge-lattice/Ward-norm failed route",
    },
    {
        "source_id": "886_zero_pole",
        "path": ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md",
        "needle": "Zero-Pole Implication Theorem",
        "role": "rank-zero/no-pole/source-cokernel implication",
    },
    {
        "source_id": "887_readout_clause",
        "path": ROOT / "887-Y5-R10-readout-only-boundary-support-action-clause-or-finite-trace-carrier-source-pack.md",
        "needle": "clean local-GR route",
        "role": "readout-only boundary-support clause and finite source pack",
    },
    {
        "source_id": "896_adoption_gate",
        "path": ROOT / "896-Y5-R10-trace-action-parent-adoption-gate-and-zero-vs-finite-branch-register.md",
        "needle": "coupling ownership",
        "role": "finite branch closure-only and coupling ownership blocker",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "attempted the trace-owner/local-rank-zero certificate and staged the finite-carrier fill branch if the certificate fails",
            "best_partial_result": "endpoint algebra gives a useful positive K_endpoint candidate, and the readout-only clause is exact, but neither supplies parent Q_* plus full K_parent plus local no-tail",
            "hard_blockers": "Q_* parent unit, K_parent quotient pairing, parent-integrated readout-only clause, compact local rank test, no-tail, and matter no-marker remain unsigned",
            "what_is_not_claimed": "parent P_tr, rank-zero, no-pole, Q_tr=0, finite alpha_tr, R10/PPN/WEP/clock/orbital pass, or local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def certificate_test_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "TOC901_0_Qtrace_Qstar_unit",
            "Q_trace/Q_* parent readout unit",
            "Q_trace=(Q_early-Q_today)/Q_* with Q_* a parent Ward/charge-lattice norm before scoring",
            "fail_for_claim",
            "881 and 885 keep Q_* missing after Ward/lattice attempts",
            "ell_tr scale and endpoint normalization remain arbitrary",
        ),
        (
            "TOC901_1_endpoint_orientation",
            "oriented endpoint action block",
            "S_trace=Q_*^2[U(R_early)-U(R_today)] with K_endpoint=diag(6,6)",
            "conditional_partial_pass",
            "880/881 supply a useful orientation contract, but not the physical arrow or full parent pairing",
            "helps K_endpoint but does not define K_parent",
        ),
        (
            "TOC901_2_Kparent_extension",
            "full parent quotient pairing",
            "K_parent extends K_endpoint and has a constrained pseudo-inverse on the gauge/constraint quotient tangent space",
            "fail_for_claim",
            "880/881/885 all keep K_parent/pseudo-inverse missing",
            "v_tr and P_tr cannot be claimed as parent objects",
        ),
        (
            "TOC901_3_readout_only_source_at_zero",
            "P_tr is source-at-zero/readout-only",
            "R_tr:Sol(S_parent)->Q_trace/Q_* is absent from physical local variation; any probe source is set to zero",
            "clause_written_not_integrated",
            "887 writes the exact clause but does not integrate it into the parent spine",
            "readout may still act as a local spurion if promoted prematurely",
        ),
        (
            "TOC901_4_compact_local_rank",
            "rank(P_loc P_tr P_loc^dagger)=0",
            "for all compact lab/solar U, j^k v_tr|_U=0 modulo gauge/exact representatives",
            "not_computable",
            "P_tr/v_tr are not parent-owned and q_loc support/no-tail is unsigned",
            "rank-zero/no-pole theorem cannot fire",
        ),
        (
            "TOC901_5_source_cokernel",
            "J_tr source-cokernel and Q_tr zero",
            "J_tr=P_tr^dagger J_parent has zero projection on physical local trace modes and matter descends through q_loc",
            "fail_for_claim",
            "matter descent/no-marker and P_tr rank-zero are both unsigned",
            "Q_tr/m must remain in the finite branch",
        ),
        (
            "TOC901_6_verdict",
            "trace-owner local-rank-zero certificate",
            CERTIFICATE_RULE,
            "not_signed",
            "first hard failures are Q_* and full K_parent; readout/no-tail also remains unsigned",
            "do not claim trace silence; stage finite carrier fill as nonclaim",
        ),
    ]
    return [
        {
            "certificate_id": certificate_id,
            "required_item": required_item,
            "mathematical_form": mathematical_form,
            "test_result": test_result,
            "evidence": evidence,
            "if_failed": if_failed,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for certificate_id, required_item, mathematical_form, test_result, evidence, if_failed in rows
    ]


def local_rank_zero_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "rank_id": "LRZ901_0_domain",
            "rank_test": "compact local trace rank",
            "mathematical_test": "rank(P_loc P_tr P_loc^dagger)=0 on each lab/solar compact U",
            "requires": "parent-owned P_tr, q_loc[U], support/no-tail class",
            "current_status": "blocked_parent_Ptr_missing",
            "result": "not_evaluable",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "LRZ901_1_boundary_support",
            "rank_test": "boundary/readout support exclusion",
            "mathematical_test": "supp(v_tr) subset boundary/FLRW and j^k v_tr|_U=0 modulo gauge/exact",
            "requires": "RO887_0..RO887_5 integrated into parent spine",
            "current_status": "clause_written_not_integrated",
            "result": "not_signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "LRZ901_2_no_pole_corollary",
            "rank_test": "no local source-coupled trace pole",
            "mathematical_test": "rank-zero implies no local source-coupled Green-function pole in H_tr",
            "requires": "886 premises plus parent trace owner",
            "current_status": "conditional_theorem_valid_but_premises_unsigned",
            "result": "not_promoted",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "LRZ901_3_verdict",
            "rank_test": "local rank-zero certificate",
            "mathematical_test": "LRZ901_0 through LRZ901_2 jointly close",
            "requires": "Q_*, K_parent, P_tr, q_loc, no-tail",
            "current_status": "fail_for_claim",
            "result": "finite_carrier_fill_required_as_nonclaim_fallback",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def finite_carrier_fill_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "FCF901_0_Ptr_Htr",
            "P_tr,H_tr",
            "H_tr=P_tr^dagger Hess(S_parent) P_tr after gauge/constraint reduction",
            "decides finite carrier versus no-pole",
            "MISSING_PARENT_PROJECTOR_HESSIAN",
            "derive parent trace owner or keep closure-only",
        ),
        (
            "FCF901_1_Ztr",
            "Z_tr",
            "principal symbol sigma_2(H_tr)=Z_tr g_obs^{mu nu} k_mu k_nu on trace scalar subspace",
            "R10/orbital alpha denominator and stability sign",
            "MISSING_PARENT_SYMBOL",
            "derive from H_tr only if finite carrier survives",
        ),
        (
            "FCF901_2_lambdatr",
            "lambda_tr",
            "lambda_tr=sqrt(Z_tr/mu_tr^2) or hbar/(m_tr c) from parent mass gap",
            "finite range for R10/orbital tests",
            "MISSING_MASS_GAP_OR_NOPOLE",
            "derive mu_tr^2 or mark absent_by_theorem",
        ),
        (
            "FCF901_3_Qtr_universal",
            "Q_tr_over_m_universal",
            "partial_vtr S_A divided by inertial mass, or J_tr body integral",
            "R10/orbital common-force amplitude",
            "MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "prove source-cokernel zero or derive body-source functional",
        ),
        (
            "FCF901_4_Qtr_species_clock",
            "Delta_AB_Q_tr_over_m,C_tr_clock_i,C_tr_alphaEM",
            "species/clock/EM response to trace direction",
            "WEP/clock/EM local arenas",
            "MISSING_NO_MARKER_OR_COEFFICIENTS",
            "derive no-marker theorem or source coefficients",
        ),
        (
            "FCF901_5_metric_source_response",
            "C_tr_gamma,C_tr_beta,C_tr_source,Gdot_tr",
            "weak-field observed metric and measured-GM/source-normalization response",
            "PPN/Newton/orbital arenas",
            "MISSING_RESPONSE_OPERATOR",
            "derive observed metric map and source-normalization split",
        ),
        (
            "FCF901_6_R10_alpha_row",
            "alpha_tr_AB(lambda_tr)",
            "alpha_tr_AB=(Q_tr^A/m_A)(Q_tr^B/m_B)/(4*pi Z_tr G_obs)",
            "first executable R10 comparator row",
            "MISSING_Z_LAMBDA_Q_INPUTS_AND_BOUND_CURVE",
            "do not compute until FCF901_1..3 and real bound curve are source-backed",
        ),
        (
            "FCF901_7_boundary_tail",
            "B_tr_tail,K_perp_trace",
            "boundary/local projection contamination from exact trace current or transverse leakage",
            "guards PPN/orbital/local-GR contamination",
            "MISSING_BOUNDARY_SUPPORT_CERTIFICATE_OR_BOUND",
            "prove no-tail or bound as explicit residual",
        ),
    ]
    return [
        {
            "fill_id": fill_id,
            "quantity": quantity,
            "definition": definition,
            "needed_for": needed_for,
            "current_value": current_value,
            "next_action": next_action,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for fill_id, quantity, definition, needed_for, current_value, next_action in rows
    ]


def fork_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fork_id": "FD901_0_certificate_pass_branch",
            "condition": "Q_*, K_parent, P_tr, compact local rank-zero, no-tail, and matter no-marker all parent-signed",
            "current_result": "not_entered",
            "decision": "no trace-zero claim",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "FD901_1_current_certificate_result",
            "condition": "current corpus after 901 certificate test",
            "current_result": "certificate_failed_for_claim",
            "decision": "finite carrier fill staged as nonclaim fallback",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "FD901_2_next_route",
            "condition": "make next step concrete",
            "current_result": "selected",
            "decision": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE901_0_parent_Ptr", "P_tr is parent-owned", "Q_* and K_parent remain missing"),
        ("CGATE901_1_rank_zero", "local trace rank is zero", "P_tr/q_loc/no-tail certificate not signed"),
        ("CGATE901_2_no_pole_Qzero", "no local pole and Q_tr=0", "rank-zero and matter descent/source-cokernel premises unsigned"),
        ("CGATE901_3_finite_branch", "finite trace carrier can be tested", "Z_tr/lambda_tr/Q_tr and response rows remain missing"),
        ("CGATE901_4_local_GR", "MTS locally reduces to GR/Newton", "trace branch and broader local-GR source-normalization gates remain open"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "claim_allowed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, claim, blocker in gates
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "build the minimum finite-trace carrier runner/source gate, while preserving a final chance to prove Q_tr source-cokernel zero before any numeric alpha row",
            "include": "P_tr/H_tr status, Z_tr, lambda_tr, Q_tr/m, R10 alpha row schema, PPN/clock/orbital response blockers, zero-proof escape hatch",
            "exclude": "claiming local GR, fitting tiny couplings, using placeholder bound curves as evidence, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_900_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_900_VALIDATION.csv"
    return path.exists() and all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    certificate_rows_: list[dict[str, object]],
    rank_rows_: list[dict[str, object]],
    finite_rows_: list[dict[str, object]],
    fork_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        certificate_rows_,
        rank_rows_,
        finite_rows_,
        fork_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V901_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V901_1_prior_900_clean",
            "result": "pass" if prior_900_clean() else "fail",
            "detail": "P8_Y5_BRR545_900_VALIDATION.csv clean",
        },
        {
            "check_id": "V901_2_certificate_rule_written",
            "result": "pass" if certificate_rows_[0]["certificate_id"] == "TOC901_0_Qtrace_Qstar_unit" else "fail",
            "detail": "trace-owner certificate stack recorded",
        },
        {
            "check_id": "V901_3_certificate_not_signed",
            "result": "pass"
            if any(row["certificate_id"] == "TOC901_6_verdict" and row["test_result"] == "not_signed" for row in certificate_rows_)
            else "fail",
            "detail": "Q_* and K_parent block parent P_tr",
        },
        {
            "check_id": "V901_4_rank_zero_not_claimed",
            "result": "pass"
            if any(row["rank_id"] == "LRZ901_3_verdict" and row["result"] == "finite_carrier_fill_required_as_nonclaim_fallback" for row in rank_rows_)
            else "fail",
            "detail": "local rank-zero certificate fails for claim",
        },
        {
            "check_id": "V901_5_finite_fill_rows_staged_missing",
            "result": "pass"
            if len(finite_rows_) == 8 and all("MISSING" in stringify(row["current_value"]) for row in finite_rows_)
            else "fail",
            "detail": f"finite_fill_rows={len(finite_rows_)} all missing/nonclaim",
        },
        {
            "check_id": "V901_6_fork_selects_next_route",
            "result": "pass" if any(row["decision"] == NEXT_TARGET for row in fork_rows_) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V901_7_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all parent/rank/finite/local claims remain blocked",
        },
        {
            "check_id": "V901_8_all_generated_rows_nonclaim",
            "result": "pass" if generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
        },
        {
            "check_id": "V901_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V901_10_route_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V901_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows_: list[dict[str, object]],
    source_rows_: list[dict[str, object]],
    certificate_rows_: list[dict[str, object]],
    rank_rows_: list[dict[str, object]],
    finite_rows_: list[dict[str, object]],
    fork_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 901 - Y5/R10 Trace Owner Local Rank-Zero Certificate Or Finite Carrier Fill

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the trace-owner/local-rank-zero certificate does not close from the current corpus**. The endpoint action/orientation work is useful because it gives a clean positive endpoint block candidate, but it still does not supply the two things that would make `P_tr` a real parent object: a parent-owned `Q_*` unit and a full `K_parent`/pseudo-inverse on the quotient tangent space. Since `P_tr` is not owned, the local rank-zero/no-pole theorem cannot be promoted. The finite-carrier fill branch is therefore staged explicitly, with every row still missing and nonclaim.

## Exact 901 Finding
This is a sharp fork, not a dead end. The best GR-safe route remains: make `P_tr` a source-at-zero boundary readout with compact-local rank zero, then use 886 to remove the local pole and source-cokernel. But the current corpus fails the certificate at `Q_*`, `K_parent`, and parent integration of the readout/no-tail clause. So the honest next move is to build the minimum finite-trace carrier source runner while keeping the `Q_tr=0` source-cokernel proof as the final escape hatch before any numeric `alpha_tr(lambda)` row is allowed.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Trace Owner Certificate Test
{md_table(certificate_rows_)}

## Local Rank-Zero Certificate
{md_table(rank_rows_)}

## Finite Carrier Fill Rows
{md_table(finite_rows_)}

## Fork Decision
{md_table(fork_rows_)}

## Claim Gate
{md_table(claim_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    certificate_rows_ = certificate_test_rows(generated_utc)
    rank_rows_ = local_rank_zero_rows(generated_utc)
    finite_rows_ = finite_carrier_fill_rows(generated_utc)
    fork_rows_ = fork_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        certificate_rows_,
        rank_rows_,
        finite_rows_,
        fork_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_901_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_901_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_901_TRACE_OWNER_CERTIFICATE_TEST.csv": certificate_rows_,
        "P8_Y5_R10_901_LOCAL_RANK_ZERO_CERTIFICATE.csv": rank_rows_,
        "P8_Y5_R10_901_FINITE_CARRIER_FILL_ROWS.csv": finite_rows_,
        "P8_Y5_R10_901_FORK_DECISION.csv": fork_rows_,
        "P8_Y5_R10_901_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_901_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_901_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "901-Y5-R10-trace-owner-local-rank-zero-certificate-or-finite-carrier-fill.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        certificate_rows_,
        rank_rows_,
        finite_rows_,
        fork_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_901_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

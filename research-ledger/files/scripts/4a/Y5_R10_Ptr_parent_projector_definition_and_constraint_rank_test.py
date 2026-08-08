from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_878_Ptr_projector_formal_construction_written_parent_pairing_missing_rank_test_blocked_nonclaim"
CLAIM_CEILING = "conditional_Ptr_projector_definition_only_no_parent_owned_trace_projector_no_zero_return_no_Htr_or_local_GR_claim"
NEXT_TARGET = "879-Y5-R10-parent-trace-covector-and-pairing-source-or-closure.md"


SOURCES = [
    {
        "source_id": "877_doc",
        "path": ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md",
        "needle": "the parent trace-Hessian route is still alive",
        "role": "immediate P_tr handoff",
    },
    {
        "source_id": "877_validation",
        "path": OUT / "P8_Y5_BRR545_877_VALIDATION.csv",
        "needle": "V877_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "864_split",
        "path": ROOT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needle": "Dq_FLRW[v_T]",
        "role": "trace visible globally and local-vertical split",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "Dq_loc[U][v_T]=0",
        "role": "local restriction/verticality lemma",
    },
    {
        "source_id": "863_trace_current",
        "path": ROOT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needle": "P_loc J_trace",
        "role": "trace current and local projection silence contract",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "post-variation observable",
        "role": "readout-after-variation/no-spurion rule",
    },
    {
        "source_id": "407_action_sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needle": "relational_MTS_state",
        "role": "primitive parent configuration-space sketch",
    },
    {
        "source_id": "382_parent_action",
        "path": ROOT / "382-parent-local-action-minimal-contract.md",
        "needle": "S_parent",
        "role": "local parent-action sector obligations",
    },
    {
        "source_id": "870_nohair",
        "path": ROOT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needle": "P_loc J_trace=0",
        "role": "trace no-hair support/no-tail blocker",
    },
    {
        "source_id": "421_fibre_decoupling",
        "path": ROOT / "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "needle": "mass gap, Hessian sign",
        "role": "rank/gap/source-independence analogy",
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
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_needle(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = Path(source["path"])
        needle = str(source["needle"])
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, needle) else "fail",
                "role": source["role"],
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
            "what_changed": "derived the formal construction a parent trace projector must satisfy and converted P_tr into a covector/pairing/rank problem",
            "best_partial_result": "if ell_tr=DQ_trace and K_parent are owned, then v_tr=K_parent^{-1}ell_tr/<ell_tr,K_parent^{-1}ell_tr> and P_tr=v_tr⊗ell_tr; local zero requires P_loc v_tr=0 or no source-coupled pole",
            "hard_blockers": "parent trace covector ell_tr, parent pairing K_parent, q_FLRW/q_loc compatibility, local support rank, source-cokernel silence",
            "what_is_not_claimed": "P_tr parent ownership, v_tr in ker(Dq_loc), no scalar pole, H_tr, Z_tr/lambda_tr, R10/PPN/WEP/local-GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def projector_construction_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "construction_id": "PC878_0_trace_covector",
            "object": "ell_tr",
            "mathematical_form": "ell_tr := DQ_trace|_Phi, a covector on parent tangent space extracting the FLRW trace endpoint",
            "owned_if": "Q_trace and its charge unit Q_* are parent variables/readouts before local testing",
            "current_status": "missing_parent_covector",
            "if_missing": "no canonical trace direction or projector exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "construction_id": "PC878_1_parent_pairing",
            "object": "K_parent",
            "mathematical_form": "K_parent is the kinetic/Hessian/symplectic pairing used to raise ell_tr into a vector direction",
            "owned_if": "parent action supplies a nondegenerate pairing on the relevant quotient tangent space or a constrained pseudo-inverse",
            "current_status": "missing_parent_pairing",
            "if_missing": "ell_tr cannot be raised to v_tr without arbitrary normalization",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "construction_id": "PC878_2_trace_vector",
            "object": "v_tr",
            "mathematical_form": "v_tr := K_parent^{-1} ell_tr / <ell_tr,K_parent^{-1}ell_tr>, so ell_tr(v_tr)=1",
            "owned_if": "ell_tr and K_parent are parent-owned and normalization is finite/nonzero",
            "current_status": "conditional_formula_only",
            "if_missing": "trace support class cannot be tested in q_loc",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "construction_id": "PC878_3_projector",
            "object": "P_tr",
            "mathematical_form": "P_tr := v_tr ⊗ ell_tr, with P_tr^2=P_tr on the parent quotient tangent space",
            "owned_if": "v_tr and ell_tr are parent-owned and gauge/constraint degeneracies are handled before readout",
            "current_status": "conditional_idempotent_formula",
            "if_missing": "H_tr=P_tr^dagger Hess(S_parent)P_tr is undefined",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "construction_id": "PC878_4_local_verticality",
            "object": "local zero test",
            "mathematical_form": "Dq_loc[U][v_tr]=0 or equivalently P_loc v_tr=0/gauge-exact for compact local U",
            "owned_if": "q_loc is a parent local quotient and v_tr has boundary/FLRW support only",
            "current_status": "not_parent_signed",
            "if_missing": "P_tr may define a local trace carrier rather than a harmless endpoint direction",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def candidate_definition_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "CD878_0_boundary_FLRW_trace",
            "candidate": "P_tr projects onto the boundary/FLRW trace endpoint direction",
            "definition_test": "ell_tr=DQ_trace and v_tr has support only in q_FLRW/boundary endpoint sector",
            "current_status": "best_conditional_route_not_parent_signed",
            "if_true": "local compact domains see no trace carrier and zero-return may close",
            "if_false": "must inspect local scalar/conformal carrier branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "CD878_1_readout_probe_only",
            "candidate": "P_tr is a post-variation observable/source-at-zero probe",
            "definition_test": "P_tr appears only in readout map or generating source evaluated at zero, never as physical spurion in S_parent",
            "current_status": "legal_if_parent_readout_rule_signed",
            "if_true": "no physical local force is introduced by the readout itself",
            "if_false": "P_tr backreacts and becomes a real coupling branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "CD878_2_local_conformal_scalar",
            "candidate": "P_tr projects onto a local metric/coframe trace scalar",
            "definition_test": "j^k(v_tr)|_U != 0 and H_tr has a reduced inverse on compact local domains",
            "current_status": "legal_counterbranch_not_derived",
            "if_true": "finite carrier must be coefficient-filled and bounded",
            "if_false": "return to boundary/readout or gauge-null route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "CD878_3_finite_fibre_trace",
            "candidate": "P_tr projects onto a relabel-invariant finite-fibre trace/class function",
            "definition_test": "trace invariant is universal, source-independent, gapped/nonpropagating, and matter-blind",
            "current_status": "not_decoupled",
            "if_true": "trace can renormalize constants only",
            "if_false": "finite-fibre trace becomes WEP/clock/fifth-force marker",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "CD878_4_rejected_time_singlet",
            "candidate": "P_tr equals old P_T time/history singlet",
            "definition_test": "reuse 321/322 P_T as trace projector",
            "current_status": "rejected_symbol_collision",
            "if_true": "would conflate amplitude cell algebra with trace local-coupling branch",
            "if_false": "notation remains disciplined",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def constraint_rank_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "rank_id": "RT878_0_rank_zero_local",
            "test": "local projection rank of trace direction",
            "mathematical_form": "rank(P_loc P_tr P_loc^dagger)=0 on compact lab/solar-system domains",
            "current_status": "not_proved",
            "if_pass": "no local trace degree enters H_tr; zero-return route advances",
            "if_fail": "rank-one or higher local trace carrier must be bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "RT878_1_no_physical_pole",
            "test": "reduced inverse/pole test",
            "mathematical_form": "H_tr has no source-coupled Green-function pole after gauge/constraint reduction",
            "current_status": "not_tested",
            "if_pass": "lambda_tr is not a physical local range",
            "if_fail": "derive Z_tr and lambda_tr from H_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "RT878_2_source_cokernel",
            "test": "source projection onto physical trace modes",
            "mathematical_form": "<u_tr,J_parent>=0 for every physical homogeneous trace mode u_tr in Coker(H_tr)",
            "current_status": "not_parent_signed",
            "if_pass": "no local trace force even with constrained trace variable",
            "if_fail": "Q_tr^A/m_A must be filled or bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "RT878_3_no_tail",
            "test": "boundary/exact current local tail",
            "mathematical_form": "P_loc dB_trace|_U=0 and no scalar-gradient/B_0i/B_TF/clock marker survives",
            "current_status": "open_from_870_874",
            "if_pass": "boundary trace endpoint remains FLRW-only",
            "if_fail": "c_T finite leakage branch remains active",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "RT878_4_rank_verdict",
            "test": "joint constraint-rank/source/no-tail decision",
            "mathematical_form": "rank_zero_local + no_pole + source_cokernel_zero + no_tail",
            "current_status": "blocked_missing_parent_inputs",
            "if_pass": "P_tr zero-return can be promoted in a later checkpoint",
            "if_fail": "H_tr coefficient-fill path is mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def source_cokernel_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "source_id": "ST878_0_matter_descent",
            "source_projection": "ordinary matter stress/current",
            "zero_condition": "S_matter factors through q_loc and v_tr in ker(Dq_loc), so Q_tr^A=0 by chain rule",
            "current_status": "conditional_not_parent_signed",
            "blocks": "WEP, clock, R10 source/test charges",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "source_id": "ST878_1_boundary_current",
            "source_projection": "J_trace boundary/exact current",
            "zero_condition": "P_loc J_trace=0 and P_loc dB_trace=0 on compact U",
            "current_status": "open_nohair",
            "blocks": "R10/orbital/PPN trace leakage",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "source_id": "ST878_2_source_normalization",
            "source_projection": "measured GM/source current",
            "zero_condition": "any universal constant trace monopole is time/range/species independent and absorbed into measured GM",
            "current_status": "not_parent_derived",
            "blocks": "Newtonian source normalization and orbital residuals",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "source_id": "ST878_3_verdict",
            "source_projection": "all trace source channels",
            "zero_condition": "matter descent + boundary nohair + source normalization all signed",
            "current_status": "not_zero",
            "blocks": "no source-cokernel theorem; coefficient-fill fallback remains active",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC878_0_selected",
            "route": "parent_trace_covector_and_pairing_source_or_closure",
            "status": "selected",
            "reason": "P_tr cannot be parent-defined without ell_tr=DQ_trace and a parent pairing K_parent to raise it",
            "include": "Q_trace covector, Q_* normalization, K_parent/Hessian pairing, quotient tangent split, pseudo-inverse if constrained",
            "exclude": "numeric fitted P_tr, local-GR claim, R10 scoring, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG878_0_no_Ptr_claim",
            "claim": "P_tr is parent-defined",
            "status": "forbidden",
            "reason": "ell_tr and K_parent/pseudo-inverse are still missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG878_1_no_rank_zero_claim",
            "claim": "local rank of P_tr is zero",
            "status": "forbidden",
            "reason": "Dq_loc[v_tr]=0 and no-tail/source-cokernel tests are not parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG878_2_no_Htr_claim",
            "claim": "H_tr is defined and computable",
            "status": "forbidden",
            "reason": "H_tr requires P_tr first, then second variation of S_parent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG878_3_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "this checkpoint only sharpens the c_T trace projector; other residual channels remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG878_4_allowed_private_result",
            "claim": "formal P_tr construction and rank tests are now explicit",
            "status": "allowed_private_nonclaim",
            "reason": "the coupling blocker is reduced to trace covector, parent pairing, and rank/source tests",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D878_0",
            "finding": "formal_Ptr_construction_written",
            "reason": "P_tr can be constructed from ell_tr and K_parent if both are parent-owned",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D878_1",
            "finding": "parent_pairing_missing",
            "reason": "the corpus does not yet supply the covector/pairing data needed to raise DQ_trace into v_tr",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D878_2",
            "finding": "rank_test_blocked",
            "reason": "local rank/no-pole/source-cokernel tests are written but cannot be evaluated without parent P_tr/H_tr",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "find or construct the parent trace covector ell_tr=DQ_trace and parent pairing K_parent/pseudo-inverse needed to define P_tr, or explicitly demote P_tr to closure-only",
            "include": "Q_trace/Q_* ownership, kinetic or symplectic pairing, quotient tangent split, normalization, gauge degeneracy/pseudo-inverse",
            "exclude": "numeric trace coefficients, R10/local-GR claims, public prose, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_877_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_877_VALIDATION.csv"
    if not path.exists():
        return False
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF)


def all_nonclaim(row_sets: Iterable[list[dict[str, object]]]) -> bool:
    for rows in row_sets:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() != "false":
                return False
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    construction_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    rank_rows: list[dict[str, object]],
    source_cokernel_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, str]]:
    generated_sets = [
        source_rows,
        construction_rows,
        candidate_rows,
        rank_rows,
        source_cokernel_rows_,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    construction_text = " ".join(str(row.get("mathematical_form", "")) for row in construction_rows)
    construction_ok = all(token in construction_text for token in ["ell_tr", "K_parent", "v_tr", "P_tr"])
    parent_missing = any(row.get("object") == "K_parent" and row.get("current_status") == "missing_parent_pairing" for row in construction_rows)
    candidates_ok = any(row.get("candidate_id") == "CD878_0_boundary_FLRW_trace" for row in candidate_rows) and any(
        row.get("current_status") == "rejected_symbol_collision" for row in candidate_rows
    )
    rank_blocked = any(row.get("rank_id") == "RT878_4_rank_verdict" and row.get("current_status") == "blocked_missing_parent_inputs" for row in rank_rows)
    source_not_zero = any(row.get("source_id") == "ST878_3_verdict" and row.get("current_status") == "not_zero" for row in source_cokernel_rows_)
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = route_rows_[0]["status"] == "selected" and next_target_rows_[0]["next_target"] == NEXT_TARGET
    fw_count = formalization_changed_count()
    checks = [
        ("V878_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V878_1_prior_877_clean", prior_877_clean(), "P8_Y5_BRR545_877_VALIDATION.csv clean"),
        ("V878_2_formal_construction_contains_projector_data", construction_ok, "ell_tr/K_parent/v_tr/P_tr construction recorded"),
        ("V878_3_parent_pairing_missing", parent_missing, "K_parent/pairing remains missing and blocks promotion"),
        ("V878_4_candidate_definitions_ready", candidates_ok, "boundary/readout/local/fibre/rejected candidates recorded"),
        ("V878_5_rank_test_blocked", rank_blocked, "constraint-rank verdict remains blocked_missing_parent_inputs"),
        ("V878_6_source_cokernel_not_zero", source_not_zero, "source-cokernel theorem not closed"),
        ("V878_7_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V878_8_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V878_9_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V878_10_route_selected", route_selected, NEXT_TARGET),
        ("V878_11_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    construction_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    rank_rows: list[dict[str, object]],
    source_cokernel_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 878 - Y5/R10 P_tr Parent Projector Definition and Constraint-Rank Test",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **`P_tr` is now a precise parent-geometry object, not a loose label**. "
        "A real trace projector requires a parent trace covector `ell_tr=DQ_trace` and a parent pairing or constrained pseudo-inverse `K_parent`. "
        "Only then can one define `v_tr=K_parent^{-1}ell_tr/<ell_tr,K_parent^{-1}ell_tr>` and `P_tr=v_tr⊗ell_tr`. "
        "The local zero route then becomes a rank/source test: `Dq_loc[U][v_tr]=0`, no physical local trace pole, and zero source-cokernel projection. "
        "The current corpus has the conditional shape but not the parent covector/pairing, so no `P_tr`, zero-return, `H_tr`, or local-GR claim is promoted.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Formal Projector Construction",
        md_table(construction_rows),
        "",
        "## Candidate Definitions",
        md_table(candidate_rows),
        "",
        "## Constraint-Rank Test",
        md_table(rank_rows),
        "",
        "## Source-Cokernel Test",
        md_table(source_cokernel_rows_),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guard",
        md_table(guard_rows),
        "",
        "## Decision",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_target_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows = source_register_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)
    construction_rows = projector_construction_rows(generated_utc)
    candidate_rows = candidate_definition_rows(generated_utc)
    rank_rows = constraint_rank_rows(generated_utc)
    source_cokernel_rows_ = source_cokernel_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        construction_rows,
        candidate_rows,
        rank_rows,
        source_cokernel_rows_,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_878_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_878_FORMAL_PROJECTOR_CONSTRUCTION.csv": construction_rows,
        "P8_Y5_R10_878_CANDIDATE_DEFINITIONS.csv": candidate_rows,
        "P8_Y5_R10_878_CONSTRAINT_RANK_TEST.csv": rank_rows,
        "P8_Y5_R10_878_SOURCE_COKERNEL_TEST.csv": source_cokernel_rows_,
        "P8_Y5_R10_878_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_878_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_878_DECISION.csv": decision_rows_,
        "P8_Y5_R10_878_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_878_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_878_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        construction_rows,
        candidate_rows,
        rank_rows,
        source_cokernel_rows_,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_878_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

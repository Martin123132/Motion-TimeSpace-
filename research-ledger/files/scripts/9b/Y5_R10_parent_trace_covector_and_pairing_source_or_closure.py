from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_879_trace_covector_pairing_source_hunt_done_Qstar_Kparent_missing_Ptr_demoted_to_closure_nonclaim"
CLAIM_CEILING = "trace_covector_pairing_hunt_only_Ptr_closure_no_parent_owned_Ptr_Htr_zero_return_R10_PPN_WEP_or_local_GR_claim"
NEXT_TARGET = "880-Y5-R10-minimal-Qtrace-Qstar-Kparent-action-contract-or-retained-cT-bound.md"


SOURCES = [
    {
        "source_id": "878_doc",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "precise parent-geometry object",
        "role": "immediate trace covector/pairing handoff",
    },
    {
        "source_id": "878_validation",
        "path": OUT / "P8_Y5_BRR545_878_VALIDATION.csv",
        "needle": "V878_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "109_boundary_charge",
        "path": ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needle": "derive Q_* and the endpoint charge split",
        "role": "normalized boundary charge/Qstar blocker",
    },
    {
        "source_id": "110_endpoint_equation",
        "path": ROOT / "110-endpoint-charge-equation-attempt.md",
        "needle": "27 R^2 - 12 R + 1 = 0",
        "role": "endpoint equation target and Qstar failure",
    },
    {
        "source_id": "111_variational_owner",
        "path": ROOT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needle": "formal potential",
        "role": "formal endpoint potential and charge metric blocker",
    },
    {
        "source_id": "861_endpoint_bridge",
        "path": ROOT / "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md",
        "needle": "Q_* = parent-normalized Ward charge unit",
        "role": "endpoint charge unit and nohair audit",
    },
    {
        "source_id": "862_trace_lift",
        "path": ROOT / "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md",
        "needle": "DeltaQ_trace/Q_*",
        "role": "trace-lift and endpoint identification audit",
    },
    {
        "source_id": "864_split",
        "path": ROOT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needle": "Q_trace=(Q_early-Q_today)/Q_*",
        "role": "local/global split and Qtrace definition candidate",
    },
    {
        "source_id": "10_symplectic",
        "path": ROOT / "10-observer-map-symplectic-contract.md",
        "needle": "Symplectic Preservation",
        "role": "symplectic pairing is not enough for local GR",
    },
    {
        "source_id": "97_canonical_R",
        "path": ROOT / "97-canonical-R-theorem-attempt.md",
        "needle": "Q_* fixes the unit boundary charge scale",
        "role": "canonical R/Qstar/Ward identity blocker",
    },
    {
        "source_id": "338_readout",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero",
        "role": "readout source versus physical spurion rule",
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
            "what_changed": "audited the corpus for ell_tr=DQ_trace and K_parent/pairing sources and demoted current P_tr usage to closure-only",
            "best_partial_result": "ell_tr can be formally written as D[(Q_early-Q_today)/Q_*], but Q_*, endpoint coordinates, and the parent pairing/charge metric are not derived",
            "hard_blockers": "Q_* unit, endpoint variables as parent coordinates, parent charge/kinetic pairing K_parent, endpoint arrow, local nohair",
            "what_is_not_claimed": "parent-owned ell_tr, K_parent, P_tr, H_tr, trace zero-return, R10 pass, PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def covector_source_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "CV879_0_Qtrace_definition",
            "object": "Q_trace",
            "candidate_source": "864 local/global split, 862 trace-lift endpoint",
            "candidate_formula": "Q_trace or DeltaQ_trace/Q_* = (Q_early-Q_today)/Q_* = 3 q_trace under conditional trace lift",
            "current_status": "named_candidate_not_parent_coordinate",
            "blocks": "ell_tr cannot be a parent covector until Q_trace is a parent variable/readout",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "CV879_1_Qstar_unit",
            "object": "Q_*",
            "candidate_source": "109/110/111/861/862/864/97",
            "candidate_formula": "Q_* = parent-normalized trace Ward/boundary charge unit",
            "current_status": "missing_repeatedly",
            "blocks": "normalization and derivative of Q_trace are arbitrary up to scale",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "CV879_2_endpoint_coordinates",
            "object": "Q_early,Q_today",
            "candidate_source": "110 endpoint equation and 111 formal variational owner",
            "candidate_formula": "stationary roots of R=Q_boundary/Q_* with target 27R^2-12R+1=0",
            "current_status": "formal_target_not_parent_derived",
            "blocks": "D Q_early and D Q_today are not defined as parent tangent covectors",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "CV879_3_elltr_formula",
            "object": "ell_tr",
            "candidate_source": "878 formal projector construction plus endpoint charge definitions",
            "candidate_formula": "ell_tr = DQ_trace = Q_*^{-1}(D Q_early - D Q_today) - Q_trace D ln Q_*",
            "current_status": "formal_formula_only",
            "blocks": "requires Q_* fixed or its derivative known, plus endpoint coordinate ownership",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "CV879_4_covector_verdict",
            "object": "ell_tr ownership",
            "candidate_source": "whole covector audit",
            "candidate_formula": "parent-owned only if Q_trace:Sol(S_parent)->R/Q_* is fixed before scoring",
            "current_status": "not_owned",
            "blocks": "P_tr cannot be parent promoted",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def pairing_source_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "KP879_0_relative_charge_pairing",
            "object": "relative charge metric",
            "candidate_source": "109 boundary charge and 111 relative charge pairing action",
            "candidate_formula": "<J_rel,J_rel>_Q or equivalent charge metric",
            "current_status": "conditional_only_not_derived",
            "blocks": "cannot raise ell_tr to v_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "KP879_1_formal_endpoint_potential",
            "object": "U''(R)",
            "candidate_source": "111 endpoint quadratic variational owner",
            "candidate_formula": "U(R)=9R^3-6R^2+R, U''(R)=54R-12",
            "current_status": "formal_not_parent_metric",
            "blocks": "curvature changes sign at roots and does not define a global positive K_parent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "KP879_2_symplectic_observer_map",
            "object": "local symplectic/phase pairing",
            "candidate_source": "10 observer-map symplectic contract",
            "candidate_formula": "J_q J_p=1 and radial observer configuration cell constraints",
            "current_status": "not_trace_boundary_pairing",
            "blocks": "generic symplectic preservation does not derive trace endpoint pairing or local GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "KP879_3_Hessian_pairing",
            "object": "Hess(S_parent) or kinetic pairing",
            "candidate_source": "877 H_tr skeleton and 421 finite-fibre decoupling analogy",
            "candidate_formula": "K_parent could be a second variation or pseudo-inverse on the quotient tangent space",
            "current_status": "not_computable",
            "blocks": "no parent action block supplies the trace Hessian/pairing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "KP879_4_pairing_verdict",
            "object": "K_parent ownership",
            "candidate_source": "whole pairing audit",
            "candidate_formula": "K_parent must be a parent charge metric, kinetic Hessian, symplectic inverse, or constrained pseudo-inverse",
            "current_status": "missing",
            "blocks": "v_tr, P_tr, H_tr and rank tests remain blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def formal_derivation_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "derivation_id": "FD879_0_if_Qstar_fixed",
            "assumption": "Q_* is a parent-fixed constant unit",
            "derivation": "Q_trace=(Q_early-Q_today)/Q_* gives ell_tr=Q_*^{-1}(D Q_early-D Q_today)",
            "status": "valid_conditional_formula",
            "claim_gap": "Q_* and endpoint coordinate covectors are not parent-derived",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "FD879_1_if_Qstar_dynamic",
            "assumption": "Q_* may vary with parent state",
            "derivation": "ell_tr=Q_*^{-1}(D Q_early-D Q_today)-Q_trace D ln Q_*",
            "status": "valid_conditional_formula",
            "claim_gap": "D ln Q_* is unknown and may add a local/source marker",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "FD879_2_raise_covector",
            "assumption": "K_parent is nondegenerate or has a parent pseudo-inverse on the quotient tangent space",
            "derivation": "v_tr=K_parent^{-1}ell_tr/<ell_tr,K_parent^{-1}ell_tr>",
            "status": "blocked_missing_Kparent",
            "claim_gap": "normalization cannot be evaluated and may be null/singular",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "FD879_3_projector",
            "assumption": "ell_tr(v_tr)=1 after normalization",
            "derivation": "P_tr=v_tr otimes ell_tr is idempotent because P_tr^2=v_tr ell_tr(v_tr) otimes ell_tr=P_tr",
            "status": "formal_only",
            "claim_gap": "depends on missing ell_tr and K_parent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "FD879_4_local_zero",
            "assumption": "Dq_loc[U][v_tr]=0 and P_loc dB_trace=0",
            "derivation": "local trace charge and local trace Green-function source vanish by quotient chain rule/source-cokernel silence",
            "status": "not_proved",
            "claim_gap": "requires local/global split, nohair, matter descent, and source normalization",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def closure_demotion_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "closure_id": "CL879_0_current_Ptr",
            "object": "P_tr",
            "current_claim_status": "closure_only_nonclaim",
            "reason": "ell_tr and K_parent are not parent-owned, so P_tr cannot be a derived projector in the present corpus",
            "allowed_use": "private theorem target and symbolic gate only",
            "forbidden_use": "R10/local-GR pass, theorem-zero, numeric coefficient source",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CL879_1_Htr",
            "object": "H_tr",
            "current_claim_status": "undefined_for_claim",
            "reason": "H_tr=P_tr^dagger Hess(S_parent)P_tr requires parent-owned P_tr first",
            "allowed_use": "minimal future action contract",
            "forbidden_use": "extract Z_tr/lambda_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CL879_2_zero_return",
            "object": "local trace zero-return",
            "current_claim_status": "not_available",
            "reason": "rank-zero/no-pole/source-cokernel tests cannot be evaluated without P_tr/H_tr",
            "allowed_use": "conditional route if 880 supplies Q_trace/Q_*/K_parent",
            "forbidden_use": "claim c_T=0 or Q_tr^A=0 now",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CL879_3_retained_branch",
            "object": "finite trace residual",
            "current_claim_status": "retained_if_no_future_parent_owner",
            "reason": "if 880 fails, the honest branch is c_T/Z_tr/lambda_tr/J_tr as retained source-normalized inputs",
            "allowed_use": "future bound/source runner with valid_for_claim=false until numeric and sourced",
            "forbidden_use": "hide as derived GR reduction",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC879_0_selected",
            "route": "minimal_Qtrace_Qstar_Kparent_action_contract_or_retained_cT_bound",
            "status": "selected",
            "reason": "the current corpus cannot define P_tr, but the exact missing action objects are Q_trace, Q_*, and K_parent",
            "include": "minimal boundary/trace charge action, Q_* unit, charge metric/pairing, endpoint variables, pseudo-inverse, or retained c_T branch",
            "exclude": "claiming P_tr, fitted trace coefficients, R10/local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG879_0_no_elltr_claim",
            "claim": "ell_tr=DQ_trace is parent-owned",
            "status": "forbidden",
            "reason": "Q_trace/Q_* and endpoint coordinate covectors remain unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG879_1_no_Kparent_claim",
            "claim": "K_parent or charge metric is parent-owned",
            "status": "forbidden",
            "reason": "relative pairing, endpoint potential, symplectic map, and Hessian routes remain conditional/non-computable",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG879_2_no_Ptr_claim",
            "claim": "P_tr is a derived projector",
            "status": "forbidden",
            "reason": "P_tr needs ell_tr and K_parent first; current status is closure_only_nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG879_3_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace channel remains closure/retained and other q_loc channels are still open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG879_4_allowed_private_result",
            "claim": "P_tr has been honestly demoted to closure-only pending parent charge/pairing action",
            "status": "allowed_private_nonclaim",
            "reason": "879 prevents a formal projector from being smuggled in as derived coupling zero",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D879_0",
            "finding": "elltr_formula_only",
            "reason": "ell_tr can be written formally from endpoint charge variables but Q_* and endpoint covectors are not parent-owned",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D879_1",
            "finding": "Kparent_missing",
            "reason": "no source supplies a trace charge metric, kinetic pairing, or constrained pseudo-inverse",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D879_2",
            "finding": "Ptr_demoted_to_closure_only",
            "reason": "without ell_tr and K_parent, P_tr cannot define a parent Hessian or zero-return theorem",
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
            "objective": "attempt one minimal action contract that supplies Q_trace, Q_*, and K_parent; if it fails, route trace leakage to retained c_T/Z_tr/lambda_tr/J_tr bound inputs",
            "include": "boundary charge variables, Q_* normalization, charge pairing/metric, endpoint Euler equation, pseudo-inverse, closure-to-bound decision",
            "exclude": "public claim, fitted trace coefficients, R10/local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_878_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_878_VALIDATION.csv"
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
    covector_rows: list[dict[str, object]],
    pairing_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, str]]:
    generated_sets = [
        source_rows,
        covector_rows,
        pairing_rows,
        derivation_rows,
        closure_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    qstar_missing = any(row.get("object") == "Q_*" and row.get("current_status") == "missing_repeatedly" for row in covector_rows)
    kparent_missing = any(row.get("object") == "K_parent ownership" and row.get("current_status") == "missing" for row in pairing_rows)
    ell_formula_ok = any(row.get("derivation_id") == "FD879_1_if_Qstar_dynamic" and "D ln Q_*" in row.get("derivation", "") for row in derivation_rows)
    ptr_demoted = any(row.get("object") == "P_tr" and row.get("current_claim_status") == "closure_only_nonclaim" for row in closure_rows)
    retained_ready = any(row.get("object") == "finite trace residual" and "retained" in row.get("current_claim_status", "") for row in closure_rows)
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = route_rows_[0]["status"] == "selected" and next_target_rows_[0]["next_target"] == NEXT_TARGET
    fw_count = formalization_changed_count()
    checks = [
        ("V879_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V879_1_prior_878_clean", prior_878_clean(), "P8_Y5_BRR545_878_VALIDATION.csv clean"),
        ("V879_2_Qstar_missing", qstar_missing, "Q_* remains missing across source audit"),
        ("V879_3_Kparent_missing", kparent_missing, "K_parent/pairing remains missing"),
        ("V879_4_elltr_formula_recorded", ell_formula_ok, "ell_tr formula includes dynamic-Qstar case"),
        ("V879_5_Ptr_demoted_to_closure", ptr_demoted, "P_tr current status closure_only_nonclaim"),
        ("V879_6_retained_branch_ready", retained_ready, "finite trace residual branch retained if parent owner fails"),
        ("V879_7_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V879_8_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V879_9_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V879_10_route_selected", route_selected, NEXT_TARGET),
        ("V879_11_validation_rows_ready", True, "validation table constructed"),
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
    covector_rows: list[dict[str, object]],
    pairing_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 879 - Y5/R10 Parent Trace Covector and Pairing Source or Closure",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **`P_tr` is demoted to closure-only in the current corpus**. "
        "The formal covector exists only as a conditional expression: "
        "`ell_tr=D[(Q_early-Q_today)/Q_*]`, which equals "
        "`Q_*^{-1}(D Q_early-D Q_today)-Q_trace D ln Q_*` if `Q_*` is allowed to vary. "
        "But `Q_*`, the endpoint coordinates, and the parent charge/kinetic pairing `K_parent` are not derived. "
        "So `ell_tr`, `v_tr`, `P_tr`, `H_tr`, `Z_tr/lambda_tr`, and trace zero-return cannot be claimed. "
        "The honest next move is one last minimal `Q_trace/Q_*/K_parent` action contract; if that fails, the trace channel becomes a retained `c_T` bound branch.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Covector Source Audit",
        md_table(covector_rows),
        "",
        "## Pairing Source Audit",
        md_table(pairing_rows),
        "",
        "## Formal Derivation",
        md_table(derivation_rows),
        "",
        "## Closure Demotion",
        md_table(closure_rows),
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
    covector_rows = covector_source_audit_rows(generated_utc)
    pairing_rows = pairing_source_audit_rows(generated_utc)
    derivation_rows = formal_derivation_rows(generated_utc)
    closure_rows = closure_demotion_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        covector_rows,
        pairing_rows,
        derivation_rows,
        closure_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_879_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_879_COVECTOR_SOURCE_AUDIT.csv": covector_rows,
        "P8_Y5_R10_879_PAIRING_SOURCE_AUDIT.csv": pairing_rows,
        "P8_Y5_R10_879_FORMAL_DERIVATION.csv": derivation_rows,
        "P8_Y5_R10_879_CLOSURE_DEMOTION.csv": closure_rows,
        "P8_Y5_R10_879_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_879_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_879_DECISION.csv": decision_rows_,
        "P8_Y5_R10_879_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_879_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_879_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "879-Y5-R10-parent-trace-covector-and-pairing-source-or-closure.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        covector_rows,
        pairing_rows,
        derivation_rows,
        closure_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_879_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

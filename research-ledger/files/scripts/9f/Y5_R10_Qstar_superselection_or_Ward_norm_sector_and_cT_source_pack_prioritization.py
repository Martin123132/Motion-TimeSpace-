from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_883_Qstar_superselection_gate_written_endpoint_Ptr_scale_invariant_but_parent_unit_unsigned_nonclaim"
CLAIM_CEILING = "Qstar_superselection_candidate_and_cT_priority_only_no_Qstar_derivation_no_DeltaR_claim_no_Ptr_Htr_or_local_GR_pass"
NEXT_TARGET = "884-Y5-R10-charge-unit-superselection-parent-clause-or-cT-P0-source-acquisition.md"


SOURCES = [
    {
        "source_id": "882_doc",
        "path": ROOT / "882-Y5-R10-relative-chain-boundary-owner-and-Qstar-unit-or-retained-cT-minimum-source-pack.md",
        "needle": "endpoint-only `Q_*` derivation",
        "role": "immediate Qstar obstruction handoff",
    },
    {
        "source_id": "882_validation",
        "path": OUT / "P8_Y5_BRR545_882_VALIDATION.csv",
        "needle": "V882_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "879_doc",
        "path": ROOT / "879-Y5-R10-parent-trace-covector-and-pairing-source-or-closure.md",
        "needle": "ell_tr=D[(Q_early-Q_today)/Q_*]",
        "role": "trace covector/Qstar dependence",
    },
    {
        "source_id": "880_doc",
        "path": ROOT / "880-Y5-R10-minimal-Qtrace-Qstar-Kparent-action-contract-or-retained-cT-bound.md",
        "needle": "K_endpoint=diag(6,6)",
        "role": "oriented endpoint Hessian block",
    },
    {
        "source_id": "878_doc",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "P_tr := v_tr",
        "role": "formal P_tr construction",
    },
    {
        "source_id": "337_exact_readout",
        "path": ROOT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needle": "q_trace = 2/27",
        "role": "conditional exact trace readout",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero",
        "role": "readout/spurion guard",
    },
    {
        "source_id": "863_Ward_trace",
        "path": ROOT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needle": "Q_* = unit(J_trace,parent)",
        "role": "Qstar Ward unit target",
    },
    {
        "source_id": "864_split",
        "path": ROOT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needle": "Qstar Normalization Audit",
        "role": "Qstar normalization audit",
    },
    {
        "source_id": "875_schema",
        "path": OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv",
        "needle": "IN875_0_Z_T",
        "role": "retained cT coefficient schema",
    },
    {
        "source_id": "882_pack",
        "path": OUT / "P8_Y5_R10_882_RETAINED_CT_MINIMUM_SOURCE_PACK.csv",
        "needle": "MCP882_0_Ztr",
        "role": "minimum retained cT source pack",
    },
    {
        "source_id": "97_canonical_R",
        "path": ROOT / "97-canonical-R-theorem-attempt.md",
        "needle": "normalized_boundary_charge_derived",
        "role": "prior Qstar theorem failure",
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
            "what_changed": "tested Q_* as a parent-fixed superselection/unit rather than a dynamical endpoint variable, and derived the endpoint P_tr scale cancellation",
            "best_partial_result": "if Q_* is parent-fixed before variation, the endpoint projector is Q_*-scale invariant: ell=(dQe-dQt)/Q_*, v=(Q_*/2)(partial_Qe-partial_Qt), so P_tr=end=(1/2)(partial_Qe-partial_Qt) tensor (dQe-dQt)",
            "hard_blockers": "parent proof that Q_* is a superselected charge unit, Ward-current norm or charge lattice, physical endpoint arrow, full K_parent extension, local no-hair/source-cokernel, retained c_T numeric inputs",
            "what_is_not_claimed": "Q_* derivation, DeltaR prediction, parent P_tr/H_tr, c_T zero/pass, R10/PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def superselection_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "SS883_0_not_dynamic",
            "requirement": "Q_* is not varied in the endpoint Euler problem",
            "formal_rule": "delta Q_*=0 because Q_* is a parent unit/superselection label, not a field coordinate",
            "if_satisfied": "882 variation obstruction is avoided without adding a fitted counterterm",
            "current_status": "admissible_shape_not_parent_signed",
            "claim_gap": "the corpus has not yet derived the unit/superselection sector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SS883_1_predata_unit",
            "requirement": "Q_* is fixed before empirical scoring",
            "formal_rule": "Q_* cannot be adjusted using SN/BAO/R10/PPN outcomes; only dimensionless ratios R=Q/Q_* are scored",
            "if_satisfied": "no calibration leakage into DeltaR or local residuals",
            "current_status": "rule_written_not_proved",
            "claim_gap": "needs a source path for the unit owner, not just a convention",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SS883_2_charge_rescaling",
            "requirement": "global charge-unit rescaling is gauge/convention or superselection",
            "formal_rule": "(Q_early,Q_today,Q_*) -> (lambda Q_early,lambda Q_today,lambda Q_*) leaves R_i and DeltaR invariant",
            "if_satisfied": "the numerical endpoint ratio is independent of the arbitrary unit scale",
            "current_status": "conditional_invariance",
            "claim_gap": "the action normalization/stiffness still needs a parent owner",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SS883_3_no_local_gradient",
            "requirement": "Q_* has no spacetime gradient or material dependence",
            "formal_rule": "partial_mu Q_*=0 and partial Q_*/partial species=0 in local matter sectors",
            "if_satisfied": "Q_* does not create clock/WEP/PPN hair",
            "current_status": "not_parent_signed",
            "claim_gap": "local no-hair and no-marker theorems remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SS883_4_no_counterterm_laundering",
            "requirement": "do not add W(Q_*) solely to cancel -8Q_*/81",
            "formal_rule": "any Q_* sector must have independent parent origin and source register",
            "if_satisfied": "prevents target-fitted Q_* normalization",
            "current_status": "guard_written",
            "claim_gap": "no W(Q_*) sector accepted in this checkpoint",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SS883_5_verdict",
            "requirement": "Q_* superselection is parent-derived",
            "formal_rule": "SS883_0 through SS883_4 plus a Ward norm/charge lattice proof all close",
            "if_satisfied": "endpoint variation can use fixed Q_* cleanly and re-enter P_tr/H_tr tests",
            "current_status": "not_derived",
            "claim_gap": "superselection is a disciplined candidate, not a theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def endpoint_projector_scale_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "calc_id": "EPS883_0_endpoint_Hessian",
            "assumptions": "oriented endpoint action and fixed Q_*",
            "calculation": "K_endpoint=diag(U''(1/3),-U''(1/9))=diag(6,6) in Q variables",
            "result": "endpoint Hessian block is independent of Q_*",
            "status": "conditional_formula",
            "claim_gap": "endpoint block is not full K_parent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "EPS883_1_covector",
            "assumptions": "Q_trace=(Q_early-Q_today)/Q_* and delta Q_*=0",
            "calculation": "ell_tr=(dQ_early-dQ_today)/Q_*",
            "result": "ell_tr carries inverse unit scale",
            "status": "conditional_formula",
            "claim_gap": "Q_* fixed-unit status is not parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "EPS883_2_norm",
            "assumptions": "K_endpoint^-1=diag(1/6,1/6)",
            "calculation": "<ell,K^-1 ell>=1/(6Q_*^2)+1/(6Q_*^2)=1/(3Q_*^2)",
            "result": "normalization is finite for nonzero Q_*",
            "status": "conditional_formula",
            "claim_gap": "does not prove nonzero Q_* unit",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "EPS883_3_vector",
            "assumptions": "v=K^-1 ell/<ell,K^-1 ell>",
            "calculation": "v=(Q_*/2)(partial_Qearly-partial_Qtoday)",
            "result": "raised trace vector carries the compensating unit scale",
            "status": "conditional_formula",
            "claim_gap": "full parent tangent-space vector still missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "EPS883_4_projector",
            "assumptions": "P_tr=v tensor ell",
            "calculation": "P_tr^end=(1/2)(partial_Qearly-partial_Qtoday) tensor (dQ_early-dQ_today)",
            "result": "Q_* cancels from the endpoint projector",
            "status": "best_partial_result",
            "claim_gap": "scale-invariant endpoint projector is not full parent P_tr or local no-hair",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "EPS883_5_idempotence",
            "assumptions": "ell(v)=1",
            "calculation": "P_tr^2=P_tr on the two-endpoint block",
            "result": "endpoint block is a genuine rank-one projector if the fixed-unit premises hold",
            "status": "conditional_projector",
            "claim_gap": "local Dq_loc[v]=0 and source-cokernel silence remain unproved",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def ward_norm_sector_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "sector_id": "WN883_0_inner_product",
            "candidate_owner": "Ward-current norm",
            "needed_clause": "Q_*^2=<J_trace,J_trace>_parent with a parent-owned measure/Hodge/pairing",
            "current_status": "missing_pairing_measure",
            "why_it_matters": "would make Q_* a fixed unit rather than an endpoint variable",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "sector_id": "WN883_1_charge_lattice",
            "candidate_owner": "trace charge quantum/lattice",
            "needed_clause": "[J_trace] lies in a relative cohomology/charge lattice with generator Q_*",
            "current_status": "not_derived",
            "why_it_matters": "would make Q_* a superselection unit and explain rational normalized charges",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "sector_id": "WN883_2_exact_readout",
            "candidate_owner": "full-cell exact readout unit",
            "needed_clause": "q_trace=2/27 is an exact parent readout, not a Wilsonian reduced-EFT coefficient",
            "current_status": "conditional_from_337_338",
            "why_it_matters": "can explain normalized ratios but still needs the absolute boundary charge unit",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "sector_id": "WN883_3_no_calibration_leak",
            "candidate_owner": "pre-data unit lock",
            "needed_clause": "Q_* source is written before cosmology/local scoring and not fitted from B_mem or bounds",
            "current_status": "policy_gate_only",
            "why_it_matters": "protects the endpoint route from target inversion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "sector_id": "WN883_4_verdict",
            "candidate_owner": "Q_* parent sector",
            "needed_clause": "one of WN883_0..WN883_2 closes with WN883_3",
            "current_status": "not_closed",
            "why_it_matters": "without this, Q_* remains closure/superselection candidate only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def ct_priority_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "priority_id": "CTP883_0_zero_or_pole",
            "priority": 0,
            "quantity": "Z_tr and no-pole/lambda_tr",
            "reason": "without kinetic sign and no-pole/range, no local force law exists to score",
            "source_status": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "next_action_if_derivation_fails": "derive H_tr from parent P_tr or source a retained Z_tr/lambda_tr template",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "priority_id": "CTP883_1_source_projection",
            "priority": 1,
            "quantity": "J_tr and Q_tr/m",
            "reason": "source projection determines whether trace carrier couples to matter at all",
            "source_status": "MISSING_SOURCE_PROJECTION",
            "next_action_if_derivation_fails": "build source-normalized trace charge rows or prove P_loc J_trace=0",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "priority_id": "CTP883_2_metric_response",
            "priority": 2,
            "quantity": "C_T_gamma,C_T_beta,C_T_source",
            "reason": "PPN/Newton comparison needs metric and source-normalization response",
            "source_status": "MISSING_RESPONSE_OPERATOR",
            "next_action_if_derivation_fails": "derive response operator or keep PPN branch unscored",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "priority_id": "CTP883_3_species_clock",
            "priority": 3,
            "quantity": "Delta_Q_tr/m and C_T_clock",
            "reason": "WEP/clock tests are high-pressure local consistency gates",
            "source_status": "MISSING_NO_MARKER_RESULT",
            "next_action_if_derivation_fails": "prove no-marker matter descent or source material-response rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "priority_id": "CTP883_4_bound_data",
            "priority": 4,
            "quantity": "R10 alpha(lambda) bound curve and arena projections",
            "reason": "numeric comparison is meaningless until theory-side coefficients exist",
            "source_status": "MISSING_FULL_CURVE_OR_ARENA_PROJECTION",
            "next_action_if_derivation_fails": "acquire data only after retained theory rows become numeric or stay as nonclaim plumbing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC883_0_selected",
            "route": "charge_unit_superselection_parent_clause_or_cT_P0_source_acquisition",
            "status": "selected",
            "reason": "Q_* superselection makes the endpoint projector scale-invariant, but parent proof of the unit is missing; next step must either derive the charge-unit sector or start priority-0 retained trace inputs",
            "include": "charge-unit superselection, Ward-current norm, charge lattice, exact-readout unit, P_tr endpoint scale invariance, c_T P0 source acquisition",
            "exclude": "Q_* claim, DeltaR claim, local-GR/Newton pass, R10/PPN pass, fitted Q_* counterterm, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG883_0_no_Qstar_claim",
            "claim": "Q_* is derived as a superselection unit",
            "status": "forbidden",
            "reason": "883 writes admissibility gates but no parent Ward norm/lattice theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG883_1_no_Ptr_claim",
            "claim": "P_tr is parent promoted",
            "status": "forbidden",
            "reason": "only the endpoint-block projector is scale-invariant; full K_parent and local projection are missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG883_2_no_DeltaR_claim",
            "claim": "DeltaR=2/9 is a parent prediction",
            "status": "forbidden",
            "reason": "endpoint arrow, Q_* unit, and parent relative-chain owner remain unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG883_3_no_cT_bound_claim",
            "claim": "retained c_T branch passes local bounds",
            "status": "forbidden",
            "reason": "c_T priority rows are still missing-input source-pack planning only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG883_4_no_local_GR_claim",
            "claim": "MTS locally reduces to GR/Newton",
            "status": "forbidden",
            "reason": "trace, matter descent, source normalization, and other residual channels remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG883_5_allowed_private_result",
            "claim": "endpoint P_tr scale cancellation is a useful private theorem target",
            "status": "allowed_private_nonclaim",
            "reason": "it narrows the Q_* problem to parent unit ownership rather than endpoint algebra",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D883_0",
            "finding": "Qstar_superselection_candidate_admissible",
            "reason": "fixed Q_* avoids the endpoint variation obstruction if the parent action owns it as a unit/superselection label",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D883_1",
            "finding": "endpoint_projector_scale_invariant",
            "reason": "ell and v carry inverse/forward Q_* powers that cancel in P_tr on the endpoint block",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D883_2",
            "finding": "parent_unit_owner_missing",
            "reason": "Ward norm, charge lattice, or exact-readout unit theorem is not present in the current corpus",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D883_3",
            "finding": "ct_source_priority_ready_if_derivation_fails",
            "reason": "retained trace branch now has a priority order starting with Z_tr/no-pole and J_tr/source projection",
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
            "objective": "derive or reject a parent charge-unit/superselection clause for Q_*; if it fails, begin priority-0 retained trace source acquisition for Z_tr/no-pole/lambda_tr and J_tr",
            "include": "Ward norm, relative cohomology charge lattice, exact-readout unit, endpoint P_tr scale-invariance, retained c_T P0 rows",
            "exclude": "public claim, Q_* fitted counterterm, R10/local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_882_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_882_VALIDATION.csv"
    if not path.exists():
        return False
    return all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF
    )


def all_nonclaim(row_sets: Iterable[list[dict[str, object]]]) -> bool:
    return all(row.get("valid_for_claim") is False for rows in row_sets for row in rows if "valid_for_claim" in row)


def validation_rows(
    source_rows: list[dict[str, object]],
    superselection_rows: list[dict[str, object]],
    projector_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_sets = [
        source_rows,
        superselection_rows,
        projector_rows,
        ward_rows,
        priority_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    superselection_candidate = any(row.get("gate_id") == "SS883_0_not_dynamic" for row in superselection_rows)
    projector_cancel = any(
        row.get("calc_id") == "EPS883_4_projector" and "Q_* cancels" in row.get("result", "")
        for row in projector_rows
    )
    finite_norm = any(
        row.get("calc_id") == "EPS883_2_norm" and "1/(3Q_*^2)" in row.get("calculation", "")
        for row in projector_rows
    )
    ward_missing = any(row.get("sector_id") == "WN883_4_verdict" and row.get("current_status") == "not_closed" for row in ward_rows)
    priority_ready = len(priority_rows) >= 5 and priority_rows[0].get("priority") == 0
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = route_rows_[0]["status"] == "selected" and next_target_rows_[0]["next_target"] == NEXT_TARGET
    fw_count = formalization_changed_count()
    checks = [
        ("V883_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V883_1_prior_882_clean", prior_882_clean(), "P8_Y5_BRR545_882_VALIDATION.csv clean"),
        ("V883_2_superselection_candidate_written", superselection_candidate, "Q_* fixed-unit/superselection gate recorded"),
        ("V883_3_endpoint_projector_scale_cancels", projector_cancel, "endpoint P_tr has Q_* cancellation"),
        ("V883_4_endpoint_norm_recorded", finite_norm, "endpoint normalization 1/(3Q_*^2) recorded"),
        ("V883_5_Ward_norm_sector_not_closed", ward_missing, "Q_* parent owner remains not closed"),
        ("V883_6_ct_priority_ready", priority_ready, "retained c_T source priority rows ready"),
        ("V883_7_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V883_8_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V883_9_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V883_10_route_selected", route_selected, NEXT_TARGET),
        ("V883_11_validation_rows_ready", True, "validation table constructed"),
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
    superselection_rows: list[dict[str, object]],
    projector_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 883 - Y5/R10 Qstar Superselection or Ward-Norm Sector and cT Source-Pack Prioritization",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **`Q_*` can be mathematically quarantined as a fixed unit, but it is not parent-derived yet**. "
        "If `Q_*` is a superselection/charge-unit label, then `delta Q_*=0` is legal and the 882 endpoint variation obstruction does not apply. "
        "Under the oriented endpoint Hessian `K_endpoint=diag(6,6)`, the endpoint trace covector and vector scale as "
        "`ell=(dQ_early-dQ_today)/Q_*` and `v=(Q_*/2)(partial_Qearly-partial_Qtoday)`, so the endpoint projector is "
        "`P_tr^end=(1/2)(partial_Qearly-partial_Qtoday) tensor (dQ_early-dQ_today)`: the `Q_*` scale cancels. "
        "That is the best new result. It still does not promote `Q_*`, full `P_tr`, `H_tr`, `DeltaR`, or local GR, because the parent Ward norm/charge lattice/superselection sector is unsigned.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Qstar Superselection Gate",
        md_table(superselection_rows),
        "",
        "## Endpoint Projector Scale Test",
        md_table(projector_rows),
        "",
        "## Ward Norm Sector Audit",
        md_table(ward_rows),
        "",
        "## cT Source Priority",
        md_table(priority_rows),
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
    superselection_rows = superselection_gate_rows(generated_utc)
    projector_rows = endpoint_projector_scale_rows(generated_utc)
    ward_rows = ward_norm_sector_rows(generated_utc)
    priority_rows = ct_priority_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        superselection_rows,
        projector_rows,
        ward_rows,
        priority_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_883_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_883_QSTAR_SUPERSELECTION_GATE.csv": superselection_rows,
        "P8_Y5_R10_883_ENDPOINT_PROJECTOR_SCALE_TEST.csv": projector_rows,
        "P8_Y5_R10_883_WARD_NORM_SECTOR_AUDIT.csv": ward_rows,
        "P8_Y5_R10_883_CT_SOURCE_PRIORITY.csv": priority_rows,
        "P8_Y5_R10_883_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_883_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_883_DECISION.csv": decision_rows_,
        "P8_Y5_R10_883_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_883_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_883_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "883-Y5-R10-Qstar-superselection-or-Ward-norm-sector-and-cT-source-pack-prioritization.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        superselection_rows,
        projector_rows,
        ward_rows,
        priority_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_883_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

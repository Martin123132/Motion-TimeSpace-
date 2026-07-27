from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_884_charge_unit_superselection_parent_clause_written_not_derived_cT_P0_source_acquisition_started_nonclaim"
CLAIM_CEILING = "charge_unit_superselection_contract_and_cT_P0_acquisition_only_no_Qstar_derivation_no_Ptr_Htr_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "885-Y5-R10-parent-charge-lattice-or-Htr-P0-zero-pole-source-fill.md"


SOURCES = [
    {
        "source_id": "883_doc",
        "path": ROOT / "883-Y5-R10-Qstar-superselection-or-Ward-norm-sector-and-cT-source-pack-prioritization.md",
        "needle": "charge-unit/superselection",
        "role": "immediate superselection handoff",
    },
    {
        "source_id": "883_validation",
        "path": OUT / "P8_Y5_BRR545_883_VALIDATION.csv",
        "needle": "V883_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "883_priority",
        "path": OUT / "P8_Y5_R10_883_CT_SOURCE_PRIORITY.csv",
        "needle": "CTP883_0_zero_or_pole",
        "role": "retained trace source priority order",
    },
    {
        "source_id": "882_doc",
        "path": ROOT / "882-Y5-R10-relative-chain-boundary-owner-and-Qstar-unit-or-retained-cT-minimum-source-pack.md",
        "needle": "endpoint action cannot derive a nonzero `Q_*`",
        "role": "endpoint-only Qstar rejection",
    },
    {
        "source_id": "863_Ward_trace",
        "path": ROOT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needle": "Q_* = unit(J_trace,parent)",
        "role": "Qstar unit theorem target and Jtrace local leakage branch",
    },
    {
        "source_id": "337_exact_readout",
        "path": ROOT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needle": "q_trace = 2/27",
        "role": "conditional exact readout ratio",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero",
        "role": "readout/spurion guard",
    },
    {
        "source_id": "109_boundary_charge",
        "path": ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needle": "boundary_charge_unit_defined",
        "role": "prior boundary charge unit failure",
    },
    {
        "source_id": "97_canonical_R",
        "path": ROOT / "97-canonical-R-theorem-attempt.md",
        "needle": "normalized_boundary_charge_derived",
        "role": "prior canonical R/Qstar failure",
    },
    {
        "source_id": "876_trace_hessian",
        "path": ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md",
        "needle": "principal-symbol normalization of the projected trace Hessian",
        "role": "P0 trace Hessian and no-pole source target",
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
            "what_changed": "wrote the exact charge-unit superselection parent clause Q_* would need, rejected current promotion, and began priority-0 retained trace source acquisition",
            "best_partial_result": "Q_* is now a precise parent-clause target: a nonzero, pre-data, locally silent generator/norm of a trace charge lattice or Ward-current unit; if signed, endpoint P_tr scale invariance from 883 can be used without varying Q_*",
            "hard_blockers": "no parent charge lattice, no Ward-current norm/pairing, exact-readout proof still conditional, no endpoint arrow, no full K_parent/H_tr, no local no-hair/source-cokernel",
            "what_is_not_claimed": "Q_* derivation, DeltaR prediction, parent P_tr/H_tr, c_T zero/pass, R10/PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def charge_unit_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "CU884_0_sector_label",
            "required_clause": "parent configuration space decomposes into fixed trace-charge sectors",
            "formal_statement": "Sol(S_parent)=union_{[Q_*]} Sol_{Q_*}; allowed variations satisfy delta Q_*=0 inside one sector",
            "if_signed": "Q_* is not a dynamical endpoint coordinate and 882 obstruction is avoided legitimately",
            "current_status": "clause_written_not_parent_signed",
            "blocker": "no parent action/source declares the sector decomposition",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "CU884_1_nonzero_unit",
            "required_clause": "Q_* is nonzero and finite",
            "formal_statement": "0<|Q_*|<infinity so R=Q/Q_* and endpoint P_tr normalization are defined",
            "if_signed": "endpoint covector/vector normalization from 883 is mathematically legal",
            "current_status": "required_not_derived",
            "blocker": "endpoint action cannot derive nonzero Q_*; separate unit owner required",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "CU884_2_charge_lattice",
            "required_clause": "trace boundary charges live in a parent charge lattice",
            "formal_statement": "[J_trace] in H_rel with Q_trace(Sigma)=n_Sigma Q_* or rational readout multiples of Q_*",
            "if_signed": "Q_* becomes a charge quantum/generator rather than a fitted scale",
            "current_status": "not_derived",
            "blocker": "relative cohomology language exists, but no integrality/lattice theorem is present",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "CU884_3_Ward_norm",
            "required_clause": "Q_* is the norm/unit of the trace Ward current",
            "formal_statement": "Q_*^2=<J_trace,J_trace>_parent or equivalent source-independent charge metric",
            "if_signed": "Q_* is fixed by the parent measure/pairing before any empirical scoring",
            "current_status": "missing_pairing_measure",
            "blocker": "no parent Hodge/measure/charge metric has been derived",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "CU884_4_exact_readout_unit",
            "required_clause": "exact readout fixes normalized trace ratios without EFT freedom",
            "formal_statement": "q_trace=2/27 is exact parent readout and not a Wilsonian fitted coupling",
            "if_signed": "rational normalized charges can be cited as parent readouts",
            "current_status": "conditional_only",
            "blocker": "337/338 still leave exact readout versus EFT/spurion proof open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "CU884_5_local_silence",
            "required_clause": "Q_* has no local gradient, species marker, or PPN hair",
            "formal_statement": "partial_mu Q_*=0, partial_A Q_*=0, and P_loc J_trace=0 in compact local domains",
            "if_signed": "charge-unit sector does not itself produce WEP/clock/PPN leakage",
            "current_status": "not_parent_signed",
            "blocker": "local no-hair and no-marker clauses remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "CU884_6_predata_lock",
            "required_clause": "Q_* source is written before data scoring",
            "formal_statement": "source path, owner, units, and fixed-sector status are recorded before SN/BAO/R10/PPN comparison",
            "if_signed": "prevents amplitude target inversion or fitted unit laundering",
            "current_status": "policy_gate_written",
            "blocker": "no source owner yet, so cannot promote",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "CU884_7_verdict",
            "required_clause": "charge-unit superselection theorem closes",
            "formal_statement": "CU884_0 through CU884_6 all parent-signed",
            "if_signed": "Q_* fixed-unit route can re-enter parent P_tr/H_tr and endpoint-arrow tests",
            "current_status": "not_derived",
            "blocker": "current corpus supplies a disciplined contract, not the proof",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG884_0_Qstar",
            "claim": "Q_* is a parent-fixed charge unit",
            "required_evidence": "charge lattice or Ward norm with pre-data source path",
            "current_evidence": "contract only",
            "gate_result": "fail_for_claim",
            "next_action": "try charge lattice/relative cohomology theorem or Ward norm owner",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG884_1_Ptr",
            "claim": "endpoint P_tr promotes to parent P_tr",
            "required_evidence": "Q_* unit plus full K_parent/pseudo-inverse and endpoint coordinates parent-owned",
            "current_evidence": "endpoint block scale-invariant only",
            "gate_result": "fail_for_claim",
            "next_action": "derive full K_parent or source H_tr P0 branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG884_2_zero_return",
            "claim": "local trace branch zero-returns",
            "required_evidence": "Dq_loc[v_tr]=0, P_loc J_trace=0, no physical pole, source-cokernel silence",
            "current_evidence": "not signed",
            "gate_result": "fail_for_claim",
            "next_action": "H_tr/no-pole and J_tr/source projection P0 acquisition",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG884_3_DeltaR",
            "claim": "DeltaR=2/9 is a parent prediction",
            "required_evidence": "Q_*, endpoint action coefficients, endpoint arrow, trace lift, no calibration leakage",
            "current_evidence": "conditional endpoint algebra and Q_* contract only",
            "gate_result": "fail_for_claim",
            "next_action": "do not score as public prediction; keep private theorem target",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def ct_p0_source_acquisition_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "p0_id": "P0_884_0_Htr",
            "quantity": "H_tr",
            "formula_or_test": "H_tr=P_tr^dagger Hess(S_parent) P_tr on the physical trace quotient sector",
            "required_source": "parent second variation plus parent P_tr/K_parent",
            "current_status": "MISSING_PARENT_HESSIAN",
            "claim_policy": "blocks Z_tr, lambda_tr, no-pole, and local trace force law",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "P0_884_1_Ztr",
            "quantity": "Z_tr",
            "formula_or_test": "principal symbol sigma_2(H_tr)=Z_tr g^{mu nu}k_mu k_nu or constrained-null result",
            "required_source": "principal symbol of H_tr or zero-return proof",
            "current_status": "MISSING_PARENT_HESSIAN",
            "claim_policy": "no R10/orbital alpha amplitude until numeric or theorem-zero",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "P0_884_2_mass_gap",
            "quantity": "mu_tr^2 and lambda_tr",
            "formula_or_test": "m_tr^2=mu_tr^2/Z_tr, lambda_tr=1/m_tr if Z_tr>0 and mu_tr^2>0",
            "required_source": "zeroth-order trace Hessian coefficient or no physical pole certificate",
            "current_status": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "claim_policy": "no finite-range local comparison until sourced",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "P0_884_3_no_pole",
            "quantity": "no physical local trace pole",
            "formula_or_test": "reduced inverse of H_tr has no source-coupled pole on compact local domains",
            "required_source": "constraint/gauge reduction, support theorem, or positive no-hair identity",
            "current_status": "MISSING_NOPOLE_CERTIFICATE",
            "claim_policy": "if proved, can zero-return range branch; otherwise bound lambda_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "P0_884_4_Jtr",
            "quantity": "J_tr",
            "formula_or_test": "delta S_int=int sqrt(-g) phi_tr J_tr and Q_tr^A=int_A J_tr",
            "required_source": "matter descent/source projection or P_loc J_trace=0 theorem",
            "current_status": "MISSING_SOURCE_PROJECTION",
            "claim_policy": "no alpha, PPN, WEP, or clock amplitude until source projection is sourced or zero",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "P0_884_5_Ploc_Jtrace",
            "quantity": "P_loc J_trace",
            "formula_or_test": "P_loc J_trace=0 or explicit retained local trace leakage source",
            "required_source": "local/global quotient split, boundary no-hair, or retained source row",
            "current_status": "MISSING_LOCAL_NOHAIR_OR_RETAINED_SOURCE",
            "claim_policy": "chooses zero-return branch or retained c_T branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC884_0_selected",
            "route": "parent_charge_lattice_or_Htr_P0_zero_pole_source_fill",
            "status": "selected",
            "reason": "charge-unit superselection is now an exact contract but not derived; the next best derivation attempt is a parent charge lattice, while the empirical fallback starts with H_tr/Z_tr/no-pole/J_tr P0 rows",
            "include": "relative cohomology charge lattice, Ward-current norm, exact-readout unit, H_tr/Z_tr/no-pole/J_tr P0 acquisition",
            "exclude": "Q_* claim, DeltaR claim, local-GR/Newton pass, R10/PPN pass, fitted counterterm, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG884_0_no_Qstar_claim",
            "claim": "Q_* superselection is proven",
            "status": "forbidden",
            "reason": "884 writes the parent clause but no charge lattice/Ward norm proof is present",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG884_1_no_Ptr_claim",
            "claim": "P_tr/H_tr are parent-derived",
            "status": "forbidden",
            "reason": "full K_parent/H_tr remains P0 missing input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG884_2_no_zero_return_claim",
            "claim": "local trace branch zero-returns",
            "status": "forbidden",
            "reason": "no-pole and P_loc J_trace/source-cokernel are not proved",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG884_3_no_retained_score_claim",
            "claim": "retained c_T branch can be scored",
            "status": "forbidden",
            "reason": "P0 rows are acquisition targets with missing parent inputs, not numeric predictions",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG884_4_no_local_GR_claim",
            "claim": "MTS locally reduces to GR/Newton",
            "status": "forbidden",
            "reason": "trace P0 plus broader source-normalization and matter-frame gates remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG884_5_allowed_private_result",
            "claim": "charge-unit superselection has an exact parent-clause contract and P0 fallback is staged",
            "status": "allowed_private_nonclaim",
            "reason": "this makes the next derivation/fallback fork explicit without laundering a claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D884_0",
            "finding": "charge_unit_clause_written",
            "reason": "Q_* must be a nonzero, pre-data, locally silent charge-unit sector with delta Q_*=0",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D884_1",
            "finding": "charge_unit_not_derived",
            "reason": "no parent charge lattice, Ward-current norm, or exact-readout unit theorem is present",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D884_2",
            "finding": "cT_P0_acquisition_started",
            "reason": "H_tr, Z_tr, mass/range/no-pole, J_tr, and P_loc J_trace are now explicit P0 source targets",
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
            "objective": "try a relative-cohomology charge lattice / Ward-current norm proof for Q_*; if it fails, fill or zero-return H_tr/Z_tr/no-pole/J_tr P0 rows",
            "include": "charge lattice, Ward-current norm, exact-readout unit, H_tr, Z_tr, mass gap, no-pole certificate, J_tr source projection",
            "exclude": "public claim, Q_* fitted counterterm, R10/local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_883_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_883_VALIDATION.csv"
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
    clause_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    p0_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_sets = [
        source_rows,
        clause_rows,
        promotion_rows,
        p0_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    clause_written = any(row.get("clause_id") == "CU884_0_sector_label" for row in clause_rows)
    unit_not_derived = any(row.get("clause_id") == "CU884_7_verdict" and row.get("current_status") == "not_derived" for row in clause_rows)
    promotion_blocked = all(row.get("gate_result") == "fail_for_claim" for row in promotion_rows)
    p0_ready = len(p0_rows) >= 6 and all("MISSING" in row.get("current_status", "") for row in p0_rows)
    p0_contains_htr = any(row.get("p0_id") == "P0_884_0_Htr" for row in p0_rows)
    p0_contains_jtr = any(row.get("p0_id") == "P0_884_4_Jtr" for row in p0_rows)
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = route_rows_[0]["status"] == "selected" and next_target_rows_[0]["next_target"] == NEXT_TARGET
    fw_count = formalization_changed_count()
    checks = [
        ("V884_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V884_1_prior_883_clean", prior_883_clean(), "P8_Y5_BRR545_883_VALIDATION.csv clean"),
        ("V884_2_charge_unit_clause_written", clause_written, "charge-unit superselection parent clause recorded"),
        ("V884_3_charge_unit_not_derived", unit_not_derived, "Q_* superselection remains not derived"),
        ("V884_4_promotion_gates_blocked", promotion_blocked, "all promotion gates fail for claim"),
        ("V884_5_cT_P0_ready", p0_ready, "P0 retained trace acquisition rows remain missing and nonclaim"),
        ("V884_6_cT_P0_has_Htr_Jtr", p0_contains_htr and p0_contains_jtr, "P0 rows include H_tr and J_tr"),
        ("V884_7_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V884_8_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V884_9_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V884_10_route_selected", route_selected, NEXT_TARGET),
        ("V884_11_validation_rows_ready", True, "validation table constructed"),
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
    clause_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    p0_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 884 - Y5/R10 Charge-Unit Superselection Parent Clause or cT P0 Source Acquisition",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the `Q_*` route is now an exact parent-clause target, not a loose escape hatch**. "
        "For `Q_*` to be legal as a fixed unit, the parent theory must supply a nonzero charge-unit/superselection sector: "
        "`Sol(S_parent)=union Sol_{Q_*}`, variations inside a sector obey `delta Q_*=0`, boundary trace charges live in a "
        "charge lattice or Ward-current norm, and `Q_*` has no local gradient/species marker. The current corpus does not prove "
        "that sector, so `Q_*`, `DeltaR`, parent `P_tr/H_tr`, and local GR remain unclaimed. Because this may fail, the retained "
        "`c_T` priority-0 acquisition branch is now started with explicit rows for `H_tr`, `Z_tr`, mass/range/no-pole, `J_tr`, and `P_loc J_trace`.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Charge Unit Parent Clause",
        md_table(clause_rows),
        "",
        "## Promotion Gate",
        md_table(promotion_rows),
        "",
        "## cT P0 Source Acquisition",
        md_table(p0_rows),
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
    clause_rows = charge_unit_clause_rows(generated_utc)
    promotion_rows = promotion_gate_rows(generated_utc)
    p0_rows = ct_p0_source_acquisition_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        clause_rows,
        promotion_rows,
        p0_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_884_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_884_CHARGE_UNIT_PARENT_CLAUSE.csv": clause_rows,
        "P8_Y5_R10_884_PROMOTION_GATE.csv": promotion_rows,
        "P8_Y5_R10_884_CT_P0_SOURCE_ACQUISITION.csv": p0_rows,
        "P8_Y5_R10_884_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_884_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_884_DECISION.csv": decision_rows_,
        "P8_Y5_R10_884_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_884_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_884_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "884-Y5-R10-charge-unit-superselection-parent-clause-or-cT-P0-source-acquisition.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        clause_rows,
        promotion_rows,
        p0_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_884_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

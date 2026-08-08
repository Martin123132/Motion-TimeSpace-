from __future__ import annotations

import csv
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_880_oriented_endpoint_action_contract_written_Qstar_Ward_normalization_and_local_nohair_unsigned_retained_cT_queue_open_nonclaim"
CLAIM_CEILING = "oriented_endpoint_action_contract_only_no_parent_signed_Qstar_Kparent_Ptr_zero_return_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "881-Y5-R10-Qstar-Ward-normalization-and-oriented-boundary-signature-or-retained-cT-bound-runner.md"


SOURCES = [
    {
        "source_id": "879_doc",
        "path": ROOT / "879-Y5-R10-parent-trace-covector-and-pairing-source-or-closure.md",
        "needle": "Q_trace/Q_*/K_parent",
        "role": "immediate handoff: missing trace charge, charge unit, and pairing",
    },
    {
        "source_id": "879_validation",
        "path": OUT / "P8_Y5_BRR545_879_VALIDATION.csv",
        "needle": "V879_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "878_doc",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "precise parent-geometry object",
        "role": "P_tr covector/pairing construction",
    },
    {
        "source_id": "876_doc",
        "path": ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md",
        "needle": "exact parent-Hessian problem",
        "role": "trace Hessian/Z_T/lambda_T contract",
    },
    {
        "source_id": "875_doc",
        "path": ROOT / "875-Y5-R10-cT-coefficient-fill-minimal-runner-and-claim-gate.md",
        "needle": "the c_T testing gate exists",
        "role": "retained c_T coefficient gate",
    },
    {
        "source_id": "875_ct_input_schema",
        "path": OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv",
        "needle": "IN875_0_Z_T",
        "role": "existing c_T coefficient/source-input schema",
    },
    {
        "source_id": "874_ct_fill_ledger",
        "path": OUT / "P8_Y5_R10_874_CT_COEFFICIENT_FILL_LEDGER.csv",
        "needle": "CTF874_0_Z_T",
        "role": "existing missing coefficient ledger",
    },
    {
        "source_id": "870_nohair",
        "path": ROOT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needle": "`c_T` remains retained",
        "role": "local no-hair/source-silence blocker",
    },
    {
        "source_id": "864_split",
        "path": ROOT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needle": "Dq_loc[U][v_T]=0",
        "role": "local/global quotient split condition",
    },
    {
        "source_id": "862_trace_lift",
        "path": ROOT / "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md",
        "needle": "DeltaQ_trace/Q_*",
        "role": "trace-lift endpoint algebra",
    },
    {
        "source_id": "111_variational_owner",
        "path": ROOT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needle": "relative charge pairing action",
        "role": "formal endpoint potential/pairing predecessor",
    },
    {
        "source_id": "110_endpoint_equation",
        "path": ROOT / "110-endpoint-charge-equation-attempt.md",
        "needle": "27 R^2 - 12 R + 1",
        "role": "endpoint polynomial target",
    },
    {
        "source_id": "109_boundary_charge",
        "path": ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needle": "derive Q_* and the endpoint charge split",
        "role": "Q_* and endpoint split blocker",
    },
    {
        "source_id": "10_symplectic",
        "path": ROOT / "10-observer-map-symplectic-contract.md",
        "needle": "Symplectic Preservation",
        "role": "symplectic pairing context, not sufficient as trace K_parent",
    },
    {
        "source_id": "97_canonical_R",
        "path": ROOT / "97-canonical-R-theorem-attempt.md",
        "needle": "Q_* fixes the unit boundary charge scale",
        "role": "canonical R/Q_* theorem blocker",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero",
        "role": "readout/source-at-zero legality",
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
            "what_changed": "constructed the sharpest minimal oriented endpoint action contract that could supply Q_trace roots and an endpoint Hessian, while keeping Q_* and local no-hair unsigned",
            "best_partial_result": "S_trace=Q_*^2[U(R_early)-U(R_today)] with U=9R^3-6R^2+R yields roots R_early=1/3, R_today=1/9, DeltaR=2/9, and positive oriented endpoint Hessian entries if the boundary orientation is parent-signed",
            "hard_blockers": "Ward-normalized Q_* unit, parent-signed boundary orientation/arrow, endpoint coordinates as parent variables, K_parent extension to quotient tangent space, local verticality/no-hair/source-cokernel",
            "what_is_not_claimed": "derived Q_*, parent-owned K_parent, P_tr promotion, Z_tr/lambda_tr, c_T=0, R10/PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def endpoint_action_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "MAC880_0_parent_variables",
            "required_object": "Q_early,Q_today,Q_*",
            "minimal_form": "R_early=Q_early/Q_* and R_today=Q_today/Q_* are parent boundary coordinates before data scoring",
            "if_signed": "Q_trace=(Q_early-Q_today)/Q_* becomes a parent readout rather than a fitted contrast",
            "current_status": "not_parent_signed",
            "blocks": "ell_tr cannot be parent-owned while endpoint coordinates and Q_* remain named variables only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MAC880_1_oriented_endpoint_action",
            "required_object": "S_trace orientation",
            "minimal_form": "S_trace=Q_*^2[U(R_early)-U(R_today)], U(R)=9R^3-6R^2+R",
            "if_signed": "Euler equations U'(R)=27R^2-12R+1=0 select roots 1/3 and 1/9 with DeltaR=2/9",
            "current_status": "formal_contract_constructed_not_parent_signed",
            "blocks": "boundary orientation/arrow is chosen by the contract, not yet derived from parent geometry",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MAC880_2_Qstar_normalization",
            "required_object": "Q_*",
            "minimal_form": "Q_* is fixed by a parent Ward current norm or charge unit before SN/BAO/R10/local scoring",
            "if_signed": "normalization of Q_trace and ell_tr is no longer arbitrary",
            "current_status": "missing_Ward_normalization",
            "blocks": "Q_trace scale and D ln Q_* term remain arbitrary",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MAC880_3_endpoint_pairing",
            "required_object": "K_endpoint",
            "minimal_form": "K_endpoint=diag(U''(1/3),-U''(1/9))=diag(6,6) on the oriented endpoint block",
            "if_signed": "endpoint trace covector can be raised without the sign-flip problem of the un-oriented potential",
            "current_status": "conditional_positive_endpoint_block",
            "blocks": "does not yet define the full parent K_parent on gauge/constraint quotient tangent space",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MAC880_4_parent_pairing_extension",
            "required_object": "K_parent or constrained pseudo-inverse",
            "minimal_form": "K_parent extends K_endpoint and has a nondegenerate inverse or constrained pseudo-inverse on the trace quotient sector",
            "if_signed": "v_tr=K_parent^-1 ell_tr/<ell_tr,K_parent^-1 ell_tr> and P_tr=v_tr tensor ell_tr become calculable",
            "current_status": "not_derived",
            "blocks": "P_tr and H_tr cannot be promoted from endpoint algebra alone",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MAC880_5_local_silence",
            "required_object": "local verticality and no-hair",
            "minimal_form": "Dq_loc[U][v_tr]=0, P_loc J_trace=0, P_loc dB_trace=0, and no clock/WEP/species marker survives",
            "if_signed": "trace endpoint can be FLRW-visible while local compact experiments retain GR/Newton silence",
            "current_status": "unsigned",
            "blocks": "finite c_T retained branch remains open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MAC880_6_claim_promotion_rule",
            "required_object": "zero-or-bound fork",
            "minimal_form": "claim only if Q_*, orientation, K_parent, P_tr/H_tr, and local no-hair all sign; otherwise source c_T/Z_tr/lambda_tr/J_tr as retained inputs",
            "if_signed": "prevents coupling laundering while preserving a testable fallback",
            "current_status": "rule_written",
            "blocks": "current branch remains private nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def formal_calculation_rows(generated_utc: str) -> list[dict[str, object]]:
    r_early = Fraction(1, 3)
    r_today = Fraction(1, 9)
    delta_r = r_early - r_today
    return [
        {
            "calc_id": "FC880_0_endpoint_potential",
            "assumption": "oriented endpoint action is parent-signed",
            "calculation": "U(R)=9R^3-6R^2+R; U_prime(R)=27R^2-12R+1",
            "result": "stationarity equation matches the prior endpoint polynomial",
            "status": "formal_exact",
            "claim_gap": "U was reconstructed as a minimal contract; not derived from parent action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "FC880_1_roots",
            "assumption": "choose the ordered endpoint arrow R_early>R_today",
            "calculation": "27R^2-12R+1=0 has roots 1/3 and 1/9",
            "result": f"R_early={r_early}; R_today={r_today}; DeltaR={delta_r}",
            "status": "formal_exact",
            "claim_gap": "arrow/order remains boundary-orientation data, not a theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "FC880_2_unoriented_hessian_problem",
            "assumption": "single potential U supplies both endpoint curvatures with no orientation",
            "calculation": "U_second(R)=54R-12 gives U_second(1/3)=6 and U_second(1/9)=-6",
            "result": "unoriented scalar potential has one positive and one negative endpoint curvature",
            "status": "blocks_positive_Kparent_if_unoriented",
            "claim_gap": "requires oriented boundary action, symplectic treatment, or constrained pseudo-inverse",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "FC880_3_oriented_hessian_candidate",
            "assumption": "S_trace=Q_*^2[U(R_early)-U(R_today)]",
            "calculation": "K_endpoint=diag(U_second(1/3),-U_second(1/9))",
            "result": "K_endpoint=diag(6,6), conditionally positive on endpoint block",
            "status": "best_new_partial_result",
            "claim_gap": "boundary sign/orientation and Q_* normalization are not parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "FC880_4_trace_covector_endpoint_block",
            "assumption": "Q_* fixed and endpoint coordinates parent-owned",
            "calculation": "ell_tr=D[(Q_early-Q_today)/Q_*]=(dQ_early-dQ_today)/Q_*",
            "result": "ell_tr has a clean endpoint-block formula if DQ_*=0",
            "status": "conditional_formula",
            "claim_gap": "D ln Q_* term returns if Q_* varies; Q_* ownership still missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "FC880_5_formal_endpoint_vector",
            "assumption": "K_endpoint=diag(6,6) and Q_* fixed",
            "calculation": "<ell,K^-1 ell>=1/(3Q_*^2); v_tr=(Q_*/2)(partial_Qearly-partial_Qtoday)",
            "result": "P_tr endpoint block can be written formally",
            "status": "conditional_formula",
            "claim_gap": "endpoint block is not the full parent quotient K_parent and local projection is unknown",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "calc_id": "FC880_6_local_zero_not_following",
            "assumption": "endpoint P_tr exists formally",
            "calculation": "local zero still requires Dq_loc[U][v_tr]=0 plus P_loc J_trace=0 and no physical trace pole",
            "result": "endpoint action alone does not derive local GR/Newton",
            "status": "blocked_retained_branch_open",
            "claim_gap": "local no-hair/source-cokernel and H_tr no-pole tests remain unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def contract_satisfaction_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CS880_0_endpoint_polynomial",
            "required_clause": "U_prime(R)=27R^2-12R+1",
            "current_evidence": "formal potential U=9R^3-6R^2+R supplies it",
            "gate_result": "conditional_pass_contract_only",
            "why_not_claim": "U is reverse-engineered from the target equation, not parent-derived",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CS880_1_DeltaR",
            "required_clause": "ordered endpoint roots differ by 2/9",
            "current_evidence": "1/3-1/9=2/9",
            "gate_result": "conditional_pass_contract_only",
            "why_not_claim": "endpoint arrow/order requires parent boundary orientation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CS880_2_Qstar",
            "required_clause": "Q_* fixed by Ward charge unit before data scoring",
            "current_evidence": "repeatedly identified as missing in 109/861/862/864/879",
            "gate_result": "fail_missing_parent_input",
            "why_not_claim": "scale of Q_trace and ell_tr is arbitrary until Q_* is derived",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CS880_3_Kendpoint",
            "required_clause": "endpoint Hessian has a healthy sign",
            "current_evidence": "oriented action gives diag(6,6)",
            "gate_result": "conditional_pass_if_orientation_signed",
            "why_not_claim": "orientation is the thing to derive; cannot be inserted as a hidden axiom",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CS880_4_Kparent",
            "required_clause": "K_endpoint extends to parent K_parent/pseudo-inverse",
            "current_evidence": "no source supplies the full quotient tangent pairing",
            "gate_result": "fail_missing_parent_input",
            "why_not_claim": "P_tr and H_tr require the full pairing, not just endpoint-block algebra",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CS880_5_local_nohair",
            "required_clause": "Dq_loc[v_tr]=0, P_loc J_trace=0, no tails, no marker charges",
            "current_evidence": "870/878/879 keep these clauses unsigned",
            "gate_result": "fail_missing_zero_theorem",
            "why_not_claim": "finite trace residual c_T remains live until local projection silence is proved or bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CS880_6_overall",
            "required_clause": "all parent action clauses signed",
            "current_evidence": "endpoint contract improved, but Q_* and K_parent/local nohair remain missing",
            "gate_result": "fail_for_claim_keep_derivation_route_alive",
            "why_not_claim": "the result is a good future action contract, not a completed local-GR derivation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def retained_ct_bound_queue_rows(generated_utc: str) -> list[dict[str, object]]:
    source_path = OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv"
    return [
        {
            "queue_id": "RCB880_0_cT",
            "quantity": "c_T",
            "role": "finite local trace leakage amplitude if local no-hair fails",
            "units": "dimensionless_or_source_normalized",
            "required_parent_input": "projection of J_trace onto local matter/metric response",
            "current_value": "MISSING_PARENT_PROJECTION",
            "source_path": str(source_path),
            "status": "retained_nonclaim_input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "RCB880_1_Ztr",
            "quantity": "Z_tr",
            "role": "trace carrier kinetic/principal-symbol normalization",
            "units": "parent_defined",
            "required_parent_input": "principal symbol of H_tr=P_tr^dagger Hess(S_parent) P_tr",
            "current_value": "MISSING_PARENT_HESSIAN",
            "source_path": str(source_path),
            "status": "retained_nonclaim_input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "RCB880_2_lambdatr",
            "quantity": "lambda_tr_or_m_tr",
            "role": "trace carrier range or no-pole certificate",
            "units": "length_or_mass_parent_defined",
            "required_parent_input": "trace mass gap, support theorem, or no physical pole result",
            "current_value": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "source_path": str(source_path),
            "status": "retained_nonclaim_input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "RCB880_3_Jtr",
            "quantity": "J_tr",
            "role": "source projection of matter/metric onto trace carrier",
            "units": "source_density_or_charge_per_mass",
            "required_parent_input": "matter descent/no-marker theorem or explicit source-normalized charge law",
            "current_value": "MISSING_SOURCE_PROJECTION",
            "source_path": str(source_path),
            "status": "retained_nonclaim_input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "RCB880_4_tau_R10",
            "quantity": "tau_R10",
            "role": "short-range alpha(lambda) projection for R10/fifth-force comparison",
            "units": "dimensionless_alpha_vs_length",
            "required_parent_input": "Z_tr, lambda_tr, source charges, real R10 bound curve",
            "current_value": "MISSING_COEFFICIENTS_AND_FULL_CURVE",
            "source_path": str(source_path),
            "status": "retained_nonclaim_input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "RCB880_5_tau_PPN",
            "quantity": "tau_PPN",
            "role": "gamma/beta/source-normalized Newtonian residual if trace leakage survives",
            "units": "dimensionless_PPN_residual",
            "required_parent_input": "metric response operator and GM absorption/source normalization",
            "current_value": "MISSING_RESPONSE_OPERATOR",
            "source_path": str(source_path),
            "status": "retained_nonclaim_input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "RCB880_6_tau_clock_WEP",
            "quantity": "tau_clock_WEP",
            "role": "clock drift, material/species marker, or composition-dependent acceleration residual",
            "units": "fractional_clock_or_Eotvos_like",
            "required_parent_input": "no-marker theorem or species trace charge response",
            "current_value": "MISSING_NO_MARKER_RESULT",
            "source_path": str(source_path),
            "status": "retained_nonclaim_input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "RCB880_7_tau_orbital",
            "quantity": "tau_orbital",
            "role": "finite-range orbital/radial acceleration or GM-drift residual",
            "units": "fractional_acceleration_or_GM_drift",
            "required_parent_input": "alpha_tr(lambda), lambda_tr, source geometry, GM absorption proof",
            "current_value": "MISSING_ORBITAL_PROJECTION",
            "source_path": str(source_path),
            "status": "retained_nonclaim_input",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC880_0_selected",
            "route": "Qstar_Ward_normalization_and_oriented_boundary_signature_before_retained_cT_runner",
            "status": "selected",
            "reason": "880 found a sharper oriented endpoint action contract, so the best next derivation target is not blind coefficient filling but the two missing signatures that would make the contract non-ad-hoc: Q_* Ward normalization and boundary orientation/arrow",
            "include": "Ward current norm, Q_* unit, oriented boundary sign, endpoint arrow, K_parent extension test, retained c_T queue kept open",
            "exclude": "local-GR claim, R10/PPN claim, fitted DeltaR, public prose, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG880_0_no_endpoint_theorem_claim",
            "claim": "DeltaR=2/9 is derived from the parent action",
            "status": "forbidden",
            "reason": "the oriented action is a minimal contract, not a parent-derived action block",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG880_1_no_Qstar_claim",
            "claim": "Q_* is Ward-normalized",
            "status": "forbidden",
            "reason": "Q_* remains the explicit next theorem target",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG880_2_no_Kparent_claim",
            "claim": "K_parent is derived",
            "status": "forbidden",
            "reason": "diag(6,6) is only an endpoint-block Hessian under a chosen orientation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG880_3_no_Ptr_Htr_claim",
            "claim": "P_tr and H_tr are promoted",
            "status": "forbidden",
            "reason": "P_tr/H_tr need Q_*, full K_parent, local quotient projection, and no-pole/source-cokernel checks",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG880_4_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "local trace no-hair, coframe/matter descent, and other residual channels remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG880_5_allowed_private_result",
            "claim": "oriented endpoint action contract is a useful private derivation target",
            "status": "allowed_private_nonclaim",
            "reason": "it converts a vague coupling gap into two exact missing signatures: Q_* normalization and boundary orientation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D880_0",
            "finding": "oriented_endpoint_contract_constructed",
            "reason": "S_trace=Q_*^2[U(R_early)-U(R_today)] produces the target roots and a positive endpoint Hessian if the orientation is parent-signed",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D880_1",
            "finding": "Qstar_and_boundary_orientation_missing",
            "reason": "without Q_* Ward normalization and boundary orientation, the contract is still a reconstructed skeleton",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D880_2",
            "finding": "retained_cT_queue_remains_open",
            "reason": "if 881 cannot sign Q_* and orientation, trace leakage must be treated as c_T/Z_tr/lambda_tr/J_tr bound inputs",
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
            "objective": "derive or reject Ward normalization for Q_* and the oriented boundary sign/arrow needed to turn the endpoint action skeleton into a parent-owned trace charge block; otherwise execute retained c_T bound runner",
            "include": "Q_* as Ward current norm, endpoint boundary orientation, arrow R_early=1/3 to R_today=1/9, K_parent extension, retained c_T queue",
            "exclude": "public claim, fitted endpoint values, local-GR claim, R10 pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_879_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_879_VALIDATION.csv"
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
    contract_rows: list[dict[str, object]],
    calc_rows: list[dict[str, object]],
    satisfaction_rows: list[dict[str, object]],
    retained_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_sets = [
        source_rows,
        contract_rows,
        calc_rows,
        satisfaction_rows,
        retained_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    endpoint_action_written = any(row.get("contract_id") == "MAC880_1_oriented_endpoint_action" for row in contract_rows)
    roots_ok = any("DeltaR=2/9" in row.get("result", "") for row in calc_rows)
    hessian_ok = any(row.get("calc_id") == "FC880_3_oriented_hessian_candidate" and "diag(6,6)" in row.get("result", "") for row in calc_rows)
    qstar_blocked = any(row.get("gate_id") == "CS880_2_Qstar" and row.get("gate_result") == "fail_missing_parent_input" for row in satisfaction_rows)
    kparent_blocked = any(row.get("gate_id") == "CS880_4_Kparent" and row.get("gate_result") == "fail_missing_parent_input" for row in satisfaction_rows)
    nohair_blocked = any(row.get("gate_id") == "CS880_5_local_nohair" and row.get("gate_result") == "fail_missing_zero_theorem" for row in satisfaction_rows)
    retained_ready = len(retained_rows) >= 8 and all(row.get("status") == "retained_nonclaim_input" for row in retained_rows)
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = route_rows_[0]["status"] == "selected" and next_target_rows_[0]["next_target"] == NEXT_TARGET
    fw_count = formalization_changed_count()
    checks = [
        ("V880_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V880_1_prior_879_clean", prior_879_clean(), "P8_Y5_BRR545_879_VALIDATION.csv clean"),
        ("V880_2_endpoint_action_contract_written", endpoint_action_written, "oriented endpoint action contract recorded"),
        ("V880_3_roots_and_DeltaR_recorded", roots_ok, "roots 1/3 and 1/9 with DeltaR=2/9 recorded"),
        ("V880_4_oriented_hessian_candidate_recorded", hessian_ok, "oriented endpoint Hessian diag(6,6) recorded"),
        ("V880_5_Qstar_remains_blocked", qstar_blocked, "Q_* Ward normalization remains missing"),
        ("V880_6_Kparent_remains_blocked", kparent_blocked, "full K_parent/pseudo-inverse remains missing"),
        ("V880_7_local_nohair_remains_blocked", nohair_blocked, "local no-hair/source-cokernel remains missing"),
        ("V880_8_retained_ct_queue_ready", retained_ready, "c_T/Z_tr/lambda_tr/J_tr retained input queue ready"),
        ("V880_9_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V880_10_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V880_11_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V880_12_route_selected", route_selected, NEXT_TARGET),
        ("V880_13_validation_rows_ready", True, "validation table constructed"),
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
    contract_rows: list[dict[str, object]],
    calc_rows: list[dict[str, object]],
    satisfaction_rows: list[dict[str, object]],
    retained_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 880 - Y5/R10 Minimal Qtrace/Qstar/Kparent Action Contract or Retained cT Bound",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the endpoint/coupling problem is sharper, but still not claimable**. "
        "A minimal oriented endpoint action `S_trace=Q_*^2[U(R_early)-U(R_today)]`, "
        "with `U(R)=9R^3-6R^2+R`, gives the target stationarity equation "
        "`U'(R)=27R^2-12R+1=0`, roots `R_early=1/3`, `R_today=1/9`, "
        "and `DeltaR=2/9`. The same orientation repairs the endpoint Hessian sign, "
        "giving `K_endpoint=diag(6,6)` instead of one positive and one negative curvature. "
        "That is a real useful contract, not a theorem: `Q_*`, the boundary orientation/arrow, "
        "the full parent `K_parent`, and local no-hair/source-cokernel silence remain unsigned. "
        "So `P_tr`, `H_tr`, `Z_tr/lambda_tr`, `c_T=0`, and local GR/Newton are not promoted.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Minimal Action Contract",
        md_table(contract_rows),
        "",
        "## Formal Calculation",
        md_table(calc_rows),
        "",
        "## Contract Satisfaction",
        md_table(satisfaction_rows),
        "",
        "## Retained cT Bound Queue",
        md_table(retained_rows),
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
    contract_rows = endpoint_action_contract_rows(generated_utc)
    calc_rows = formal_calculation_rows(generated_utc)
    satisfaction_rows = contract_satisfaction_rows(generated_utc)
    retained_rows = retained_ct_bound_queue_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        contract_rows,
        calc_rows,
        satisfaction_rows,
        retained_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_880_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_880_MINIMAL_ACTION_CONTRACT.csv": contract_rows,
        "P8_Y5_R10_880_FORMAL_CALCULATION.csv": calc_rows,
        "P8_Y5_R10_880_CONTRACT_SATISFACTION.csv": satisfaction_rows,
        "P8_Y5_R10_880_RETAINED_CT_BOUND_QUEUE.csv": retained_rows,
        "P8_Y5_R10_880_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_880_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_880_DECISION.csv": decision_rows_,
        "P8_Y5_R10_880_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_880_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_880_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "880-Y5-R10-minimal-Qtrace-Qstar-Kparent-action-contract-or-retained-cT-bound.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        contract_rows,
        calc_rows,
        satisfaction_rows,
        retained_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_880_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

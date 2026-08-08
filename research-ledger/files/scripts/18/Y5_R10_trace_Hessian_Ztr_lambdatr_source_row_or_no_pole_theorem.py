from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_892_trace_Hessian_Ztr_lambdatr_source_rows_written_no_pole_theorem_conditional_not_signed_nonclaim"
CLAIM_CEILING = "trace_Hessian_source_rows_and_conditional_no_pole_theorem_only_no_Ztr_lambda_numeric_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "893-Y5-R10-Ptr-rank-zero-parent-signature-or-Htr-principal-symbol-source-fill.md"

SOURCE_SPECS = [
    {
        "source_id": "891_doc",
        "path": ROOT / "891-Y5-R10-finite-trace-coefficient-source-row-builder-with-zero-route-watch.md",
        "needle": "finite trace fallback now has a disciplined source-row manifest",
        "role": "immediate handoff from finite trace source-row manifest",
    },
    {
        "source_id": "891_validation",
        "path": OUT / "P8_Y5_BRR545_891_VALIDATION.csv",
        "needle": "V891_13_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "891_coeff_rows",
        "path": OUT / "P8_Y5_R10_891_TRACE_COEFFICIENT_SOURCE_ROWS.csv",
        "needle": "TCSR891_1_lambda_tr",
        "role": "upstream Z_tr/lambda_tr source rows",
    },
    {
        "source_id": "891_zero_watch",
        "path": OUT / "P8_Y5_R10_891_ZERO_ROUTE_WATCH.csv",
        "needle": "ZRW891_2_no_pole",
        "role": "upstream no-pole watch",
    },
    {
        "source_id": "876_trace_hessian",
        "path": ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md",
        "needle": "`Z_T` must be the principal-symbol normalization",
        "role": "parent trace-Hessian extraction contract",
    },
    {
        "source_id": "877_htr_skeleton",
        "path": ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md",
        "needle": "H_tr=P_tr^dagger Hess(S_parent) P_tr",
        "role": "minimal H_tr action skeleton",
    },
    {
        "source_id": "878_projector",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "`P_tr` is now a precise parent-geometry object",
        "role": "P_tr construction and local rank test",
    },
    {
        "source_id": "885_htr_fill",
        "path": OUT / "P8_Y5_R10_885_HTR_ZERO_POLE_SOURCE_FILL.csv",
        "needle": "HZ885_5_bound_branch",
        "role": "retained finite trace branch source-fill queue",
    },
    {
        "source_id": "886_zero_pole",
        "path": ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md",
        "needle": "rank-zero/no-pole/source-cokernel",
        "role": "conditional zero-pole implication theorem",
    },
    {
        "source_id": "872_projection_formulas",
        "path": ROOT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md",
        "needle": "alpha_T_AB = Q_T^A Q_T^B/(4*pi*Z_T*G_obs*m_A*m_B)",
        "role": "finite trace alpha/lambda observable formulas",
    },
    {
        "source_id": "875_ct_schema",
        "path": OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv",
        "needle": "IN875_1_lambda_T",
        "role": "minimal c_T input schema",
    },
    {
        "source_id": "890_no_tail",
        "path": OUT / "P8_Y5_R10_890_BOUNDARY_NO_TAIL_THEOREM_ATTEMPT.csv",
        "needle": "NT890_5_no_tail_corollary",
        "role": "boundary/no-tail corollary feeding rank-zero route",
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
            "what_changed": "wrote the trace-Hessian source rows for H_tr, Z_tr, mu_tr^2, lambda_tr, sign/stability, source-coupled domain, units, and provenance; also sharpened the no-pole theorem attempt",
            "best_partial_result": "a source-coupled trace pole now has an exact fork: either rank(P_loc P_tr P_loc^dagger)=0 or readout-only/constraint-null status kills the local pole, or the finite branch must source H_tr principal and mass symbols",
            "hard_blockers": "P_tr is not parent-signed, q_loc compact restriction is not owned, H_tr is not computed, source-cokernel/matter descent is unsigned, and no numeric Z_tr or lambda_tr exists",
            "what_is_not_claimed": "numeric Z_tr, numeric lambda_tr, no local trace pole, trace zero-return, R10 pass, PPN pass, clock/WEP/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def trace_hessian_source_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "THS892_0_Htr_definition",
            "quantity": "H_tr",
            "mathematical_form": "H_tr=P_tr^dagger Hess(S_parent) P_tr on the gauge/constraint-reduced parent quotient tangent space",
            "needed_for": "owning the trace branch operator before any Z_tr or lambda_tr readout",
            "current_status": "MISSING_PARENT_HESSIAN",
            "missing_clause": "actual second variation of the parent action after P_tr is parent-defined",
            "if_filled": "compute principal symbol, mass term, reduced inverse, and source-coupled domain",
            "if_zero_route": "unnecessary if P_tr is signed as rank-zero/readout-only before H_tr exists locally",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "THS892_1_Ztr_principal_symbol",
            "quantity": "Z_tr",
            "mathematical_form": "sigma_2(H_tr)=Z_tr g^{mu nu} k_mu k_nu on the physical scalar trace subspace",
            "needed_for": "alpha amplitude normalization, ghost check, finite carrier branch",
            "current_status": "MISSING_PRINCIPAL_SYMBOL",
            "missing_clause": "parent H_tr principal symbol and normalization convention",
            "if_filled": "Z_tr>0 would be required for a healthy finite scalar carrier",
            "if_zero_route": "not a physical local input if no source-coupled H_tr pole exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "THS892_2_mutr_mass_term",
            "quantity": "mu_tr^2",
            "mathematical_form": "H_tr approx Z_tr(-box)+mu_tr^2 at quadratic order after reduction",
            "needed_for": "trace mass gap and range",
            "current_status": "MISSING_ZEROTH_ORDER_SYMBOL",
            "missing_clause": "zeroth-order parent Hessian coefficient and stability sign",
            "if_filled": "m_tr^2=mu_tr^2/Z_tr can be tested for positive, zero, tachyonic, or constrained status",
            "if_zero_route": "irrelevant if the reduced inverse has no local source-coupled pole",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "THS892_3_lambdatr_range",
            "quantity": "lambda_tr_or_m_tr",
            "mathematical_form": "lambda_tr=1/m_tr in natural units or hbar/(m_tr c) in SI once parent units are fixed",
            "needed_for": "R10 alpha(lambda), orbital Yukawa profile, range-dependent local residuals",
            "current_status": "MISSING_MASS_GAP_OR_NOPOLE",
            "missing_clause": "Z_tr and mu_tr^2, or a theorem that lambda_tr is not physical",
            "if_filled": "finite branch can be compared to R10/orbital bounds only after Q_tr and bound curves are sourced",
            "if_zero_route": "lambda_tr is not populated because the local Green function is absent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "THS892_4_sign_stability",
            "quantity": "Z_tr_sign_and_mu_tr2_sign",
            "mathematical_form": "healthy finite carrier needs Z_tr>0 and mu_tr^2>=0 unless the mode is gauge/constraint-null",
            "needed_for": "no ghost/tachyon discipline before empirical scoring",
            "current_status": "MISSING_SIGN_CERTIFICATE",
            "missing_clause": "parent Hessian signature on the reduced trace subspace",
            "if_filled": "decides whether finite branch is healthy, unstable, or auxiliary/constraint-only",
            "if_zero_route": "constraint-null sign certificate becomes the no-pole certificate",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "THS892_5_source_coupled_domain",
            "quantity": "local_source_coupled_domain",
            "mathematical_form": "a pole requires nonzero local image and nonzero source-cokernel pairing for H_tr^{-1}J_tr",
            "needed_for": "deciding whether a finite local force carrier exists at all",
            "current_status": "MISSING_LOCAL_IMAGE_OR_ZERO_THEOREM",
            "missing_clause": "rank(P_loc P_tr P_loc^dagger), q_loc support, reduced inverse, and J_tr source-cokernel",
            "if_filled": "nonzero domain keeps finite carrier legal and requires bounds",
            "if_zero_route": "rank-zero or source-cokernel zero kills R10/clock/WEP/orbital trace amplitudes",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "THS892_6_units_convention",
            "quantity": "trace_units_and_normalization",
            "mathematical_form": "canonical trace field normalization, SI conversion, and G_obs convention must be fixed before alpha_tr_AB",
            "needed_for": "dimensional consistency and comparison to alpha(lambda) bounds",
            "current_status": "MISSING_UNITS_CONVENTION",
            "missing_clause": "canonical field map from parent variables to local scalar normalization",
            "if_filled": "prevents hiding dimensional errors in Z_tr/lambda_tr/Q_tr rows",
            "if_zero_route": "still record theorem-zero units/provenance, but no alpha row is promoted",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "THS892_7_provenance",
            "quantity": "source_path_and_parent_signature",
            "mathematical_form": "every numeric or theorem-zero row must cite the parent source path, clause, units, and extraction method",
            "needed_for": "claim hygiene and reproducibility",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "missing_clause": "source-backed parent coefficients or source-backed theorem-zero signatures",
            "if_filled": "candidate branch can move to arena projection rows",
            "if_zero_route": "zero theorem can be promoted only with the same provenance burden",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def no_pole_theorem_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "NPT892_0_rank_zero_domain",
            "clause": "rank(P_loc P_tr P_loc^dagger)=0 on compact lab/solar-system domains",
            "derivation": "Let V_loc be the compact-local quotient tangent image and V_tr the trace projector image. A local Green-function pole requires a nonzero source-coupled vector in V_loc intersect V_tr. Rank zero makes this intersection trivial.",
            "proof_status": "conditional_theorem_valid",
            "missing_signature": "P_tr owner, q_loc compact restriction, and boundary/readout support are not parent-signed",
            "if_signed": "H_tr has no compact-local trace domain and lambda_tr is not a physical local range",
            "if_failed": "finite trace carrier remains legal and H_tr symbols must be sourced",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NPT892_1_readout_only_no_spurion",
            "clause": "P_tr is post-variation readout/source-at-zero, not a spurion in S_parent",
            "derivation": "A source inserted only after solving the parent equations can label a solution branch but cannot add a local quadratic operator or local matter force term.",
            "proof_status": "conditional_rule_valid",
            "missing_signature": "readout-only/action-level clause for the trace endpoint is not parent-signed",
            "if_signed": "no local H_tr pole is introduced by the readout itself",
            "if_failed": "P_tr can backreact and the finite branch must be bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NPT892_2_constraint_null_inverse",
            "clause": "H_tr is gauge/constraint-null after reduction",
            "derivation": "If all trace directions lie in a constraint/gauge kernel and the reduced operator has no inverse on a physical local scalar subspace, the apparent pole is removed before sources couple.",
            "proof_status": "conditional_theorem_valid",
            "missing_signature": "reduced Hessian rank, gauge bracket, and constraint algebra are not computed",
            "if_signed": "Z_tr/lambda_tr are gauge-bookkeeping rather than physical local inputs",
            "if_failed": "principal symbol and mass gap rows become mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NPT892_3_source_cokernel_silence",
            "clause": "J_tr has zero projection on every physical local H_tr cokernel mode",
            "derivation": "If matter descends through q_loc and v_tr is local-vertical, chain rule gives partial_{v_tr}S_matter=0; equivalently <u_tr,J_tr>=0 for all physical local cokernel modes.",
            "proof_status": "conditional_theorem_valid",
            "missing_signature": "matter descent/no-marker and source-owner clauses are still unsigned",
            "if_signed": "even a formal trace variable carries no R10/WEP/clock/orbital source amplitude",
            "if_failed": "Q_tr/m and species/clock response rows must be filled",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NPT892_4_verdict",
            "clause": "no local trace pole requires rank-zero or readout-only/constraint-null plus source-cokernel silence",
            "derivation": "The mathematical implication is clean, but the current corpus still lacks the parent signatures needed to instantiate the premises.",
            "proof_status": "conditional_not_parent_signed",
            "missing_signature": "P_tr, q_loc compact restriction, boundary/no-tail, reduced H_tr rank, matter descent, and source-cokernel provenance",
            "if_signed": "trace branch can zero-return locally, though local GR still needs the other residual channels",
            "if_failed": "source H_tr principal symbol and mass/range in 893 before any bound claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def hessian_input_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "HIG892_0_Htr_definition",
            "required_input": "parent-owned H_tr=P_tr^dagger Hess(S_parent)P_tr",
            "current_evidence": "skeleton only",
            "gate_result": "fail_for_claim",
            "claim_allowed": False,
            "next_action": "parent-sign P_tr or construct the reduced trace Hessian",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "HIG892_1_principal_symbol",
            "required_input": "Z_tr from sigma_2(H_tr)",
            "current_evidence": "MISSING_PRINCIPAL_SYMBOL",
            "gate_result": "fail_for_claim",
            "claim_allowed": False,
            "next_action": "derive principal symbol or prove no source-coupled pole",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "HIG892_2_mass_range",
            "required_input": "mu_tr^2, m_tr, lambda_tr",
            "current_evidence": "MISSING_MASS_GAP_OR_NOPOLE",
            "gate_result": "fail_for_claim",
            "claim_allowed": False,
            "next_action": "derive mass gap or keep lambda_tr unphysical by theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "HIG892_3_source_domain",
            "required_input": "nonzero/zero local source-coupled domain",
            "current_evidence": "MISSING_LOCAL_IMAGE_OR_ZERO_THEOREM",
            "gate_result": "fail_for_claim",
            "claim_allowed": False,
            "next_action": "run P_tr rank-zero/source-cokernel branch before empirical scoring",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "HIG892_4_units_provenance",
            "required_input": "units, normalization, source paths, extraction method",
            "current_evidence": "SCHEMA_READY_VALUES_MISSING",
            "gate_result": "fail_for_claim",
            "claim_allowed": False,
            "next_action": "no numeric row can become valid_for_claim without provenance",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def zero_route_impact_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "impact_id": "ZRI892_0_if_no_pole_signed",
            "condition": "rank-zero/readout-only/constraint-null and source-cokernel clauses are parent-signed",
            "result": "no physical local lambda_tr; no finite trace Yukawa alpha(lambda) row is populated",
            "status": "conditional_not_claimed",
            "what_it_buys": "kills this trace branch without tuning a tiny coupling",
            "remaining_debt": "other q_loc residual channels still required for local GR/Newton",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "ZRI892_1_if_finite_pole_survives",
            "condition": "P_tr has nonzero compact-local image and H_tr has a source-coupled reduced inverse",
            "result": "Z_tr, mu_tr^2, lambda_tr, Q_tr/m, metric response, and real bounds become mandatory",
            "status": "retained_nonclaim",
            "what_it_buys": "a disciplined finite-carrier branch rather than an ad hoc coupling",
            "remaining_debt": "source all coefficients before R10/PPN/clock/orbital scoring",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "ZRI892_2_R10",
            "condition": "R10 comparison requested",
            "result": "blocked until either no-pole is signed or finite MTS alpha(lambda) and external bound curve are valid",
            "status": "blocked",
            "what_it_buys": "prevents fake R10 pass from placeholder lambda/alpha rows",
            "remaining_debt": "real parent coefficients plus source-backed bound curve",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "ZRI892_3_PPN_local_GR",
            "condition": "local GR/Newton claim requested",
            "result": "blocked even if trace branch closes because coframe/projector/source-normalization channels remain separate",
            "status": "blocked",
            "what_it_buys": "keeps the scope honest",
            "remaining_debt": "full local residual vector and GR limit proof",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def blocker_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BL892_0_Ptr_parent_signature",
            "blocker": "P_tr is not yet parent-owned as a quotient projector or readout-only boundary direction",
            "why_it_blocks": "no rank-zero/no-pole theorem can be instantiated without a real projector",
            "next_action": "parent-sign P_tr or demote it to closure-only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL892_1_Htr_principal_symbol",
            "blocker": "Z_tr principal symbol is missing",
            "why_it_blocks": "finite branch cannot predict amplitude or stability",
            "next_action": "source sigma_2(H_tr) if no-pole route fails",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL892_2_Htr_mass_gap",
            "blocker": "mu_tr^2/m_tr/lambda_tr is missing",
            "why_it_blocks": "R10/orbital range is undefined",
            "next_action": "derive mass gap or prove no physical pole",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL892_3_source_cokernel",
            "blocker": "J_tr source-cokernel and matter no-marker descent remain unsigned",
            "why_it_blocks": "even with a pole, local force amplitudes require source charge",
            "next_action": "prove J_tr=0 or fill Q_tr/m and species rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL892_4_no_tail_support",
            "blocker": "boundary/no-tail route is conditional only",
            "why_it_blocks": "compact local leakage could still activate trace residuals",
            "next_action": "parent-lock no-tail/support to same q_loc domain",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL892_5_other_local_channels",
            "blocker": "trace closure is not the whole local GR proof",
            "why_it_blocks": "coframe, projector, source-normalization, clock/EM, and PPN branches still need closure or bounds",
            "next_action": "keep local GR gate blocked until the full residual vector is controlled",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG892_0_Ztr_numeric",
            "promotion_target": "numeric Z_tr",
            "required_to_pass": "parent H_tr principal symbol with units/sign/provenance",
            "current_evidence": "missing",
            "gate_result": "fail_for_claim",
            "next_action": "893 finite-symbol branch if no-pole cannot be signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG892_1_lambdatr_numeric",
            "promotion_target": "numeric lambda_tr",
            "required_to_pass": "mu_tr^2/Z_tr and physical local pole, or theorem that range is absent",
            "current_evidence": "missing_or_unphysical_pending_no_pole",
            "gate_result": "fail_for_claim",
            "next_action": "derive mass gap or no-pole",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG892_2_no_pole",
            "promotion_target": "no source-coupled local trace pole",
            "required_to_pass": "rank-zero/readout-only/constraint-null plus source-cokernel silence",
            "current_evidence": "conditional implication only",
            "gate_result": "fail_for_claim",
            "next_action": "parent-sign P_tr rank-zero or readout-only support",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG892_3_finite_branch",
            "promotion_target": "finite trace carrier source pack",
            "required_to_pass": "Z_tr, lambda_tr, Q_tr/m, metric/source response, real bounds",
            "current_evidence": "source rows only",
            "gate_result": "fail_for_claim",
            "next_action": "do not score until source pack is numeric and sourced",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG892_4_local_GR",
            "promotion_target": "local GR/Newton limit",
            "required_to_pass": "trace closure plus every other local residual/source-normalization branch",
            "current_evidence": "trace Hessian gate only",
            "gate_result": "fail_for_claim",
            "next_action": "no local-GR claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC892_0_selected",
            "route": "Ptr_rank_zero_parent_signature_or_Htr_principal_symbol_source_fill",
            "status": "selected",
            "reason": "the no-pole theorem is mathematically clean but unsigned; the next least-scrutiny route is to sign rank-zero/readout-only P_tr, otherwise fill finite H_tr principal and mass symbols",
            "include": "P_tr rank-zero/readout-only support, q_loc compact restriction, H_tr principal symbol, mass gap, source-cokernel fork",
            "exclude": "R10/PPN/local-GR claim, fitted tiny coupling, public prose, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG892_0_no_Ztr_claim",
            "forbidden_claim": "Z_tr is known",
            "status": "forbidden",
            "reason": "principal symbol is missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG892_1_no_lambda_claim",
            "forbidden_claim": "lambda_tr is known or physical",
            "status": "forbidden",
            "reason": "mass gap is missing and no-pole is not signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG892_2_no_no_pole_claim",
            "forbidden_claim": "H_tr has no source-coupled local pole",
            "status": "forbidden",
            "reason": "rank-zero/readout-only/constraint-null premises are conditional only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG892_3_no_R10_claim",
            "forbidden_claim": "R10/fifth-force branch passes",
            "status": "forbidden",
            "reason": "no valid MTS alpha(lambda) row and no valid theorem-zero certificate",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG892_4_no_local_GR_claim",
            "forbidden_claim": "MTS locally reduces to GR/Newton",
            "status": "forbidden",
            "reason": "trace Hessian is one unresolved branch and wider local residual stack remains open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG892_5_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "892 sharpens the exact fork between theorem-zero and finite trace carrier source fill",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D892_0",
            "finding": "trace_Hessian_source_rows_written",
            "reason": "H_tr, Z_tr, mu_tr^2, lambda_tr, sign, source-domain, units, and provenance are now separately gated",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D892_1",
            "finding": "no_pole_theorem_conditional",
            "reason": "rank-zero/readout-only/constraint-null plus source-cokernel silence would kill the local pole, but premises are not parent-signed",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D892_2",
            "finding": "next_fork_selected",
            "reason": "the next checkpoint must either parent-sign P_tr rank-zero/readout-only status or source H_tr principal/mass symbols",
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
            "objective": "either parent-sign the P_tr rank-zero/readout-only route so no local trace pole exists, or fill the finite H_tr principal-symbol/mass-gap source rows without claiming a pass",
            "include": "P_tr rank-zero support, q_loc compact domain, source-at-zero/readout clause, H_tr principal symbol, mu_tr^2/lambda_tr source fill",
            "exclude": "R10/local-GR pass, public claim, fitted coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_891_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_891_VALIDATION.csv"
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


def all_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if stringify(row.get("valid_for_claim", False)).lower() != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    trace_rows_: list[dict[str, object]],
    no_pole_rows_: list[dict[str, object]],
    hessian_gate_rows_: list[dict[str, object]],
    zero_impact_rows_: list[dict[str, object]],
    blocker_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    trace_ids = {row["row_id"] for row in trace_rows_}
    no_pole_verdict = next(row for row in no_pole_rows_ if row["theorem_id"] == "NPT892_4_verdict")
    formalization_count = formalization_changed_count()
    row_groups = [
        source_rows_,
        summary_rows_,
        trace_rows_,
        no_pole_rows_,
        hessian_gate_rows_,
        zero_impact_rows_,
        blocker_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V892_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows_) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V892_1_prior_891_clean",
            "result": "pass" if prior_891_clean() else "fail",
            "detail": "P8_Y5_BRR545_891_VALIDATION.csv clean",
        },
        {
            "check_id": "V892_2_trace_Hessian_rows_complete",
            "result": "pass"
            if {
                "THS892_0_Htr_definition",
                "THS892_1_Ztr_principal_symbol",
                "THS892_2_mutr_mass_term",
                "THS892_3_lambdatr_range",
                "THS892_4_sign_stability",
                "THS892_5_source_coupled_domain",
                "THS892_6_units_convention",
                "THS892_7_provenance",
            }.issubset(trace_ids)
            else "fail",
            "detail": "H_tr/Z_tr/mu_tr/lambda_tr/source-domain/provenance rows present",
        },
        {
            "check_id": "V892_3_Ztr_lambda_missing_block_claim",
            "result": "pass"
            if any(row["row_id"] == "THS892_1_Ztr_principal_symbol" and "MISSING" in row["current_status"] for row in trace_rows_)
            and any(row["row_id"] == "THS892_3_lambdatr_range" and "MISSING" in row["current_status"] for row in trace_rows_)
            else "fail",
            "detail": "Z_tr and lambda_tr remain missing/nonclaim",
        },
        {
            "check_id": "V892_4_no_pole_conditional_not_promoted",
            "result": "pass" if no_pole_verdict["proof_status"] == "conditional_not_parent_signed" else "fail",
            "detail": "no-pole theorem is conditional only",
        },
        {
            "check_id": "V892_5_hessian_input_gates_blocked",
            "result": "pass" if all(row["claim_allowed"] is False and row["gate_result"] == "fail_for_claim" for row in hessian_gate_rows_) else "fail",
            "detail": "all H_tr input gates fail for claim",
        },
        {
            "check_id": "V892_6_zero_route_not_promoted",
            "result": "pass" if any(row["status"] == "conditional_not_claimed" for row in zero_impact_rows_) else "fail",
            "detail": "zero route impact remains nonclaim",
        },
        {
            "check_id": "V892_7_blockers_present",
            "result": "pass" if len(blocker_rows_) >= 5 else "fail",
            "detail": "blocker ledger contains parent/Htr/source/local-GR blockers",
        },
        {
            "check_id": "V892_8_promotion_gates_blocked",
            "result": "pass" if all(row["gate_result"] == "fail_for_claim" for row in promotion_rows_) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V892_9_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V892_10_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V892_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V892_12_route_selected",
            "result": "pass" if route_rows_ and next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V892_13_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    return [{**row, "generated_utc": generated_utc} for row in checks]


def write_markdown(
    path: Path,
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    trace_rows_: list[dict[str, object]],
    no_pole_rows_: list[dict[str, object]],
    hessian_gate_rows_: list[dict[str, object]],
    zero_impact_rows_: list[dict[str, object]],
    blocker_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 892 - Y5/R10 Trace-Hessian Ztr Lambdatr Source Row or No-Pole Theorem",
        "",
        f"Status: `{STATUS}`",
        f"Claim ceiling: `{CLAIM_CEILING}`",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the trace-Hessian branch has been sharpened into an exact fork, but still no claim**. Either `P_tr` is parent-signed as rank-zero/readout-only/constraint-null so the local source-coupled pole never exists, or the finite branch must source `H_tr`, `Z_tr`, `mu_tr^2`, `lambda_tr`, source-cokernel, units, and provenance before any R10/PPN/local-GR scoring. The theorem implication is clean; its premises are not yet parent-signed.",
        "",
        "## Exact 892 Lemma",
        "Let `V_loc` be the compact-local quotient tangent image and `V_tr=Im(P_tr)` the trace direction. A source-coupled local pole of `H_tr=P_tr^dagger Hess(S_parent)P_tr` requires a nonzero physical vector in `V_loc` that also lies in the trace image and pairs nontrivially with `J_tr`. If `rank(P_loc P_tr P_loc^dagger)=0`, or if `P_tr` is only a post-variation readout/source-at-zero, or if the reduced trace sector is constraint-null, then no physical compact-local trace Green pole is present. This would make `lambda_tr` nonphysical locally. The current work cannot promote that result because the parent signatures for `P_tr`, `q_loc`, boundary support/no-tail, and source-cokernel silence are still missing.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows_),
        "",
        "## Source Register",
        md_table(source_rows_),
        "",
        "## Trace-Hessian Source Rows",
        md_table(trace_rows_),
        "",
        "## No-Pole Theorem Attempt",
        md_table(no_pole_rows_),
        "",
        "## Hessian Input Gates",
        md_table(hessian_gate_rows_),
        "",
        "## Zero-Route Impact",
        md_table(zero_impact_rows_),
        "",
        "## Blocker Ledger",
        md_table(blocker_rows_),
        "",
        "## Promotion Gates",
        md_table(promotion_rows_),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guards",
        md_table(claim_rows_),
        "",
        "## Decision",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    trace_rows_ = trace_hessian_source_rows(generated_utc)
    no_pole_rows_ = no_pole_theorem_rows(generated_utc)
    hessian_gate_rows_ = hessian_input_gate_rows(generated_utc)
    zero_impact_rows_ = zero_route_impact_rows(generated_utc)
    blocker_rows_ = blocker_ledger_rows(generated_utc)
    promotion_rows_ = promotion_gate_rows(generated_utc)
    route_rows_ = route_choice_rows(generated_utc)
    claim_rows_ = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        trace_rows_,
        no_pole_rows_,
        hessian_gate_rows_,
        zero_impact_rows_,
        blocker_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_892_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_892_TRACE_HESSIAN_SOURCE_ROWS.csv": trace_rows_,
        "P8_Y5_R10_892_NO_POLE_THEOREM_ATTEMPT.csv": no_pole_rows_,
        "P8_Y5_R10_892_HESSIAN_INPUT_GATE.csv": hessian_gate_rows_,
        "P8_Y5_R10_892_ZERO_ROUTE_IMPACT.csv": zero_impact_rows_,
        "P8_Y5_R10_892_BLOCKER_LEDGER.csv": blocker_rows_,
        "P8_Y5_R10_892_PROMOTION_GATE.csv": promotion_rows_,
        "P8_Y5_R10_892_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_892_CLAIM_GUARD.csv": claim_rows_,
        "P8_Y5_R10_892_DECISION.csv": decision_rows_,
        "P8_Y5_R10_892_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_R10_892_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_BRR545_892_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "892-Y5-R10-trace-Hessian-Ztr-lambdatr-source-row-or-no-pole-theorem.md"
    write_markdown(
        doc_path,
        generated_utc,
        source_rows_,
        summary_rows_,
        trace_rows_,
        no_pole_rows_,
        hessian_gate_rows_,
        zero_impact_rows_,
        blocker_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_892_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

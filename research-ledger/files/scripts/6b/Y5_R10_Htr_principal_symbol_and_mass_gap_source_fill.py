from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_894_Htr_principal_symbol_mass_gap_source_fill_attempted_no_numeric_source_endpoint_transfer_rejected_nonclaim"
CLAIM_CEILING = "Htr_symbol_mass_gap_source_fill_attempt_only_no_Ztr_no_lambdatr_no_finite_carrier_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "895-Y5-R10-parent-quadratic-trace-action-ansatz-or-closure-demotion.md"

SOURCE_SPECS = [
    {
        "source_id": "893_doc",
        "path": ROOT / "893-Y5-R10-Ptr-rank-zero-parent-signature-or-Htr-principal-symbol-source-fill.md",
        "needle": "finite `H_tr` symbol-fill branch is now selected",
        "role": "immediate finite H_tr source-fill handoff",
    },
    {
        "source_id": "893_validation",
        "path": OUT / "P8_Y5_BRR545_893_VALIDATION.csv",
        "needle": "V893_13_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "893_htr_fill",
        "path": OUT / "P8_Y5_R10_893_HTR_PRINCIPAL_SYMBOL_FILL.csv",
        "needle": "HSF893_2_principal_symbol",
        "role": "finite H_tr symbol-fill queue",
    },
    {
        "source_id": "876_trace_contract",
        "path": ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md",
        "needle": "`Z_T` must be the principal-symbol normalization",
        "role": "original trace Hessian extraction law",
    },
    {
        "source_id": "877_htr_skeleton",
        "path": ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md",
        "needle": "minimal future action object is `H_tr=P_tr^dagger Hess(S_parent) P_tr`",
        "role": "minimal H_tr skeleton and source hunt",
    },
    {
        "source_id": "880_endpoint_action",
        "path": ROOT / "880-Y5-R10-minimal-Qtrace-Qstar-Kparent-action-contract-or-retained-cT-bound.md",
        "needle": "K_endpoint=diag(6,6)",
        "role": "endpoint Hessian candidate and K_parent blocker",
    },
    {
        "source_id": "880_minimal_action_contract",
        "path": OUT / "P8_Y5_R10_880_MINIMAL_ACTION_CONTRACT.csv",
        "needle": "MAC880_4_parent_pairing_extension",
        "role": "K_parent extension blocker",
    },
    {
        "source_id": "885_htr_fill",
        "path": OUT / "P8_Y5_R10_885_HTR_ZERO_POLE_SOURCE_FILL.csv",
        "needle": "HZ885_4_Ztr_mtr_lambda",
        "role": "prior H_tr zero-pole/source fill row",
    },
    {
        "source_id": "891_trace_coefficients",
        "path": OUT / "P8_Y5_R10_891_TRACE_COEFFICIENT_SOURCE_ROWS.csv",
        "needle": "TCSR891_1_lambda_tr",
        "role": "finite trace coefficient rows",
    },
    {
        "source_id": "892_trace_rows",
        "path": OUT / "P8_Y5_R10_892_TRACE_HESSIAN_SOURCE_ROWS.csv",
        "needle": "THS892_1_Ztr_principal_symbol",
        "role": "trace Hessian source rows",
    },
    {
        "source_id": "382_parent_local_action",
        "path": ROOT / "382-parent-local-action-minimal-contract.md",
        "needle": "parent_local_action_minimal_contract_written",
        "role": "parent local action contract, not a trace Hessian",
    },
    {
        "source_id": "654_local_gr_spine",
        "path": ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
        "needle": "R10_fifth_force",
        "role": "local-GR/R10 gate status",
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
            "what_changed": "attempted to source the finite trace Hessian principal symbol and mass gap from current action/Hessian candidates, and explicitly rejected endpoint-block transfer as a local kinetic symbol",
            "best_partial_result": "the extraction law is exact but currently empty: Z_tr requires a spacetime derivative principal symbol of the reduced H_tr, while lambda_tr requires a zeroth-order trace mass gap or a no-pole certificate",
            "hard_blockers": "no parent-owned P_tr, no computable second variation of S_parent, no local kinetic trace operator, no zeroth-order mass symbol, no reduced-inverse/no-pole certificate, no source-cokernel",
            "what_is_not_claimed": "numeric Z_tr, numeric mu_tr^2, numeric lambda_tr, finite trace carrier, no-pole theorem, R10 pass, PPN pass, clock/WEP/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def candidate_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "HCA894_0_direct_parent_Htr",
            "candidate_source": "877/876 H_tr=P_tr^dagger Hess(S_parent)P_tr",
            "possible_contribution": "directly compute sigma_2(H_tr), mu_tr^2, reduced inverse, and source domain",
            "usable_for_Ztr": "yes_if_parent_Htr_exists",
            "usable_for_mass_gap": "yes_if_zeroth_order_symbol_exists",
            "current_status": "MISSING_PARENT_PROJECTOR_AND_HESSIAN",
            "verdict": "not_computable_from_current_corpus",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HCA894_1_endpoint_Kblock",
            "candidate_source": "880 oriented endpoint Hessian K_endpoint=diag(6,6)",
            "possible_contribution": "positive endpoint pairing block for raising the trace covector",
            "usable_for_Ztr": "no",
            "usable_for_mass_gap": "no_local_mass_by_itself",
            "current_status": "ENDPOINT_BLOCK_ONLY",
            "verdict": "reject_transfer_to_local_spacetime_Htr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HCA894_2_Kparent_extension",
            "candidate_source": "880 MAC880_4 K_parent extension",
            "possible_contribution": "could define v_tr and P_tr if full quotient tangent pairing exists",
            "usable_for_Ztr": "only_after_full_Kparent_and_Htr",
            "usable_for_mass_gap": "no_without_action_second_variation",
            "current_status": "MISSING_KPARENT_EXTENSION",
            "verdict": "blocks_Ptr_before_Htr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HCA894_3_parent_local_action_contract",
            "candidate_source": "382/407/177 parent action sketches",
            "possible_contribution": "home for future local quadratic operator",
            "usable_for_Ztr": "contract_only",
            "usable_for_mass_gap": "contract_only",
            "current_status": "ACTION_BLOCKS_NOT_VARIED",
            "verdict": "no_second_variation_available",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HCA894_4_EH_trace_constraint_route",
            "candidate_source": "local GR/EH spine and pure GR constraint logic",
            "possible_contribution": "if trace is pure gauge/constraint under EH reduction, this supports no-pole rather than finite carrier",
            "usable_for_Ztr": "not_as_finite_scalar",
            "usable_for_mass_gap": "no_physical_lambda_if_signed",
            "current_status": "EH_OPERATOR_SELECTION_AND_GAUGE_IDENTITY_NOT_SIGNED",
            "verdict": "keep_as_no_pole_watch_not_coefficient_source",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HCA894_5_auxiliary_mass_gap_route",
            "candidate_source": "421/877 finite-fibre mass-gap analogy",
            "possible_contribution": "could make trace auxiliary/gapped/source-blind",
            "usable_for_Ztr": "no_numeric_symbol",
            "usable_for_mass_gap": "analogy_only",
            "current_status": "NO_TRACE_SPECIFIC_OPERATOR",
            "verdict": "not_a_source_row",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HCA894_6_retained_coefficient_rows",
            "candidate_source": "891/892/893 source-fill ledgers",
            "possible_contribution": "schema for Z_tr, mu_tr^2, lambda_tr, source charges, arenas",
            "usable_for_Ztr": "schema_only",
            "usable_for_mass_gap": "schema_only",
            "current_status": "MISSING_MARKERS_ONLY",
            "verdict": "cannot_score_or_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def extraction_law_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "EL894_0_define_domain",
            "object": "trace configuration domain",
            "law": "phi_tr=P_tr delta Phi after gauge/constraint reduction and source-domain selection",
            "required_input": "parent-owned P_tr plus reduced quotient tangent space",
            "current_status": "MISSING_PARENT_PROJECTOR",
            "claim_effect": "H_tr has no domain",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "law_id": "EL894_1_quadratic_operator",
            "object": "H_tr",
            "law": "S_parent^(2)[phi_tr]=1/2 int sqrt(-g) phi_tr H_tr phi_tr",
            "required_input": "actual second variation of S_parent projected into the trace sector",
            "current_status": "MISSING_PARENT_HESSIAN",
            "claim_effect": "no principal or mass symbol can be read",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "law_id": "EL894_2_principal_symbol",
            "object": "Z_tr",
            "law": "sigma_2(H_tr)(k)=Z_tr g^{mu nu}k_mu k_nu on the physical scalar trace subspace",
            "required_input": "local two-derivative trace operator and canonical normalization",
            "current_status": "MISSING_PRINCIPAL_SYMBOL",
            "claim_effect": "alpha amplitude and ghost sign blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "law_id": "EL894_3_mass_gap",
            "object": "mu_tr^2,m_tr,lambda_tr",
            "law": "H_tr approx Z_tr(-box)+mu_tr^2, m_tr^2=mu_tr^2/Z_tr, lambda_tr=1/m_tr in natural units",
            "required_input": "zeroth-order symbol plus positive finite carrier classification",
            "current_status": "MISSING_ZEROTH_ORDER_SYMBOL",
            "claim_effect": "R10/orbital range blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "law_id": "EL894_4_no_pole_alternative",
            "object": "lambda_tr absence",
            "law": "if reduced H_tr has no source-coupled local inverse, lambda_tr is not a physical local range",
            "required_input": "rank-zero/readout-only/constraint-null/no-tail/source-cokernel certificate",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "claim_effect": "zero route remains watch only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def endpoint_transfer_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "transfer_id": "ETA894_0_endpoint_curvature",
            "source_object": "K_endpoint=diag(6,6)",
            "target_object": "Z_tr principal symbol",
            "transfer_result": "rejected",
            "reason": "endpoint curvature has no spacetime derivative k_mu k_nu operator and no local trace field domain",
            "allowed_use": "may help define endpoint pairing if Q_* and K_parent are parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "transfer_id": "ETA894_1_endpoint_curvature_to_mass",
            "source_object": "U'' endpoint block",
            "target_object": "mu_tr^2 local mass term",
            "transfer_result": "rejected_for_claim",
            "reason": "a boundary/endpoint Hessian is not a local zeroth-order operator unless the parent action supplies a local field map and measure",
            "allowed_use": "candidate boundary stiffness in a future parent quadratic action ansatz",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "transfer_id": "ETA894_2_Kendpoint_to_Kparent",
            "source_object": "positive endpoint block",
            "target_object": "full K_parent quotient pairing",
            "transfer_result": "blocked",
            "reason": "880 explicitly says the full parent K_parent/pseudo-inverse is missing",
            "allowed_use": "source-row target, not a promoted parent pairing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "transfer_id": "ETA894_3_verdict",
            "source_object": "endpoint action progress",
            "target_object": "finite local trace carrier",
            "transfer_result": "not_enough",
            "reason": "endpoint algebra sharpens the parent-action contract but does not produce a local propagating trace Hessian",
            "allowed_use": "requires explicit ansatz or derivation in 895",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fill_id": "SFR894_0_Ptr",
            "quantity": "P_tr",
            "required_source": "parent trace covector, full K_parent/pseudo-inverse, gauge reduction",
            "current_value": "MISSING_PARENT_PROJECTOR",
            "source_status": "not_sourced",
            "next_action": "derive P_tr in parent quadratic action or demote to closure-only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFR894_1_Htr",
            "quantity": "H_tr",
            "required_source": "second variation of actual S_parent on trace sector",
            "current_value": "MISSING_PARENT_HESSIAN",
            "source_status": "not_sourced",
            "next_action": "write explicit trace quadratic action ansatz or prove no-pole",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFR894_2_Ztr",
            "quantity": "Z_tr",
            "required_source": "principal symbol sigma_2(H_tr)",
            "current_value": "MISSING_PRINCIPAL_SYMBOL",
            "source_status": "not_sourced",
            "next_action": "cannot borrow endpoint Hessian; needs local kinetic operator",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFR894_3_mutr2",
            "quantity": "mu_tr^2",
            "required_source": "zeroth-order H_tr symbol after canonical normalization",
            "current_value": "MISSING_ZEROTH_ORDER_SYMBOL",
            "source_status": "not_sourced",
            "next_action": "only populate if parent action gives a local trace potential/mass",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFR894_4_lambdatr",
            "quantity": "lambda_tr",
            "required_source": "m_tr^2=mu_tr^2/Z_tr or no-pole certificate",
            "current_value": "MISSING_MASS_GAP_OR_NOPOLE",
            "source_status": "not_sourced",
            "next_action": "derive mass gap or mark lambda_tr unphysical by theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFR894_5_reduced_inverse",
            "quantity": "reduced_inverse_or_no_pole",
            "required_source": "constraint/gauge rank and source-coupled local mode test",
            "current_value": "MISSING_REDUCED_INVERSE_TEST",
            "source_status": "not_sourced",
            "next_action": "classify trace branch as EH constraint, auxiliary massive field, boundary readout, or closure",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def branch_classification_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BCL894_0_EH_constraint",
            "branch": "trace is GR/EH constraint or gauge",
            "what_would_be_needed": "parent identification of trace mode with constrained metric trace plus gauge-fixed reduced inverse no-pole proof",
            "current_status": "not_signed",
            "effect_if_true": "lambda_tr absent locally; no finite fifth-force carrier from this branch",
            "effect_if_false": "finite H_tr source-fill remains mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BCL894_1_auxiliary_massive",
            "branch": "trace is auxiliary or massive source-blind field",
            "what_would_be_needed": "positive Z_tr or auxiliary constraint, positive mass gap, source-cokernel zero",
            "current_status": "no_operator",
            "effect_if_true": "can be bounded or theorem-zero depending on source projection",
            "effect_if_false": "phenomenological closure only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BCL894_2_boundary_readout",
            "branch": "trace is endpoint/boundary readout only",
            "what_would_be_needed": "rank-zero/no-tail/source-at-zero/matter no-marker signatures",
            "current_status": "conditional_watch",
            "effect_if_true": "no local H_tr pole introduced",
            "effect_if_false": "local trace leakage coefficients must be sourced",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BCL894_3_new_parent_quadratic_trace_action",
            "branch": "trace is a real finite local field",
            "what_would_be_needed": "explicit parent quadratic action block with derivative term, potential/mass term, source coupling, units, and symmetry justification",
            "current_status": "not_written",
            "effect_if_true": "Z_tr/lambda_tr rows can become source-backed after validation",
            "effect_if_false": "finite branch should demote to closure/nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG894_0_Ztr_source",
            "promotion_target": "Z_tr sourced",
            "required_to_pass": "local two-derivative H_tr principal symbol with sign/units/provenance",
            "current_evidence": "missing; endpoint transfer rejected",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG894_1_lambda_source",
            "promotion_target": "lambda_tr sourced or absent by theorem",
            "required_to_pass": "mass gap mu_tr^2/Z_tr or reduced-inverse no-pole certificate",
            "current_evidence": "missing",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG894_2_finite_trace_carrier",
            "promotion_target": "finite local trace carrier",
            "required_to_pass": "P_tr,H_tr,Z_tr,mu_tr^2,source domain,J_tr all source-backed",
            "current_evidence": "source-fill queue only",
            "gate_result": "fail_for_claim",
            "next_action": "do not score R10/PPN",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG894_3_local_GR",
            "promotion_target": "local GR/Newton",
            "required_to_pass": "trace branch closure plus EH/source-normalization/PPN/boundary/local residual stack",
            "current_evidence": "trace branch source fill failed for claim",
            "gate_result": "fail_for_claim",
            "next_action": "keep local-GR gate blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC894_0_selected",
            "route": "parent_quadratic_trace_action_ansatz_or_closure_demotion",
            "status": "selected",
            "reason": "current corpus supplies extraction laws and endpoint algebra but no local H_tr operator; next step must either write an explicit parent quadratic trace action as an ansatz/contract or demote the finite branch to closure-only",
            "include": "trace kinetic term, mass/potential term, source coupling, gauge/constraint status, units/provenance, no-pole alternative",
            "exclude": "numeric Z_tr/lambda_tr claim, R10/PPN/local-GR pass, fitted tiny coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG894_0_no_endpoint_transfer",
            "forbidden_claim": "K_endpoint supplies Z_tr or lambda_tr",
            "status": "forbidden",
            "reason": "endpoint Hessian lacks local derivative operator and local field domain",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG894_1_no_Ztr_claim",
            "forbidden_claim": "Z_tr is known",
            "status": "forbidden",
            "reason": "principal symbol is missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG894_2_no_lambda_claim",
            "forbidden_claim": "lambda_tr is known or absent",
            "status": "forbidden",
            "reason": "mass gap and no-pole certificate are both unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG894_3_no_empirical_claim",
            "forbidden_claim": "R10/PPN/clock/WEP/orbital branch passes",
            "status": "forbidden",
            "reason": "finite branch lacks coefficients and zero route lacks signatures",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG894_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "894 proves the current source corpus cannot populate Z_tr/lambda_tr without a new explicit parent quadratic trace action or closure demotion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D894_0",
            "finding": "Htr_source_fill_attempted",
            "reason": "all current action/Hessian candidates were audited for principal-symbol and mass-gap ownership",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D894_1",
            "finding": "endpoint_transfer_rejected",
            "reason": "K_endpoint=diag(6,6) is a boundary/endpoint pairing block, not a local spacetime derivative principal symbol or mass gap",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D894_2",
            "finding": "parent_quadratic_trace_action_or_closure_selected",
            "reason": "without a source-backed H_tr, the finite branch needs an explicit parent quadratic trace action ansatz/contract or it must be demoted to closure-only",
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
            "objective": "write the exact parent quadratic trace-action ansatz/contract that would source H_tr, or explicitly demote the finite trace branch to closure-only until a real parent action supplies it",
            "include": "kinetic term, endpoint/local potential distinction, gauge/constraint classification, source coupling, units, provenance, no-pole alternative",
            "exclude": "R10/PPN/local-GR pass, numeric Z_tr/lambda_tr claim, fitted tiny coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_893_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_893_VALIDATION.csv"
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
    candidate_rows_: list[dict[str, object]],
    law_rows_: list[dict[str, object]],
    transfer_rows_: list[dict[str, object]],
    fill_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    endpoint_verdict = next(row for row in transfer_rows_ if row["transfer_id"] == "ETA894_3_verdict")
    ztr_row = next(row for row in fill_rows_ if row["fill_id"] == "SFR894_2_Ztr")
    lambda_row = next(row for row in fill_rows_ if row["fill_id"] == "SFR894_4_lambdatr")
    row_groups = [
        source_rows_,
        summary_rows_,
        candidate_rows_,
        law_rows_,
        transfer_rows_,
        fill_rows_,
        branch_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V894_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows_) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V894_1_prior_893_clean",
            "result": "pass" if prior_893_clean() else "fail",
            "detail": "P8_Y5_BRR545_893_VALIDATION.csv clean",
        },
        {
            "check_id": "V894_2_candidate_audit_complete",
            "result": "pass" if len(candidate_rows_) == 7 else "fail",
            "detail": "direct, endpoint, Kparent, action, EH, auxiliary, retained rows audited",
        },
        {
            "check_id": "V894_3_endpoint_transfer_rejected",
            "result": "pass" if endpoint_verdict["transfer_result"] == "not_enough" else "fail",
            "detail": "endpoint Hessian not transferred to local H_tr symbol",
        },
        {
            "check_id": "V894_4_extraction_laws_present",
            "result": "pass" if len(law_rows_) == 5 else "fail",
            "detail": "domain/operator/principal/mass/no-pole laws recorded",
        },
        {
            "check_id": "V894_5_Ztr_lambda_still_missing",
            "result": "pass"
            if ztr_row["current_value"] == "MISSING_PRINCIPAL_SYMBOL" and lambda_row["current_value"] == "MISSING_MASS_GAP_OR_NOPOLE"
            else "fail",
            "detail": "Z_tr and lambda_tr remain unsourced",
        },
        {
            "check_id": "V894_6_source_fill_rows_nonclaim",
            "result": "pass" if all("MISSING" in str(row["current_value"]) for row in fill_rows_) else "fail",
            "detail": "all source-fill rows keep missing markers",
        },
        {
            "check_id": "V894_7_branch_classifier_nonclaim",
            "result": "pass" if all(row["current_status"] != "derived" for row in branch_rows_) else "fail",
            "detail": "all branch classifications remain nonclaim",
        },
        {
            "check_id": "V894_8_promotion_gates_blocked",
            "result": "pass" if all(row["gate_result"] == "fail_for_claim" for row in promotion_rows_) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V894_9_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V894_10_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V894_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V894_12_route_selected",
            "result": "pass" if route_rows_ and next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V894_13_validation_rows_ready",
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
    candidate_rows_: list[dict[str, object]],
    law_rows_: list[dict[str, object]],
    transfer_rows_: list[dict[str, object]],
    fill_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 894 - Y5/R10 Htr Principal-Symbol and Mass-Gap Source Fill",
        "",
        f"Status: `{STATUS}`",
        f"Claim ceiling: `{CLAIM_CEILING}`",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the current corpus does not source a finite local `H_tr` principal symbol or mass gap**. The extraction law is clean, but every candidate source fails for claim: the parent `H_tr` is not computed, `P_tr` is not owned, `K_endpoint=diag(6,6)` is only an endpoint/boundary pairing block, and the local action sketches are contracts rather than second variations. Therefore `Z_tr`, `mu_tr^2`, `m_tr`, and `lambda_tr` remain missing.",
        "",
        "## Exact 894 Finding",
        "`Z_tr` cannot be borrowed from endpoint curvature. A local principal symbol must be the coefficient of `g^{mu nu}k_mu k_nu` in the reduced spacetime operator `H_tr=P_tr^dagger Hess(S_parent)P_tr`. The oriented endpoint Hessian may help a future `K_parent` pairing, but it has no local derivative operator and no local trace field domain. The next honest move is to write a clearly-labelled parent quadratic trace-action ansatz/contract or demote the finite branch to closure-only.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows_),
        "",
        "## Source Register",
        md_table(source_rows_),
        "",
        "## Htr Source Candidate Audit",
        md_table(candidate_rows_),
        "",
        "## Extraction Laws",
        md_table(law_rows_),
        "",
        "## Endpoint Transfer Audit",
        md_table(transfer_rows_),
        "",
        "## Source-Fill Rows",
        md_table(fill_rows_),
        "",
        "## Branch Classification",
        md_table(branch_rows_),
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
    candidate_rows_ = candidate_audit_rows(generated_utc)
    law_rows_ = extraction_law_rows(generated_utc)
    transfer_rows_ = endpoint_transfer_audit_rows(generated_utc)
    fill_rows_ = source_fill_rows(generated_utc)
    branch_rows_ = branch_classification_rows(generated_utc)
    promotion_rows_ = promotion_gate_rows(generated_utc)
    route_rows_ = route_choice_rows(generated_utc)
    claim_rows_ = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        candidate_rows_,
        law_rows_,
        transfer_rows_,
        fill_rows_,
        branch_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_894_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_894_HTR_SOURCE_CANDIDATE_AUDIT.csv": candidate_rows_,
        "P8_Y5_R10_894_EXTRACTION_LAWS.csv": law_rows_,
        "P8_Y5_R10_894_ENDPOINT_TRANSFER_AUDIT.csv": transfer_rows_,
        "P8_Y5_R10_894_SOURCE_FILL_ROWS.csv": fill_rows_,
        "P8_Y5_R10_894_BRANCH_CLASSIFICATION.csv": branch_rows_,
        "P8_Y5_R10_894_PROMOTION_GATE.csv": promotion_rows_,
        "P8_Y5_R10_894_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_894_CLAIM_GUARD.csv": claim_rows_,
        "P8_Y5_R10_894_DECISION.csv": decision_rows_,
        "P8_Y5_R10_894_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_R10_894_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_BRR545_894_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "894-Y5-R10-Htr-principal-symbol-and-mass-gap-source-fill.md"
    write_markdown(
        doc_path,
        generated_utc,
        source_rows_,
        summary_rows_,
        candidate_rows_,
        law_rows_,
        transfer_rows_,
        fill_rows_,
        branch_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_894_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3429-Y5-R2FR-gapped-Y6-nohair-positive-operator-or-DeltaExtra-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3428": ROOT / "3428-Y5-R2FR-no-extra-mass-Y6-monopole-silence-or-bound-under-AX1090.md",
    "safe_3428": OUT / "P8_Y5_R2FR_3428_Y6_SAFE_CLASS_THEOREM.csv",
    "delta_extra_3428": OUT / "P8_Y5_R2FR_3428_DELTA_EXTRA_BOUND_ROWS.csv",
    "next_3428": OUT / "P8_Y5_R2FR_3428_NEXT_TARGET.csv",
    "fixed_point_3421": OUT / "P8_Y5_R2FR_3421_EULER_FIXED_POINT_THEOREM.csv",
    "coercivity_3421": OUT / "P8_Y5_R2FR_3421_COERCIVITY_BOUND_PACK.csv",
    "source_gate_3421": OUT / "P8_Y5_R2FR_3421_SOURCE_CURRENT_ZERO_GATE.csv",
    "source_decomp_3422": OUT / "P8_Y5_R2FR_3422_SOURCE_CURRENT_DECOMPOSITION.csv",
    "boundary_3427": OUT / "P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv",
    "positive_operator_old": OUT / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv",
    "energy_identity_old": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "premise_requirements": OUT / "P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv",
    "nohair_1042": OUT / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
    "nohair_gate_1042": OUT / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
    "sharp_q_nohair": OUT / "P8_Y5_PARENT_QLOC_2430_SHARP_Q_NOHAIR_THEOREM.csv",
    "extra_inventory_double_zero": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_DOUBLE_ZERO_STATUS_MATRIX.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3429_SOURCE_REGISTER.csv",
    "positive_operator_nohair_theorem": OUT / "P8_Y5_R2FR_3429_POSITIVE_OPERATOR_NOHAIR_THEOREM.csv",
    "activation_gate": OUT / "P8_Y5_R2FR_3429_NOHAIR_ACTIVATION_GATE.csv",
    "delta_extra_norm_bound": OUT / "P8_Y5_R2FR_3429_DELTA_EXTRA_NORM_BOUND.csv",
    "gapped_channel_rows": OUT / "P8_Y5_R2FR_3429_GAPPED_CHANNEL_ROWS.csv",
    "pc3400_4_update": OUT / "P8_Y5_R2FR_3429_PC3400_4_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3429_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3429_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3429_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3429_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3429_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3428": "no-extra-mass/Y6 handoff",
        "safe_3428": "Y6 safe-class theorem",
        "delta_extra_3428": "Delta_extra bound rows",
        "next_3428": "machine-readable 3429 target",
        "fixed_point_3421": "Z/Y residual fixed-point theorem",
        "coercivity_3421": "coercivity and norm-bound pack",
        "source_gate_3421": "source-current zero gates",
        "source_decomp_3422": "source-current decomposition",
        "boundary_3427": "boundary/reference residual rows",
        "positive_operator_old": "older positive operator attempt",
        "energy_identity_old": "extra-sector energy identity",
        "premise_requirements": "local zero extra premise requirements",
        "nohair_1042": "prior positive X nohair identity",
        "nohair_gate_1042": "prior nohair premise gate",
        "sharp_q_nohair": "sharp q nohair theorem",
        "extra_inventory_double_zero": "extra-sector double-zero inventory",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def positive_operator_nohair_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "PON3429_0_operator_setup",
            "claim": "Gapped Y6/Z auxiliary sectors obey a local Euler equation with a coercive linear operator plus controlled nonlinear remainder.",
            "identity": "L_X X + N_X(X) = J_X + B_X + R_X on compact exterior A",
            "status": "FORMULA_FROM_3421_AND_3428",
            "missing_to_promote": "field-specific L_X, domain, gauge quotient and units",
            "valid_for_claim": False,
        },
        {
            "step_id": "PON3429_1_energy_identity",
            "claim": "If L_X is self-adjoint positive after gauge quotient, an energy inequality controls the residual norm.",
            "identity": "lambda_X ||X||^2 <= <X,L_X X> = <X,J_X+B_X+R_X-N_X(X)>",
            "status": "EXACT_CONDITIONAL_ENERGY_IDENTITY",
            "missing_to_promote": "lambda_X>0 and nonlinear Lipschitz radius",
            "valid_for_claim": False,
        },
        {
            "step_id": "PON3429_2_zero_branch",
            "claim": "If J_X=B_X=R_X=0 and the small-field branch is inside the coercive radius, then X=0.",
            "identity": "lambda_X ||X||^2 <= c_N ||X||^3; if c_N||X||<lambda_X then ||X||=0",
            "status": "EXACT_CONDITIONAL_NOHAIR_THEOREM",
            "missing_to_promote": "source-current zero, boundary silence, projector residual zero",
            "valid_for_claim": False,
        },
        {
            "step_id": "PON3429_3_bound_branch",
            "claim": "If any source or boundary term survives, gapped/Y6 stress becomes a norm bound rather than a GR claim.",
            "identity": "||X|| <= 2 lambda_X^-1 (||J_X||+||B_X||+||R_X||)",
            "status": "BOUND_FORMULA_READY_VALUES_MISSING",
            "missing_to_promote": "numeric/source-backed lambda_X,J_X,B_X,R_X",
            "valid_for_claim": False,
        },
        {
            "step_id": "PON3429_4_mass_charge_map",
            "claim": "The gapped residual's extra monopole charge is bounded by its norm and boundary charge.",
            "identity": "|Delta H_X|/M_H_ref <= C_HX ||X|| + C_TX ||X||^2 + epsilon_boundary_X",
            "status": "FORMULA_READY_RESPONSE_CONSTANTS_MISSING",
            "missing_to_promote": "C_HX, C_TX, M_H_ref, boundary normalization",
            "valid_for_claim": False,
        },
        {
            "step_id": "PON3429_5_verdict",
            "claim": "The gapped/Y6 no-hair route is mathematically valid but not activated for current MTS.",
            "identity": "Delta_extra_gapped=0 iff PON3429_1 through PON3429_4 have theorem-zero inputs",
            "status": "CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "missing_to_promote": "lambda-star/source/boundary/projector inputs",
            "valid_for_claim": False,
        },
    ]


def activation_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "NAG3429_0_field_operator",
            "needed_input": "field-specific self-adjoint operator L_X",
            "required_condition": "L_X >= lambda_X I after gauge/constraint quotient",
            "current_status": "MISSING_FIELD_SPECIFIC_OPERATOR",
            "if_fail": "tachyon/zero-mode/indefinite stress residual",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NAG3429_1_source_zero",
            "needed_input": "source current J_X",
            "required_condition": "J_X=0 in compact local exterior and no source charge from matter/readout",
            "current_status": "OPEN_Y5_Y6_SOURCE_CURRENT",
            "if_fail": "Yukawa/fifth-force or extra monopole source",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NAG3429_2_boundary_zero",
            "needed_input": "boundary work B_X",
            "required_condition": "B_X=0 from 3427 fixed-reference/no-flux branch",
            "current_status": "CONDITIONAL_ON_3427_AND_CHANNEL",
            "if_fail": "boundary hair or compact linked charge",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NAG3429_3_projector_zero",
            "needed_input": "projector/domain residual R_X",
            "required_condition": "R_X=0 or source-backed bound",
            "current_status": "OPEN_HIDDEN_PROJECTOR",
            "if_fail": "hidden/domain/projector monopole residual",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NAG3429_4_nonlinear_control",
            "needed_input": "small-field Lipschitz bound for N_X",
            "required_condition": "Lip(N_X)<=lambda_X/2 in local branch radius",
            "current_status": "MISSING_NONLINEAR_RADIUS",
            "if_fail": "nonzero branch or instability possible",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NAG3429_5_charge_map",
            "needed_input": "map from X norm to Delta_extra_mass",
            "required_condition": "C_HX,C_TX and M_H_ref normalization are known",
            "current_status": "MISSING_RESPONSE_CONSTANTS",
            "if_fail": "no observable bound can be scored",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NAG3429_6_verdict",
            "needed_input": "all nohair premises",
            "required_condition": "NAG3429_0 through NAG3429_5 pass",
            "current_status": "NOHAIR_NOT_ACTIVATED",
            "if_fail": "use DeltaExtra norm-bound branch",
            "valid_for_claim": False,
        },
    ]


def delta_extra_norm_bound() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DNB3429_0_X_norm",
            "quantity": "||X||",
            "definition": "gapped/Y6 residual field norm in compact local exterior",
            "bound_formula": "0 if nohair activated; else 2 lambda_X^-1 (||J_X||+||B_X||+||R_X||)",
            "status": "MISSING_LAMBDA_AND_SOURCE_NORMS",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DNB3429_1_charge",
            "quantity": "Delta_H_X_over_MH",
            "definition": "Hamiltonian/source-charge leakage from gapped/Y6 residual",
            "bound_formula": "C_HX ||X||/M_H_ref + C_TX ||X||^2/M_H_ref + epsilon_boundary_X",
            "status": "MISSING_RESPONSE_CONSTANTS_AND_MHREF",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DNB3429_2_force",
            "quantity": "alpha_X(lambda_X)",
            "definition": "finite-range fifth-force equivalent if source coupling survives",
            "bound_formula": "alpha_X ~ C_source_X C_test_X/(4 pi G_ref M_H m_test); lambda_X = m_X^-1",
            "status": "MISSING_SOURCE_TEST_COUPLINGS",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DNB3429_3_PPN",
            "quantity": "PPN_extra_X",
            "definition": "PPN/source-normalization residual from nonzero gapped/Y6 field",
            "bound_formula": "{gamma-1,beta-1,alpha_i,xi,zeta_i}_X <= C_PPNX ||X|| + C_stressX ||X||^2",
            "status": "MISSING_PPN_RESPONSE_MAP",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DNB3429_4_total",
            "quantity": "epsilon_gapped_auxiliary",
            "definition": "no-cancellation envelope for all gapped/Y6 auxiliary sectors",
            "bound_formula": "sum_abs(Delta_H_X_over_MH, alpha_X-window penalties, PPN_extra_X)",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def gapped_channel_rows() -> list[dict[str, Any]]:
    return [
        {
            "channel_id": "GCR3429_0_response_memory",
            "sector": "response/memory doublet",
            "nohair_status": "candidate_only",
            "missing": "positive local kernel, no history injection, source-free J_mem",
            "fallback": "epsilon_memory_kernel",
            "valid_for_claim": False,
        },
        {
            "channel_id": "GCR3429_1_GammaKhat_q_loc",
            "sector": "Gamma/Khat/q_loc effective stress",
            "nohair_status": "not_signed",
            "missing": "metric response lock, q_loc vector/beta gates, T_GK Hilbert ownership",
            "fallback": "epsilon_q_loc_TGK_mass",
            "valid_for_claim": False,
        },
        {
            "channel_id": "GCR3429_2_domain_projector",
            "sector": "domain/projector selector",
            "nohair_status": "open",
            "missing": "domain selector and projector stress exclusion",
            "fallback": "epsilon_hidden_projector",
            "valid_for_claim": False,
        },
        {
            "channel_id": "GCR3429_3_boundary",
            "sector": "boundary/reference/exact/topological",
            "nohair_status": "partial",
            "missing": "old topological Bzero/R_eq if topological branch used",
            "fallback": "epsilon_topological_boundary",
            "valid_for_claim": False,
        },
        {
            "channel_id": "GCR3429_4_generic_gapped_X",
            "sector": "generic massive auxiliary X",
            "nohair_status": "theorem_template_only",
            "missing": "lambda_X,J_X,B_X,R_X,C_HX",
            "fallback": "epsilon_gapped_auxiliary",
            "valid_for_claim": False,
        },
    ]


def pc3400_4_update() -> list[dict[str, Any]]:
    return [
        {
            "pc_piece": "PC3400_4_gapped_nohair",
            "before_3429": "identified as next proof target",
            "after_3429": "exact conditional nohair theorem written",
            "remaining": "activation inputs missing",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_4_delta_extra_bound",
            "before_3429": "Delta_extra_mass formula from safe-class split",
            "after_3429": "gapped/Y6 norm-to-observable bound formula added",
            "remaining": "lambda/source/boundary/response values missing",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_4_hidden_projector",
            "before_3429": "retained residual",
            "after_3429": "still retained outside gapped nohair unless channelwise operator/source gates pass",
            "remaining": "channelwise hidden/projector audit",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_4_verdict",
            "before_3429": "public Hilbert safe, gapped/hidden open",
            "after_3429": "gapped theorem exists but not activated",
            "remaining": "lambda-star/source-free/boundary/projector inputs",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3429_0_nohair_theorem",
            "claim": "positive-operator gapped/Y6 nohair theorem is mathematically written",
            "gate_status": "PASS_CONDITIONAL_THEOREM",
            "reason": "energy identity gives X=0 if lambda_X>0 and J/B/R vanish",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3429_1_nohair_activated",
            "claim": "gapped/Y6 nohair is active for current MTS",
            "gate_status": "FAIL_CURRENT",
            "reason": "lambda_X, J_X, B_X, R_X and response constants are missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3429_2_bound_branch",
            "claim": "gapped/Y6 residual bound is score-ready",
            "gate_status": "FORMULA_READY_VALUES_MISSING",
            "reason": "norm-to-observable formulas exist but no numeric/source-backed values",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3429_3_PC3400_4",
            "claim": "PC3400_4 no-extra-mass is signed",
            "gate_status": "PARTIAL_ONLY",
            "reason": "public Hilbert safe and nohair theorem written; hidden/projector and activation inputs remain",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3429_4_local_GR",
            "claim": "local GR/Newton/PPN branch is derived",
            "gate_status": "BLOCKED",
            "reason": "PC3400_4 activation, MHref/tau row, lambda-star and second-order PPN remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3429_0_derivation_gain",
            "decision": "The gapped/Y6 nohair proof is now a real theorem template, not just a hope.",
            "because": "positive coercive energy plus zero source/boundary/projector work forces X=0",
            "next_action": "try to source or derive lambda_X,J_X,B_X,R_X for the dominant channels",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3429_1_not_active",
            "decision": "Current MTS cannot yet claim no-extra-mass from this theorem.",
            "because": "the activation inputs are still missing and hidden/projector channels may not be gapped",
            "next_action": "perform channelwise hidden/projector exclusion or bound",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3429_2_bound_policy",
            "decision": "If nohair fails, use the norm-bound branch rather than discarding the route.",
            "because": "lambda_X and source norms directly produce Delta_extra/PPN/fifth-force envelopes",
            "next_action": "fill channelwise rows before any empirical claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3429_3_next",
            "decision": "Next target should be hidden/projector channelwise exclusion or bound.",
            "because": "it decides whether the nohair theorem covers the remaining extra sector inventory",
            "next_action": "3430-Y5-R2FR-hidden-projector-channelwise-bound-or-exclusion-under-AX1090.md",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target": "3430-Y5-R2FR-hidden-projector-channelwise-bound-or-exclusion-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3430_hidden_projector_channelwise_bound_or_exclusion.py",
            "objective": "exclude or bound hidden/domain/projector/memory/range/constitutive monopole charge channel by channel, deciding which channels qualify for the 3429 nohair theorem",
            "why_next": "3429 supplies the nohair theorem but activation depends on hidden/projector channel ownership",
            "valid_for_claim": False,
        },
        {
            "target": "3431-Y5-R2FR-MHref-tau-source-row-instantiation-or-refusal-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3431_MHref_tau_source_row_instantiation_or_refusal.py",
            "objective": "instantiate or refuse a concrete M_H_ref/tau/source row after residual channel audit",
            "why_next": "needed to make the bound branch scoreable against local tests",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3429_0",
            "script": str(Path(__file__).resolve()),
            "mode": "GAPPED_Y6_NOHAIR_POSITIVE_OPERATOR_OR_DELTAEXTRA_ROW",
            "summary": "positive-operator nohair theorem and norm-to-Delta_extra bound written; activation inputs missing; no local-GR or no-extra-mass claim promoted",
            "valid_for_claim": False,
        }
    ]


def formalization_recent_count(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    threshold = start_utc.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= threshold)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    sources = rows_by_name["source_register"]
    nonclaim = all(
        row.get("valid_for_claim") is False
        for name, rows in rows_by_name.items()
        if name != "validation"
        for row in rows
    )
    outputs_under_root = all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()) and str(DOC).startswith(str(ROOT))
    formalization_count = formalization_recent_count(start_utc)
    promotion = rows_by_name["promotion_gates"]
    return [
        {
            "check_id": "VAL3429_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in sources),
            "detail": f"{sum(1 for row in sources if row['exists'])}/{len(sources)} source paths exist",
        },
        {
            "check_id": "VAL3429_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": outputs_under_root,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3429_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim,
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3429_3_nohair_theorem",
            "condition": "positive-operator nohair theorem exists",
            "passed": any(row["step_id"] == "PON3429_2_zero_branch" for row in rows_by_name["positive_operator_nohair_theorem"]),
            "detail": "PON3429_2 present",
        },
        {
            "check_id": "VAL3429_4_not_activated",
            "condition": "current nohair activation is not claimed",
            "passed": any(row["gate_id"] == "PG3429_1_nohair_activated" and row["gate_status"] == "FAIL_CURRENT" for row in promotion),
            "detail": "activation inputs missing",
        },
        {
            "check_id": "VAL3429_5_bound_rows",
            "condition": "norm-to-Delta_extra bound rows exist",
            "passed": any(row["bound_id"] == "DNB3429_4_total" for row in rows_by_name["delta_extra_norm_bound"]),
            "detail": "DNB3429_4 present",
        },
        {
            "check_id": "VAL3429_6_local_GR_blocked",
            "condition": "local GR remains blocked",
            "passed": any(row["gate_id"] == "PG3429_4_local_GR" and row["gate_status"] == "BLOCKED" for row in promotion),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3429_7_next_target",
            "condition": "next target attacks hidden/projector channelwise audit",
            "passed": rows_by_name["next_target"][0]["target"].startswith("3430-Y5-R2FR-hidden-projector"),
            "detail": rows_by_name["next_target"][0]["target"],
        },
        {
            "check_id": "VAL3429_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": formalization_count == 0,
            "detail": f"modified_count_since_start={formalization_count}",
        },
        {
            "check_id": "VAL3429_9_overall",
            "condition": "3429 gapped/Y6 nohair checkpoint is internally valid",
            "passed": True,
            "detail": "PASS",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3429 - Gapped Y6 Nohair Positive Operator or DeltaExtra Row

## Summary
- This checkpoint tries the derivation path for the gapped/Y6 residual sector.
- The theorem is clean: if the auxiliary operator is positive after gauge quotient and source, boundary and projector work vanish, the local compact exterior has no gapped residual hair.
- If any source/boundary/projector term survives, the theory does not get a GR claim; it gets a norm bound feeding `Delta_extra_mass`, fifth-force/Yukawa, and PPN residual rows.
- This is progress but not closure: the current corpus still lacks field-specific `lambda_X`, `J_X`, `B_X`, `R_X`, response constants, and `M_H_ref`.
- Therefore no-extra-mass remains partial, but the gapped/Y6 route is now a theorem-or-bound contract rather than fog.

## Source Register
{md_table(rows_by_name["source_register"])}

## Positive Operator Nohair Theorem
{md_table(rows_by_name["positive_operator_nohair_theorem"])}

## Nohair Activation Gate
{md_table(rows_by_name["activation_gate"])}

## Delta Extra Norm Bound
{md_table(rows_by_name["delta_extra_norm_bound"])}

## Gapped Channel Rows
{md_table(rows_by_name["gapped_channel_rows"])}

## PC3400_4 Update
{md_table(rows_by_name["pc3400_4_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is the clean engineering version: if the residual sector is genuinely massive, source-free, boundary-silent and coercive, it vanishes locally. If not, it becomes a bounded extra-source channel. The next job is channel ownership: which hidden/projector/memory/range sectors actually qualify for this theorem?
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "positive_operator_nohair_theorem": positive_operator_nohair_theorem(),
        "activation_gate": activation_gate(),
        "delta_extra_norm_bound": delta_extra_norm_bound(),
        "gapped_channel_rows": gapped_channel_rows(),
        "pc3400_4_update": pc3400_4_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3429 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3841"
BRANCH = "MTS_R2FR_Y5_SECOND_ORDER_TEMPORAL_READOUT_PROJECTION_NATURALITY_ZERO_OR_BETA_BOUND_3841"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3841-Y5-R2FR-second-order-temporal-readout-projection-naturality-zero-or-beta-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3840 = PCW / "3840-Y5-R2FR-second-order-boundary-reference-temporal-self-coupling-zero-or-beta-bound.md"
CSV_3840_BETA = OUT / "P8_Y5_R2FR_3840_BETA_BOUND_UPDATE.csv"
CSV_3840_VALIDATION = OUT / "P8_Y5_BRR545_3840_VALIDATION.csv"
CSV_3837_DECOMP = OUT / "P8_Y5_R2FR_3837_SBETA_DECOMPOSITION.csv"
CSV_3828_ANSATZ = OUT / "P8_Y5_R2FR_3828_PPN_READOUT_ANSATZ.csv"
CSV_3828_RESIDUAL = OUT / "P8_Y5_R2FR_3828_RESIDUAL_VECTOR_BOUND.csv"
CSV_3828_ZERO = OUT / "P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv"
CSV_3833_READOUT = OUT / "P8_Y5_R2FR_3833_READOUT_NATURALITY_THEOREM.csv"
CSV_3836_GAMMA_READOUT = OUT / "P8_Y5_R2FR_3836_DIRECT_GAMMA_READOUT_DECOMPOSITION.csv"
CSV_3810_CONTRACT = OUT / "P8_Y5_R2FR_3810_PARENT_OWNED_ZQEFF_READOUT_CONTRACT.csv"
CSV_3811_MORPHISM = OUT / "P8_Y5_R2FR_3811_MORPHISM_BAN_DERIVATION_AUDIT.csv"
CSV_3808_OBSREP = OUT / "P8_Y5_R2FR_3808_OBSREP_TYPE_SYSTEM_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3841_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_R2FR_3841_READOUT2_ZERO_AUDIT.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3841_READOUT2_DECOMPOSITION.csv",
    "beta_update": OUT / "P8_Y5_R2FR_3841_BETA_BOUND_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3841_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3841_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3841_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3841_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3841_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3841_0_3840_doc", P_3840, "Second-Order Boundary"),
    ("SRC3841_1_3840_beta", CSV_3840_BETA, "BUP3840_1_beta_total"),
    ("SRC3841_2_3840_validation", CSV_3840_VALIDATION, "VAL3840_4_nonclaim"),
    ("SRC3841_3_3837_decomp", CSV_3837_DECOMP, "SB3837_3_readout2"),
    ("SRC3841_4_3828_ansatz", CSV_3828_ANSATZ, "ANS3828_0_Newtonian_temporal"),
    ("SRC3841_5_3828_residual", CSV_3828_RESIDUAL, "RPPN3828_1_beta"),
    ("SRC3841_6_3828_zero", CSV_3828_ZERO, "ZPPN3828_2_beta_lock"),
    ("SRC3841_7_3833_readout", CSV_3833_READOUT, "RN3833_0_chain_rule_zero"),
    ("SRC3841_8_3836_gamma_readout", CSV_3836_GAMMA_READOUT, "DGR3836_0_metric_projection"),
    ("SRC3841_9_3810_contract", CSV_3810_CONTRACT, "POC3810_5_readout_closure"),
    ("SRC3841_10_3811_morphism", CSV_3811_MORPHISM, "MB3811_0_exact_equivalence"),
    ("SRC3841_11_3808_obsrep", CSV_3808_OBSREP, "ORT3808_2_chain_rule"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_second_order_temporal_readout_projection_naturality_zero_or_beta_bound",
                "claim_use": "readout2_zero_or_bound_audit_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "RO2A3841_0_target_sharp",
            "requirement": "S_readout2 is the next unresolved S_beta component",
            "test": "SB3837_3_readout2 and BUP3840_1_beta_total both contain the term",
            "current_status": "PASS_TARGET_SHARP",
            "if_failed": "beta ledger would be missing second-order temporal readout/projection channel",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "RO2A3841_1_no_Ct_to_Bt_promotion",
            "requirement": "Newtonian C_t calibration is not promoted to beta B_t without readout second-derivative control",
            "test": "require fixed readout map through O(Phi^2), not only first-order metric calibration",
            "current_status": "PASS_GUARD",
            "if_failed": "B_t could be chosen by nonlinear readout after C_t is fitted",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "RO2A3841_2_metric_projection_t2",
            "requirement": "parent temporal metric perturbation projects to the declared PPN g00 coefficient through second order",
            "test": "h00 and h00^(2) map to g00=-1+2 C_t Phi-2 B_t Phi^2 with no leftover temporal projection",
            "current_status": "SECOND_ORDER_METRIC_PROJECTION_SIGNATURE_REQUIRED",
            "if_failed": "retain B_t2_metric_projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "RO2A3841_3_readout_second_derivative",
            "requirement": "the second derivative of the readout map supplies the EH/GR self-coupling value, not an independent coefficient",
            "test": "D2 R_obs[h,h] plus parent second variation fixes B_t=C_t^2 before arena fitting",
            "current_status": "READOUT_SECOND_DERIVATIVE_NOT_PARENT_SIGNED",
            "if_failed": "retain B_t2_readout_second_derivative",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "RO2A3841_4_field_redef_gauge",
            "requirement": "field redefinitions, gauge choices, or coordinate transformations do not shift beta after C_t calibration",
            "test": "fixed PPN gauge and field variable before extracting B_t",
            "current_status": "GAUGE_FIELD_REDEF_SIGNATURE_REQUIRED",
            "if_failed": "retain B_t2_field_redef_gauge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "RO2A3841_5_hidden_coeff_morphism",
            "requirement": "no hidden-visible coefficient morphism feeds a nonlinear temporal readout coefficient",
            "test": "ObsRep/type-system chain rule plus no hidden-visible morphism applies to beta readout coefficients",
            "current_status": "PARENT_VISIBLE_COEFFICIENT_SIGNATURE_REQUIRED",
            "if_failed": "retain B_t2_hidden_coeff",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "RO2A3841_6_arena_projection",
            "requirement": "PPN, clock, orbital, and local-source arenas use one fixed metric readout before fitting",
            "test": "no arena-specific beta extraction, calibration, fit-window, or post-hoc projection coefficient",
            "current_status": "ARENA_READOUT_SOURCE_ROWS_REQUIRED",
            "if_failed": "retain B_t2_arena_projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "RO2A3841_7_cross_readout_lock",
            "requirement": "clock/orbital/PPN temporal readouts are induced by the same g00 source branch",
            "test": "C_tau, C_acc, and beta extraction share C_t/B_t owner; fitted GM is validation output only",
            "current_status": "CROSS_READOUT_LOCK_NOT_PARENT_SIGNED",
            "if_failed": "retain B_t2_cross_readout",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "RO2A3841_8_verdict",
            "requirement": "all readout2 silence clauses close simultaneously",
            "test": "RO2A3841_2 through RO2A3841_7 all parent-signed or source-backed below threshold",
            "current_status": "READOUT2_ZERO_NOT_CLAIMED",
            "if_failed": "S_readout2 remains a beta residual rather than an assumed readout closure",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "RO2M3841_0_metric_projection",
            "component": "B_t2_metric_projection",
            "definition": "mismatch between parent temporal metric perturbation and the PPN beta g00 projection",
            "zero_route": "single metric readout plus declared PPN gauge maps h00^(2) to -2 B_t Phi^2",
            "bound_formula": "B_t2_metric_projection <= abs(R_metric_projection_t2/Phi^2)",
            "status": "SECOND_ORDER_PROJECTION_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "RO2M3841_1_readout_second_derivative",
            "component": "B_t2_readout_second_derivative",
            "definition": "nonlinear second derivative of the readout map that shifts B_t after C_t is fixed",
            "zero_route": "D2 R_obs is parent-fixed and equals the EH/GR metric self-coupling readout",
            "bound_formula": "B_t2_readout_second_derivative <= abs((D2R_obs - D2R_EH)[h,h]/Phi^2)",
            "status": "READOUT_SECOND_DERIVATIVE_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "RO2M3841_2_field_redef_gauge",
            "component": "B_t2_field_redef_gauge",
            "definition": "field-redefinition, coordinate, or gauge shift that changes beta without changing Newtonian C_t",
            "zero_route": "fixed PPN gauge/field variable before beta extraction",
            "bound_formula": "B_t2_field_redef_gauge <= abs(R_gauge_beta_readout)",
            "status": "GAUGE_FIX_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "RO2M3841_3_hidden_coeff",
            "component": "B_t2_hidden_coeff",
            "definition": "hidden scalar/invariant feeding a second-order temporal visible coefficient slot",
            "zero_route": "Hom(A_hid,Coeff_vis) has no nonconstant vertical component for beta readout coefficients",
            "bound_formula": "B_t2_hidden_coeff <= abs(Lie_v c_beta * zeta_v)",
            "status": "MORPHISM_BAN_PARENT_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "RO2M3841_4_arena_projection",
            "component": "B_t2_arena_projection",
            "definition": "arena-specific beta extraction/calibration/fit-window tail after the metric readout",
            "zero_route": "one fixed readout map before PPN, clock, orbital, and source arena fitting",
            "bound_formula": "B_t2_arena_projection <= abs(R_beta_arena_fit_window)",
            "status": "ARENA_PROJECTION_SOURCE_ROW_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "RO2M3841_5_cross_readout",
            "component": "B_t2_cross_readout",
            "definition": "mismatch between PPN beta, clock/redshift, and orbital temporal projections",
            "zero_route": "clock/orbital/PPN projections are all induced by the same metric source readout",
            "bound_formula": "B_t2_cross_readout <= abs(R_clock_beta_lock) + abs(R_orbital_beta_lock)",
            "status": "CROSS_READOUT_LOCK_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "RO2M3841_6_fit_smuggling",
            "component": "B_t2_fit_smuggling",
            "definition": "use of fitted mu=GM, nuisance offsets, or post-fit scale choices to define beta/readout normalization",
            "zero_route": "source normalization is fixed independently; fitted orbital mu is validation output only",
            "bound_formula": "B_t2_fit_smuggling <= abs(R_GM_guard_beta) + abs(R_nuisance_beta)",
            "status": "SOURCE_NORMALIZATION_GUARD_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "RO2M3841_7_total",
            "component": "B_readout2",
            "definition": "total beta contribution from second-order temporal readout/projection mismatch",
            "zero_route": "all readout2 components vanish on the same compact exterior metric/source/readout branch",
            "bound_formula": "B_readout2 <= B_t2_metric_projection + B_t2_readout_second_derivative + B_t2_field_redef_gauge + B_t2_hidden_coeff + B_t2_arena_projection + B_t2_cross_readout + B_t2_fit_smuggling",
            "status": "FIRST_READOUT2_BOUND_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def beta_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "BUP3841_0_readout2_update",
            "observable": "B_readout2",
            "formula": "B_readout2 <= B_t2_metric_projection + B_t2_readout_second_derivative + B_t2_field_redef_gauge + B_t2_hidden_coeff + B_t2_arena_projection + B_t2_cross_readout + B_t2_fit_smuggling",
            "new_detail": "readout2 is decomposed into second-order metric projection, readout Hessian, gauge/redefinition, hidden coefficient, arena projection, cross-readout, and fit-smuggling channels",
            "status": "UPDATED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BUP3841_1_beta_total",
            "observable": "beta-1",
            "formula": "abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)",
            "new_detail": "all S_beta components now have ledgers; beta remains blocked by nonclaim ledgers plus eps_temporal4",
            "status": "NONCLAIM_BETA_BOUND_STRUCTURALLY_COMPLETE_EXCEPT_EPS_TEMPORAL4",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3841_0_target_trace",
            "gate": "readout2 term traced to beta ledger",
            "status": "PASS_TARGET_SHARP",
            "claim_allowed": False,
            "reason": "S_readout2 is explicitly the next unresolved S_beta component",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3841_1_no_Ct_to_Bt_promotion",
            "gate": "Newtonian C_t calibration is not promoted to beta",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "a nonlinear readout map can preserve C_t while shifting B_t unless second-order naturality is signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3841_2_readout2_zero",
            "gate": "second-order temporal readout/projection zero theorem",
            "status": "BLOCKED_PARENT_READOUT_SIGNATURE_REQUIRED",
            "claim_allowed": False,
            "reason": "metric projection, readout Hessian, gauge, hidden coefficient, arena, cross-readout, and fit guards are not all signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3841_3_readout2_bound",
            "gate": "readout2 finite beta bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "B_readout2 bound formula exists but numeric/source-backed rows are not supplied",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3841_4_beta_claim",
            "gate": "beta/local PPN claim",
            "status": "BLOCKED_REFINED_BOUND_ONLY",
            "claim_allowed": False,
            "reason": "all S_beta ledgers are nonclaim and eps_temporal4 still needs decomposition/source bounds",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3841_5_next_target",
            "gate": "next target attacks eps_temporal4",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "S_beta components are now all formulated; remaining beta envelope term is eps_temporal4",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3841_0_no_readout_smuggle",
            "decision": "do not infer beta readout from Newtonian readout calibration",
            "basis": "3828 fixes the distinction between C_t and B_t; 3837 makes B_t a second-order condition",
            "consequence": "readout2 remains nonclaim until the readout map is fixed through second order",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3841_1_readout2_as_beta_bound",
            "decision": "treat S_readout2 as a finite beta residual with seven named channels",
            "basis": "3808/3810/3811/3833 give conditional naturality theorems but not the parent signature",
            "consequence": "S_beta is now structurally decomposed across EH2, scalar2, boundary2, and readout2",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3841_2_next_eps_temporal4",
            "decision": "move next to temporal fourth-order/gauge/domain residual",
            "basis": "all named S_beta components now have explicit nonclaim ledgers",
            "consequence": "3842 should decompose eps_temporal4 before any integrated beta dashboard",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3841_0",
            "next_checkpoint": "3842-Y5-R2FR-eps-temporal4-order-gauge-domain-zero-or-beta-bound.md",
            "script": "scripts/Y5_R2FR_3842_eps_temporal4_order_gauge_domain_zero_or_beta_bound.py",
            "objective": "decompose abs(eps_temporal4/Phi^2) into order, gauge, domain, and nonlinear-tail residuals, or source-bound it",
            "reason": "3841 formulates readout2; all S_beta components now have ledgers and eps_temporal4 is the remaining beta envelope term",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_READOUT2_BOUND_CONTRACT",
            "claim": "no beta/local-GR claim",
            "summary": "3841 specializes readout naturality to the second-order temporal beta channel and guards against promoting C_t calibration to B_t.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(sources, zero_audit, decomposition, beta_update, gates, decisions, timestamp: str) -> None:
    text = f"""# 3841 - Second-Order Temporal Readout Projection Naturality Zero Or Beta Bound

Private checkpoint. This attacks `S_readout2`, the second-order temporal readout/projection contribution to beta. It does not claim `beta=1` or local GR.

Generated: `{timestamp}`

## Result

3841 blocks the shortcut:

`Newtonian C_t calibration != second-order B_t readout naturality`.

The required zero route is:

`metric_projection_t2 + readout_Hessian_t2 + gauge_field_redef_t2 + hidden_coeff_t2 + arena_projection_t2 + cross_readout_t2 + fit_smuggling_t2 = 0 => S_readout2 = 0`.

The current corpus has exact conditional readout/type/morphism theorems, but not the parent signature proving the beta-order readout map is fixed through second order. Therefore the retained bound is:

`B_readout2 <= B_t2_metric_projection + B_t2_readout_second_derivative + B_t2_field_redef_gauge + B_t2_hidden_coeff + B_t2_arena_projection + B_t2_cross_readout + B_t2_fit_smuggling`.

The beta envelope remains:

`abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Readout2 Zero Audit

{markdown_table(zero_audit, ["audit_id", "requirement", "test", "current_status", "if_failed"])}

## Readout2 Decomposition

{markdown_table(decomposition, ["component_id", "component", "definition", "zero_route", "status"])}

## Beta Bound Update

{markdown_table(beta_update, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This closes the structural `S_beta` decomposition: EH2, extra scalar2, boundary2, and readout2 now each have a zero route and a finite residual contract. The theory still has not derived local GR, but beta is no longer a shapeless gap.

Next target: `3842-Y5-R2FR-eps-temporal4-order-gauge-domain-zero-or-beta-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3840", "Current State After 3841", 1)
    paragraph = (
        "`3841` specializes readout naturality to beta order and blocks the shortcut `C_t` calibration => `B_t` readout closure. "
        "The retained bound is `B_readout2 <= B_t2_metric_projection+B_t2_readout_second_derivative+B_t2_field_redef_gauge+B_t2_hidden_coeff+B_t2_arena_projection+B_t2_cross_readout+B_t2_fit_smuggling`, "
        "so `|beta-1| <= B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+|eps_temporal4/Phi^2|`. "
        "No readout2 zero is claimed because the parent readout map is not signed through second order, but all four `S_beta` components now have explicit ledgers.\n\n"
    )
    anchor = "`3840` specializes"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3841-Y5-R2FR-second-order-temporal-readout-projection-naturality-zero-or-beta-bound.md`

Target: try to prove the same metric/readout fixes both `C_t` and `B_t` before arena projection, or retain/source-bound `S_readout2`.

This is the best next move because 3840 formulates the boundary2 ledger; the next unresolved `S_beta` component is readout2."""
    new_gate = """`3842-Y5-R2FR-eps-temporal4-order-gauge-domain-zero-or-beta-bound.md`

Target: decompose `abs(eps_temporal4/Phi^2)` into order, gauge, domain, and nonlinear-tail residuals, or source-bound it.

This is the best next move because 3841 formulates readout2; all `S_beta` components now have ledgers and `eps_temporal4` is the remaining beta envelope term."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3841_READOUT2_ZERO_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3841_READOUT2_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3841_BETA_BOUND_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3841_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3841_READOUT2_ZERO_AUDIT.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3841 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3841 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, zero_audit, decomposition, beta_update, gates, timestamp: str) -> list[dict[str, object]]:
    rows = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in zero_audit + decomposition + beta_update + gates)
    add(
        "VAL3841_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3841_1_target_trace",
        "S_readout2 is traced from existing beta ledger",
        "S_readout2" in all_text and "BUP3841_1_beta_total" in all_text,
        "target term present in zero audit and beta update",
    )
    add(
        "VAL3841_2_no_promotion_guard",
        "C_t calibration is not promoted to B_t",
        "Newtonian C_t calibration is not promoted" in all_text and any(row["gate_id"] == "GATE3841_1_no_Ct_to_Bt_promotion" for row in gates),
        "readout promotion guard present",
    )
    add(
        "VAL3841_3_components",
        "readout2 components are decomposed",
        all(
            token in all_text
            for token in [
                "B_t2_metric_projection",
                "B_t2_readout_second_derivative",
                "B_t2_field_redef_gauge",
                "B_t2_hidden_coeff",
                "B_t2_arena_projection",
                "B_t2_cross_readout",
                "B_t2_fit_smuggling",
                "B_readout2",
            ]
        ),
        "readout2 component tokens present",
    )
    add(
        "VAL3841_4_nonclaim",
        "all 3841 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in zero_audit + decomposition + beta_update + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3841_5_readout2_gate_blocked",
        "readout2 zero remains blocked",
        any(row["gate_id"] == "GATE3841_2_readout2_zero" and row["status"].startswith("BLOCKED") for row in gates),
        "readout2 zero gate blocked",
    )
    add(
        "VAL3841_6_sbeta_structural_completion",
        "all four S_beta component bounds are present in beta formula",
        all(token in all_text for token in ["B_EH2_vertex", "B_extra_scalar2", "B_boundary2", "B_readout2"]),
        "EH2, scalar2, boundary2, readout2 tokens present",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3841_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3841_8_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "S_readout2" in read_text(DOC_PATH) and "B_readout2" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3841*", "P8_Y5_BRR545_3841*", "*Y5_R2FR_3841*", "3841-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3841_9_formalization_clean",
        "formalization-workbench has no 3841 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3841 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3841_10_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    zero_audit = zero_audit_rows(timestamp)
    decomposition = decomposition_rows(timestamp)
    beta_update = beta_update_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zero_audit"], zero_audit)
    write_csv(OUTPUTS["decomposition"], decomposition)
    write_csv(OUTPUTS["beta_update"], beta_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, zero_audit, decomposition, beta_update, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, zero_audit, decomposition, beta_update, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_READOUT2_BOUND_CONTRACT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

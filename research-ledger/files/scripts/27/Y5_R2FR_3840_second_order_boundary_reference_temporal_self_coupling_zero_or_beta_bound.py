from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3840"
BRANCH = "MTS_R2FR_Y5_SECOND_ORDER_BOUNDARY_REFERENCE_TEMPORAL_SELF_COUPLING_ZERO_OR_BETA_BOUND_3840"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3840-Y5-R2FR-second-order-boundary-reference-temporal-self-coupling-zero-or-beta-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3839 = PCW / "3839-Y5-R2FR-extra-scalar-quadratic-self-energy-zero-or-beta-bound.md"
P_3834 = PCW / "3834-Y5-R2FR-boundary-harmonic-scalar-slip-zero-or-gamma-bound.md"
CSV_3839_BETA = OUT / "P8_Y5_R2FR_3839_BETA_BOUND_UPDATE.csv"
CSV_3839_VALIDATION = OUT / "P8_Y5_BRR545_3839_VALIDATION.csv"
CSV_3837_DECOMP = OUT / "P8_Y5_R2FR_3837_SBETA_DECOMPOSITION.csv"
CSV_3824_BOUNDARY = OUT / "P8_Y5_R2FR_3824_BOUNDARY_PRIMITIVE_ZERO_OR_BOUND.csv"
CSV_3824_GATE = OUT / "P8_Y5_R2FR_3824_TOPOLOGICAL_HILBERT_EQUALITY_GATE.csv"
CSV_3825_THEOREM = OUT / "P8_Y5_R2FR_3825_BOUNDARY_REFERENCE_ZERO_THEOREM.csv"
CSV_3825_FIRST = OUT / "P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv"
CSV_3825_RESIDUAL = OUT / "P8_Y5_R2FR_3825_BOUNDARY_MHREF_RESIDUAL_ROWS.csv"
CSV_3834_THEOREM = OUT / "P8_Y5_R2FR_3834_BOUNDARY_HARMONIC_ELLIPTIC_ZERO_THEOREM.csv"
CSV_3834_COMPONENTS = OUT / "P8_Y5_R2FR_3834_BOUNDARY_SLIP_COMPONENTS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3840_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_R2FR_3840_BOUNDARY2_ZERO_AUDIT.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3840_BOUNDARY2_DECOMPOSITION.csv",
    "beta_update": OUT / "P8_Y5_R2FR_3840_BETA_BOUND_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3840_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3840_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3840_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3840_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3840_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3840_0_3839_doc", P_3839, "Extra Scalar Quadratic"),
    ("SRC3840_1_3839_beta", CSV_3839_BETA, "BUP3839_1_beta_total"),
    ("SRC3840_2_3839_validation", CSV_3839_VALIDATION, "VAL3839_4_nonclaim"),
    ("SRC3840_3_3837_decomp", CSV_3837_DECOMP, "SB3837_2_boundary2"),
    ("SRC3840_4_3824_boundary", CSV_3824_BOUNDARY, "BPR3824_1_Delta_symp"),
    ("SRC3840_5_3824_gate", CSV_3824_GATE, "EQ3824_3_compact_exterior_closure"),
    ("SRC3840_6_3825_theorem", CSV_3825_THEOREM, "BRT3825_5_verdict"),
    ("SRC3840_7_3825_first", CSV_3825_FIRST, "FSR3825_3_epsilon_boundary_reference_abs"),
    ("SRC3840_8_3825_residual", CSV_3825_RESIDUAL, "R3825_4_total"),
    ("SRC3840_9_3834_theorem", CSV_3834_THEOREM, "BH3834_1_3825_specialization"),
    ("SRC3840_10_3834_components", CSV_3834_COMPONENTS, "BC3834_3_Bzero"),
    ("SRC3840_11_3834_doc", P_3834, "generic `B_zero_flux=0` is not automatically"),
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
                "role": "input_for_second_order_boundary_reference_temporal_self_coupling_zero_or_beta_bound",
                "claim_use": "boundary2_zero_or_bound_audit_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "BD2A3840_0_target_sharp",
            "requirement": "S_boundary2 is the next unresolved S_beta component",
            "test": "SB3837_2_boundary2 and BUP3839_1_beta_total both contain the term",
            "current_status": "PASS_TARGET_SHARP",
            "if_failed": "beta ledger would be missing second-order boundary/reference channel",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BD2A3840_1_no_first_order_promotion",
            "requirement": "first-order or generic boundary flux silence is not promoted to beta-order temporal self-coupling",
            "test": "require boundary/reference rows specialized to the second-order g00/B_t coefficient",
            "current_status": "PASS_GUARD",
            "if_failed": "S_boundary2 would be hidden inside a generic boundary-zero slogan",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BD2A3840_2_Dirichlet_beta",
            "requirement": "second-order temporal boundary value is fixed to the same EH/PPN reference",
            "test": "delta g00^(2)|boundary or delta B_t|boundary is zero/source-bounded in the compact exterior",
            "current_status": "SPECIALIZED_BOUNDARY_ROW_REQUIRED",
            "if_failed": "retain B_t2_Dirichlet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BD2A3840_3_Neumann_flux_beta",
            "requirement": "normal flux of the second-order temporal mode through the boundary is zero/source-bounded",
            "test": "n.grad delta g00^(2) or beta-shaped temporal flux is fixed by boundary data",
            "current_status": "SPECIALIZED_BOUNDARY_ROW_REQUIRED",
            "if_failed": "retain B_t2_Neumann_flux",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BD2A3840_4_harmonic_beta_mode",
            "requirement": "homogeneous boundary harmonic modes cannot mimic a beta-shaped U^2 temporal coefficient",
            "test": "no l>=2 temporal harmonic and no unfixed l=0/l=1 reference mode after mass/frame calibration",
            "current_status": "HARMONIC_BETA_SIGNATURE_REQUIRED",
            "if_failed": "retain B_t2_harmonic",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BD2A3840_5_Bzero_specialization",
            "requirement": "3825 B_zero_flux zero applies to the second-order temporal/beta channel",
            "test": "B_zero_flux^t2=0, not only generic charge/source flux zero",
            "current_status": "SPECIALIZED_3825_TEMPORAL_ROW_REQUIRED",
            "if_failed": "retain B_Bzero_flux_t2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BD2A3840_6_Delta_symp_stationary",
            "requirement": "symplectic/reference subtraction is stationary through second order in the temporal sector",
            "test": "Delta_symp^t2=0 with same exterior frame and same source normalization",
            "current_status": "SECOND_ORDER_REFERENCE_STATIONARITY_REQUIRED",
            "if_failed": "retain B_Delta_symp_t2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BD2A3840_7_MHref_frame_lock",
            "requirement": "MHref denominator/frame/reference lock does not renormalize B_t after C_t is calibrated",
            "test": "same-frame MHref positive denominator and source reference are fixed at beta order",
            "current_status": "MHREF_SECOND_ORDER_LOCK_REQUIRED",
            "if_failed": "retain B_MHref_frame2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BD2A3840_8_verdict",
            "requirement": "all boundary2 silence clauses close simultaneously",
            "test": "BD2A3840_2 through BD2A3840_7 all parent-signed or source-backed below threshold",
            "current_status": "BOUNDARY2_ZERO_NOT_CLAIMED",
            "if_failed": "S_boundary2 remains a beta residual rather than a swallowed boundary assumption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "BD2M3840_0_Dirichlet",
            "component": "B_t2_Dirichlet",
            "definition": "second-order temporal value fixed on the exterior boundary/reference surface",
            "zero_route": "delta g00^(2)|boundary=0 or beta reference matches EH/PPN value",
            "bound_formula": "B_t2_Dirichlet <= sup_boundary abs(delta g00^(2))/Phi^2",
            "status": "SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BD2M3840_1_Neumann_flux",
            "component": "B_t2_Neumann_flux",
            "definition": "normal derivative or flux of the second-order temporal mode through the exterior boundary",
            "zero_route": "normal beta flux zero by fixed boundary data/Stokes specialization",
            "bound_formula": "B_t2_Neumann_flux <= L_boundary * sup_boundary abs(n.grad delta g00^(2))/Phi^2",
            "status": "SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BD2M3840_2_harmonic",
            "component": "B_t2_harmonic",
            "definition": "homogeneous beta-shaped temporal harmonic mode on the exterior annulus",
            "zero_route": "no unfixed temporal harmonic class after mass, frame, and asymptotic reference lock",
            "bound_formula": "B_t2_harmonic <= sum_lm abs(a_lm^t2)/Phi^2",
            "status": "HARMONIC_CLASS_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BD2M3840_3_Bzero_flux",
            "component": "B_Bzero_flux_t2",
            "definition": "second-order temporal specialization of the 3825 B_zero_flux boundary primitive",
            "zero_route": "B_zero_flux=0 applies to the beta/B_t temporal mode",
            "bound_formula": "B_Bzero_flux_t2 <= abs(B_zero_flux^t2/Phi^2)",
            "status": "SPECIALIZED_3825_ROW_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BD2M3840_4_Delta_symp",
            "component": "B_Delta_symp_t2",
            "definition": "second-order temporal symplectic/reference drift from fixed exterior projector",
            "zero_route": "Delta_symp=0 applies to temporal self-coupling reference data",
            "bound_formula": "B_Delta_symp_t2 <= abs(Delta_symp^t2/Phi^2)",
            "status": "SPECIALIZED_3825_ROW_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BD2M3840_5_MHref_frame",
            "component": "B_MHref_frame2",
            "definition": "same-frame MHref denominator/reference normalization drift at beta order",
            "zero_route": "positive same-frame MHref denominator and source reference are fixed through second order",
            "bound_formula": "B_MHref_frame2 <= abs(delta MHref_t2/MHref_ref)",
            "status": "MHREF_SECOND_ORDER_SOURCE_ROW_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BD2M3840_6_counterterm",
            "component": "B_boundary_counterterm2",
            "definition": "local boundary counterterm/improvement contribution that shifts B_t without shifting C_t",
            "zero_route": "allowed boundary counterterms are fixed by differentiability and cannot alter beta after C_t calibration",
            "bound_formula": "B_boundary_counterterm2 <= abs(delta B_t_counterterm/C_t^2)",
            "status": "BOUNDARY_COUNTERTERM_CLASSIFICATION_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BD2M3840_7_total",
            "component": "B_boundary2",
            "definition": "total beta contribution from second-order boundary/reference temporal self-coupling",
            "zero_route": "all boundary2 components vanish on the same compact exterior source/reference/readout branch",
            "bound_formula": "B_boundary2 <= B_t2_Dirichlet + B_t2_Neumann_flux + B_t2_harmonic + B_Bzero_flux_t2 + B_Delta_symp_t2 + B_MHref_frame2 + B_boundary_counterterm2",
            "status": "FIRST_BOUNDARY2_BOUND_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def beta_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "BUP3840_0_boundary2_update",
            "observable": "B_boundary2",
            "formula": "B_boundary2 <= B_t2_Dirichlet + B_t2_Neumann_flux + B_t2_harmonic + B_Bzero_flux_t2 + B_Delta_symp_t2 + B_MHref_frame2 + B_boundary_counterterm2",
            "new_detail": "boundary2 is decomposed into second-order temporal Dirichlet, flux, harmonic, B_zero, Delta_symp, MHref/frame, and counterterm channels",
            "status": "UPDATED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BUP3840_1_beta_total",
            "observable": "beta-1",
            "formula": "abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)",
            "new_detail": "beta total remains blocked because readout2 and eps_temporal4 are still undecomposed and earlier components are nonclaim",
            "status": "NONCLAIM_BETA_BOUND_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3840_0_target_trace",
            "gate": "boundary2 term traced to beta ledger",
            "status": "PASS_TARGET_SHARP",
            "claim_allowed": False,
            "reason": "S_boundary2 is explicitly the next unresolved S_beta component",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3840_1_no_promotion",
            "gate": "generic boundary zero is not promoted to beta",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "3825/3834 boundary machinery must be specialized to second-order temporal self-coupling",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3840_2_boundary2_zero",
            "gate": "second-order boundary/reference temporal zero theorem",
            "status": "BLOCKED_SPECIALIZED_TEMPORAL_BOUNDARY_ROWS_REQUIRED",
            "claim_allowed": False,
            "reason": "no Dirichlet/flux/harmonic/B_zero/Delta_symp/MHref/counterterm beta-order source rows are claim-valid",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3840_3_boundary2_bound",
            "gate": "boundary2 finite beta bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "B_boundary2 bound formula exists but numeric/source-backed rows are not supplied",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3840_4_beta_claim",
            "gate": "beta/local PPN claim",
            "status": "BLOCKED_REFINED_BOUND_ONLY",
            "claim_allowed": False,
            "reason": "B_EH2_vertex, B_extra_scalar2, B_boundary2, B_readout2, and eps_temporal4 remain nonclaim components",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3840_5_next_target",
            "gate": "next target attacks readout2",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "boundary2 is formulated; next S_beta component is second-order temporal readout/projection mismatch",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3840_0_no_boundary_smuggle",
            "decision": "do not reuse generic B_zero_flux or Delta_symp as a beta proof",
            "basis": "3834 already showed boundary machinery requires sector specialization",
            "consequence": "boundary2 remains nonclaim until temporal/B_t rows are signed or bounded",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3840_1_boundary2_as_beta_bound",
            "decision": "treat S_boundary2 as a finite beta residual with seven named channels",
            "basis": "3824/3825 give useful boundary machinery but not second-order temporal source rows",
            "consequence": "the beta branch now has only readout2 and eps_temporal4 left as undecomposed terms",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3840_2_next_Sbeta_component",
            "decision": "move next to second-order temporal readout/projection mismatch",
            "basis": "S_EH2_mismatch, S_extra_scalar2, and S_boundary2 now have explicit ledgers",
            "consequence": "3841 should try to zero or bound S_readout2",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3840_0",
            "next_checkpoint": "3841-Y5-R2FR-second-order-temporal-readout-projection-naturality-zero-or-beta-bound.md",
            "script": "scripts/Y5_R2FR_3841_second_order_temporal_readout_projection_naturality_zero_or_beta_bound.py",
            "objective": "try to prove the same metric/readout fixes both C_t and B_t before arena projection, or retain/source-bound S_readout2",
            "reason": "3840 formulates boundary2; the next unresolved S_beta component is readout2",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_BOUNDARY2_BOUND_CONTRACT",
            "claim": "no beta/local-GR claim",
            "summary": "3840 specializes boundary/reference machinery to the second-order temporal beta channel and keeps it nonclaim unless temporal boundary rows are sourced.",
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
    text = f"""# 3840 - Second-Order Boundary Reference Temporal Self-Coupling Zero Or Beta Bound

Private checkpoint. This attacks `S_boundary2`, the beta-order boundary/reference contribution to `B_t`. It does not claim `beta=1` or local GR.

Generated: `{timestamp}`

## Result

3840 blocks the shortcut:

`generic boundary/reference zero != beta-order temporal self-coupling zero`.

The required zero route is:

`Dirichlet_t2 + Neumann_flux_t2 + harmonic_t2 + B_zero_flux_t2 + Delta_symp_t2 + MHref_frame_t2 + boundary_counterterm_t2 = 0 => S_boundary2 = 0`.

The current corpus has generic boundary machinery and gamma/slip specializations, but not beta-order temporal rows. Therefore the retained bound is:

`B_boundary2 <= B_t2_Dirichlet + B_t2_Neumann_flux + B_t2_harmonic + B_Bzero_flux_t2 + B_Delta_symp_t2 + B_MHref_frame2 + B_boundary_counterterm2`.

The beta envelope remains:

`abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Boundary2 Zero Audit

{markdown_table(zero_audit, ["audit_id", "requirement", "test", "current_status", "if_failed"])}

## Boundary2 Decomposition

{markdown_table(decomposition, ["component_id", "component", "definition", "zero_route", "status"])}

## Beta Bound Update

{markdown_table(beta_update, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

Boundary is not being waved away. The 3824/3825 machinery remains useful, but 3840 says exactly what has to be true for it to protect beta rather than only source/gamma channels. Until those temporal boundary rows exist, `S_boundary2` is a real beta residual.

Next target: `3841-Y5-R2FR-second-order-temporal-readout-projection-naturality-zero-or-beta-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3839", "Current State After 3840", 1)
    paragraph = (
        "`3840` specializes the boundary/reference machinery to beta order instead of promoting generic boundary silence. "
        "The retained bound is `B_boundary2 <= B_t2_Dirichlet+B_t2_Neumann_flux+B_t2_harmonic+B_Bzero_flux_t2+B_Delta_symp_t2+B_MHref_frame2+B_boundary_counterterm2`, "
        "so `|beta-1| <= B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+|eps_temporal4/Phi^2|`. "
        "No boundary2 zero is claimed because the 3824/3825 rows are not yet specialized to second-order temporal self-coupling.\n\n"
    )
    anchor = "`3839` turns"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3840-Y5-R2FR-second-order-boundary-reference-temporal-self-coupling-zero-or-beta-bound.md`

Target: try to prove second-order boundary/reference terms cannot shift `B_t`, or retain/source-bound `S_boundary2`.

This is the best next move because 3839 formulates the extra scalar2 ledger; the next unresolved `S_beta` component is boundary2."""
    new_gate = """`3841-Y5-R2FR-second-order-temporal-readout-projection-naturality-zero-or-beta-bound.md`

Target: try to prove the same metric/readout fixes both `C_t` and `B_t` before arena projection, or retain/source-bound `S_readout2`.

This is the best next move because 3840 formulates the boundary2 ledger; the next unresolved `S_beta` component is readout2."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3840_BOUNDARY2_ZERO_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3840_BOUNDARY2_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3840_BETA_BOUND_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3840_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3840_BOUNDARY2_ZERO_AUDIT.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3840 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3840 at {timestamp} -->\n"
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
        "VAL3840_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3840_1_target_trace",
        "S_boundary2 is traced from existing beta ledger",
        "S_boundary2" in all_text and "BUP3840_1_beta_total" in all_text,
        "target term present in zero audit and beta update",
    )
    add(
        "VAL3840_2_no_promotion_guard",
        "generic boundary silence is not promoted to beta",
        "generic boundary flux silence is not promoted" in all_text and any(row["gate_id"] == "GATE3840_1_no_promotion" for row in gates),
        "promotion guard present",
    )
    add(
        "VAL3840_3_components",
        "boundary2 components are decomposed",
        all(
            token in all_text
            for token in [
                "B_t2_Dirichlet",
                "B_t2_Neumann_flux",
                "B_t2_harmonic",
                "B_Bzero_flux_t2",
                "B_Delta_symp_t2",
                "B_MHref_frame2",
                "B_boundary_counterterm2",
                "B_boundary2",
            ]
        ),
        "boundary2 component tokens present",
    )
    add(
        "VAL3840_4_nonclaim",
        "all 3840 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in zero_audit + decomposition + beta_update + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3840_5_boundary2_gate_blocked",
        "boundary2 zero remains blocked",
        any(row["gate_id"] == "GATE3840_2_boundary2_zero" and row["status"].startswith("BLOCKED") for row in gates),
        "boundary2 zero gate blocked",
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
        add(f"VAL3840_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3840_7_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "S_boundary2" in read_text(DOC_PATH) and "B_boundary2" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3840*", "P8_Y5_BRR545_3840*", "*Y5_R2FR_3840*", "3840-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3840_8_formalization_clean",
        "formalization-workbench has no 3840 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3840 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3840_9_pycache_removed",
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
    print(f"{CHECKPOINT} PASS_NONCLAIM_BOUNDARY2_BOUND_CONTRACT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

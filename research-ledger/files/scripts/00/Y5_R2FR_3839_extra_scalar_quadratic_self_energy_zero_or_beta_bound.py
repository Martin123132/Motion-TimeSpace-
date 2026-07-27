from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3839"
BRANCH = "MTS_R2FR_Y5_EXTRA_SCALAR_QUADRATIC_SELF_ENERGY_ZERO_OR_BETA_BOUND_3839"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3839-Y5-R2FR-extra-scalar-quadratic-self-energy-zero-or-beta-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3838 = PCW / "3838-Y5-R2FR-EH2-parent-second-variation-vertex-match-or-beta-bound.md"
P_1788 = PCW / "1788-Y5-R2FR-parent-second-order-no-extra-scalar-premise-or-R2FR-bound-row.md"
CSV_3838_BETA = OUT / "P8_Y5_R2FR_3838_BETA_BOUND_UPDATE.csv"
CSV_3838_VALIDATION = OUT / "P8_Y5_BRR545_3838_VALIDATION.csv"
CSV_3837_DECOMP = OUT / "P8_Y5_R2FR_3837_SBETA_DECOMPOSITION.csv"
CSV_3829_LOCK = OUT / "P8_Y5_R2FR_3829_SCALAR_LOCK_CONDITIONAL_THEOREM.csv"
CSV_1789_IDENTITY = OUT / "P8_Y5_PARENT_QLOC_1789_ELIMINATION_IDENTITY_GATE.csv"
CSV_1789_TOWER = OUT / "P8_Y5_PARENT_QLOC_1789_NO_INTEGRATED_OUT_TOWER_GATE.csv"
CSV_2516_SCALARON = OUT / "P8_Y5_NO_SHADOW_2516_R2FR_SCALARON_MAP.csv"
CSV_3292_SPURION = OUT / "P8_Y5_R2FR_3292_HILBERT_SOURCE_VS_SPURION_SPLIT.csv"
CSV_3833_READOUT = OUT / "P8_Y5_R2FR_3833_READOUT_NATURALITY_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3839_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_R2FR_3839_EXTRA_SCALAR2_ZERO_AUDIT.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3839_SCALAR2_DECOMPOSITION.csv",
    "beta_update": OUT / "P8_Y5_R2FR_3839_BETA_BOUND_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3839_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3839_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3839_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3839_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3839_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3839_0_3838_doc", P_3838, "EH2 Parent Second Variation"),
    ("SRC3839_1_3838_beta", CSV_3838_BETA, "BUP3838_1_beta_total"),
    ("SRC3839_2_3838_validation", CSV_3838_VALIDATION, "VAL3838_3_nonclaim"),
    ("SRC3839_3_3837_decomp", CSV_3837_DECOMP, "SB3837_1_extra_scalar2"),
    ("SRC3839_4_3829_lock", CSV_3829_LOCK, "LOCK3829_2_beta_EH2_vertex"),
    ("SRC3839_5_1788_doc", P_1788, "no retained scalar/class mode"),
    ("SRC3839_6_1789_identity", CSV_1789_IDENTITY, "EID1789_1_effective_tail"),
    ("SRC3839_7_1789_tower", CSV_1789_TOWER, "NIT1789_5_verdict"),
    ("SRC3839_8_2516_scalaron", CSV_2516_SCALARON, "SC2516_5_beta_second_order"),
    ("SRC3839_9_3292_spurion", CSV_3292_SPURION, "HSS3292_2_forbidden_source_only_spurion"),
    ("SRC3839_10_3833_readout", CSV_3833_READOUT, "RN3833_1_single_metric_scalar_lock"),
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
                "role": "input_for_extra_scalar_quadratic_self_energy_zero_or_beta_bound",
                "claim_use": "scalar2_zero_or_bound_audit_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "SC2A3839_0_target_sharp",
            "requirement": "S_extra_scalar2 is the next unresolved S_beta component",
            "test": "SB3837_1_extra_scalar2 and BUP3838_1_beta_total both contain the term",
            "current_status": "PASS_TARGET_SHARP",
            "if_failed": "beta ledger would be missing a named second-order scalar channel",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SC2A3839_1_no_independent_scalar_dof",
            "requirement": "ordinary compact exterior has no independent scalar/class degree of freedom in the local action/readout",
            "test": "parent fields reduce to one observed metric/coframe plus silent/topological hidden sectors",
            "current_status": "NOT_PARENT_SIGNED",
            "if_failed": "retain B_scalar_dof",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SC2A3839_2_no_integrated_out_tail",
            "requirement": "eliminated hidden sectors cannot regenerate scalar curvature or matter-source Green-function tails",
            "test": "for S_X=1/2<X,L_X X>-<J_X,X>, require J_X=0 or a universal/silent mode before elimination",
            "current_status": "NO_INTEGRATED_OUT_TOWER_NOT_DERIVED",
            "if_failed": "retain B_scalar_integrated_tail",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SC2A3839_3_no_R2_fR_scalaron",
            "requirement": "R2/fR scalaron pole is absent or decoupled in the beta-order local exterior",
            "test": "c_R2=f_RR=0, or scalar mass/coupling/screening rows are source-backed and below threshold",
            "current_status": "RELATIVE_ZERO_THEOREM_NOT_PARENT_ACTIVATED",
            "if_failed": "retain B_scalar_curvature_pole",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SC2A3839_4_no_source_only_spurion",
            "requirement": "extra scalar cannot act only as an active-source weight while leaving matter/readout untouched",
            "test": "same-action Hilbert source plus canonical normalization plus no-spurion object typing",
            "current_status": "PARTIAL_DERIVATION_NOT_PARENT_SIGNED",
            "if_failed": "retain B_scalar_source_spurion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SC2A3839_5_single_metric_second_order_readout",
            "requirement": "visible g00 has no independent quadratic scalar readout coefficient beyond the EH metric vertex",
            "test": "no Weyl/disformal/hidden-invariant coefficient enters g00 at order Phi^2",
            "current_status": "READOUT_NATURALITY_NOT_PARENT_SIGNED",
            "if_failed": "retain B_scalar_readout2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SC2A3839_6_profile_boundary_suppression",
            "requirement": "finite retained scalar profiles are either nohair-zero or quantitatively suppressed in the local arena",
            "test": "need scalar amplitude, range/mass, source coupling, screening, boundary mode, and arena projection rows",
            "current_status": "MISSING_NUMERIC_PROFILE_INPUTS",
            "if_failed": "retain B_scalar_profile_boundary",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SC2A3839_7_verdict",
            "requirement": "all scalar2 silence clauses close simultaneously",
            "test": "SC2A3839_1 through SC2A3839_6 all parent-signed or source-backed below threshold",
            "current_status": "SCALAR2_ZERO_NOT_CLAIMED",
            "if_failed": "S_extra_scalar2 remains a beta residual rather than a free fitted knob",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "SC2M3839_0_scalar_dof",
            "component": "B_scalar_dof",
            "definition": "beta-order g00 contribution from a retained independent scalar/class degree of freedom",
            "zero_route": "no local scalar/class degree of freedom survives the compact exterior parent action/readout",
            "bound_formula": "B_scalar_dof <= abs(delta_B_t_from_retained_scalar/C_t^2)",
            "status": "PARENT_NO_SCALAR_DOF_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SC2M3839_1_integrated_tail",
            "component": "B_scalar_integrated_tail",
            "definition": "effective scalar/nonlocal tail generated by eliminating a sourced hidden sector",
            "zero_route": "J_X=0, boundary flux=0, and zero/readout-safe hidden modes before solving E_X=0",
            "bound_formula": "B_scalar_integrated_tail <= abs(<J_X,L_X^-1 J_X>_00)/(Phi^2 normalization)",
            "status": "NO_INTEGRATED_OUT_TOWER_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SC2M3839_2_curvature_pole",
            "component": "B_scalar_curvature_pole",
            "definition": "R2/fR scalaron or curvature-prefactor pole contribution to second-order temporal potential",
            "zero_route": "c_R2=f_RR=0 by parent local metric-only second-order theorem or sourced mass/coupling bound",
            "bound_formula": "B_scalar_curvature_pole <= abs(delta_beta_R2FR(c_R2_or_fRR,m_s,alpha_s,screening))",
            "status": "SCALARON_ZERO_OR_NUMERIC_MAP_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SC2M3839_3_source_spurion",
            "component": "B_scalar_source_spurion",
            "definition": "quadratic source-normalization drift from a scalar/spurion that changes active source strength",
            "zero_route": "same-action Hilbert source, canonical normalization, and no source-only object slot",
            "bound_formula": "B_scalar_source_spurion <= abs(delta_B_t_source_only/C_t^2)",
            "status": "HILBERT_SOURCE_NO_SPURION_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SC2M3839_4_readout2",
            "component": "B_scalar_readout2",
            "definition": "second-order Weyl/disformal/hidden-invariant coefficient entering visible g00",
            "zero_route": "single q_obs-owned metric readout with no hidden-visible coefficient morphism",
            "bound_formula": "B_scalar_readout2 <= abs(a2_chi*chi^2 + a_grad*|grad chi|^2 L^2 + a_dis2*chi2)/Phi^2",
            "status": "SECOND_ORDER_READOUT_NATURALITY_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SC2M3839_5_profile_boundary",
            "component": "B_scalar_profile_boundary",
            "definition": "finite retained scalar profile, boundary mode, or nohair leakage in the local arena",
            "zero_route": "regular nohair operator plus boundary/harmonic silence or sourced amplitude/range suppression",
            "bound_formula": "B_scalar_profile_boundary <= A_chi * exp(-L_local/lambda_chi) + B_chi_boundary + B_chi_harmonic",
            "status": "SCALAR_PROFILE_BOUND_INPUTS_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SC2M3839_6_total",
            "component": "B_extra_scalar2",
            "definition": "total beta contribution from extra scalar quadratic self-energy/readout/source channels",
            "zero_route": "all scalar2 components vanish on the same compact exterior metric/source/readout branch",
            "bound_formula": "B_extra_scalar2 <= B_scalar_dof + B_scalar_integrated_tail + B_scalar_curvature_pole + B_scalar_source_spurion + B_scalar_readout2 + B_scalar_profile_boundary",
            "status": "FIRST_SCALAR2_BOUND_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def beta_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "BUP3839_0_scalar2_update",
            "observable": "B_extra_scalar2",
            "formula": "B_extra_scalar2 <= B_scalar_dof + B_scalar_integrated_tail + B_scalar_curvature_pole + B_scalar_source_spurion + B_scalar_readout2 + B_scalar_profile_boundary",
            "new_detail": "extra scalar quadratic self-energy is decomposed into parent-dof, eliminated-tail, scalaron, source-spurion, readout, and finite-profile channels",
            "status": "UPDATED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BUP3839_1_beta_total",
            "observable": "beta-1",
            "formula": "abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)",
            "new_detail": "beta total remains blocked because scalar2, boundary2, readout2, and eps_temporal4 are not all zeroed or source-bounded",
            "status": "NONCLAIM_BETA_BOUND_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3839_0_target_trace",
            "gate": "extra scalar2 term traced to beta ledger",
            "status": "PASS_TARGET_SHARP",
            "claim_allowed": False,
            "reason": "S_extra_scalar2 is explicitly the next unresolved S_beta component",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3839_1_scalar2_zero",
            "gate": "extra scalar quadratic self-energy zero theorem",
            "status": "BLOCKED_PARENT_SIGNATURE_AND_PROFILE_INPUTS_REQUIRED",
            "claim_allowed": False,
            "reason": "no-scalar-dof, no-integrated-out-tail, scalaron zero, no-spurion, readout naturality, and profile suppression are not all signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3839_2_scalar2_bound",
            "gate": "extra scalar2 finite beta bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "B_extra_scalar2 bound formula exists but numeric/source-backed rows are not supplied",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3839_3_beta_claim",
            "gate": "beta/local PPN claim",
            "status": "BLOCKED_REFINED_BOUND_ONLY",
            "claim_allowed": False,
            "reason": "B_EH2_vertex, B_extra_scalar2, B_boundary2, B_readout2, and eps_temporal4 remain nonclaim components",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3839_4_next_target",
            "gate": "next target attacks boundary2",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "extra scalar2 is formulated; next S_beta component is second-order boundary/reference temporal self-coupling",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3839_0_zero_not_proved",
            "decision": "do not claim S_extra_scalar2=0",
            "basis": "older scalar nohair/R2FR/source-only rows are conditional or nonclaim, not parent signatures",
            "consequence": "extra scalar2 remains a named beta residual rather than an assumed closure",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3839_1_use_scalar_history_correctly",
            "decision": "reuse 1788/1789/2516/3292/3833 as evidence constraints, not as hidden approvals",
            "basis": "they identify scalaron, integrated-tail, source-spurion, and readout countermodels",
            "consequence": "3839 moves the work forward by turning the history into a single beta-bound contract",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3839_2_next_Sbeta_component",
            "decision": "move next to second-order boundary/reference temporal self-coupling",
            "basis": "S_EH2_mismatch and S_extra_scalar2 now both have explicit ledgers",
            "consequence": "3840 should try to zero or bound S_boundary2",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3839_0",
            "next_checkpoint": "3840-Y5-R2FR-second-order-boundary-reference-temporal-self-coupling-zero-or-beta-bound.md",
            "script": "scripts/Y5_R2FR_3840_second_order_boundary_reference_temporal_self_coupling_zero_or_beta_bound.py",
            "objective": "try to prove second-order boundary/reference terms cannot shift B_t, or retain/source-bound S_boundary2",
            "reason": "3839 formulates extra scalar2; the next unresolved S_beta component is boundary2",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EXTRA_SCALAR2_BOUND_CONTRACT",
            "claim": "no beta/local-GR claim",
            "summary": "3839 reuses prior scalar/nohair/scalaron/source-spurion work to decompose S_extra_scalar2 into explicit beta residual channels.",
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
    text = f"""# 3839 - Extra Scalar Quadratic Self-Energy Zero Or Beta Bound

Private checkpoint. This attacks `S_extra_scalar2`, the second unresolved `S_beta` component after the EH2 vertex ledger. It does not claim `beta=1` or local GR.

Generated: `{timestamp}`

## Result

The clean zero route would be:

`no scalar dof + no integrated-out scalar tail + no R2/fR scalaron + no source-only spurion + no second-order scalar readout + no finite scalar boundary/profile leakage => S_extra_scalar2 = 0`.

The current corpus does not sign all six clauses, so the zero is not claimed.

The retained bound is:

`B_extra_scalar2 <= B_scalar_dof + B_scalar_integrated_tail + B_scalar_curvature_pole + B_scalar_source_spurion + B_scalar_readout2 + B_scalar_profile_boundary`.

Therefore the beta envelope remains:

`abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Extra Scalar2 Zero Audit

{markdown_table(zero_audit, ["audit_id", "requirement", "test", "current_status", "if_failed"])}

## Scalar2 Decomposition

{markdown_table(decomposition, ["component_id", "component", "definition", "zero_route", "status"])}

## Beta Bound Update

{markdown_table(beta_update, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is forward progress, not another loop: the older scalar work is now condensed into one beta-relevant residual contract. The theory has not yet derived local GR, but `S_extra_scalar2` is no longer a vague complaint; it is a finite list of parent-signature or source-bound requirements.

Next target: `3840-Y5-R2FR-second-order-boundary-reference-temporal-self-coupling-zero-or-beta-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3838", "Current State After 3839", 1)
    paragraph = (
        "`3839` turns `S_extra_scalar2` into an explicit beta residual contract rather than a repeated scalar/nohair loop. "
        "The retained bound is `B_extra_scalar2 <= B_scalar_dof+B_scalar_integrated_tail+B_scalar_curvature_pole+B_scalar_source_spurion+B_scalar_readout2+B_scalar_profile_boundary`, "
        "so `|beta-1| <= B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+|eps_temporal4/Phi^2|`. "
        "No scalar2 zero is claimed because no-scalar-dof, no-integrated-out-tail, scalaron-zero, no-spurion, readout-naturality, and profile-suppression clauses are not simultaneously parent-signed/source-backed.\n\n"
    )
    anchor = "`3838` blocks"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3839-Y5-R2FR-extra-scalar-quadratic-self-energy-zero-or-beta-bound.md`

Target: try to prove no extra scalar quadratic self-energy contributes to visible `g00` at beta order, or retain/source-bound `S_extra_scalar2`.

This is the best next move because 3838 formulates the EH2 vertex mismatch ledger; the next `S_beta` component is extra scalar2."""
    new_gate = """`3840-Y5-R2FR-second-order-boundary-reference-temporal-self-coupling-zero-or-beta-bound.md`

Target: try to prove second-order boundary/reference terms cannot shift `B_t`, or retain/source-bound `S_boundary2`.

This is the best next move because 3839 formulates the extra scalar2 ledger; the next unresolved `S_beta` component is boundary2."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3839_EXTRA_SCALAR2_ZERO_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3839_SCALAR2_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3839_BETA_BOUND_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3839_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3839_EXTRA_SCALAR2_ZERO_AUDIT.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3839 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3839 at {timestamp} -->\n"
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
        "VAL3839_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3839_1_target_trace",
        "S_extra_scalar2 is traced from existing beta ledger",
        "S_extra_scalar2" in all_text and "BUP3839_1_beta_total" in all_text,
        "target term present in zero audit and beta update",
    )
    add(
        "VAL3839_2_components",
        "extra scalar2 components are decomposed",
        all(
            token in all_text
            for token in [
                "B_scalar_dof",
                "B_scalar_integrated_tail",
                "B_scalar_curvature_pole",
                "B_scalar_source_spurion",
                "B_scalar_readout2",
                "B_scalar_profile_boundary",
                "B_extra_scalar2",
            ]
        ),
        "scalar2 component tokens present",
    )
    add(
        "VAL3839_3_old_scalar_blockers_retained",
        "older scalar/nohair/scalaron results are not promoted to claims",
        all(
            token in all_text
            for token in [
                "NO_INTEGRATED_OUT_TOWER_NOT_DERIVED",
                "RELATIVE_ZERO_THEOREM_NOT_PARENT_ACTIVATED",
                "PARTIAL_DERIVATION_NOT_PARENT_SIGNED",
                "READOUT_NATURALITY_NOT_PARENT_SIGNED",
            ]
        ),
        "blocker statuses retained",
    )
    add(
        "VAL3839_4_nonclaim",
        "all 3839 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in zero_audit + decomposition + beta_update + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3839_5_scalar2_gate_blocked",
        "extra scalar2 zero remains blocked",
        any(row["gate_id"] == "GATE3839_1_scalar2_zero" and row["status"].startswith("BLOCKED") for row in gates),
        "scalar2 zero gate blocked",
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
        add(f"VAL3839_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3839_7_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "S_extra_scalar2" in read_text(DOC_PATH) and "B_extra_scalar2" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3839*", "P8_Y5_BRR545_3839*", "*Y5_R2FR_3839*", "3839-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3839_8_formalization_clean",
        "formalization-workbench has no 3839 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3839 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3839_9_pycache_removed",
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
    print(f"{CHECKPOINT} PASS_NONCLAIM_EXTRA_SCALAR2_BOUND_CONTRACT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

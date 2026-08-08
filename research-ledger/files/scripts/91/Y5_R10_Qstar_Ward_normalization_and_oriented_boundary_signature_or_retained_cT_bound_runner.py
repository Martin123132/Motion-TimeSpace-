from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_881_boundary_orientation_shape_found_Qstar_Ward_unit_missing_retained_cT_dry_runner_blocked_nonclaim"
CLAIM_CEILING = "orientation_shape_and_retained_dry_runner_only_no_Qstar_unit_no_parent_Kparent_no_Ptr_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "882-Y5-R10-relative-chain-boundary-owner-and-Qstar-unit-or-retained-cT-minimum-source-pack.md"


SOURCES = [
    {
        "source_id": "880_doc",
        "path": ROOT / "880-Y5-R10-minimal-Qtrace-Qstar-Kparent-action-contract-or-retained-cT-bound.md",
        "needle": "oriented endpoint action",
        "role": "immediate oriented endpoint/Qstar handoff",
    },
    {
        "source_id": "880_validation",
        "path": OUT / "P8_Y5_BRR545_880_VALIDATION.csv",
        "needle": "V880_13_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "109_boundary_charge",
        "path": ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needle": "relative_boundary_language_exists",
        "role": "relative boundary language and Qstar failure",
    },
    {
        "source_id": "110_endpoint_equation",
        "path": ROOT / "110-endpoint-charge-equation-attempt.md",
        "needle": "27 R^2 - 12 R + 1",
        "role": "endpoint equation and Qstar failure",
    },
    {
        "source_id": "111_variational_owner",
        "path": ROOT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needle": "endpoint_arrow_derived",
        "role": "formal potential and arrow blocker",
    },
    {
        "source_id": "337_exact_readout",
        "path": ROOT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needle": "q_trace = 2/27",
        "role": "exact readout/trace normalization candidate",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero",
        "role": "readout not physical spurion rule",
    },
    {
        "source_id": "356_Ward_identity",
        "path": ROOT / "356-parent-action-ward-identity-and-projector-variation.md",
        "needle": "F_boundary^nu",
        "role": "explicit Ward force-channel ledger",
    },
    {
        "source_id": "862_trace_lift",
        "path": ROOT / "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md",
        "needle": "DeltaQ_trace/Q_*",
        "role": "trace-lift/Qstar endpoint bridge",
    },
    {
        "source_id": "863_Ward_trace",
        "path": ROOT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needle": "Q_* = unit(J_trace,parent)",
        "role": "Qstar unit and local projection blocker",
    },
    {
        "source_id": "864_split",
        "path": ROOT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needle": "endpoint arrow",
        "role": "local/global split, endpoint arrow, and Qstar blockers",
    },
    {
        "source_id": "875_schema",
        "path": OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv",
        "needle": "IN875_0_Z_T",
        "role": "retained cT runner coefficient schema",
    },
    {
        "source_id": "880_queue",
        "path": OUT / "P8_Y5_R10_880_RETAINED_CT_BOUND_QUEUE.csv",
        "needle": "RCB880_0_cT",
        "role": "retained cT/Ztr/lambdatr/Jtr queue",
    },
    {
        "source_id": "97_canonical_R",
        "path": ROOT / "97-canonical-R-theorem-attempt.md",
        "needle": "Q_* fixes the unit boundary charge scale",
        "role": "canonical R/Qstar theorem blocker",
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
            "what_changed": "separated boundary orientation from physical endpoint arrow, audited Q_* Ward normalization, and executed the retained c_T branch as a dry runner that refuses claims with missing inputs",
            "best_partial_result": "relative/oriented boundary structure can explain why an endpoint action has opposite signs between early and today surfaces, so the diag(6,6) endpoint Hessian is no longer pure algebra if a parent relative-chain owner is signed",
            "hard_blockers": "Q_* Ward charge unit, parent owner for the relative boundary chain, physical arrow assigning 1/3 to early and 1/9 to today, full K_parent extension, local no-hair/source-cokernel, numeric retained c_T coefficients",
            "what_is_not_claimed": "Q_* derivation, endpoint prediction, parent K_parent, P_tr/H_tr promotion, c_T=0, retained c_T pass, R10/PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def orientation_signature_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "signature_id": "OS881_0_boundary_sign",
            "object": "oriented relative boundary",
            "candidate_derivation": "for an oriented spacetime/relative chain, boundary evaluations enter as future/outer minus past/inner or early minus today depending on chosen cobordism orientation",
            "effect_on_880": "explains the sign pattern S_trace=Q_*^2[U(R_early)-U(R_today)] without using two unrelated potentials",
            "status": "derivation_shape_found_parent_owner_missing",
            "claim_gap": "corpus has relative boundary language but not a parent-signed relative-chain action owner",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "OS881_1_endpoint_arrow",
            "object": "physical arrow R_early=1/3 to R_today=1/9",
            "candidate_derivation": "orientation gives a subtraction order; a relaxation/entropy/expansion arrow would have to choose the high root as early and low root as today",
            "effect_on_880": "DeltaR positive can be made meaningful only if root assignment is owned before cosmology scoring",
            "status": "not_derived",
            "claim_gap": "111 explicitly leaves endpoint_arrow_derived failed; 864 also lists endpoint arrow as not parent derived",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "OS881_2_endpoint_Hessian",
            "object": "K_endpoint sign",
            "candidate_derivation": "orientation changes the today endpoint second variation from U''(1/9)=-6 to -U''(1/9)=+6",
            "effect_on_880": "conditional endpoint block is K_endpoint=diag(6,6), avoiding an immediate wrong-sign endpoint mode",
            "status": "conditional_pass_if_OS881_0_and_OS881_1_signed",
            "claim_gap": "positive endpoint block is not the full K_parent/pseudo-inverse and does not prove local silence",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "OS881_3_readout_spurion_guard",
            "object": "boundary/readout label versus physical spurion",
            "candidate_derivation": "endpoint/readout terms must be post-variation or source-at-zero unless the action owns their stress and local projection",
            "effect_on_880": "prevents the oriented endpoint action from quietly adding a local material defect",
            "status": "guard_imported_not_closed",
            "claim_gap": "338 leaves parent proof of probe-not-spurion open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "OS881_4_orientation_verdict",
            "object": "boundary orientation signature",
            "candidate_derivation": "relative-chain orientation is the best non-ad-hoc source of the 880 sign flip",
            "effect_on_880": "orientation route remains alive and sharpened, but not promoted",
            "status": "partial_progress_nonclaim",
            "claim_gap": "need parent action owner for the relative chain plus physical arrow root assignment",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def qstar_ward_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "QW881_0_exact_readout",
            "object": "q_trace=2/27",
            "candidate_source": "337/338 exact parent readout",
            "candidate_formula": "q_trace=Tr(P_active H_parent)/27=2/27 under exact parent readout",
            "status": "conditional_available",
            "claim_gap": "exact readout branch does not by itself define the boundary charge unit Q_*",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "QW881_1_trace_lift",
            "object": "DeltaQ_trace/Q_*",
            "candidate_source": "862/863 trace-lift theorem shape",
            "candidate_formula": "DeltaQ_trace/Q_* = q_1+q_2+q_3 = 3 q_trace",
            "status": "conditional_algebra_available",
            "claim_gap": "requires J_trace current ownership, endpoint identification, and Q_* unit",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "QW881_2_Qstar_norm",
            "object": "Q_*",
            "candidate_source": "863 Q_* = unit(J_trace,parent), 97/109 normalized boundary charge",
            "candidate_formula": "Q_* := norm or unit charge of the parent trace Ward current",
            "status": "missing_parent_normalization",
            "claim_gap": "Ward conservation can preserve a charge, but the corpus does not yet supply its absolute unit/norm or calibration-independent scale",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "QW881_3_Ward_force_channel",
            "object": "F_boundary^nu / J_trace",
            "candidate_source": "356 explicit Ward force-channel ledger",
            "candidate_formula": "F_boundary^nu is explicit, so boundary charge cannot be hidden inside E_MTS",
            "status": "ledger_available_not_normalization",
            "claim_gap": "ledger tells us where a boundary force must live, not the Q_* unit or no-hair value",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "QW881_4_Qstar_verdict",
            "object": "Q_* Ward normalization",
            "candidate_source": "whole Qstar audit",
            "candidate_formula": "derive Q_* before data scoring or demote trace amplitude to retained/closure branch",
            "status": "not_derived",
            "claim_gap": "Q_* remains the main numerical-theorem blocker for promoting DeltaR=2/9",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def endpoint_to_projector_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "map_id": "EP881_0_endpoint_block",
            "input": "oriented endpoint action plus fixed Q_*",
            "formal_output": "ell_tr=(dQ_early-dQ_today)/Q_* and K_endpoint=diag(6,6)",
            "status": "conditional_endpoint_block",
            "claim_gap": "Q_* and parent relative-chain owner missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "map_id": "EP881_1_projector",
            "input": "K_endpoint extended to full K_parent quotient pairing",
            "formal_output": "v_tr=K_parent^-1 ell_tr/<ell_tr,K_parent^-1 ell_tr>; P_tr=v_tr tensor ell_tr",
            "status": "blocked_missing_Kparent_extension",
            "claim_gap": "endpoint block alone cannot raise the covector on full parent tangent space",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "map_id": "EP881_2_local_zero",
            "input": "P_tr plus local/global quotient split",
            "formal_output": "Dq_loc[U][v_tr]=0 and P_loc J_trace=0",
            "status": "blocked_missing_local_nohair",
            "claim_gap": "trace endpoint can still leak into local PPN/WEP/clock/orbital channels",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "map_id": "EP881_3_projector_verdict",
            "input": "881 orientation and Qstar audit",
            "formal_output": "no P_tr/H_tr promotion in current corpus",
            "status": "not_promoted",
            "claim_gap": "orientation progress is not enough without Q_*, K_parent, and no-hair",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def retained_ct_dry_runner_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "dry_id": "DR881_0_load_queue",
            "runner_step": "load retained c_T queue from 880",
            "required_inputs": "c_T,Z_tr,lambda_tr,J_tr,tau_R10,tau_PPN,tau_clock_WEP,tau_orbital",
            "observed_inputs": "all rows remain MISSING_PARENT_* or MISSING_*",
            "dry_result": "loaded_but_invalid_for_claim",
            "next_action": "source parent coefficients or prove zero theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dry_id": "DR881_1_R10",
            "runner_step": "R10 alpha(lambda) comparison",
            "required_inputs": "Z_tr,lambda_tr,source charges,real alpha(lambda) bound curve",
            "observed_inputs": "MISSING_PARENT_HESSIAN_OR_NOPOLE and MISSING_SOURCE_PROJECTION",
            "dry_result": "blocked_no_numeric_run",
            "next_action": "fill retained trace source row or prove P_loc J_trace=0",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dry_id": "DR881_2_PPN",
            "runner_step": "PPN gamma/beta/source-normalized Newtonian residual",
            "required_inputs": "metric response operator, GM absorption/source normalization, trace charge response",
            "observed_inputs": "MISSING_RESPONSE_OPERATOR",
            "dry_result": "blocked_no_numeric_run",
            "next_action": "derive metric response from H_tr/J_tr or keep PPN branch open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dry_id": "DR881_3_clock_WEP",
            "runner_step": "clock/WEP species-marker residual",
            "required_inputs": "no-marker theorem or species trace charge response",
            "observed_inputs": "MISSING_NO_MARKER_RESULT",
            "dry_result": "blocked_no_numeric_run",
            "next_action": "prove matter constants factor through q_loc or source material response rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dry_id": "DR881_4_orbital",
            "runner_step": "finite-range orbital/GM-drift residual",
            "required_inputs": "alpha_tr(lambda),lambda_tr,source geometry,GM absorption proof",
            "observed_inputs": "MISSING_ORBITAL_PROJECTION",
            "dry_result": "blocked_no_numeric_run",
            "next_action": "fill orbital projection only after trace carrier/source exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dry_id": "DR881_5_verdict",
            "runner_step": "retained c_T runner claim gate",
            "required_inputs": "all retained inputs numeric, source-backed, and valid_for_claim=true",
            "observed_inputs": "no retained input satisfies claim requirements",
            "dry_result": "claim_refused_correctly",
            "next_action": "either parent-sign zero route or build minimum executable retained source pack",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC881_0_selected",
            "route": "relative_chain_boundary_owner_and_Qstar_unit_or_retained_cT_minimum_source_pack",
            "status": "selected",
            "reason": "881 found a plausible non-ad-hoc source for the orientation sign, but Q_* and the parent owner of the relative chain are still missing; retained c_T dry-run refuses claims until numeric/source inputs exist",
            "include": "relative chain owner, Q_* Ward unit, physical endpoint arrow, K_parent extension, minimum retained c_T source pack if derivation fails",
            "exclude": "claiming DeltaR, local-GR/Newton pass, R10/PPN pass, fitted coefficients, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG881_0_no_Qstar_claim",
            "claim": "Q_* is Ward-normalized",
            "status": "forbidden",
            "reason": "the audit still finds no parent norm/unit for J_trace",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG881_1_no_endpoint_arrow_claim",
            "claim": "the physical endpoint arrow is derived",
            "status": "forbidden",
            "reason": "orientation suggests a sign structure but not the high-root-to-low-root cosmological arrow",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG881_2_no_Kparent_claim",
            "claim": "full K_parent exists",
            "status": "forbidden",
            "reason": "endpoint K_endpoint does not supply a quotient tangent-space pairing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG881_3_no_retained_bound_pass",
            "claim": "retained c_T passes local bounds",
            "status": "forbidden",
            "reason": "the dry runner has only missing symbolic inputs and correctly refuses numeric scoring",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG881_4_no_local_GR_claim",
            "claim": "MTS locally reduces to GR/Newton",
            "status": "forbidden",
            "reason": "trace branch still lacks Q_*, K_parent, no-hair, source-cokernel, and other local residual closures",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG881_5_allowed_private_result",
            "claim": "orientation sign source has been sharpened to relative-chain ownership",
            "status": "allowed_private_nonclaim",
            "reason": "this is useful derivation progress but remains a theorem target",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D881_0",
            "finding": "orientation_shape_found",
            "reason": "relative/oriented boundary structure can naturally supply the sign flip used in 880 if parent-owned",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D881_1",
            "finding": "Qstar_not_derived",
            "reason": "exact readout and trace lift supply conditional ratios, but no parent norm/unit for Q_*",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D881_2",
            "finding": "retained_cT_runner_refuses_claim",
            "reason": "all retained trace inputs remain missing, so no local-bound score can be claimed",
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
            "objective": "try to parent-own the relative-chain boundary object that supplies the orientation sign and Q_* unit; if that fails, build the minimum executable retained c_T source pack rather than claiming a derived zero",
            "include": "relative-chain action owner, boundary orientation, Q_* charge norm, endpoint arrow, retained c_T minimum source inputs",
            "exclude": "R10/local-GR pass, fitted endpoint values, public claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_880_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_880_VALIDATION.csv"
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


def retained_queue_missing() -> bool:
    path = OUT / "P8_Y5_R10_880_RETAINED_CT_BOUND_QUEUE.csv"
    if not path.exists():
        return False
    rows = read_csv(path)
    return rows and all("MISSING" in row.get("current_value", "") for row in rows)


def validation_rows(
    source_rows: list[dict[str, object]],
    orientation_rows: list[dict[str, object]],
    qstar_rows: list[dict[str, object]],
    projector_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_sets = [
        source_rows,
        orientation_rows,
        qstar_rows,
        projector_rows,
        dry_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    orientation_shape = any(row.get("signature_id") == "OS881_0_boundary_sign" and "shape" in row.get("status", "") for row in orientation_rows)
    arrow_blocked = any(row.get("signature_id") == "OS881_1_endpoint_arrow" and row.get("status") == "not_derived" for row in orientation_rows)
    qstar_missing = any(row.get("audit_id") == "QW881_4_Qstar_verdict" and row.get("status") == "not_derived" for row in qstar_rows)
    dry_claim_refused = any(row.get("dry_id") == "DR881_5_verdict" and row.get("dry_result") == "claim_refused_correctly" for row in dry_rows)
    projector_not_promoted = any(row.get("map_id") == "EP881_3_projector_verdict" and row.get("status") == "not_promoted" for row in projector_rows)
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = route_rows_[0]["status"] == "selected" and next_target_rows_[0]["next_target"] == NEXT_TARGET
    fw_count = formalization_changed_count()
    checks = [
        ("V881_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V881_1_prior_880_clean", prior_880_clean(), "P8_Y5_BRR545_880_VALIDATION.csv clean"),
        ("V881_2_orientation_shape_found", orientation_shape, "relative/oriented boundary sign route recorded"),
        ("V881_3_endpoint_arrow_blocked", arrow_blocked, "physical high-root-to-low-root arrow remains not derived"),
        ("V881_4_Qstar_not_derived", qstar_missing, "Q_* Ward normalization remains missing"),
        ("V881_5_projector_not_promoted", projector_not_promoted, "P_tr/H_tr not promoted from endpoint block"),
        ("V881_6_retained_queue_missing_inputs", retained_queue_missing(), "880 retained c_T queue contains only missing inputs"),
        ("V881_7_retained_dry_runner_refuses_claim", dry_claim_refused, "dry runner refuses local-bound claim"),
        ("V881_8_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V881_9_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V881_10_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V881_11_route_selected", route_selected, NEXT_TARGET),
        ("V881_12_validation_rows_ready", True, "validation table constructed"),
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
    orientation_rows: list[dict[str, object]],
    qstar_rows: list[dict[str, object]],
    projector_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 881 - Y5/R10 Qstar Ward Normalization and Oriented Boundary Signature or Retained cT Bound Runner",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the boundary sign has a plausible parent-geometry route, but `Q_*` still does not**. "
        "A relative/oriented boundary chain can naturally explain why the endpoint action appears as "
        "`U(R_early)-U(R_today)`, which is exactly the sign needed for the 880 endpoint Hessian "
        "`K_endpoint=diag(6,6)`. However, orientation is not yet the same thing as the physical arrow: "
        "the corpus still has to own why the high root `1/3` is early and the low root `1/9` is today. "
        "The Ward audit also does not derive `Q_*`; exact readout gives a conditional ratio `q_trace=2/27`, "
        "and trace lift gives conditional `DeltaQ_trace/Q_*=3q_trace`, but no parent norm/unit for `J_trace`. "
        "The retained `c_T` runner was therefore executed only as a dry gate, and it correctly refuses any local-bound claim because all trace coefficients remain missing.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Orientation Signature Audit",
        md_table(orientation_rows),
        "",
        "## Qstar Ward Audit",
        md_table(qstar_rows),
        "",
        "## Endpoint To Projector Map",
        md_table(projector_rows),
        "",
        "## Retained cT Dry Runner",
        md_table(dry_rows),
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
    orientation_rows = orientation_signature_rows(generated_utc)
    qstar_rows = qstar_ward_audit_rows(generated_utc)
    projector_rows = endpoint_to_projector_rows(generated_utc)
    dry_rows = retained_ct_dry_runner_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        orientation_rows,
        qstar_rows,
        projector_rows,
        dry_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_881_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_881_ORIENTATION_SIGNATURE_AUDIT.csv": orientation_rows,
        "P8_Y5_R10_881_QSTAR_WARD_AUDIT.csv": qstar_rows,
        "P8_Y5_R10_881_ENDPOINT_TO_PROJECTOR_MAP.csv": projector_rows,
        "P8_Y5_R10_881_RETAINED_CT_DRY_RUNNER.csv": dry_rows,
        "P8_Y5_R10_881_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_881_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_881_DECISION.csv": decision_rows_,
        "P8_Y5_R10_881_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_881_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_881_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "881-Y5-R10-Qstar-Ward-normalization-and-oriented-boundary-signature-or-retained-cT-bound-runner.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        orientation_rows,
        qstar_rows,
        projector_rows,
        dry_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_881_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

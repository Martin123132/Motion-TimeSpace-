from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "784-Y5-R10-observed-metric-from-psi-map-or-coupling-owner-demotion.md"
NEXT_TARGET = "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md"
STATUS = "Y5_R10_784_observed_metric_from_psi_partial_pass_coframe_connection_action_missing_owner_route_narrowed_nonclaim"
CLAIM_CEILING = "observed_metric_from_psi_gate_only_partial_metric_anchor_no_coframe_connection_action_owner_no_coupling_zero_no_local_GR_Newton_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_784_SOURCE_REGISTER.csv"
METRIC_GATE_PATH = RESIDUALS / "P8_Y5_R10_784_OBSERVED_METRIC_FROM_PSI_GATE.csv"
COFRAME_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_784_COFRAME_CONNECTION_REQUIREMENTS.csv"
OWNER_DEMOTION_PATH = RESIDUALS / "P8_Y5_R10_784_OWNER_ROUTE_DEMOTION_DECISION.csv"
RESIDUAL_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_784_RESIDUAL_INTERFACE_UPDATE.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_784_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_784_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_784_PSI_METRIC_OWNER_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_784_COUPLING_OWNER_ADOPTION.csv",
    RESIDUALS / "P8_Y5_R10_784_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    METRIC_GATE_PATH,
    COFRAME_REQUIREMENTS_PATH,
    OWNER_DEMOTION_PATH,
    RESIDUAL_UPDATE_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "783_doc": {
        "path": POST_CHECKPOINT / "783-Y5-R10-coupling-owner-field-map-to-MTS-spine-or-residual-interface-runner.md",
        "needles": ["FM783_2_e_obs", "784-Y5-R10-observed-metric-from-psi-map-or-coupling-owner-demotion.md"],
        "role": "immediate 784 handoff",
    },
    "783_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_783_VALIDATION.csv",
        "needles": ["V783_4_metric_partial_anchor", "V783_8_not_adopted"],
        "role": "prior validation guard",
    },
    "783_field_map": {
        "path": RESIDUALS / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv",
        "needles": ["FM783_2_e_obs", "strongest_partial_alignment"],
        "role": "field map handoff",
    },
    "ledger_14": {
        "path": FORMALIZATION / "14-field-definitions-dimensional-ledger.md",
        "needles": ["g_μν = η_μν + L_*²", "[ψ] = 1"],
        "role": "metric ansatz and dimensions",
    },
    "postulates_18": {
        "path": FORMALIZATION / "18-sign-conventions-and-field-postulates.md",
        "needles": ["G_μν = κ_GR T_total", "Q^ν = ∇_μ T_matter"],
        "role": "Einstein convention and exchange postulates",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["ψ", "g_μν", "MTS parent theory -> effective GR"],
        "role": "spine metric and limit standard",
    },
    "testing_145": {
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": ["MTS -> GR -> Newton", "missing GR-limit theorem"],
        "role": "GR-limit demand",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCE_SPECS.items()
    ]


def metric_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "OMG784_0_dimension",
            "gate": "Dimensional consistency of g_obs = eta + L_*^2 <partial psi partial psi>.",
            "test": "[psi]=1, [partial psi]=L^-1, [L_*^2 partial psi partial psi]=1",
            "result": "pass_formal",
            "what_it_gives": "dimensionless metric perturbation candidate",
            "missing_before_claim": "normalization and universality of L_*",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OMG784_1_symmetry",
            "gate": "Metric symmetry.",
            "test": "<partial_mu psi partial_nu psi> is symmetric in mu,nu for scalar psi after smoothing",
            "result": "pass_formal",
            "what_it_gives": "symmetric rank-2 tensor candidate",
            "missing_before_claim": "smoothing operator covariance and gauge/frame definition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OMG784_2_signature",
            "gate": "Lorentz signature and nondegeneracy.",
            "test": "det(g_obs) != 0 and signature(g_obs)=(-,+,+,+)",
            "result": "not_guaranteed",
            "what_it_gives": "condition, not theorem",
            "missing_before_claim": "bounds on L_*^2 <partial psi partial psi> or construction preserving Lorentz signature",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OMG784_3_covariance",
            "gate": "Diffeomorphism/covariant definition.",
            "test": "eta_mu_nu and coordinate smoothing must be replaced by a covariant background/renormalized operator or derived effective metric",
            "result": "blocked",
            "what_it_gives": "identifies the core mathematical gap",
            "missing_before_claim": "covariant smoothing/coarse-graining operator and background independence rule",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OMG784_4_coframe",
            "gate": "Observed coframe/tetrad exists and is matter-owned.",
            "test": "find e_obs such that g_obs=e_obs^T eta e_obs and matter uses this e_obs only",
            "result": "open",
            "what_it_gives": "local tetrad exists only if metric is Lorentzian and oriented/time-oriented",
            "missing_before_claim": "explicit tetrad branch, spin connection, orientation, and no hidden matter frame",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OMG784_5_connection",
            "gate": "Compatible connection and derivative stack.",
            "test": "omega_m and D_m must be functions of e_obs plus owned gauge fields",
            "result": "open",
            "what_it_gives": "matter derivative descent target",
            "missing_before_claim": "Levi-Civita/spin connection or torsion/nonmetricity ownership",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OMG784_6_action_owner",
            "gate": "Parent action derives the metric map.",
            "test": "Euler equations of S_parent imply or extremize the psi-to-metric relation",
            "result": "not_derived",
            "what_it_gives": "metric ansatz remains kinematic",
            "missing_before_claim": "parent action or constraint/gauge theorem deriving g_obs[psi]",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OMG784_7_GR_limit",
            "gate": "Metric map yields Einstein/GR then Newton.",
            "test": "g_obs[psi] dynamics -> G_mu_nu=kappa_GR T_total -> weak-field Newton",
            "result": "not_sufficient",
            "what_it_gives": "metric candidate only",
            "missing_before_claim": "Einstein equation derivation, stress map, PPN vector, q_loc/Y5/Y6/boundary closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OMG784_8_verdict",
            "gate": "Promote observed metric from psi as coupling owner anchor?",
            "test": "all gates OMG784_0..OMG784_7 close",
            "result": "partial_anchor_not_owner",
            "what_it_gives": "best next subproblem, not a parent coupling owner",
            "missing_before_claim": "coframe/connection/action/covariance/GR-limit gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coframe_requirement_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "req_id": "CCR784_0_lorentzian_metric",
            "requirement": "g_obs must be Lorentzian and nondegenerate",
            "why_needed": "otherwise no physical rods/clocks/light cones",
            "acceptance_gate": "signature theorem or controlled perturbative domain",
            "fallback": "retain b_g/c_g residual and no owner adoption",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "req_id": "CCR784_1_tetrad_branch",
            "requirement": "choose e_obs with g_obs=e_obs^T eta e_obs",
            "why_needed": "matter and spinors couple to coframe/connection, not just metric prose",
            "acceptance_gate": "explicit tetrad construction with local Lorentz gauge handled",
            "fallback": "readout/frame residual remains",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "req_id": "CCR784_2_connection",
            "requirement": "define omega[e_obs] and D[e_obs,A_owned]",
            "why_needed": "derivative couplings can reintroduce hidden representative data",
            "acceptance_gate": "Levi-Civita/spin connection or owned torsion/nonmetricity rows",
            "fallback": "connection leakage residual remains",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "req_id": "CCR784_3_covariant_smoothing",
            "requirement": "make <partial psi partial psi>_smooth covariant",
            "why_needed": "fixed coordinate smoothing would not define a parent covariant field theory",
            "acceptance_gate": "bitensor/kernel/coarse-graining rule or local EFT operator with covariance proof",
            "fallback": "metric map remains kinematic ansatz",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "req_id": "CCR784_4_matter_blindness",
            "requirement": "matter sees e_obs only, not psi gradients independently",
            "why_needed": "direct psi-matter terms would re-open the coupling residual",
            "acceptance_gate": "S_matter[Psi,e_obs,theta] with no direct psi, Gamma_mem, chi, or q_loc dependence",
            "fallback": "b_g/b_theta/C_qmu interface remains active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "req_id": "CCR784_5_action_derivation",
            "requirement": "metric map is derived from parent action or owned constraint",
            "why_needed": "otherwise the owner action is a repair ansatz",
            "acceptance_gate": "Euler/constraint/gauge derivation of g_obs[psi]",
            "fallback": "demote coupling owner route to empirical interface",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def owner_demotion_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "ODD784_0_metric_anchor",
            "decision": "retain observed metric from psi as the strongest derivation subproblem",
            "reason": "dimension and symmetry gates pass formally, and the ansatz is already in the field ledger",
            "result": "retain_subproblem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "ODD784_1_owner_route",
            "decision": "do not adopt coupling owner route yet",
            "reason": "coframe, connection, covariance, action ownership, and GR/Newton limit are missing",
            "result": "not_adopted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "ODD784_2_demotion_rule",
            "decision": "demote owner route if 785 cannot derive coframe/connection/action ownership",
            "reason": "without those, e_obs[psi] is only a metric ansatz and b_g/c_g remains live",
            "result": "conditional_demotion_rule_set",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "ODD784_3_next_target",
            "decision": "try psi-metric coframe/connection contract or lock b_g residual",
            "reason": "this is the smallest hard theorem needed by the coupling owner branch",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def residual_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RUP784_0_b_g",
            "coefficient": "b_g/c_g",
            "update": "stays live until e_obs[psi] coframe/connection/action ownership closes",
            "why": "metric ansatz does not prove matter-frame blindness",
            "next_input": "coframe/connection contract or finite frame-response bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RUP784_1_C_qmu",
            "coefficient": "C_qmu",
            "update": "unchanged active residual",
            "why": "q_loc/R_phys remains diagnostic and not part of e_obs[psi] derivation",
            "next_input": "q_loc theorem-zero/profile plus source-measure coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RUP784_2_W_Ic",
            "coefficient": "W_Ic",
            "update": "unchanged active residual",
            "why": "PPN/readout response needs separate gauge/frame certificate",
            "next_input": "PPN coupling response matrix or theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "observed metric from psi passes formal dimension/symmetry checks but fails as owner because covariance, coframe, connection, action derivation, and GR/Newton limit are missing",
            "hard_blocker": "e_obs[psi] is a kinematic metric ansatz until coframe/connection/action ownership is derived",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    metric_gates: list[dict[str, Any]],
    coframe: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_783_clean = all(validation_clean(number) for number in range(665, 784))
    metric_gate_complete = len(metric_gates) == 9
    formal_passes_recorded = sum(1 for row in metric_gates if row["result"] == "pass_formal") >= 2
    covariance_blocked = any(row["gate_id"] == "OMG784_3_covariance" and row["result"] == "blocked" for row in metric_gates)
    owner_not_promoted = any(row["gate_id"] == "OMG784_8_verdict" and row["result"] == "partial_anchor_not_owner" for row in metric_gates)
    coframe_requirements_complete = len(coframe) == 6
    demotion_complete = len(demotion) == 4
    demotion_rule_set = any(row["decision_id"] == "ODD784_2_demotion_rule" for row in demotion)
    residual_update_complete = len(residuals) == 3
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "ODD784_3_next_target" for row in demotion)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, metric_gates, coframe, demotion, residuals, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V784_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V784_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V784_2_prior_665_783_clean", prior_665_783_clean, "665-783 validation rows have no failures"),
        ("V784_3_metric_gate_complete", metric_gate_complete, "observed metric gate rows complete"),
        ("V784_4_formal_passes_recorded", formal_passes_recorded, "dimension and symmetry formal passes recorded"),
        ("V784_5_covariance_blocked", covariance_blocked, "covariance gap blocks owner claim"),
        ("V784_6_owner_not_promoted", owner_not_promoted, "metric anchor not promoted to owner"),
        ("V784_7_coframe_requirements_complete", coframe_requirements_complete, "coframe/connection requirements complete"),
        ("V784_8_demotion_complete", demotion_complete, "demotion decision rows complete"),
        ("V784_9_demotion_rule_set", demotion_rule_set, "conditional demotion rule recorded"),
        ("V784_10_residual_update_complete", residual_update_complete, "residual interface update complete"),
        ("V784_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V784_12_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V784_13_claim_artifacts_absent", claim_artifacts_absent, "no metric-owner/coupling-owner/local-GR claim artifact fabricated"),
        ("V784_14_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V784_15_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V784_16_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    metric_gates: list[dict[str, Any]],
    coframe: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 784 - Y5 R10 Observed Metric From Psi Map Or Coupling Owner Demotion

Current result: **the observed metric from `psi` is a useful partial anchor, not a coupling-owner proof**. The metric ansatz passes formal dimension and symmetry checks, but it does not yet provide a covariant coframe/connection/action owner or derive the GR/Newton limit. So the next move is narrow: either derive the `psi -> g_obs -> e_obs -> omega/D_m` chain properly, or demote the coupling owner route and keep `b_g/c_g` live.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Observed Metric From Psi Gate

{markdown_table(metric_gates, ["gate_id", "gate", "test", "result", "what_it_gives", "missing_before_claim", "valid_for_claim"])}

## Coframe Connection Requirements

{markdown_table(coframe, ["req_id", "requirement", "why_needed", "acceptance_gate", "fallback", "valid_for_claim"])}

## Owner Route Demotion Decision

{markdown_table(demotion, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Residual Interface Update

{markdown_table(residuals, ["residual_id", "coefficient", "update", "why", "next_input", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is useful, but it is not a free bridge to GR. The metric ansatz is the best anchor we have for the coupling-owner route because it touches the actual MTS spine. But unless 785 can provide the coframe, connection, covariance, and parent-action ownership, the honest move is to keep `b_g/c_g` as a residual rather than pretending the matter frame is solved.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    metric_gates = metric_gate_rows(generated_utc)
    coframe = coframe_requirement_rows(generated_utc)
    demotion = owner_demotion_rows(generated_utc)
    residuals = residual_update_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, metric_gates, coframe, demotion, residuals, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(METRIC_GATE_PATH, metric_gates, ["gate_id", "gate", "test", "result", "what_it_gives", "missing_before_claim", "valid_for_claim", "generated_utc"])
    write_csv(COFRAME_REQUIREMENTS_PATH, coframe, ["req_id", "requirement", "why_needed", "acceptance_gate", "fallback", "valid_for_claim", "generated_utc"])
    write_csv(OWNER_DEMOTION_PATH, demotion, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUAL_UPDATE_PATH, residuals, ["residual_id", "coefficient", "update", "why", "next_input", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, metric_gates, coframe, demotion, residuals, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"784 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()

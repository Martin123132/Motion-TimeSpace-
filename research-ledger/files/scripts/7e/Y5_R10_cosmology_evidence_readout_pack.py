from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "844-Y5-R10-cosmology-evidence-readout-pack.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_844_SOURCE_REGISTER.csv"
EVIDENCE_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_844_COSMOLOGY_EVIDENCE_LEDGER.csv"
GATE_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_844_COSMOLOGY_GATE_LEDGER.csv"
AMPLITUDE_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_844_AMPLITUDE_STATUS_LEDGER.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_844_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_844_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_844_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_844_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_844_VALIDATION.csv"

STATUS = "Y5_R10_844_cosmology_alive_as_constraint_C0_closure_benchmark_nonclaim"
CLAIM_CEILING = "cosmology_constraint_clue_no_support_no_death_no_fundamental_claim"
NEXT_TARGET = "845-Y5-R10-strict-MTS-cosmology-branch-contract.md"

SOURCE_SPECS = [
    {
        "source_id": "843_doc",
        "path": POST_CHECKPOINT / "843-Y5-R10-testing-readiness-and-GR-limit-map.md",
        "needles": [
            "Cosmology is selected as the first near-term empirical readout",
            "844-Y5-R10-cosmology-evidence-readout-pack.md",
            "Local GR/PPN remains a closure guardrail only.",
        ],
        "role": "empirical pillar selection handoff",
    },
    {
        "source_id": "843_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_843_VALIDATION.csv",
        "needles": [
            "V843_6_cosmology_selected_first,pass",
            "V843_8_all_rows_nonclaim,pass",
            "V843_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "147_cosmology_evidence_readout",
        "path": FORMALIZATION / "147-cosmology-evidence-readout-pack.md",
        "needles": [
            "phenomenological_constraint_clue",
            "effective_FLRW_projection_survives",
            "raw_M4_M6_not_stable_evidence",
            "mixed_validation_not_claimable",
        ],
        "role": "background-cosmology evidence readout",
    },
    {
        "source_id": "155_Hz_covariance_status",
        "path": FORMALIZATION / "155-cosmology-status-after-Hz-covariance.md",
        "needles": [
            "phenomenological_constraint_clue_with_Hz_non_support",
            "H(z) does not rescue M6.",
            "derive the growth/CMB consistency contract before any more cosmology data fits.",
        ],
        "role": "direct H(z) and covariance status",
    },
    {
        "source_id": "173_joint_growth_CMB_radflat",
        "path": FORMALIZATION / "173-joint-growth-CMB-radflat-readout.md",
        "needles": [
            "joint_growth_CMB_radflat_internal_viability_survives_bmem_law_next",
            "C0 frozen joint Delta AIC is 3.317309;",
            "public support claim remains blocked;",
        ],
        "role": "joint growth/CMB radflat readout",
    },
    {
        "source_id": "175_full_joint_radflat_fit",
        "path": FORMALIZATION / "175-full-joint-radflat-phenomenology-fit.md",
        "needles": [
            "full_joint_radflat_phenomenology_C0_bmem_not_stable",
            "C0 frozen is near-competitive by AIC;",
            "b_mem positive-and-stable gate.",
            "no support claim is allowed;",
        ],
        "role": "full joint radflat phenomenology fit",
    },
    {
        "source_id": "176_C0_demotion_decision",
        "path": FORMALIZATION / "176-C0-radflat-demotion-decision.md",
        "needles": [
            "C0_demoted_to_closure_benchmark_parent_amplitude_repair_required",
            "C0_frozen_delta_AIC_vs_best_baseline = 0.36437287900487547",
            "C0_b_mem_fractional_shift = 6.148693776912986",
            "177-parent-amplitude-repair-contract.md",
        ],
        "role": "C0 demotion decision",
    },
    {
        "source_id": "178_parent_amplitude_attempt",
        "path": FORMALIZATION / "178-parent-amplitude-theorem-attempt.md",
        "needles": [
            "parent_amplitude_theorem_partial_corridor_not_prediction",
            "amplitude corridor derived = true",
            "amplitude prediction derived = false",
            "179-strict-MTS-cosmology-branch-contract.md",
        ],
        "role": "latest parent-amplitude theorem attempt",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def evidence_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "evidence_id": "E844_0_FLRW_projection",
            "source": "147",
            "finding": "effective FLRW memory-fluid projection survives",
            "numeric_or_formula": "E(z)^2=Omega_m0(1+z)^3+Omega_Gamma(z); Omega_Gamma=1-Omega_m0+b_mem F(z)",
            "status": "survives_as_effective_mathematical_object",
            "interpretation": "internally coherent background-fluid construction",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "evidence_id": "E844_1_noSH0ES_compressed_memory",
            "source": "147",
            "finding": "M6_min_edge_free_shape compressed no-SH0ES branch is a hint",
            "numeric_or_formula": "chi2=1464.30212537; AIC=1472.30212537; BIC=1493.90460768; vs wCDM Delta AIC=-0.39981263; vs CPL Delta BIC=-7.38293835",
            "status": "survives_as_hint_not_claim",
            "interpretation": "background shape is interesting but not stable evidence",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "evidence_id": "E844_2_raw_M4_M6",
            "source": "147",
            "finding": "raw M4/M6 branches are prior-edge seeking",
            "numeric_or_formula": "SH0ES M6_transition Delta AIC=-10.80748256, Delta BIC=-1.77829892; verdict=prior-edge seeking",
            "status": "not_stable_evidence",
            "interpretation": "numerical improvement cannot be treated as support",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "evidence_id": "E844_3_Hz_covariance",
            "source": "155",
            "finding": "direct H(z) does not independently support fixed-shape M6",
            "numeric_or_formula": "32-row delta chi2=+0.401106909; 15-row covariance delta chi2=+0.238933676505; M0 remains preferred",
            "status": "Hz_non_support",
            "interpretation": "chronometer/covariance checks prefer baseline direction",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "evidence_id": "E844_4_joint_growth_CMB_radflat",
            "source": "173",
            "finding": "C0 frozen radflat branch remains internally viable but below best baseline",
            "numeric_or_formula": "Delta growth chi2=1.317309001005178; Delta AIC=3.3173089995964204; Delta BIC=4.207680757492582",
            "status": "near_but_not_preferred",
            "interpretation": "not crushed; not support",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "evidence_id": "E844_5_full_joint_radflat",
            "source": "175",
            "finding": "full joint radflat C0 is near-competitive by AIC and edge-free",
            "numeric_or_formula": "C0 frozen Delta AIC=0.36437287900487547; Delta BIC=1.2547446369010444",
            "status": "phenomenologically_viable_not_evidential",
            "interpretation": "useful hit-and-warning result",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "evidence_id": "E844_6_C0_demotion",
            "source": "176",
            "finding": "C0 demoted to closure-only benchmark",
            "numeric_or_formula": "b_mem reference=0.015730508794745142; full-joint=0.1124525903286696; fractional shift=6.148693776912986",
            "status": "closure_benchmark_only",
            "interpretation": "not dead, not support; amplitude is unstable and not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "evidence_id": "E844_7_parent_amplitude",
            "source": "178",
            "finding": "parent amplitude route gives a corridor, not a prediction",
            "numeric_or_formula": "amplitude corridor derived=true; amplitude prediction derived=false",
            "status": "partial_corridor_not_prediction",
            "interpretation": "parent route is plausible, not proven; more C0 fitting would be rescue-fitting",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gate_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G844_0_edge_dependence",
            "gate": "prior-edge stability",
            "current_result": "mixed",
            "evidence": "raw M4/M6 prior-edge seeking; C0 frozen full-joint edge-free",
            "decision": "do not use raw M4/M6; keep C0 only as closure benchmark",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G844_1_baseline_fairness",
            "gate": "baseline comparison",
            "current_result": "not_preferred",
            "evidence": "H(z), joint growth/CMB, and full joint radflat do not clearly beat baselines after penalties",
            "decision": "near-competitive/tied language allowed; support language blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G844_2_residual_anatomy",
            "gate": "residual anatomy",
            "current_result": "interesting_but_fragile",
            "evidence": "BAO/DH and H(z) checks do not independently validate M6",
            "decision": "treat as clue source only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G844_3_amplitude_prediction",
            "gate": "parent amplitude derivation",
            "current_result": "fails_prediction",
            "evidence": "amplitude corridor derived but no unique no-fit b_mem prediction",
            "decision": "strict branch contract required before more C0 support work",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G844_4_local_GR_separation",
            "gate": "local GR separation",
            "current_result": "protected",
            "evidence": "843/842 keep local GR as closure-only guardrail",
            "decision": "cosmology cannot change local-GR closure status",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def amplitude_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "amplitude_id": "A844_0_C0_target",
            "quantity": "b_mem_full_joint_target",
            "value": "0.1124525903286696",
            "source": "176/178",
            "status": "target_scale_only",
            "problem": "was not predicted before fitting",
            "next_requirement": "strict branch must predeclare or derive amplitude freedom",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "amplitude_id": "A844_1_CMB_only_reference",
            "quantity": "b_mem_CMB_only_reference",
            "value": "0.015730508794745142",
            "source": "176",
            "status": "demoted_reference",
            "problem": "small radiation-consistent CMB-only amplitude shifts by factor 6.148693776912986",
            "next_requirement": "cannot be used as stable support amplitude",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "amplitude_id": "A844_2_parent_corridor",
            "quantity": "parent_amplitude_corridor",
            "value": "derived_true_prediction_false",
            "source": "178",
            "status": "plausible_not_proven",
            "problem": "corridor is not a unique prediction",
            "next_requirement": "derive no-fit amplitude law or define stricter branch with fewer amplitude freedoms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG844_0_no_cosmology_support",
            "claim": "MTS cosmology is supported by current data",
            "status": "forbidden",
            "reason": "baselines remain competitive/preferred and amplitude prediction is not derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG844_1_no_cosmology_death",
            "claim": "MTS cosmology is dead",
            "status": "forbidden",
            "reason": "C0 is near-competitive by AIC, edge-free in full joint radflat, and amplitude corridor is plausible",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG844_2_no_dark_energy_claim",
            "claim": "MTS derives dark energy or parent memory",
            "status": "forbidden",
            "reason": "parent amplitude prediction and parent cosmology derivation remain missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG844_3_no_local_GR_leak",
            "claim": "cosmology results support local GR reduction",
            "status": "forbidden",
            "reason": "local GR remains a separate closure-only theory obligation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG844_4_allowed_private_status",
            "claim": "cosmology is alive as a constraint/clue and C0 is a closure benchmark pending a stricter branch",
            "status": "allowed_private_nonclaim",
            "reason": "this matches the latest evidence without support or death language",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D844_0",
            "finding": "cosmology remains alive as a constraint clue",
            "reason": "coherent FLRW memory branch and near-competitive C0 results survive",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D844_1",
            "finding": "C0 is closure benchmark only",
            "reason": "full-joint AIC is close, but b_mem is unstable and not predicted",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D844_2",
            "finding": "strict cosmology branch is required",
            "reason": "more C0 fitting without a no-fit amplitude law would be rescue-fitting",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "define a stricter MTS cosmology branch with fewer free amplitude freedoms while keeping C0 as closure benchmark",
            "include": "predeclared amplitude law, allowed parameter freedoms, baseline set, growth/CMB/H(z) gates, support/death claim guards",
            "exclude": "more C0 rescue-fitting, public support claim, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "compressed the latest cosmology chain through C0 demotion and parent-amplitude attempt into one current evidence ledger",
            "what_survives": "effective FLRW memory branch, near-competitive edge-free C0 full-joint result, plausible parent amplitude corridor",
            "what_fails": "public support, parent amplitude prediction, stable b_mem, H(z) rescue, local-GR relevance",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    evidence_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    amplitude_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_843_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    latest_included = any(row["source_id"] == "178_parent_amplitude_attempt" and row["needle_check"] == "pass" for row in source_rows)
    evidence_complete = {row["evidence_id"] for row in evidence_rows} == {
        "E844_0_FLRW_projection",
        "E844_1_noSH0ES_compressed_memory",
        "E844_2_raw_M4_M6",
        "E844_3_Hz_covariance",
        "E844_4_joint_growth_CMB_radflat",
        "E844_5_full_joint_radflat",
        "E844_6_C0_demotion",
        "E844_7_parent_amplitude",
    }
    gates_complete = {row["gate_id"] for row in gate_rows} == {
        "G844_0_edge_dependence",
        "G844_1_baseline_fairness",
        "G844_2_residual_anatomy",
        "G844_3_amplitude_prediction",
        "G844_4_local_GR_separation",
    }
    amplitude_state = any(row["status"] == "plausible_not_proven" for row in amplitude_rows_)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    support_blocked = any(row["guard_id"] == "CG844_0_no_cosmology_support" and row["status"] == "forbidden" for row in guard_rows)
    death_blocked = any(row["guard_id"] == "CG844_1_no_cosmology_death" and row["status"] == "forbidden" for row in guard_rows)
    nonclaim_ok = all_valid_for_claim_false([source_rows, evidence_rows, gate_rows, amplitude_rows_, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V844_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V844_1_prior_843_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V844_2_latest_cosmology_status_included",
            "result": "pass" if latest_included else "fail",
            "detail": "178 parent-amplitude attempt included as latest status",
        },
        {
            "check_id": "V844_3_evidence_ledger_complete",
            "result": "pass" if evidence_complete else "fail",
            "detail": "FLRW, M6, H(z), growth/CMB, radflat, demotion, and amplitude statuses recorded",
        },
        {
            "check_id": "V844_4_gate_ledger_complete",
            "result": "pass" if gates_complete else "fail",
            "detail": "edge, baseline, residual, amplitude, and local-GR gates recorded",
        },
        {
            "check_id": "V844_5_amplitude_status_nonprediction",
            "result": "pass" if amplitude_state else "fail",
            "detail": "parent amplitude corridor is plausible but not a prediction",
        },
        {
            "check_id": "V844_6_support_and_death_claims_blocked",
            "result": "pass" if no_claim and support_blocked and death_blocked else "fail",
            "detail": "both support and death claims are blocked",
        },
        {
            "check_id": "V844_7_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V844_8_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V844_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V844_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    evidence_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    amplitude_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 844 - Y5 R10 Cosmology Evidence Readout Pack",
        "",
        "Current result: **cosmology is alive as a constraint/clue, not as support**. The effective FLRW memory branch survives as a coherent mathematical object, and C0 is near-competitive in the full joint radflat fit, but `b_mem` is not stable or parent-predicted. Therefore C0 is a closure-only benchmark, not an evidence pillar; the next move is a stricter MTS cosmology branch with fewer free amplitude freedoms.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_survives", "what_fails", "next_target", "valid_for_claim"]),
        "",
        "## Cosmology Evidence Ledger",
        "",
        csv_table(evidence_rows, ["evidence_id", "source", "finding", "numeric_or_formula", "status", "interpretation", "claim_allowed", "valid_for_claim"]),
        "",
        "## Gate Ledger",
        "",
        csv_table(gate_rows, ["gate_id", "gate", "current_result", "evidence", "decision", "valid_for_claim"]),
        "",
        "## Amplitude Status Ledger",
        "",
        csv_table(amplitude_rows_, ["amplitude_id", "quantity", "value", "source", "status", "problem", "next_requirement", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    evidence_rows = evidence_ledger_rows(generated_utc)
    gate_rows = gate_ledger_rows(generated_utc)
    amplitude_rows_ = amplitude_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, evidence_rows, gate_rows, amplitude_rows_, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(EVIDENCE_LEDGER_PATH, evidence_rows, ["evidence_id", "source", "finding", "numeric_or_formula", "status", "interpretation", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(GATE_LEDGER_PATH, gate_rows, ["gate_id", "gate", "current_result", "evidence", "decision", "valid_for_claim", "generated_utc"])
    write_csv(AMPLITUDE_LEDGER_PATH, amplitude_rows_, ["amplitude_id", "quantity", "value", "source", "status", "problem", "next_requirement", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_survives", "what_fails", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, evidence_rows, gate_rows, amplitude_rows_, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

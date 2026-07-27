from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_859_SOURCE_REGISTER.csv"
AMPLITUDE_INVERSION_PATH = RESIDUALS / "P8_Y5_R10_859_PARENT_AMPLITUDE_INVERSION_LEDGER.csv"
EMPIRICAL_CURVATURE_PATH = RESIDUALS / "P8_Y5_R10_859_EMPIRICAL_CURVATURE_LEDGER.csv"
DERIVATION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_859_DERIVATION_CONTRACT.csv"
SHAPE_REPAIR_PATH = RESIDUALS / "P8_Y5_R10_859_SHAPE_REPAIR_OPTIONS.csv"
GR_LIMIT_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_859_GR_NEWTON_LIMIT_CONTRACT.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_859_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_859_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_859_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_859_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_859_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_859_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_858_VALIDATION.csv"
JOINT_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_858_PARENT_ONLY_JOINT_LEDGER.csv"
SECTOR_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_858_SN_BAO_SECTOR_LEDGER.csv"
CONFIG_PATH = FORMALIZATION / "configs" / "cosmology_background_R1_current.json"

STATUS = "Y5_R10_859_parent_memory_derivation_gate_written_nonclaim"
CLAIM_CEILING = "derivation_gate_only_no_parent_action_no_support_no_local_GR_claim"
NEXT_TARGET = "860-Y5-R10-parent-amplitude-law-and-GR-limit-derivation-contract.md"

SOURCE_SPECS = [
    {
        "source_id": "858_doc",
        "path": POST_CHECKPOINT / "858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md",
        "needles": [
            "borderline_parent_only_private_nonclaim",
            "P858_2_midpoint_parent",
            "859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md",
        ],
        "role": "parent-only stress-test handoff",
    },
    {
        "source_id": "858_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V858_12_acceptance_passes,pass",
            "V858_14_all_rows_nonclaim,pass",
            "V858_16_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "858_joint_ledger",
        "path": JOINT_LEDGER_PATH,
        "needles": [
            "P858_2_midpoint_parent",
            "borderline_parent_only_private_nonclaim",
            "blocked_parent_prediction_missing",
        ],
        "role": "shared-parent combined readout",
    },
    {
        "source_id": "858_sector_ledger",
        "path": SECTOR_LEDGER_PATH,
        "needles": [
            "delta_chi2_sn_vs_bic_baseline",
            "delta_chi2_bao_vs_bic_baseline",
            "P858_2_midpoint_parent",
        ],
        "role": "SN/BAO sector pressure",
    },
    {
        "source_id": "857_contract",
        "path": POST_CHECKPOINT / "857-Y5-R10-branch-invariant-memory-projection-repair-contract.md",
        "needles": [
            "E2_B(z)=E2_LCDM_B(z)+b_P A_P(z)+b_R[B] A_R_B(z)",
            "q_B=0 or MISSING_SOURCE => b_R[B]=0",
            "b_P=0 and b_R[B]=0 => E2_B(z)=E2_LCDM_B(z)",
        ],
        "role": "parent-plus-response contract",
    },
    {
        "source_id": "854_parent_law",
        "path": POST_CHECKPOINT / "854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md",
        "needles": [
            "b_parent = a_F DeltaR/(3 eta^2)",
            "eta/a_F/DeltaR remain unsigned",
            "formal_identity_survives",
        ],
        "role": "parent amplitude identity",
    },
    {
        "source_id": "R1_cosmology_config",
        "path": CONFIG_PATH,
        "needles": ['"id": "M6"', '"alpha_act": 0.48', '"nu_act": 1.2', '"b_mem": 0.05'],
        "role": "current assumed M6 shape parameters",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def finite_float(value: object) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: object) -> str:
    number = finite_float(value)
    return "" if number is None else f"{number:.12g}"


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


def best_joint_row() -> dict[str, str]:
    rows = read_csv(JOINT_LEDGER_PATH)
    nonnull = [
        row
        for row in rows
        if row["candidate_id"] != "P858_0_null_parent" and finite_float(row["combined_delta_bic"]) is not None
    ]
    return min(nonnull, key=lambda row: float(row["combined_delta_bic"]))


def parent_product(b_parent: float, eta: float) -> float:
    return 3.0 * b_parent * eta * eta


def amplitude_inversion_rows(best: dict[str, str], generated_utc: str) -> list[dict[str, object]]:
    joint_rows = read_csv(JOINT_LEDGER_PATH)
    candidates = [
        row
        for row in joint_rows
        if row["candidate_id"] in {
            "P858_1_no_sh0es_anchor_parent",
            "P858_2_midpoint_parent",
            "P858_3_sh0es_anchor_parent",
            "P858_5_corridor_eta1_aFDeltaR_0p3",
        }
    ]
    rows: list[dict[str, object]] = []
    for row in candidates:
        b_parent = float(row["b_parent"])
        for eta in (0.5, 1.0, 2.0):
            rows.append(
                {
                    "inversion_id": f"AI859_{row['candidate_id']}_eta_{str(eta).replace('.', 'p')}",
                    "candidate_id": row["candidate_id"],
                    "b_parent": fmt(b_parent),
                    "eta_assumption": fmt(eta),
                    "required_aF_DeltaR": fmt(parent_product(b_parent, eta)),
                    "identity_used": "b_P = a_F DeltaR/(3 eta^2)",
                    "status": "target_inversion_only_not_derivation",
                    "reason": "a_F, DeltaR, and eta are not independently sourced from the parent action",
                    "valid_for_claim": "false",
                    "generated_utc": generated_utc,
                }
            )
    rows.append(
        {
            "inversion_id": "AI859_best_target_corridor",
            "candidate_id": best["candidate_id"],
            "b_parent": best["b_parent"],
            "eta_assumption": "eta_unsolved",
            "required_aF_DeltaR": "3*b_P*eta^2 = " + fmt(3.0 * float(best["b_parent"])) + "*eta^2",
            "identity_used": "b_P = a_F DeltaR/(3 eta^2)",
            "status": "empirical_target_corridor_only",
            "reason": "best parent-only value gives the corridor a_F DeltaR ≈ 0.1923 eta^2 but does not derive it",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    )
    return rows


def solve_quadratic(points: list[tuple[float, float]]) -> tuple[float, float, float]:
    matrix = [[x * x, x, 1.0, y] for x, y in points]
    for pivot in range(3):
        max_row = max(range(pivot, 3), key=lambda idx: abs(matrix[idx][pivot]))
        matrix[pivot], matrix[max_row] = matrix[max_row], matrix[pivot]
        scale = matrix[pivot][pivot]
        if abs(scale) < 1e-15:
            raise ValueError("singular quadratic fit")
        for col in range(pivot, 4):
            matrix[pivot][col] /= scale
        for row in range(3):
            if row == pivot:
                continue
            factor = matrix[row][pivot]
            for col in range(pivot, 4):
                matrix[row][col] -= factor * matrix[pivot][col]
    return matrix[0][3], matrix[1][3], matrix[2][3]


def empirical_curvature_rows(generated_utc: str) -> list[dict[str, object]]:
    joint_rows = {
        row["candidate_id"]: row
        for row in read_csv(JOINT_LEDGER_PATH)
        if finite_float(row["combined_delta_bic"]) is not None
    }
    window_ids = ["P858_4_corridor_eta1_aFDeltaR_0p1", "P858_2_midpoint_parent", "P858_5_corridor_eta1_aFDeltaR_0p3"]
    bic_points = [(float(joint_rows[candidate_id]["b_parent"]), float(joint_rows[candidate_id]["combined_delta_bic"])) for candidate_id in window_ids]
    raw_points = [
        (
            float(joint_rows[candidate_id]["b_parent"]),
            float(joint_rows[candidate_id]["combined_delta_chi2_sn_vs_bic_baseline"]) + float(joint_rows[candidate_id]["combined_delta_chi2_bao_vs_bic_baseline"]),
        )
        for candidate_id in window_ids
    ]
    bic_a, bic_b, bic_c = solve_quadratic(bic_points)
    raw_a, raw_b, raw_c = solve_quadratic(raw_points)
    bic_opt = -bic_b / (2.0 * bic_a)
    raw_opt = -raw_b / (2.0 * raw_a)
    return [
        {
            "curvature_id": "EC859_0_bic_window",
            "fit_window": ";".join(window_ids),
            "observable": "combined_delta_bic",
            "quadratic_a": fmt(bic_a),
            "quadratic_b": fmt(bic_b),
            "quadratic_c": fmt(bic_c),
            "estimated_empirical_optimum_b_parent": fmt(bic_opt),
            "estimated_empirical_minimum": fmt(bic_a * bic_opt * bic_opt + bic_b * bic_opt + bic_c),
            "status": "diagnostic_only_not_derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "curvature_id": "EC859_1_raw_sector_window",
            "fit_window": ";".join(window_ids),
            "observable": "combined_SN_plus_BAO_delta_chi2_vs_BIC_baselines",
            "quadratic_a": fmt(raw_a),
            "quadratic_b": fmt(raw_b),
            "quadratic_c": fmt(raw_c),
            "estimated_empirical_optimum_b_parent": fmt(raw_opt),
            "estimated_empirical_minimum": fmt(raw_a * raw_opt * raw_opt + raw_b * raw_opt + raw_c),
            "status": "diagnostic_only_not_derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "curvature_id": "EC859_2_shape_pressure_readout",
            "fit_window": "858 sector ledger",
            "observable": "SN_and_BAO_sector_signs",
            "quadratic_a": "",
            "quadratic_b": "",
            "quadratic_c": "",
            "estimated_empirical_optimum_b_parent": "0.06_to_0.10_private_corridor",
            "estimated_empirical_minimum": "",
            "status": "shape_helps_both_SN_and_BAO_near_midpoint_but_amplitude_unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def derivation_contract_rows(best: dict[str, str], generated_utc: str) -> list[dict[str, object]]:
    best_b = float(best["b_parent"])
    return [
        {
            "contract_id": "DC859_0_parent_identity",
            "requirement": "derive b_P from parent fields, not from the cosmology target",
            "mathematical_form": "b_P = a_F DeltaR/(3 eta^2)",
            "current_readout": f"best_private_target b_P={fmt(best_b)} implies a_F DeltaR={fmt(3.0 * best_b)} eta^2",
            "missing_input": "parent-sourced eta, a_F normalization, DeltaR endpoint memory",
            "status": "open_required_for_support",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "DC859_1_shape_projection",
            "requirement": "derive the FLRW shape A_P(z), including current alpha_act=0.48 and nu_act=1.2 or replacements",
            "mathematical_form": "E2(z)=E2_LCDM(z)+b_P A_P(z)",
            "current_readout": "858 used current M6 shape and found borderline parent-only survival",
            "missing_input": "parent FLRW projection or action-level memory kernel",
            "status": "open_required_for_support",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "DC859_2_no_target_inversion",
            "requirement": "the empirical optimum may define a target window but cannot be inserted as a derivation",
            "mathematical_form": "source(a_F,DeltaR,eta) independent of argmin_BIC(b_P)",
            "current_readout": "empirical corridor near b_P≈0.06-0.10 is diagnostic only",
            "missing_input": "independent parent source rows",
            "status": "guard_active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "DC859_3_conservation",
            "requirement": "the parent memory deformation must satisfy the FLRW continuity/Bianchi accounting",
            "mathematical_form": "nabla_mu(G^{mu nu}-8piG T^{mu nu}-T_mem^{mu nu})=0",
            "current_readout": "not checked by 858 scoring",
            "missing_input": "stress-energy or effective-fluid derivation for A_P(z)",
            "status": "open_required_for_support",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "DC859_4_local_GR_limit",
            "requirement": "the same parent source must switch off in local vacuum/PPN regimes",
            "mathematical_form": "q_loc^nu=0 => b_P/local memory force absent; weak-field limit reduces to GR/Newton",
            "current_readout": "local GR bridge remains unsatisfied in this cosmology checkpoint",
            "missing_input": "parent action clause connecting FLRW memory to q_loc^nu suppression",
            "status": "open_required_for_framework",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def shape_repair_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "option_id": "SR859_0_keep_shape_derive_amplitude",
            "option": "keep current M6 parent shape and try deriving eta/a_F/DeltaR first",
            "evidence": "858 midpoint parent improves both SN and BAO sector chi2 against BIC baselines",
            "risk": "shape parameters alpha_act=0.48 and nu_act=1.2 remain assumed",
            "decision": "selected_next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "option_id": "SR859_1_shape_repair",
            "option": "repair A_P(z) only if derivation or sector residuals force it",
            "evidence": "upper amplitude overdrives both sectors; current shape is not obviously broken near midpoint",
            "risk": "extra shape freedom becomes another phenomenological knob",
            "decision": "defer",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "option_id": "SR859_2_response_reopen",
            "option": "reopen response channel",
            "evidence": "857 response source gate failed and 858 survived borderline without response",
            "risk": "branch split returns as hidden calibration knob",
            "decision": "reject_until_independent_q_B",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gr_limit_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "limit_id": "GR859_0_zero_memory_background",
            "requirement": "b_P=0 must recover LCDM/GR background behavior in the cosmology code path",
            "evidence_now": "858 null parent parity passes",
            "missing_for_full_theory": "action-level statement that memory source can vanish without residual force",
            "status": "background_check_passed_not_full_GR_derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "limit_id": "GR859_1_local_vacuum_switch_off",
            "requirement": "local q_loc^nu must vanish or be bounded so the parent memory field does not spoil PPN/Newton",
            "evidence_now": "not supplied by cosmology stress test",
            "missing_for_full_theory": "derive q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) suppression from parent action",
            "status": "open_required_for_MTS_GR_bridge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "limit_id": "GR859_2_newtonian_limit",
            "requirement": "weak-field slow-motion limit must reduce to Newtonian mechanics through GR, not by separate fitting",
            "evidence_now": "not addressed by SN/BAO evidence",
            "missing_for_full_theory": "linearized parent equations with Poisson limit and conserved matter coupling",
            "status": "open_required_for_MTS_GR_bridge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC859_0_selected",
            "route": "derive_parent_amplitude_law_and_GR_limit_before_more_shape_freedom",
            "status": "selected",
            "reason": "current shape is borderline-competitive and improves SN/BAO near midpoint, so the missing piece is derivation of b_P and the GR/local switch-off",
            "include": "eta, a_F, DeltaR, FLRW projection, Bianchi accounting, local q_loc suppression",
            "exclude": "new response knob, fitted target inversion, public support claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC859_1_deferred",
            "route": "shape_repair_or_basis_expansion",
            "status": "deferred",
            "reason": "extra shape freedom is premature until the parent amplitude law is attempted",
            "include": "only if 860 fails or derives a different kernel",
            "exclude": "phenomenological shape tuning",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG859_0_no_derived_amplitude",
            "claim": "b_P≈0.0641 has been derived",
            "status": "forbidden",
            "reason": "859 only records the required parent-law inversion and missing inputs",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG859_1_no_shape_derivation",
            "claim": "M6 shape parameters are derived",
            "status": "forbidden",
            "reason": "alpha_act and nu_act remain current assumed shape parameters",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG859_2_no_local_GR",
            "claim": "local GR/Newton limit is solved",
            "status": "forbidden",
            "reason": "859 only states the required bridge from parent memory to q_loc suppression",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG859_3_allowed_derivation_gate",
            "claim": "parent amplitude/shape derivation gate is now explicit",
            "status": "allowed_private_nonclaim",
            "reason": "the next route is constrained to derive eta/a_F/DeltaR and the GR limit before claiming support",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(best: dict[str, str], generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D859_0",
            "finding": "derive_amplitude_before_shape_repair",
            "reason": f"best parent-only candidate {best['candidate_id']} is borderline with combined_delta_bic={best['combined_delta_bic']}; current shape improves SN/BAO sectors near midpoint",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D859_1",
            "finding": "parent law must connect cosmology to local GR/Newton switch-off",
            "reason": "a serious field theory cannot keep a cosmology memory amplitude unless the same parent action suppresses local residuals",
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
            "objective": "attempt the parent amplitude law derivation while enforcing the local GR/Newton zero-memory limit",
            "include": "derive or block eta, a_F, DeltaR; FLRW kernel A_P(z); Bianchi/continuity; q_loc suppression; no target inversion",
            "exclude": "more scoring, response source, public support claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(best: dict[str, str], generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "converted the parent-only empirical corridor into an explicit derivation and GR-limit gate",
            "best_private_target": best["candidate_id"],
            "best_b_parent": best["b_parent"],
            "required_parent_product": "a_F DeltaR = " + fmt(3.0 * float(best["b_parent"])) + " eta^2",
            "what_is_not_claimed": "derived amplitude, derived shape, local GR/Newton limit, support, public evidence",
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
    amplitude_rows: list[dict[str, object]],
    curvature_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    shape_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    amplitude_ok = any(row["status"] == "empirical_target_corridor_only" for row in amplitude_rows) and all(row["valid_for_claim"] == "false" for row in amplitude_rows)
    curvature_ok = len(curvature_rows) == 3 and any("0.06_to_0.10" in str(row["estimated_empirical_optimum_b_parent"]) for row in curvature_rows)
    derivation_ok = len(derivation_rows) == 5 and any(row["contract_id"] == "DC859_4_local_GR_limit" for row in derivation_rows)
    shape_ok = any(row["decision"] == "selected_next" and row["option_id"] == "SR859_0_keep_shape_derive_amplitude" for row in shape_rows)
    gr_ok = len(gr_rows) == 3 and any(row["limit_id"] == "GR859_1_local_vacuum_switch_off" for row in gr_rows)
    route_ok = any(row["route_id"] == "RC859_0_selected" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, amplitude_rows, curvature_rows, derivation_rows, shape_rows, gr_rows, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V859_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V859_1_prior_858_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V859_2_amplitude_inversion_nonclaim", "result": "pass" if amplitude_ok else "fail", "detail": "parent-law inversion rows remain target-only nonclaims"},
        {"check_id": "V859_3_empirical_curvature_recorded", "result": "pass" if curvature_ok else "fail", "detail": "empirical optimum/corridor recorded as diagnostic only"},
        {"check_id": "V859_4_derivation_contract_ready", "result": "pass" if derivation_ok else "fail", "detail": "eta/a_F/DeltaR, shape, conservation, local-GR clauses recorded"},
        {"check_id": "V859_5_shape_route_selected", "result": "pass" if shape_ok else "fail", "detail": "derive amplitude before adding shape freedom"},
        {"check_id": "V859_6_GR_Newton_limit_open", "result": "pass" if gr_ok else "fail", "detail": "local vacuum and Newtonian limit clauses remain explicit"},
        {"check_id": "V859_7_route_selected", "result": "pass" if route_ok else "fail", "detail": "parent amplitude and GR-limit derivation selected"},
        {"check_id": "V859_8_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V859_9_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V859_10_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V859_11_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V859_12_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    amplitude_rows: list[dict[str, object]],
    curvature_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    shape_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 859 - Y5 R10 Parent Memory Shape Amplitude Repair Or Derivation",
        "",
        "Current result: **the empirical parent-only corridor has been converted into a derivation gate**. The best private target is useful, but it is not a derivation: `b_P≈0.0641` only becomes serious if `eta`, `a_F`, and `DeltaR` come from the parent action and the same construction preserves the local GR/Newton limit.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "best_private_target", "best_b_parent", "required_parent_product", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Parent Amplitude Inversion Ledger",
        "",
        csv_table(amplitude_rows, ["inversion_id", "candidate_id", "b_parent", "eta_assumption", "required_aF_DeltaR", "identity_used", "status", "reason", "valid_for_claim"]),
        "",
        "## Empirical Curvature Ledger",
        "",
        csv_table(curvature_rows, ["curvature_id", "fit_window", "observable", "estimated_empirical_optimum_b_parent", "estimated_empirical_minimum", "status", "valid_for_claim"]),
        "",
        "## Derivation Contract",
        "",
        csv_table(derivation_rows, ["contract_id", "requirement", "mathematical_form", "current_readout", "missing_input", "status", "valid_for_claim"]),
        "",
        "## Shape Repair Options",
        "",
        csv_table(shape_rows, ["option_id", "option", "evidence", "risk", "decision", "valid_for_claim"]),
        "",
        "## GR Newton Limit Contract",
        "",
        csv_table(gr_rows, ["limit_id", "requirement", "evidence_now", "missing_for_full_theory", "status", "valid_for_claim"]),
        "",
        "## Route Choice",
        "",
        csv_table(routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
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
    best = best_joint_row()
    source_rows = source_register_rows(generated_utc)
    amplitude_rows = amplitude_inversion_rows(best, generated_utc)
    curvature_rows = empirical_curvature_rows(generated_utc)
    derivation_rows = derivation_contract_rows(best, generated_utc)
    shape_rows = shape_repair_rows(generated_utc)
    gr_rows = gr_limit_contract_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(best, generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(best, generated_utc)
    validation = validation_rows(
        source_rows,
        amplitude_rows,
        curvature_rows,
        derivation_rows,
        shape_rows,
        gr_rows,
        routes,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(AMPLITUDE_INVERSION_PATH, amplitude_rows, ["inversion_id", "candidate_id", "b_parent", "eta_assumption", "required_aF_DeltaR", "identity_used", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(EMPIRICAL_CURVATURE_PATH, curvature_rows, ["curvature_id", "fit_window", "observable", "quadratic_a", "quadratic_b", "quadratic_c", "estimated_empirical_optimum_b_parent", "estimated_empirical_minimum", "status", "valid_for_claim", "generated_utc"])
    write_csv(DERIVATION_CONTRACT_PATH, derivation_rows, ["contract_id", "requirement", "mathematical_form", "current_readout", "missing_input", "status", "valid_for_claim", "generated_utc"])
    write_csv(SHAPE_REPAIR_PATH, shape_rows, ["option_id", "option", "evidence", "risk", "decision", "valid_for_claim", "generated_utc"])
    write_csv(GR_LIMIT_CONTRACT_PATH, gr_rows, ["limit_id", "requirement", "evidence_now", "missing_for_full_theory", "status", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "best_private_target", "best_b_parent", "required_parent_product", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, amplitude_rows, curvature_rows, derivation_rows, shape_rows, gr_rows, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"best_private_target={best['candidate_id']}")
    print(f"best_b_parent={best['b_parent']}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

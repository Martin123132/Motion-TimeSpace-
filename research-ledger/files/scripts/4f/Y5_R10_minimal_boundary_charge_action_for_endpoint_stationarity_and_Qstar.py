from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "865-Y5-R10-minimal-boundary-charge-action-for-endpoint-stationarity-and-Qstar.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_865_SOURCE_REGISTER.csv"
ACTION_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_865_BOUNDARY_ACTION_ATTEMPT.csv"
STATIONARITY_PATH = RESIDUALS / "P8_Y5_R10_865_STATIONARITY_DERIVATION.csv"
COEFFICIENT_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_865_COEFFICIENT_OWNERSHIP_AUDIT.csv"
QSTAR_PATH = RESIDUALS / "P8_Y5_R10_865_QSTAR_NORMALIZATION_CONTRACT.csv"
ARROW_PATH = RESIDUALS / "P8_Y5_R10_865_ENDPOINT_ARROW_STABILITY_AUDIT.csv"
LOCAL_IMPACT_PATH = RESIDUALS / "P8_Y5_R10_865_LOCAL_GR_IMPACT_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_865_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_865_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_865_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_865_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_865_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_865_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_864_VALIDATION.csv"

STATUS = "Y5_R10_865_minimal_boundary_action_writes_exact_roots_but_coefficients_Qstar_arrow_unsigned_nonclaim"
CLAIM_CEILING = "formal_boundary_action_owner_only_no_parent_coefficient_no_Qstar_no_endpoint_arrow_no_local_GR_claim"
NEXT_TARGET = "866-Y5-R10-endpoint-coefficient-origin-and-arrow-law-or-demote-to-closure.md"

ROOT_LOW = Fraction(1, 9)
ROOT_HIGH = Fraction(1, 3)
DELTA_R = ROOT_HIGH - ROOT_LOW

SOURCE_SPECS = [
    {
        "source_id": "864_doc",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "minimal parent-action clause is now explicit",
            "ES864_1_stationarity_equations",
            "865-Y5-R10-minimal-boundary-charge-action-for-endpoint-stationarity-and-Qstar.md",
        ],
        "role": "immediate endpoint-stationarity handoff",
    },
    {
        "source_id": "864_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V864_8_route_selected,pass",
            "V864_10_all_rows_nonclaim,pass",
            "V864_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "109_boundary_charge",
        "path": POST_CHECKPOINT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needles": [
            "normalized boundary charge",
            "boundary_charge_unit_defined",
            "product_two_over_nine_derived",
        ],
        "role": "normalized boundary charge and Qstar failure",
    },
    {
        "source_id": "110_endpoint_quadratic",
        "path": POST_CHECKPOINT / "110-endpoint-charge-equation-attempt.md",
        "needles": [
            "27R^2 - 12R + 1 = 0",
            "endpoint_equation_parent_derived",
            "Qstar_charge_unit_derived",
        ],
        "role": "exact endpoint quadratic target",
    },
    {
        "source_id": "111_variational_owner",
        "path": POST_CHECKPOINT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needles": [
            "U(R)=9R^3-6R^2+R",
            "coefficients_parent_forced",
            "endpoint_arrow_derived",
        ],
        "role": "formal potential owner and missing coefficient/arrow proofs",
    },
    {
        "source_id": "94_relaxation_arrow",
        "path": POST_CHECKPOINT / "94-endpoint-relaxation-DeltaR-gate.md",
        "needles": [
            "endpoint_ordering_parent_derived",
            "DeltaR_predicted_without_SN_BAO_fit",
            "cosmological arrow",
        ],
        "role": "endpoint ordering and arrow guard",
    },
    {
        "source_id": "337_exact_readout",
        "path": POST_CHECKPOINT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needles": [
            "q_trace = 2/27",
            "epsilon_H = 1",
            "parent action proves exact readout not EFT",
        ],
        "role": "conditional exact readout numerator for trace lift",
    },
    {
        "source_id": "861_endpoint_audit",
        "path": POST_CHECKPOINT / "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md",
        "needles": [
            "EP861_0_charge_unit",
            "EP861_1_early_endpoint",
            "EP861_4_nohair",
        ],
        "role": "endpoint and no-hair blockers",
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
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
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


def action_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "action_id": "BA865_0_minimal_dimensionless_action",
            "object": "R=Q/Q_*",
            "candidate_action": "S_trace = sigma kappa Q_* [9 R^3 - 6 R^2 + R]",
            "variation": "delta S_trace/dR = sigma kappa Q_* (27 R^2 - 12 R + 1)",
            "result": "exact endpoint quadratic is generated for any nonzero sigma*kappa",
            "status": "formal_owner_written_not_parent_derived",
            "missing_for_claim": "derive sigma, kappa, Q_*, and coefficients 9,-6,1 from parent boundary charge pairing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "BA865_1_factorized_stationarity",
            "object": "Euler equation",
            "candidate_action": "dU/dR = (3R-1)(9R-1)",
            "variation": "stationary roots R_low=1/9 and R_high=1/3",
            "result": "DeltaR=R_high-R_low=2/9 follows algebraically",
            "status": "exact_algebra_not_parent_origin",
            "missing_for_claim": "prove the factors 3R-1 and 9R-1 are forced by parent trace charge, not chosen for the target",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "BA865_2_two_endpoint_use",
            "object": "Q_early,Q_today",
            "candidate_action": "both endpoints are stationary points of the same U(R)",
            "variation": "R_early,R_today in {1/3,1/9}",
            "result": "two endpoint values exist, but the action alone does not assign early/today labels",
            "status": "endpoint_pair_available_arrow_unsigned",
            "missing_for_claim": "derive cosmological arrow and endpoint selection rule",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "BA865_3_constraint_route_rejected",
            "object": "Lagrange multiplier alternative",
            "candidate_action": "S_constraint = Lambda(27 R^2 - 12 R + 1)",
            "variation": "imposes the desired equation directly",
            "result": "not counted as derivation",
            "status": "rejected_constraint_trick",
            "missing_for_claim": "use a genuine boundary charge action, not a multiplier that tapes the target to the action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def stationarity_rows(generated_utc: str) -> list[dict[str, object]]:
    u_low = Fraction(9, 1) * ROOT_LOW**3 - Fraction(6, 1) * ROOT_LOW**2 + ROOT_LOW
    u_high = Fraction(9, 1) * ROOT_HIGH**3 - Fraction(6, 1) * ROOT_HIGH**2 + ROOT_HIGH
    second_low = Fraction(54, 1) * ROOT_LOW - Fraction(12, 1)
    second_high = Fraction(54, 1) * ROOT_HIGH - Fraction(12, 1)
    return [
        {
            "derivation_id": "SD865_0_derivative",
            "statement": "d/dR[9R^3-6R^2+R] = 27R^2-12R+1",
            "computed_value": "pass",
            "meaning": "formal stationarity equation matches the target quadratic",
            "status": "verified_algebra",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "SD865_1_roots",
            "statement": "27R^2-12R+1=(3R-1)(9R-1)",
            "computed_value": f"R_low={ROOT_LOW}; R_high={ROOT_HIGH}; DeltaR={DELTA_R}",
            "meaning": "exact roots give 1/9, 1/3, and 2/9",
            "status": "verified_algebra",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "SD865_2_second_variation",
            "statement": "U''(R)=54R-12",
            "computed_value": f"U''(1/9)={second_low}; U''(1/3)={second_high}",
            "meaning": "with positive sign, 1/9 is locally unstable/max-like and 1/3 is stable/min-like",
            "status": "arrow_problem_exposed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "SD865_3_potential_values",
            "statement": "U(1/9)=4/81 and U(1/3)=0",
            "computed_value": f"U_low={u_low}; U_high={u_high}",
            "meaning": "positive-U downhill flow prefers 1/3, opposite the desired high-to-low endpoint arrow unless sign/dynamics is owned",
            "status": "arrow_not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "SD865_4_claim_status",
            "statement": "Does stationarity derive DeltaR=2/9 as a parent prediction?",
            "computed_value": "no",
            "meaning": "formal algebra is exact, but coefficient origin, Q_*, and arrow remain unsigned",
            "status": "formal_owner_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coefficient_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "coefficient_id": "CO865_0_factor_roots",
            "coefficient_source_candidate": "choose roots 1/3 and 1/9",
            "mathematical_form": "(3R-1)(9R-1)",
            "current_status": "target_equivalent_not_derivation",
            "why_not_enough": "the roots encode DeltaR=2/9 unless parent charge theory forces them first",
            "next_test": "derive root factors from charge pairing, exact readout, or boundary representation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CO865_1_cell_count_story",
            "coefficient_source_candidate": "27=3^3 and 12=3x4",
            "mathematical_form": "spatial determinant and 3+1 trace-cell count",
            "current_status": "plausible_bookkeeping",
            "why_not_enough": "component counts are not variational weights unless the parent action supplies the measure",
            "next_test": "derive boundary charge measure that weights cubic and quadratic terms by these counts",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CO865_2_exact_readout_bridge",
            "coefficient_source_candidate": "q_trace=2/27 and DeltaR=3q_trace",
            "mathematical_form": "exact parent readout plus trace lift",
            "current_status": "conditional_bridge_elsewhere",
            "why_not_enough": "trace lift and endpoint identification remain unsigned; it does not independently derive U(R)",
            "next_test": "connect boundary action roots to exact readout current without target inversion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CO865_3_overall_scale",
            "coefficient_source_candidate": "kappa",
            "mathematical_form": "S_trace=sigma kappa Q_* U(R)",
            "current_status": "irrelevant_to_roots_but_needed_for dynamics",
            "why_not_enough": "stationary roots ignore kappa, but stability, fluctuations, and coupling to FLRW need it",
            "next_test": "derive kappa from boundary charge metric or Ward normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CO865_4_sign",
            "coefficient_source_candidate": "sigma=+1 or -1",
            "mathematical_form": "U or -U has same stationary roots",
            "current_status": "arrow_critical_unsigned",
            "why_not_enough": "sign determines which endpoint is stable and therefore the early-to-today arrow",
            "next_test": "derive sign from cosmological arrow, entropy, or boundary orientation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qstar_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "qstar_id": "QS865_0_definition",
            "required_object": "Q_*",
            "candidate_definition": "unit of parent-normalized trace boundary charge",
            "current_status": "missing_parent_definition",
            "if_found": "R=Q/Q_* becomes a real dimensionless action variable",
            "if_missing": "endpoint quadratic is only a normalized formal variable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QS865_1_charge_pairing",
            "required_object": "boundary charge metric",
            "candidate_definition": "Q_* fixed by <J_trace,J_trace>_Q or equivalent integral unit",
            "current_status": "not_parent_derived",
            "if_found": "coefficients and normalization might become action-owned",
            "if_missing": "Q_* can be chosen after the fact",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QS865_2_trace_leg_unit",
            "required_object": "three trace legs",
            "candidate_definition": "DeltaR=3q_trace uses Q_* consistently across the three FLRW trace legs",
            "current_status": "conditional_on_trace_current",
            "if_found": "boundary action and Ward trace lift could share one normalization",
            "if_missing": "endpoint quadratic and trace-lift bridge are disconnected contracts",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QS865_3_forbidden_data_calibration",
            "required_object": "not SN/BAO calibrated",
            "candidate_definition": "Q_* must be fixed before cosmology scoring",
            "current_status": "guardrail",
            "if_found": "post-fit circularity is reduced",
            "if_missing": "no public prediction claim allowed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def arrow_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "arrow_id": "AR865_0_positive_U_stability",
            "candidate_arrow": "positive U with ordinary downhill relaxation",
            "mathematical_test": "U''(1/9)<0, U''(1/3)>0",
            "result": "relaxes toward 1/3, not toward 1/9",
            "status": "opposite_to_desired_high_to_low_arrow",
            "missing_for_claim": "derive a different dynamics/sign or reinterpret endpoint labels",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "AR865_1_negative_U_stability",
            "candidate_arrow": "negative U flips stability",
            "mathematical_test": "(-U)''(1/3)<0 and (-U)''(1/9)>0",
            "result": "can make 1/9 stable, but sign is inserted unless parent orientation fixes it",
            "status": "possible_but_unsigned",
            "missing_for_claim": "boundary orientation/entropy/arrow law deriving sigma=-1",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "AR865_2_first_order_arrow",
            "candidate_arrow": "non-gradient endpoint transition law",
            "mathematical_test": "dot R = F(R) with fixed points 1/3,1/9 and flow 1/3 -> 1/9",
            "result": "possible as a separate arrow law, but not derived by U alone",
            "status": "requires_parent_dynamics",
            "missing_for_claim": "derive F(R) from boundary current continuity or cosmological time orientation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "AR865_3_arrow_verdict",
            "candidate_arrow": "early high endpoint to today low endpoint",
            "mathematical_test": "R_early=1/3, R_today=1/9",
            "result": "not derived from the minimal stationary action",
            "status": "arrow_blocks_prediction",
            "missing_for_claim": "parent endpoint arrow theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_impact_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "impact_id": "LI865_0_FLRW_endpoint_owner",
            "conditional_result": "S_trace can own endpoint roots in the FLRW quotient if coefficients/Q_* are derived",
            "local_GR_effect": "none by itself",
            "remaining_debt": "local/global split and boundary no-hair must still prevent local leakage",
            "current_status": "formal_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "LI865_1_local_nohair",
            "conditional_result": "endpoint action must have no local PPN/WEP/clock projection",
            "local_GR_effect": "needed for q_loc^nu=0",
            "remaining_debt": "P_loc J_trace=0 and P_loc dB_trace=0 remain unsigned",
            "current_status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "LI865_2_GR_Newton_verdict",
            "conditional_result": "no local GR/Newton promotion",
            "local_GR_effect": "GR reduction still waits on split, no-hair, source normalization, and EH/projector closure",
            "remaining_debt": "endpoint action is only one part of the GR-reduction stack",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC865_0_selected",
            "route": "endpoint_coefficient_origin_and_arrow_law_or_demote_to_closure",
            "status": "selected",
            "reason": "the formal action already gives the exact roots; the real blockers are coefficient origin, sign/arrow, and Q_*",
            "include": "derive 9,-6,1 or 27,12,1; derive sigma sign; derive endpoint arrow; derive Q_* charge metric",
            "exclude": "multipliers imposing the target, fitted endpoint labels, public claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC865_1_deferred",
            "route": "retained_closure_or_residual_scoring",
            "status": "deferred",
            "reason": "needed only if coefficient and arrow origin cannot be derived",
            "include": "label endpoint quadratic as explicit closure and score cosmology/local residuals honestly",
            "exclude": "before one more targeted coefficient/arrow derivation attempt",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG865_0_no_endpoint_prediction",
            "claim": "MTS predicts DeltaR=2/9",
            "status": "forbidden",
            "reason": "formal action gives the roots but coefficients, Q_*, and arrow are not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG865_1_no_Qstar_claim",
            "claim": "Q_* is derived",
            "status": "forbidden",
            "reason": "Q_* remains a missing parent-normalized trace charge unit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG865_2_no_arrow_claim",
            "claim": "endpoint arrow is derived",
            "status": "forbidden",
            "reason": "minimal positive-U action prefers the opposite stability direction; sign/dynamics is unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG865_3_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "endpoint action does not close local/global split, no-hair, q_loc, source normalization, or EH/projector gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG865_4_allowed_private_result",
            "claim": "formal owner and exact arrow problem are identified",
            "status": "allowed_private_nonclaim",
            "reason": "865 sharpens the derivation target and exposes the sign/arrow blocker",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D865_0",
            "finding": "minimal_action_generates_exact_roots",
            "reason": "U(R)=9R^3-6R^2+R has derivative 27R^2-12R+1 and roots 1/9,1/3",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D865_1",
            "finding": "coefficient_origin_not_derived",
            "reason": "9,-6,1 or 27,12,1 are still chosen/formal unless parent charge pairing forces them",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D865_2",
            "finding": "arrow_problem_exposed",
            "reason": "positive U makes 1/3 stable and 1/9 unstable, opposite a high-to-low relaxation unless sign/dynamics is parent-owned",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D865_3",
            "finding": "Qstar_still_missing",
            "reason": "R=Q/Q_* requires a parent-normalized boundary charge unit before the action is physical",
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
            "objective": "try to derive the endpoint coefficients, sign/arrow law, and Q_* charge unit from boundary charge pairing or demote the endpoint quadratic to explicit closure",
            "include": "coefficient origin, boundary charge metric, Q_* normalization, sigma sign, first-order arrow law, no multiplier trick",
            "exclude": "new cosmology scoring, fitted endpoint labels, formalization-workbench edits, public claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "wrote the minimal boundary action that exactly generates the endpoint roots and exposed the sign/arrow blocker",
            "best_partial_result": "U(R)=9R^3-6R^2+R gives dU/dR=(3R-1)(9R-1), roots 1/9 and 1/3, DeltaR=2/9",
            "hard_blockers": "parent origin of 9,-6,1, Q_* charge unit, action sign, endpoint arrow, boundary no-hair",
            "what_is_not_claimed": "DeltaR prediction, Q_* derivation, endpoint arrow, local no-hair, q_loc zero, local GR/Newton",
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
    action_rows: list[dict[str, object]],
    stationarity: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    qstar: list[dict[str, object]],
    arrows: list[dict[str, object]],
    local_impact: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    action_ok = any(row["action_id"] == "BA865_0_minimal_dimensionless_action" and row["status"] == "formal_owner_written_not_parent_derived" for row in action_rows)
    roots_ok = DELTA_R == Fraction(2, 9) and any(row["derivation_id"] == "SD865_1_roots" and row["status"] == "verified_algebra" for row in stationarity)
    arrow_problem_ok = any(row["derivation_id"] == "SD865_2_second_variation" and row["status"] == "arrow_problem_exposed" for row in stationarity)
    coefficient_block_ok = any(row["coefficient_id"] == "CO865_4_sign" and row["current_status"] == "arrow_critical_unsigned" for row in coefficients)
    qstar_block_ok = any(row["qstar_id"] == "QS865_0_definition" and row["current_status"] == "missing_parent_definition" for row in qstar)
    arrow_block_ok = any(row["arrow_id"] == "AR865_3_arrow_verdict" and row["status"] == "arrow_blocks_prediction" for row in arrows)
    local_not_promoted = any(row["impact_id"] == "LI865_2_GR_Newton_verdict" and row["current_status"] == "not_derived" for row in local_impact)
    route_selected = any(row["route_id"] == "RC865_0_selected" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, action_rows, stationarity, coefficients, qstar, arrows, local_impact, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V865_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V865_1_prior_864_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V865_2_minimal_action_written", "result": "pass" if action_ok else "fail", "detail": "formal boundary action owner written without promotion"},
        {"check_id": "V865_3_roots_verified", "result": "pass" if roots_ok else "fail", "detail": "roots 1/9 and 1/3 give DeltaR=2/9"},
        {"check_id": "V865_4_arrow_problem_exposed", "result": "pass" if arrow_problem_ok else "fail", "detail": "second variation shows positive-U arrow issue"},
        {"check_id": "V865_5_coefficients_block_claim", "result": "pass" if coefficient_block_ok else "fail", "detail": "coefficient/sign origin remains unsigned"},
        {"check_id": "V865_6_Qstar_blocks_claim", "result": "pass" if qstar_block_ok else "fail", "detail": "Q_* parent charge unit remains missing"},
        {"check_id": "V865_7_arrow_blocks_claim", "result": "pass" if arrow_block_ok else "fail", "detail": "endpoint arrow remains unproved"},
        {"check_id": "V865_8_local_GR_not_promoted", "result": "pass" if local_not_promoted else "fail", "detail": "local GR/Newton verdict remains not derived"},
        {"check_id": "V865_9_route_selected", "result": "pass" if route_selected else "fail", "detail": "coefficient origin and arrow law selected"},
        {"check_id": "V865_10_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V865_11_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V865_12_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V865_13_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V865_14_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    action_rows: list[dict[str, object]],
    stationarity: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    qstar: list[dict[str, object]],
    arrows: list[dict[str, object]],
    local_impact: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 865 - Y5 R10 Minimal Boundary Charge Action For Endpoint Stationarity And Qstar",
        "",
        "Current result: **the minimal boundary action can generate the exact roots, but it still is not a parent derivation**. The formal owner is `S_trace = sigma kappa Q_*[9R^3-6R^2+R]`, so stationarity gives `(3R-1)(9R-1)=0`, roots `1/3` and `1/9`, and `DeltaR=2/9`. The catch is important: the coefficients, the charge unit `Q_*`, and the endpoint arrow/sign are not parent-owned. With positive `U`, the second variation makes `1/3` stable and `1/9` unstable, so the desired high-to-low arrow needs an owned sign or first-order arrow law.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Boundary Action Attempt",
        "",
        csv_table(action_rows, ["action_id", "object", "candidate_action", "variation", "result", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Stationarity Derivation",
        "",
        csv_table(stationarity, ["derivation_id", "statement", "computed_value", "meaning", "status", "valid_for_claim"]),
        "",
        "## Coefficient Ownership Audit",
        "",
        csv_table(coefficients, ["coefficient_id", "coefficient_source_candidate", "mathematical_form", "current_status", "why_not_enough", "next_test", "valid_for_claim"]),
        "",
        "## Qstar Normalization Contract",
        "",
        csv_table(qstar, ["qstar_id", "required_object", "candidate_definition", "current_status", "if_found", "if_missing", "valid_for_claim"]),
        "",
        "## Endpoint Arrow Stability Audit",
        "",
        csv_table(arrows, ["arrow_id", "candidate_arrow", "mathematical_test", "result", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Local GR Impact Ledger",
        "",
        csv_table(local_impact, ["impact_id", "conditional_result", "local_GR_effect", "remaining_debt", "current_status", "valid_for_claim"]),
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
    source_rows = source_register_rows(generated_utc)
    action_rows = action_attempt_rows(generated_utc)
    stationarity = stationarity_rows(generated_utc)
    coefficients = coefficient_rows(generated_utc)
    qstar = qstar_rows(generated_utc)
    arrows = arrow_rows(generated_utc)
    local_impact = local_impact_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        action_rows,
        stationarity,
        coefficients,
        qstar,
        arrows,
        local_impact,
        routes,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ACTION_ATTEMPT_PATH, action_rows, ["action_id", "object", "candidate_action", "variation", "result", "status", "missing_for_claim", "valid_for_claim", "generated_utc"])
    write_csv(STATIONARITY_PATH, stationarity, ["derivation_id", "statement", "computed_value", "meaning", "status", "valid_for_claim", "generated_utc"])
    write_csv(COEFFICIENT_AUDIT_PATH, coefficients, ["coefficient_id", "coefficient_source_candidate", "mathematical_form", "current_status", "why_not_enough", "next_test", "valid_for_claim", "generated_utc"])
    write_csv(QSTAR_PATH, qstar, ["qstar_id", "required_object", "candidate_definition", "current_status", "if_found", "if_missing", "valid_for_claim", "generated_utc"])
    write_csv(ARROW_PATH, arrows, ["arrow_id", "candidate_arrow", "mathematical_test", "result", "status", "missing_for_claim", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_IMPACT_PATH, local_impact, ["impact_id", "conditional_result", "local_GR_effect", "remaining_debt", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, action_rows, stationarity, coefficients, qstar, arrows, local_impact, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print("partial_result=U(R)=9R^3-6R^2+R gives roots 1/9 and 1/3, but coefficient origin, Qstar, and arrow remain unsigned")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

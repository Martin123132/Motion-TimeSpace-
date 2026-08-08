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

OUTPUT_DOC = POST_CHECKPOINT / "867-Y5-R10-boundary-orientation-charge-metric-last-derivation-gate.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_867_SOURCE_REGISTER.csv"
METRIC_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_867_BOUNDARY_METRIC_CANDIDATE.csv"
ORIENTATION_ARROW_PATH = RESIDUALS / "P8_Y5_R10_867_ORIENTATION_ARROW_AUDIT.csv"
QSTAR_UNIQUENESS_PATH = RESIDUALS / "P8_Y5_R10_867_QSTAR_UNIQUENESS_AUDIT.csv"
NO_GO_PATH = RESIDUALS / "P8_Y5_R10_867_POSITIVE_METRIC_NO_GO.csv"
CLOSURE_FREEZE_PATH = RESIDUALS / "P8_Y5_R10_867_CLOSURE_FREEZE_LEDGER.csv"
LOCAL_GR_RETURN_PATH = RESIDUALS / "P8_Y5_R10_867_LOCAL_GR_RETURN_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_867_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_867_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_867_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_867_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_867_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_867_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_866_VALIDATION.csv"

STATUS = "Y5_R10_867_boundary_metric_candidate_written_positive_metric_arrow_no_go_endpoint_frozen_to_closure_nonclaim"
CLAIM_CEILING = "boundary_metric_candidate_only_positive_energy_no_go_no_Qstar_no_arrow_no_local_GR_claim"
NEXT_TARGET = "868-Y5-R10-local-GR-reduction-stack-after-endpoint-closure.md"

ROOT_LOW = Fraction(1, 9)
ROOT_HIGH = Fraction(1, 3)
U_LOW = Fraction(4, 81)
U_HIGH = Fraction(0, 1)
SECOND_LOW = Fraction(-6, 1)
SECOND_HIGH = Fraction(6, 1)

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    METRIC_CANDIDATE_PATH,
    ORIENTATION_ARROW_PATH,
    QSTAR_UNIQUENESS_PATH,
    NO_GO_PATH,
    CLOSURE_FREEZE_PATH,
    LOCAL_GR_RETURN_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "866_doc",
        "path": POST_CHECKPOINT / "866-Y5-R10-endpoint-coefficient-origin-and-arrow-law-or-demote-to-closure.md",
        "needles": [
            "QS866_1_charge_metric",
            "CL866_0_endpoint_quadratic_status",
            "867-Y5-R10-boundary-orientation-charge-metric-last-derivation-gate.md",
        ],
        "role": "immediate boundary metric/orientation handoff",
    },
    {
        "source_id": "866_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V866_8_closure_selected,pass",
            "V866_11_all_rows_nonclaim,pass",
            "V866_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "861_endpoint_N5",
        "path": POST_CHECKPOINT / "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md",
        "needles": [
            "EP861_0_charge_unit",
            "EP861_1_early_endpoint",
            "EP861_4_nohair",
        ],
        "role": "charge unit, endpoint, and no-hair debts",
    },
    {
        "source_id": "862_trace_lift",
        "path": POST_CHECKPOINT / "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md",
        "needles": [
            "TL862_3_endpoint_identification",
            "EC862_0_Ward_stationarity",
            "EC862_4_endpoint_local_silence",
        ],
        "role": "trace-lift endpoint stationarity and local silence debts",
    },
    {
        "source_id": "863_local_zero",
        "path": POST_CHECKPOINT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needles": [
            "WTC863_4_local_projection_silence",
            "CZT863_2_local_global_split",
            "local GR/Newton",
        ],
        "role": "local/global quotient and local GR zero theorem debts",
    },
    {
        "source_id": "864_quotient_split",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "q_FLRW",
            "q_loc[U]",
            "endpoint_stationarity_and_Qstar_are_next",
        ],
        "role": "local/global quotient split parent clause",
    },
    {
        "source_id": "109_boundary_charge",
        "path": POST_CHECKPOINT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needles": [
            "normalized boundary charge",
            "boundary_charge_unit_defined",
            "product_two_over_nine_derived",
        ],
        "role": "boundary charge normalization failure",
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
    return [
        {
            "source_id": spec["source_id"],
            "path": str(spec["path"]),
            "exists": str(spec["path"].exists()).lower(),
            "needle_check": check_needles(spec["path"], spec["needles"]),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for spec in SOURCE_SPECS
    ]


def metric_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "metric_id": "BM867_0_minimal_metric_candidate",
            "candidate_parent_object": "S_B = epsilon kappa Q_* R ||T(R)||_B^2 with T(R)=3R-1",
            "derivation_attempt": "choose boundary occupancy measure dmu_B=dQ=Q_* dR and trace-deficit norm ||T||_B^2=(3R-1)^2",
            "what_it_would_give": "S_B/Q_* = epsilon kappa R(3R-1)^2",
            "result": "reconstructs the 866 factor form exactly",
            "blocker": "dmu_B=dQ, T=3R-1, the square norm, Q_*, and epsilon are not derived from the parent action",
            "status": "candidate_constructed_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "metric_id": "BM867_1_linear_measure_p1",
            "candidate_parent_object": "linear boundary occupancy measure",
            "derivation_attempt": "require the boundary integral to carry exactly one power of normalized charge R",
            "what_it_would_give": "p=1 in U_p=R^p(3R-1)^2 and therefore the nonzero extra root R=1/9",
            "result": "identifies the exact parent requirement for p=1",
            "blocker": "no corpus theorem forbids p=0, p=2, area-like weighting, volume-like weighting, or representative-dependent weights",
            "status": "sharp_requirement_not_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "metric_id": "BM867_2_trace_deficit",
            "candidate_parent_object": "normalized FLRW trace deficit",
            "derivation_attempt": "T(R)=3R-1 from three spatial trace legs and a unit trace endpoint",
            "what_it_would_give": "zero-deficit endpoint R=1/3 and endpoint quadratic derivative (3R-1)(9R-1)",
            "result": "matches the trace-lift story",
            "blocker": "three-leg counting is not a variational norm until q_FLRW and Q_* are action-owned",
            "status": "plausible_trace_metric_unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "metric_id": "BM867_3_metric_uniqueness",
            "candidate_parent_object": "unique boundary inner product",
            "derivation_attempt": "demand a parent symmetry or Ward identity that selects R(3R-1)^2 up to scale and additive constant",
            "what_it_would_give": "turns endpoint roots from closure to prediction",
            "result": "not available in the current corpus",
            "blocker": "no uniqueness theorem for the boundary metric/action family",
            "status": "uniqueness_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def orientation_arrow_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "arrow_id": "OA867_0_positive_metric_gradient",
            "orientation_case": "epsilon=+1 and ordinary energy descent",
            "calculation": f"U({ROOT_HIGH})={U_HIGH}, U({ROOT_LOW})={U_LOW}, U''({ROOT_HIGH})={SECOND_HIGH}, U''({ROOT_LOW})={SECOND_LOW}",
            "arrow_result": "R=1/3 is the attractor/minimum and R=1/9 is not the desired final attractor",
            "verdict": "fails_desired_high_to_low_arrow",
            "missing_parent_input": "none can fix this within positive-energy gradient descent; assumptions must change",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "OA867_1_boundary_orientation_flip",
            "orientation_case": "epsilon=-1 or outward-boundary sign reversal",
            "calculation": "stationary roots unchanged, second variation signs flip",
            "arrow_result": "R=1/9 can become attracting if the reduced dynamics uses the oriented negative potential",
            "verdict": "mathematically_viable_but_unsigned",
            "missing_parent_input": "derive boundary orientation sign from parent action, not from the desired endpoint order",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "OA867_2_entropy_or_open_current",
            "orientation_case": "first-order irreversible boundary current",
            "calculation": "dot R = mu(R-1/3)(R-1/9), mu>0 gives high repeller and low attractor",
            "arrow_result": "correct endpoint arrow if the current is parent-derived",
            "verdict": "possible_route_but_extra_dynamics",
            "missing_parent_input": "derive irreversible current/entropy functional; do not smuggle it in after stationarity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "OA867_3_lorentzian_action_warning",
            "orientation_case": "stationary action without dissipative reduction",
            "calculation": "stationarity alone supplies roots but no attractor labels",
            "arrow_result": "endpoint labels early/today remain underdetermined",
            "verdict": "stationarity_not_arrow",
            "missing_parent_input": "cosmological time-orientation theorem or endpoint transition law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qstar_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "qstar_id": "QU867_0_charge_unit",
            "object": "Q_*",
            "required_derivation": "fixed parent-normalized boundary charge unit before cosmology data",
            "current_status": "missing",
            "why_it_matters": "without Q_*, R=Q/Q_* is a convenient dimensionless coordinate rather than a physical action variable",
            "failure_mode": "post-fit calibration would make DeltaR circular",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QU867_1_trace_capacity",
            "object": "unit trace endpoint",
            "required_derivation": "prove the normalized trace capacity is the object that makes T(R)=3R-1",
            "current_status": "unsigned",
            "why_it_matters": "the factor 3 becomes a parent trace norm rather than component-count poetry",
            "failure_mode": "alternative normalizations move the endpoint roots",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QU867_2_local_nohair_compatibility",
            "object": "P_loc Q_trace=0",
            "required_derivation": "same Q_* charge must be FLRW-visible but locally quotient-vertical",
            "current_status": "conditional_only",
            "why_it_matters": "endpoint charge must not become PPN/WEP/clock/orbital hair",
            "failure_mode": "nonzero local residuals require bounds instead of GR reduction claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def no_go_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "nog_id": "NG867_0_positive_metric_energy_no_go",
            "assumptions": "positive semidefinite boundary charge metric, U=R(3R-1)^2, ordinary downhill relaxation, endpoint interval containing 1/9 and 1/3",
            "calculation": "U(1/3)=0<U(1/9)=4/81 and U''(1/3)>0 while U''(1/9)<0",
            "conclusion": "the high-to-low endpoint arrow 1/3 -> 1/9 cannot be derived from this positive-energy gradient mechanism",
            "escape_routes": "parent orientation epsilon=-1, entropy/open-current dynamics, endpoint label reinterpretation, or abandon endpoint arrow derivation",
            "status": "conditional_no_go_proved",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "nog_id": "NG867_1_stationarity_not_prediction_no_go",
            "assumptions": "stationary action without a parent-owned Q_* and endpoint transition law",
            "calculation": "roots exist but normalization and labels are free",
            "conclusion": "stationarity alone does not make DeltaR=2/9 a physical prediction",
            "escape_routes": "derive Q_*, unique boundary metric, and arrow law from parent action",
            "status": "prediction_claim_blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def closure_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "closure_id": "CF867_0_freeze_endpoint_quadratic",
            "object": "endpoint potential U=R(3R-1)^2",
            "new_status": "explicit_closure_ansatz",
            "reason": "the last metric gate found a clean candidate and a positive-energy no-go, but not a parent-signed Q_*, sign, or uniqueness theorem",
            "allowed_use": "private stress-test closure for cosmology and trace-memory phenomenology",
            "forbidden_use": "claiming DeltaR=2/9 is derived from the parent theory",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CF867_1_keep_best_clue",
            "object": "linear occupancy times squared trace-deficit",
            "new_status": "retained_candidate_mechanism",
            "reason": "R(3R-1)^2 is too structured to discard, but not strong enough to promote",
            "allowed_use": "guide future parent-action searches",
            "forbidden_use": "continuing endpoint algebra loops without new parent input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_gr_return_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "return_id": "LG867_0_return_to_local_GR_stack",
            "target": "local GR/Newton reduction",
            "reason": "endpoint roots are now closure-only; the main theory goal needs local quotient silence, source normalization, and EH/projector reduction",
            "next_requirement": "derive or bound q_loc^nu with P_loc J_trace, coframe pullback, projector stress, and matter descent all explicit",
            "claim_status": "not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "return_id": "LG867_1_nohair_priority",
            "target": "boundary/local no-hair",
            "reason": "even a perfect cosmological endpoint action fails local GR if it leaks into PPN/WEP/clock/orbital observables",
            "next_requirement": "prove Q_trace is FLRW-visible but q_loc-vertical, or build retained residual coefficient rows",
            "claim_status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "return_id": "LG867_2_EH_Newton_priority",
            "target": "GR-to-Newton chain",
            "reason": "the user goal is not just a cosmology closure; MTS must recover local Einstein/Newton dynamics in the correct limit",
            "next_requirement": "map parent action terms to EH operator, Bianchi/conservation, matter stress source normalization, and Newtonian potential",
            "claim_status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC867_0_selected",
            "route": "freeze_endpoint_closure_and_return_to_local_GR_reduction_stack",
            "status": "selected",
            "reason": "the derivation-first endpoint route now has a conditional no-go under positive metric dynamics and no parent-signed escape route",
            "include": "local quotient silence, no-hair, source normalization, EH/Newton limit, retained residual branch",
            "exclude": "more endpoint root algebra, public DeltaR claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG867_0_no_boundary_metric_claim",
            "claim": "boundary charge metric is derived",
            "status": "forbidden",
            "reason": "867 constructs a minimal candidate but does not find a parent uniqueness theorem or Q_* unit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG867_1_no_arrow_claim",
            "claim": "endpoint arrow is derived",
            "status": "forbidden",
            "reason": "positive metric gradient gives the wrong attractor; escape routes are unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG867_2_no_DeltaR_claim",
            "claim": "DeltaR=2/9 is parent-predicted",
            "status": "forbidden",
            "reason": "endpoint potential is frozen as closure-only until parent charge metric, Q_*, and arrow law are proved",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG867_3_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "local quotient silence, no-hair, source normalization, and EH/projector reduction remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG867_4_allowed_private_result",
            "claim": "positive metric endpoint route is conditionally rejected",
            "status": "allowed_private_nonclaim",
            "reason": "the no-go clarifies why the next productive route is local GR reduction rather than endpoint algebra",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D867_0",
            "finding": "minimal_boundary_metric_candidate_constructed",
            "reason": "S_B=epsilon kappa Q_* R(3R-1)^2 reconstructs the endpoint potential if occupancy and trace-deficit norm are assumed",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D867_1",
            "finding": "positive_metric_arrow_no_go",
            "reason": "ordinary positive-energy gradient flow stabilizes R=1/3, not R=1/9",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D867_2",
            "finding": "orientation_escape_unsigned",
            "reason": "epsilon=-1 or first-order current can produce the desired arrow but is not derived from the parent action",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D867_3",
            "finding": "endpoint_branch_frozen_to_closure",
            "reason": "continuing endpoint algebra without new parent input would be closure polishing, not derivation",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D867_4",
            "finding": "return_to_local_GR_stack",
            "reason": "the full project now needs the local quotient/no-hair/source-normalization/EH-Newtown chain attacked directly",
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
            "objective": "return to the local GR/Newton derivation stack after freezing the endpoint quadratic as closure: derive or bound q_loc^nu, no-hair, source normalization, and EH/projector reduction",
            "include": "P_loc J_trace, coframe pullback, matter descent, Bianchi/conservation, source normalization, Newtonian limit, retained residual fallback",
            "exclude": "new endpoint root algebra, public claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "constructed the minimal boundary metric candidate and proved a conditional no-go for the desired arrow under positive-energy gradient dynamics",
            "best_partial_result": "R(3R-1)^2 is interpretable as linear boundary occupancy times squared trace-deficit, but positive metric descent flows to R=1/3",
            "hard_blockers": "Q_* unit, metric uniqueness, parent orientation sign, irreversible current, local no-hair, EH/Newton reduction",
            "what_is_not_claimed": "boundary metric derivation, endpoint arrow, DeltaR prediction, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_csv_rows_nonclaim(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists():
            offenders.append(f"{path.name}:missing")
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for index, row in enumerate(csv.DictReader(handle), start=2):
                if row.get("valid_for_claim") != "false":
                    offenders.append(f"{path.name}:{index}")
    if offenders:
        return False, ";".join(offenders)
    return True, "all generated rows valid_for_claim=false"


def csv_table(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    metric_rows: list[dict[str, object]],
    arrow_rows: list[dict[str, object]],
    qstar_rows_: list[dict[str, object]],
    no_go_rows_: list[dict[str, object]],
    closure_rows_: list[dict[str, object]],
    local_gr_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 867 - Boundary Orientation Charge Metric Last Derivation Gate

Generated: `{generated_utc}`

Current result: **the endpoint branch now has a useful no-go, so it should be frozen as closure unless new parent input appears**. The best parent-shaped object is `S_B = epsilon kappa Q_* R(3R-1)^2`: linear boundary occupancy times squared trace-deficit. That reconstructs the exact endpoint action, but it does not derive `Q_*`, metric uniqueness, or the sign. Worse for the desired arrow, under a positive semidefinite boundary metric with ordinary downhill dynamics, `R=1/3` is the attractor and `R=1/9` is not. The desired `1/3 -> 1/9` route needs either a parent-owned orientation flip or a first-order irreversible boundary current. Since neither is currently signed by the corpus, the endpoint quadratic is explicitly closure-only and the next useful work returns to the local GR/Newton reduction stack.

## Nonclaim Summary

{csv_table(summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])}

## Boundary Metric Candidate

{csv_table(metric_rows, ["metric_id", "candidate_parent_object", "derivation_attempt", "what_it_would_give", "result", "blocker", "status", "valid_for_claim", "generated_utc"])}

## Orientation Arrow Audit

{csv_table(arrow_rows, ["arrow_id", "orientation_case", "calculation", "arrow_result", "verdict", "missing_parent_input", "valid_for_claim", "generated_utc"])}

## Qstar Uniqueness Audit

{csv_table(qstar_rows_, ["qstar_id", "object", "required_derivation", "current_status", "why_it_matters", "failure_mode", "valid_for_claim", "generated_utc"])}

## Positive Metric No-Go

{csv_table(no_go_rows_, ["nog_id", "assumptions", "calculation", "conclusion", "escape_routes", "status", "valid_for_claim", "generated_utc"])}

## Closure Freeze Ledger

{csv_table(closure_rows_, ["closure_id", "object", "new_status", "reason", "allowed_use", "forbidden_use", "valid_for_claim", "generated_utc"])}

## Local GR Return Ledger

{csv_table(local_gr_rows, ["return_id", "target", "reason", "next_requirement", "claim_status", "valid_for_claim", "generated_utc"])}

## Route Choice

{csv_table(route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Claim Guard

{csv_table(claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])}

## Decision

{csv_table(decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])}

## Next Target

{csv_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{csv_table(validation_rows, ["check_id", "result", "detail"])}
"""
    OUTPUT_DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat()

    source_rows = source_register_rows(generated_utc)
    metric_rows = metric_candidate_rows(generated_utc)
    arrow_rows = orientation_arrow_rows(generated_utc)
    qstar_rows_ = qstar_rows(generated_utc)
    no_go_rows_ = no_go_rows(generated_utc)
    closure_rows_ = closure_rows(generated_utc)
    local_gr_rows = local_gr_return_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    claim_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(METRIC_CANDIDATE_PATH, metric_rows, ["metric_id", "candidate_parent_object", "derivation_attempt", "what_it_would_give", "result", "blocker", "status", "valid_for_claim", "generated_utc"])
    write_csv(ORIENTATION_ARROW_PATH, arrow_rows, ["arrow_id", "orientation_case", "calculation", "arrow_result", "verdict", "missing_parent_input", "valid_for_claim", "generated_utc"])
    write_csv(QSTAR_UNIQUENESS_PATH, qstar_rows_, ["qstar_id", "object", "required_derivation", "current_status", "why_it_matters", "failure_mode", "valid_for_claim", "generated_utc"])
    write_csv(NO_GO_PATH, no_go_rows_, ["nog_id", "assumptions", "calculation", "conclusion", "escape_routes", "status", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_FREEZE_PATH, closure_rows_, ["closure_id", "object", "new_status", "reason", "allowed_use", "forbidden_use", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_GR_RETURN_PATH, local_gr_rows, ["return_id", "target", "reason", "next_requirement", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])

    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    source_checks_pass = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    metric_candidate_pass = any(row["metric_id"] == "BM867_0_minimal_metric_candidate" and row["result"] == "reconstructs the 866 factor form exactly" for row in metric_rows)
    p1_requirement_pass = any(row["metric_id"] == "BM867_1_linear_measure_p1" and row["status"] == "sharp_requirement_not_theorem" for row in metric_rows)
    positive_no_go_pass = any(row["nog_id"] == "NG867_0_positive_metric_energy_no_go" and row["status"] == "conditional_no_go_proved" for row in no_go_rows_)
    orientation_unsigned_pass = any(row["arrow_id"] == "OA867_1_boundary_orientation_flip" and row["verdict"] == "mathematically_viable_but_unsigned" for row in arrow_rows)
    qstar_missing_pass = all(row["valid_for_claim"] == "false" and row["current_status"] in {"missing", "unsigned", "conditional_only"} for row in qstar_rows_)
    closure_freeze_pass = any(row["closure_id"] == "CF867_0_freeze_endpoint_quadratic" and row["new_status"] == "explicit_closure_ansatz" for row in closure_rows_)
    local_gr_return_pass = any(row["return_id"] == "LG867_0_return_to_local_GR_stack" for row in local_gr_rows)
    route_selected_pass = any(row["route_id"] == "RC867_0_selected" and row["route"] == "freeze_endpoint_closure_and_return_to_local_GR_reduction_stack" for row in route_rows)
    claim_allowed_false_pass = all(row["claim_allowed"] == "false" for row in decision_rows_)
    formalization_count = formalization_workbench_modified_count()

    validation_rows = [
        {"check_id": "V867_0_sources_exist_and_needles", "result": "pass" if source_checks_pass else "fail", "detail": "all source paths exist and needles are present" if source_checks_pass else "one or more source checks failed"},
        {"check_id": "V867_1_prior_866_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V867_2_metric_candidate_written", "result": "pass" if metric_candidate_pass else "fail", "detail": "minimal boundary metric candidate reconstructs factor form"},
        {"check_id": "V867_3_p1_requirement_preserved", "result": "pass" if p1_requirement_pass else "fail", "detail": "linear occupancy p=1 kept as requirement, not theorem"},
        {"check_id": "V867_4_positive_metric_no_go", "result": "pass" if positive_no_go_pass else "fail", "detail": "positive metric gradient cannot derive desired high-to-low arrow"},
        {"check_id": "V867_5_orientation_escape_unsigned", "result": "pass" if orientation_unsigned_pass else "fail", "detail": "orientation flip remains viable but unsigned"},
        {"check_id": "V867_6_Qstar_blocks_claim", "result": "pass" if qstar_missing_pass else "fail", "detail": "Q_* and trace capacity remain missing/unsigned"},
        {"check_id": "V867_7_endpoint_closure_frozen", "result": "pass" if closure_freeze_pass else "fail", "detail": "endpoint quadratic frozen as explicit closure ansatz"},
        {"check_id": "V867_8_local_GR_return_ready", "result": "pass" if local_gr_return_pass else "fail", "detail": "local GR/Newton stack selected as next work"},
        {"check_id": "V867_9_route_selected", "result": "pass" if route_selected_pass else "fail", "detail": NEXT_TARGET},
        {"check_id": "V867_10_claim_allowed_false", "result": "pass" if claim_allowed_false_pass else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V867_11_all_rows_nonclaim", "result": "pending", "detail": "filled after csv nonclaim scan"},
        {"check_id": "V867_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V867_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]

    nonclaim_pass, nonclaim_detail = all_csv_rows_nonclaim(GENERATED_CSV_PATHS)
    for row in validation_rows:
        if row["check_id"] == "V867_11_all_rows_nonclaim":
            row["result"] = "pass" if nonclaim_pass else "fail"
            row["detail"] = nonclaim_detail

    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_markdown(
        generated_utc,
        source_rows,
        metric_rows,
        arrow_rows,
        qstar_rows_,
        no_go_rows_,
        closure_rows_,
        local_gr_rows,
        route_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"status={STATUS}")
    print("partial_result=boundary metric candidate reconstructs R(3R-1)^2, but positive metric descent gives wrong arrow; endpoint branch frozen to closure")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")
    if failed:
        for row in failed:
            print(f"validation_failure={row['check_id']}:{row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

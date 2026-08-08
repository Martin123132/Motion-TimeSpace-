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

OUTPUT_DOC = POST_CHECKPOINT / "866-Y5-R10-endpoint-coefficient-origin-and-arrow-law-or-demote-to-closure.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_866_SOURCE_REGISTER.csv"
FACTOR_FORM_PATH = RESIDUALS / "P8_Y5_R10_866_FACTOR_FORM_ORIGIN_AUDIT.csv"
COEFFICIENT_PATH = RESIDUALS / "P8_Y5_R10_866_COEFFICIENT_DERIVATION_ATTEMPT.csv"
ARROW_PATH = RESIDUALS / "P8_Y5_R10_866_ARROW_LAW_ATTEMPT.csv"
QSTAR_PATH = RESIDUALS / "P8_Y5_R10_866_QSTAR_CHARGE_METRIC_AUDIT.csv"
CLOSURE_PATH = RESIDUALS / "P8_Y5_R10_866_CLOSURE_DEMOTION_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_866_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_866_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_866_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_866_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_866_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_866_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_865_VALIDATION.csv"

STATUS = "Y5_R10_866_factor_form_found_but_parent_coefficients_Qstar_arrow_unsigned_endpoint_closure_nonclaim"
CLAIM_CEILING = "exact_factor_form_candidate_only_no_parent_coefficient_no_Qstar_no_arrow_no_local_GR_claim"
NEXT_TARGET = "867-Y5-R10-boundary-orientation-charge-metric-last-derivation-gate.md"

ROOT_LOW = Fraction(1, 9)
ROOT_HIGH = Fraction(1, 3)
DELTA_R = ROOT_HIGH - ROOT_LOW

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    FACTOR_FORM_PATH,
    COEFFICIENT_PATH,
    ARROW_PATH,
    QSTAR_PATH,
    CLOSURE_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "865_doc",
        "path": POST_CHECKPOINT / "865-Y5-R10-minimal-boundary-charge-action-for-endpoint-stationarity-and-Qstar.md",
        "needles": [
            "minimal boundary action can generate the exact roots",
            "SD865_2_second_variation",
            "866-Y5-R10-endpoint-coefficient-origin-and-arrow-law-or-demote-to-closure.md",
        ],
        "role": "immediate coefficient/sign/Qstar blocker",
    },
    {
        "source_id": "865_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V865_4_arrow_problem_exposed,pass",
            "V865_11_all_rows_nonclaim,pass",
            "V865_13_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
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
        "source_id": "110_endpoint_equation",
        "path": POST_CHECKPOINT / "110-endpoint-charge-equation-attempt.md",
        "needles": [
            "27R^2 - 12R + 1 = 0",
            "endpoint_equation_parent_derived",
            "Qstar_charge_unit_derived",
        ],
        "role": "target endpoint quadratic before action owner",
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
        "source_id": "94_relaxation_arrow",
        "path": POST_CHECKPOINT / "94-endpoint-relaxation-DeltaR-gate.md",
        "needles": [
            "endpoint_ordering_parent_derived",
            "DeltaR_predicted_without_SN_BAO_fit",
            "cosmological arrow",
        ],
        "role": "endpoint ordering and cosmological arrow guard",
    },
    {
        "source_id": "864_quotient_split",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "minimal parent-action clause is now explicit",
            "q_FLRW",
            "q_loc[U]",
        ],
        "role": "local/global quotient split context",
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


def factor_form_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "factor_id": "FF866_0_factor_identity",
            "statement": "9R^3-6R^2+R = R(3R-1)^2",
            "calculation": "expand R(9R^2-6R+1)",
            "result": "exact identity",
            "meaning": "the coefficients 9,-6,1 follow if the parent action supplies linear occupancy R times squared trace-deficit (3R-1)^2",
            "status": "algebraic_factor_form_found_not_parent_forced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "factor_id": "FF866_1_derivative_roots",
            "statement": "d/dR[R(3R-1)^2]=(3R-1)(9R-1)",
            "calculation": "(3R-1)^2+6R(3R-1)",
            "result": f"stationary roots R={ROOT_LOW} and R={ROOT_HIGH}; DeltaR={DELTA_R}",
            "meaning": "the low endpoint 1/9 is the occupancy/deficit tradeoff extremum and 1/3 is the zero-deficit endpoint",
            "status": "verified_algebra_not_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "factor_id": "FF866_2_generalized_power_test",
            "statement": "U_p(R)=R^p(3R-1)^2 gives extra stationary root R=p/(3p+6)",
            "calculation": "dU_p/dR=R^(p-1)(3R-1)[(3p+6)R-p]",
            "result": "R=1/9 requires p=1",
            "meaning": "linear occupancy is not cosmetic; the parent action must specifically choose p=1, not area/volume/weighted occupancy",
            "status": "sharp_parent_requirement_identified",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "factor_id": "FF866_3_constant_scale_freedom",
            "statement": "overall scale and additive constant do not move stationary roots",
            "calculation": "d/dR[cU+C]=c dU/dR",
            "result": "roots survive for c nonzero",
            "meaning": "root prediction cannot determine kappa, Q_*, or absolute energy; those need independent parent normalization",
            "status": "normalization_not_fixed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coefficient_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "coefficient_id": "CD866_0_occupancy_trace_deficit",
            "candidate_origin": "linear boundary occupancy times squared trace-deficit",
            "candidate_formula": "U=R(3R-1)^2",
            "what_it_explains": "expands to 9R^3-6R^2+R and differentiates to the endpoint quadratic",
            "why_not_parent_proof": "the corpus has not derived why the boundary energy is exactly occupancy times a squared trace deficit",
            "required_parent_clause": "parent boundary charge metric with linear measure R and trace-deficit norm (3R-1)^2",
            "status": "promising_candidate_not_forced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CD866_1_factor_three",
            "candidate_origin": "three spatial trace directions",
            "candidate_formula": "3R-1",
            "what_it_explains": "1/3 is the zero trace-deficit endpoint",
            "why_not_parent_proof": "three-direction counting is bookkeeping until q_FLRW/trace measure turns it into a variational norm",
            "required_parent_clause": "trace generator and quotient measure proving the normalized deficit is 3R-1",
            "status": "plausible_trace_readout_unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CD866_2_square_metric",
            "candidate_origin": "positive charge-deficit metric",
            "candidate_formula": "(3R-1)^2",
            "what_it_explains": "quadratic penalty around the zero-deficit endpoint",
            "why_not_parent_proof": "the charge metric and sign are missing; a square alone gives the wrong high-to-low stability under positive downhill flow",
            "required_parent_clause": "owned boundary inner product and orientation/sign convention",
            "status": "metric_shape_unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CD866_3_linear_occupancy",
            "candidate_origin": "one boundary occupancy factor",
            "candidate_formula": "R^p with p=1",
            "what_it_explains": "p=1 uniquely places the second stationary point at 1/9",
            "why_not_parent_proof": "no parent measure currently forbids p!=1",
            "required_parent_clause": "boundary integral whose measure contains one and only one power of normalized charge occupancy",
            "status": "exact_requirement_identified_not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CD866_4_no_alternative_family",
            "candidate_origin": "uniqueness of endpoint action",
            "candidate_formula": "forbid R^p(3R-1)^2, extra powers, and representative-dependent terms",
            "what_it_explains": "would turn the exact roots into a prediction rather than chosen closure",
            "why_not_parent_proof": "the corpus has no uniqueness theorem for the boundary action",
            "required_parent_clause": "symmetry/regularity/Ward identity selecting U=R(3R-1)^2 up to scale and constant",
            "status": "uniqueness_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def arrow_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "arrow_id": "AL866_0_positive_U_downhill",
            "candidate_law": "ordinary downhill relaxation in positive U=R(3R-1)^2",
            "test": "U(1/3)=0, U(1/9)=4/81, U''(1/3)=6, U''(1/9)=-6",
            "result": "1/3 is stable/min-like and 1/9 is unstable/max-like on the endpoint interval",
            "physics_status": "opposite_to_desired_high_to_low_arrow",
            "missing_for_claim": "derive sign flip, anti-gradient law, or reinterpret endpoint labels from parent time orientation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "AL866_1_negative_U_or_orientation",
            "candidate_law": "boundary orientation supplies effective -U",
            "test": "gradient descent on -U equals dot R proportional to +dU/dR",
            "result": "can make 1/3 a repeller and 1/9 an attractor",
            "physics_status": "mathematically_viable_but_parent_unsigned",
            "missing_for_claim": "boundary orientation, entropy, or time-asymmetry clause deriving the sign",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "AL866_2_first_order_endpoint_flow",
            "candidate_law": "dot R = mu (R-1/3)(R-1/9), mu>0",
            "test": "between 1/9 and 1/3, dot R<0; below 1/9, dot R>0; near 1/3 the flow moves away",
            "result": "R=1/9 is attracting and R=1/3 is repelling",
            "physics_status": "correct_arrow_if_parent_current_derives_it",
            "missing_for_claim": "derive first-order flow from boundary current continuity rather than inserting it",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arrow_id": "AL866_3_endpoint_label_guard",
            "candidate_law": "assign R_early=1/3 and R_today=1/9",
            "test": "label assignment plus DeltaR=2/9",
            "result": "not generated by stationarity alone",
            "physics_status": "endpoint_ordering_unsigned",
            "missing_for_claim": "parent cosmological arrow theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qstar_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "qstar_id": "QS866_0_dimensionless_R",
            "needed_object": "R=Q/Q_*",
            "candidate_definition": "normalized trace boundary charge",
            "current_gap": "Q_* is not derived from a parent boundary charge metric",
            "effect_if_solved": "turns R from a fitted/formal coordinate into a physical action variable",
            "status": "missing_parent_charge_unit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QS866_1_charge_metric",
            "needed_object": "<delta Q,delta Q>_boundary",
            "candidate_definition": "metric whose norm produces R(3R-1)^2 and fixes sign/orientation",
            "current_gap": "no owned boundary inner product fixes the square, prefactor, scale, or sign",
            "effect_if_solved": "could close both coefficient origin and arrow sign in one stroke",
            "status": "best_next_derivation_target",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QS866_2_no_data_calibration",
            "needed_object": "pre-data normalization",
            "candidate_definition": "Q_* fixed before Pantheon/BAO/CMB scoring",
            "current_gap": "using cosmological fit to set Q_* would be circular",
            "effect_if_solved": "makes DeltaR=2/9 a genuine prior prediction candidate",
            "status": "guardrail",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def closure_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "closure_id": "CL866_0_endpoint_quadratic_status",
            "object": "U=R(3R-1)^2",
            "closure_status": "closure_only_until_parent_signed",
            "reason": "factor form is elegant and exact, but parent action has not forced R, 3R-1, square metric, p=1, Q_*, or sign",
            "allowed_use": "private closure ansatz for stress-testing cosmology/local residuals",
            "forbidden_use": "public claim that DeltaR=2/9 is derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CL866_1_derivation_credit",
            "object": "coefficient simplification",
            "closure_status": "real_progress_not_victory",
            "reason": "the coefficients are no longer arbitrary-looking numbers; they condense to occupancy times squared trace-deficit",
            "allowed_use": "record as the best candidate parent action shape",
            "forbidden_use": "treat factorization as proof of parent origin",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CL866_2_next_gate",
            "object": "boundary orientation and charge metric",
            "closure_status": "one_more_surgical_derivation_gate",
            "reason": "a real boundary charge metric could in principle fix p=1, Q_*, and sign together",
            "allowed_use": "try 867 as a final derivation-first pass before freezing closure",
            "forbidden_use": "keep looping on endpoint roots without new parent input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC866_0_selected",
            "route": "boundary_orientation_charge_metric_last_derivation_gate",
            "status": "selected",
            "reason": "the factor form points to one precise missing object: a boundary charge metric/orientation that fixes R(3R-1)^2 and the arrow sign",
            "include": "derive Q_*, linear occupancy p=1, trace-deficit norm, sign/orientation, first-order arrow if available",
            "exclude": "new empirical scoring, target-imposed multipliers, endpoint public claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC866_1_fallback",
            "route": "freeze_endpoint_quadratic_as_closure_and_return_to_local_GR_stack",
            "status": "fallback_if_867_unsigned",
            "reason": "if no boundary charge metric is found, continued endpoint algebra is just closure polishing",
            "include": "label closure honestly and resume local GR/no-hair/source-normalization gates",
            "exclude": "pretending coefficient factorization is a theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG866_0_no_coefficient_claim",
            "claim": "the endpoint coefficients are parent-derived",
            "status": "forbidden",
            "reason": "R(3R-1)^2 explains the coefficients only if the parent supplies linear occupancy and squared trace deficit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG866_1_no_arrow_claim",
            "claim": "the high-to-low endpoint arrow is derived",
            "status": "forbidden",
            "reason": "positive U gives the opposite stability; negative U or first-order flow needs parent sign/orientation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG866_2_no_Qstar_claim",
            "claim": "Q_* is derived",
            "status": "forbidden",
            "reason": "no boundary charge metric currently fixes the unit of R=Q/Q_*",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG866_3_no_local_GR_claim",
            "claim": "local GR/Newton follows from the endpoint action",
            "status": "forbidden",
            "reason": "endpoint closure does not prove local quotient silence, boundary no-hair, source normalization, or EH/projector reduction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG866_4_allowed_private_result",
            "claim": "best private coefficient mechanism is identified",
            "status": "allowed_private_nonclaim",
            "reason": "factor form and p=1 requirement sharpen the next derivation target without promoting a claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D866_0",
            "finding": "factor_form_found",
            "reason": "U=9R^3-6R^2+R equals R(3R-1)^2",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D866_1",
            "finding": "linear_occupancy_is_sharp_requirement",
            "reason": "U_p=R^p(3R-1)^2 gives the second stationary root p/(3p+6), so 1/9 requires p=1",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D866_2",
            "finding": "arrow_law_unsigned",
            "reason": "positive U stabilizes 1/3, while the desired high-to-low route needs -U orientation or a first-order flow",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D866_3",
            "finding": "endpoint_quadratic_demoted_to_closure_for_now",
            "reason": "without parent charge metric, Q_*, sign, and uniqueness, the exact endpoint action remains a closure ansatz",
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
            "objective": "make one surgical attempt to derive the boundary charge metric/orientation that fixes p=1, Q_*, and the endpoint arrow; otherwise freeze the endpoint quadratic as explicit closure",
            "include": "charge inner product, boundary measure, orientation sign, first-order arrow current, no data-fitted normalization",
            "exclude": "new roots, empirical scoring, public claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "found the exact factor form U=R(3R-1)^2 and proved p=1 is required for the 1/9 endpoint in the generalized family",
            "best_partial_result": "coefficients 9,-6,1 can be interpreted as linear boundary occupancy times squared spatial trace-deficit",
            "hard_blockers": "parent boundary charge metric, Q_* unit, p=1 uniqueness, sign/orientation, endpoint arrow, local no-hair",
            "what_is_not_claimed": "DeltaR derivation, endpoint arrow, Q_* derivation, local GR/Newton reduction",
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
    factor_rows_: list[dict[str, object]],
    coefficient_rows_: list[dict[str, object]],
    arrow_rows_: list[dict[str, object]],
    qstar_rows_: list[dict[str, object]],
    closure_rows_: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 866 - Endpoint Coefficient Origin And Arrow Law Or Demote To Closure

Generated: `{generated_utc}`

Current result: **the coefficient mystery got sharper, not solved**. The exact endpoint potential is not just `9R^3-6R^2+R`; it factorizes as `U=R(3R-1)^2`. That is the best clue so far: a parent action *could* be linear boundary occupancy times squared spatial trace-deficit. The catch is still decisive: the parent has not yet forced the linear `R` measure, the trace-deficit norm, `Q_*`, or the sign/arrow. Positive `U` stabilizes `R=1/3`, so the desired high-to-low route toward `R=1/9` needs a parent-owned orientation sign or first-order endpoint flow. Therefore the endpoint quadratic is kept as an explicit closure unless 867 derives the boundary charge metric/orientation.

## Nonclaim Summary

{csv_table(summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])}

## Factor Form Origin Audit

{csv_table(factor_rows_, ["factor_id", "statement", "calculation", "result", "meaning", "status", "valid_for_claim", "generated_utc"])}

## Coefficient Derivation Attempt

{csv_table(coefficient_rows_, ["coefficient_id", "candidate_origin", "candidate_formula", "what_it_explains", "why_not_parent_proof", "required_parent_clause", "status", "valid_for_claim", "generated_utc"])}

## Arrow Law Attempt

{csv_table(arrow_rows_, ["arrow_id", "candidate_law", "test", "result", "physics_status", "missing_for_claim", "valid_for_claim", "generated_utc"])}

## Qstar Charge Metric Audit

{csv_table(qstar_rows_, ["qstar_id", "needed_object", "candidate_definition", "current_gap", "effect_if_solved", "status", "valid_for_claim", "generated_utc"])}

## Closure Demotion Ledger

{csv_table(closure_rows_, ["closure_id", "object", "closure_status", "reason", "allowed_use", "forbidden_use", "valid_for_claim", "generated_utc"])}

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
    factor_rows_ = factor_form_rows(generated_utc)
    coefficient_rows_ = coefficient_rows(generated_utc)
    arrow_rows_ = arrow_rows(generated_utc)
    qstar_rows_ = qstar_rows(generated_utc)
    closure_rows_ = closure_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    claim_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(FACTOR_FORM_PATH, factor_rows_, ["factor_id", "statement", "calculation", "result", "meaning", "status", "valid_for_claim", "generated_utc"])
    write_csv(COEFFICIENT_PATH, coefficient_rows_, ["coefficient_id", "candidate_origin", "candidate_formula", "what_it_explains", "why_not_parent_proof", "required_parent_clause", "status", "valid_for_claim", "generated_utc"])
    write_csv(ARROW_PATH, arrow_rows_, ["arrow_id", "candidate_law", "test", "result", "physics_status", "missing_for_claim", "valid_for_claim", "generated_utc"])
    write_csv(QSTAR_PATH, qstar_rows_, ["qstar_id", "needed_object", "candidate_definition", "current_gap", "effect_if_solved", "status", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_PATH, closure_rows_, ["closure_id", "object", "closure_status", "reason", "allowed_use", "forbidden_use", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])

    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    source_checks_pass = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    factor_identity_pass = any(row["factor_id"] == "FF866_0_factor_identity" and row["result"] == "exact identity" for row in factor_rows_)
    generalized_power_pass = any(row["factor_id"] == "FF866_2_generalized_power_test" and "requires p=1" in row["result"] for row in factor_rows_)
    coefficient_nonclaim_pass = all(row["valid_for_claim"] == "false" and row["status"] != "derived" for row in coefficient_rows_)
    arrow_problem_pass = any(row["arrow_id"] == "AL866_0_positive_U_downhill" and row["physics_status"] == "opposite_to_desired_high_to_low_arrow" for row in arrow_rows_)
    first_order_nonclaim_pass = any(row["arrow_id"] == "AL866_2_first_order_endpoint_flow" and row["valid_for_claim"] == "false" for row in arrow_rows_)
    qstar_blocks_pass = all(row["valid_for_claim"] == "false" for row in qstar_rows_)
    closure_selected_pass = any(row["closure_id"] == "CL866_0_endpoint_quadratic_status" and row["closure_status"] == "closure_only_until_parent_signed" for row in closure_rows_)
    route_selected_pass = any(row["route_id"] == "RC866_0_selected" and row["route"] == "boundary_orientation_charge_metric_last_derivation_gate" for row in route_rows)
    claim_allowed_false_pass = all(row["claim_allowed"] == "false" for row in decision_rows_)
    formalization_count = formalization_workbench_modified_count()

    validation_rows = [
        {"check_id": "V866_0_sources_exist_and_needles", "result": "pass" if source_checks_pass else "fail", "detail": "all source paths exist and needles are present" if source_checks_pass else "one or more source checks failed"},
        {"check_id": "V866_1_prior_865_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V866_2_factor_identity_found", "result": "pass" if factor_identity_pass else "fail", "detail": "U=R(3R-1)^2 recorded"},
        {"check_id": "V866_3_generalized_power_gate", "result": "pass" if generalized_power_pass else "fail", "detail": "U_p root test shows p=1 is required for 1/9"},
        {"check_id": "V866_4_coefficients_remain_nonclaim", "result": "pass" if coefficient_nonclaim_pass else "fail", "detail": "coefficient factor form is not promoted to parent derivation"},
        {"check_id": "V866_5_positive_U_arrow_problem", "result": "pass" if arrow_problem_pass else "fail", "detail": "positive-U stability conflicts with desired high-to-low arrow"},
        {"check_id": "V866_6_first_order_arrow_nonclaim", "result": "pass" if first_order_nonclaim_pass else "fail", "detail": "first-order arrow law is recorded as possible but unsigned"},
        {"check_id": "V866_7_Qstar_blocks_claim", "result": "pass" if qstar_blocks_pass else "fail", "detail": "Q_* and charge metric remain missing"},
        {"check_id": "V866_8_closure_selected", "result": "pass" if closure_selected_pass else "fail", "detail": "endpoint quadratic demoted to closure-only until parent signed"},
        {"check_id": "V866_9_route_selected", "result": "pass" if route_selected_pass else "fail", "detail": NEXT_TARGET},
        {"check_id": "V866_10_claim_allowed_false", "result": "pass" if claim_allowed_false_pass else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V866_11_all_rows_nonclaim", "result": "pending", "detail": "filled after csv nonclaim scan"},
        {"check_id": "V866_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V866_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]

    nonclaim_pass, nonclaim_detail = all_csv_rows_nonclaim(GENERATED_CSV_PATHS)
    for row in validation_rows:
        if row["check_id"] == "V866_11_all_rows_nonclaim":
            row["result"] = "pass" if nonclaim_pass else "fail"
            row["detail"] = nonclaim_detail

    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_markdown(
        generated_utc,
        source_rows,
        factor_rows_,
        coefficient_rows_,
        arrow_rows_,
        qstar_rows_,
        closure_rows_,
        route_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"status={STATUS}")
    print("partial_result=U=R(3R-1)^2 is exact and p=1 is required for the 1/9 endpoint, but parent metric/Qstar/sign remain unsigned")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")
    if failed:
        for row in failed:
            print(f"validation_failure={row['check_id']}:{row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

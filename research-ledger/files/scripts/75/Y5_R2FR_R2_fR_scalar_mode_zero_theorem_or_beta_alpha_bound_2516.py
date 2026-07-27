from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_R2_FR_SCALAR_MODE_ZERO_OR_BETA_ALPHA_BOUND_2516"
CHECKPOINT_ID = "2516"
DOC = ROOT / "2516-Y5-R2FR-R2-fR-scalar-mode-zero-theorem-or-beta-alpha-bound.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2516_SOURCE_REGISTER.csv",
    "zero_attempt": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2516_R2FR_ZERO_THEOREM_ATTEMPT.csv",
    "scalaron_map": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2516_R2FR_SCALARON_MAP.csv",
    "finite_inputs": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2516_R2FR_FINITE_INPUT_ROWS.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2516_BOUND_RUNNER_DRYRUN.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2516_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2516_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2516_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2516_VALIDATION.csv",
}

BRANCH_COPIES = {
    "zero_attempt": ROOT
    / "source-intake"
    / "local_bounds"
    / "R2FR_zero_theorem_attempt_2516_NONCLAIM.csv",
    "scalaron_map": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "R2FR_scalaron_map_2516_NONCLAIM.csv",
    "finite_inputs": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2516_R2FR_FINITE_INPUT_ROWS_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2516_CR2_EFFECTIVE_COEFFICIENT_OWNER_SPLIT_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2516_0_2515_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2515_NEXT_TARGET.csv",
        "needles": ["NEXT2515_0_selected", "R2/f(R) coefficient"],
        "role": "authoritative handoff to R2/f(R) zero-or-bound checkpoint",
    },
    {
        "source_id": "SRC2516_1_2515_r11_vector",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2515_R11_BETA_RESIDUAL_VECTOR.csv",
        "needles": ["R11_2515_01", "R2_fR_scalar_mode"],
        "role": "current R11 row being attacked",
    },
    {
        "source_id": "SRC2516_2_962_relative_theorem",
        "path": "962-Y5-R10-R2-fR-zero-clause-proof-or-scalar-mode-bound-source-acquisition.md",
        "needles": ["RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED", "m_s^2=1/(6a)"],
        "role": "prior relative theorem: nonlinear f(R) creates scalar/higher-derivative branch",
    },
    {
        "source_id": "SRC2516_3_964_minimality_blocker",
        "path": "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
        "needles": ["THEOREM_NOT_PROVEN_CURRENT_CORPUS", "CM964_0_EH_plus_R2"],
        "role": "parent minimality/no-higher-derivative activator remains unproven",
    },
    {
        "source_id": "SRC2516_4_1588_scalaron_map",
        "path": "1588-Y5-R2FR-scalaron-coefficient-map-or-full-curve-bound-intake.md",
        "needles": ["m_s^2=1/(6 c_R2)", "alpha_s=1/3"],
        "role": "scalaron formula and coupling convention, not yet an MTS prediction",
    },
    {
        "source_id": "SRC2516_5_1589_coefficient_law",
        "path": "1589-Y5-R2FR-parent-coefficient-source-hunt-or-curve-QA-promotion.md",
        "needles": ["c_R2_eff(k)=c_bare+1/2 B^T L^-1(k)B+c_measure+c_boundary", "NO_CLAIM_READY_PARENT_COEFFICIENT_FOUND"],
        "role": "effective coefficient law and missing owner verdict",
    },
    {
        "source_id": "SRC2516_6_1590_owner_bundle",
        "path": "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md",
        "needles": ["fixed-L0 double-zero", "CLAIM_BLOCKED"],
        "role": "best current closure branch narrows but does not zero c_R2_eff",
    },
    {
        "source_id": "SRC2516_7_ppn_beta_bound",
        "path": "source-intake/local_bounds/PPN_source_weight_bound_interface_2513_NONCLAIM.csv",
        "needles": ["PBOUND2513_1_beta", "7.8e-05"],
        "role": "beta-minus-one comparator bound for future finite row",
    },
    {
        "source_id": "SRC2516_8_2515_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2515_VALIDATION.csv",
        "needles": ["VAL2515_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found),
                role=spec["role"],
                source_pass=path.exists() and len(found) == len(spec["needles"]),
            )
        )
    return rows


def zero_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "R2Z2516_0_target",
            "claim_attempted": "derive c_R2=c_fR=0 for the retained R11 scalar-mode row",
            "result": "TARGET_DEFINED_FROM_2515",
            "mathematical_step": "attack the operator sqrt(-g)(c_R2 R^2 + c_fR f_extra(R)) before local-GR or beta promotion",
            "blocking_input": "parent has not yet signed the exact no-higher-derivative/no-extra-scalar activator",
        },
        {
            "step_id": "R2Z2516_1_variation_filter",
            "claim_attempted": "show nonlinear f(R) violates the EH second-order metric operator class",
            "result": "RELATIVE_THEOREM_STEP_PASS",
            "mathematical_step": "delta_g int sqrt(-g)f(R) gives f_R R_mn - 1/2 f g_mn + (g_mn Box - nabla_m nabla_n)f_R = kappa T_mn",
            "blocking_input": "to make this an MTS zero theorem, parent must prove f_RR=0 or no retained scalar branch",
        },
        {
            "step_id": "R2Z2516_2_trace_scalar_pole",
            "claim_attempted": "show R+aR^2 carries a scalaron unless a=0 or decoupled",
            "result": "RELATIVE_THEOREM_STEP_PASS",
            "mathematical_step": "trace equation 3 Box f_R + f_R R - 2f = kappa T; around flat R+aR^2 gives (Box - 1/(6a)) delta R = -kappa T/(6a)",
            "blocking_input": "no parent-owned a/c_R2/fRR value or theorem-zero source is present",
        },
        {
            "step_id": "R2Z2516_3_topological_redundant_escape",
            "claim_attempted": "classify R2/f(R) as harmless topological/redefinition term",
            "result": "ESCAPE_NOT_CERTIFIED",
            "mathematical_step": "4D Gauss-Bonnet can be topological as a special combination, but isolated R^2/generic f(R) is not that certificate",
            "blocking_input": "no invariant field-redefinition/readout certificate proves observables are unchanged",
        },
        {
            "step_id": "R2Z2516_4_effective_coefficient_guard",
            "claim_attempted": "zero the full effective scalaron coefficient",
            "result": "ZERO_SIGNATURE_REFINED_NOT_SIGNED",
            "mathematical_step": "c_R2_eff(k)=c_bare + 1/2 B^T L^-1(k)B + c_measure + c_boundary + c_frame",
            "blocking_input": "all terms must be individually zero-owned or related by a parent identity; no cancellation by hand",
        },
        {
            "step_id": "R2Z2516_5_relative_zero_theorem",
            "claim_attempted": "state the exact conditional zero law",
            "result": "RELATIVE_THEOREM_PROVEN_PARENT_ACTIVATOR_UNSIGNED",
            "mathematical_step": "if the parent local exterior is exactly 4D, local, diffeo-invariant, metric-only, Levi-Civita, second-order, no-extra-scalar, no hidden integrated-out R coupling, and no measure/boundary/frame leakage, then c_R2_eff=0",
            "blocking_input": "2515 EH premise audit and 964/1589/1590 owner audits show the activator is still unsigned",
        },
        {
            "step_id": "R2Z2516_6_countermodels",
            "claim_attempted": "exclude legal countermodels",
            "result": "COUNTERMODELS_REMAIN_LIVE",
            "mathematical_step": "EH+epsilon R^2, auxiliary phi R integrated out, marker F(sigma)R, and nonlocal R Box^-1 R all remain legal unless minimality/no-marker/source-owner clauses are strengthened",
            "blocking_input": "primitive quotient/no-natural-marker and response-bundle owner theorems remain incomplete",
        },
        {
            "step_id": "R2Z2516_7_verdict",
            "claim_attempted": "promote R2/f(R) absence as MTS-owned",
            "result": "ABSOLUTE_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "mathematical_step": "R2/f(R) is boxed as either theorem-zero-if-activator-signed or finite scalaron residual",
            "blocking_input": "must proceed to effective coefficient owner split or finite nonclaim rows",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, claim_pass=False, **row) for row in rows]


def scalaron_map_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map_id": "SC2516_0_effective_coefficient",
            "map_piece": "effective R2/f(R) coefficient",
            "formula_or_rule": "c_R2_eff(k)=c_bare + 1/2 B^T L^-1(k)B + c_measure + c_boundary + c_frame",
            "required_inputs": "c_bare, B_X, L_X or Z_X/M_X^2, measure Jacobian, boundary term, frame/readout transfer",
            "status": "SYMBOLIC_LAW_AVAILABLE_VALUES_MISSING",
        },
        {
            "map_id": "SC2516_1_mass",
            "map_piece": "simple scalaron mass",
            "formula_or_rule": "for f(R)=R+c_R2 R^2 around flat space, m_s^2=1/(6 c_R2) after EH normalization",
            "required_inputs": "c_R2 value, sign, units and normalization; c_R2>0 for non-tachyonic simple branch",
            "status": "FORMULA_READY_PARENT_COEFFICIENT_MISSING",
        },
        {
            "map_id": "SC2516_2_range",
            "map_piece": "scalaron range",
            "formula_or_rule": "lambda_s=sqrt(6 c_R2) in c=hbar=1 convention, or lambda_s=hbar c/m_s after unit conversion",
            "required_inputs": "same coefficient plus explicit unit convention",
            "status": "FORMULA_READY_PARENT_COEFFICIENT_MISSING",
        },
        {
            "map_id": "SC2516_3_yukawa_alpha",
            "map_piece": "simple unscreened metric-f(R) Yukawa amplitude",
            "formula_or_rule": "alpha_s=1/3 only for the simple unscreened metric-f(R) scalar with universal matter coupling",
            "required_inputs": "screening regime, source/test coupling, matter frame and branch context",
            "status": "CONDITIONAL_COUPLING_NOT_MTS_PREDICTION",
        },
        {
            "map_id": "SC2516_4_gamma_slip",
            "map_piece": "linear weak-field gamma slip",
            "formula_or_rule": "with potentials Phi=-GM/r(1+alpha e^-r/lambda), Psi=-GM/r(1-alpha e^-r/lambda), gamma(r)=(1-alpha e^-r/lambda)/(1+alpha e^-r/lambda)",
            "required_inputs": "alpha, lambda, regime and observed-frame convention",
            "status": "MAP_SHAPE_READY_INPUTS_MISSING",
        },
        {
            "map_id": "SC2516_5_beta_second_order",
            "map_piece": "PPN beta residual",
            "formula_or_rule": "beta requires second-order scalar self-interaction/source/readout map; it is not supplied by the linear Yukawa alpha row alone",
            "required_inputs": "second-order scalar potential, source normalization and observed-GM convention",
            "status": "MISSING_BETA_SECOND_ORDER_MAP",
        },
        {
            "map_id": "SC2516_6_verdict",
            "map_piece": "MTS R2/f(R) prediction",
            "formula_or_rule": "claim row requires theorem-zero or complete c_R2_eff, m_s/lambda_s, alpha_s, beta/gamma maps and source paths",
            "required_inputs": "all prior inputs plus claim-grade R10/PPN comparator data",
            "status": "NO_SCALARON_PREDICTION_CURRENT_CORPUS",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, claim_pass=False, **row) for row in rows]


def finite_input_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "input_id": "R2IN2516_0_zero_switch",
            "row_type": "zero_theorem",
            "quantity": "c_R2_eff",
            "required_value_or_formula": "0 if and only if the parent activator in R2Z2516_5 is signed",
            "current_status": "ZERO_THEOREM_UNSIGNED",
            "observable_links": "R11;local_GR;beta;gamma;R10",
        },
        {
            "input_id": "R2IN2516_1_cR2_eff",
            "row_type": "finite_coefficient",
            "quantity": "c_R2_eff",
            "required_value_or_formula": "numeric length^2 or inverse-mass-squared value with sign and normalization",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "observable_links": "R10;PPN_gamma;PPN_beta",
        },
        {
            "input_id": "R2IN2516_2_component_split",
            "row_type": "coefficient_components",
            "quantity": "c_bare;B_X;L_X;c_measure;c_boundary;c_frame",
            "required_value_or_formula": "componentwise values or theorem-zero identities with no cancellation",
            "current_status": "MISSING_COMPONENT_VALUES_AND_ZERO_OWNERS",
            "observable_links": "R11;Qnorm;R10;PPN",
        },
        {
            "input_id": "R2IN2516_3_scalar_mass_range",
            "row_type": "derived_range",
            "quantity": "m_s;lambda_s",
            "required_value_or_formula": "m_s^2=1/(6c_R2_eff), lambda_s=sqrt(6c_R2_eff) in declared units",
            "current_status": "FORMULA_READY_INPUT_MISSING",
            "observable_links": "R10_alpha_lambda;solar_system_range_split",
        },
        {
            "input_id": "R2IN2516_4_alpha_lambda",
            "row_type": "yukawa_prediction",
            "quantity": "alpha_s(lambda_s)",
            "required_value_or_formula": "alpha_s=1/3 only if simple unscreened metric-f(R) regime is parent-signed",
            "current_status": "CONDITIONAL_COUPLING_NOT_SIGNED",
            "observable_links": "R10",
        },
        {
            "input_id": "R2IN2516_5_gamma_map",
            "row_type": "PPN_gamma_map",
            "quantity": "gamma_minus_1(r)",
            "required_value_or_formula": "gamma(r) map plus observed-GM convention and source/readout frame",
            "current_status": "MAP_SHAPE_READY_INPUTS_MISSING",
            "observable_links": "Cassini;PPN",
        },
        {
            "input_id": "R2IN2516_6_beta_map",
            "row_type": "PPN_beta_map",
            "quantity": "beta_minus_1",
            "required_value_or_formula": "second-order scalar/source/readout map in fixed observed-GM convention",
            "current_status": "MISSING_SECOND_ORDER_BETA_MAP",
            "observable_links": "PPN_beta_bound_7.8e-05",
        },
        {
            "input_id": "R2IN2516_7_bound_curve",
            "row_type": "R10_bound_source",
            "quantity": "alpha_bound(lambda)",
            "required_value_or_formula": "claim-grade full curve or explicitly nonclaim review/smoke curve",
            "current_status": "CLAIM_GRADE_CURVE_NOT_USED_WITHOUT_PREDICTION",
            "observable_links": "R10",
        },
        {
            "input_id": "R2IN2516_8_source_paths",
            "row_type": "provenance",
            "quantity": "source_file;normalization;units;assumptions",
            "required_value_or_formula": "every numeric/theorem row cites source path and convention",
            "current_status": "REQUIRED_FOR_ANY_FUTURE_SCORING",
            "observable_links": "all_local_arenas",
        },
    ]
    return [
        base_row(
            score_ready=False,
            valid_prediction_row=False,
            accepted_for_scoring=False,
            claim_pass=False,
            **row,
        )
        for row in rows
    ]


def dryrun_result_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2516_0_formula_only",
            "case_description": "use m_s^2=1/(6c_R2) and alpha_s=1/3 without parent c_R2",
            "result_status": "REJECTED_MISSING_PARENT_COEFFICIENT",
            "blocking_markers": "MISSING_C_R2_EFF;MISSING_UNITS;MISSING_SIGN",
        },
        {
            "case_id": "DRY2516_1_parent_zero",
            "case_description": "set c_R2_eff=0 from relative theorem alone",
            "result_status": "REJECTED_ZERO_THEOREM_ACTIVATOR_UNSIGNED",
            "blocking_markers": "MISSING_PARENT_SECOND_ORDER_NO_EXTRA_SCALAR_SIGNATURE",
        },
        {
            "case_id": "DRY2516_2_EH_import",
            "case_description": "use EH/Lovelock as imported proof that R2/f(R) is absent",
            "result_status": "REJECTED_GR_IMPORT_AS_MTS_ZERO_THEOREM",
            "blocking_markers": "EH_PREMISES_NOT_PARENT_SIGNED",
        },
        {
            "case_id": "DRY2516_3_anchor_backsolve",
            "case_description": "backsolve lambda or c_R2 from an R10 alpha=1 threshold",
            "result_status": "FORBIDDEN_BOUND_TO_PREDICTION_INVERSION",
            "blocking_markers": "BOUND_IS_NOT_PARENT_COEFFICIENT",
        },
        {
            "case_id": "DRY2516_4_beta_score",
            "case_description": "score beta with only linear Yukawa alpha/gamma map",
            "result_status": "REJECTED_MISSING_SECOND_ORDER_BETA_MAP",
            "blocking_markers": "MISSING_SCALAR_SELF_INTERACTION;MISSING_SOURCE_READOUT_TRANSFER",
        },
        {
            "case_id": "DRY2516_5_future_complete_template",
            "case_description": "future theorem-zero or finite scalaron row with real coefficient and maps",
            "result_status": "WOULD_ACCEPT_SCHEMA_IF_REAL_VALUES_AND_FILES_EXIST",
            "blocking_markers": "CURRENT_ROW_STILL_MISSING_REAL_INPUTS",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
            comparator_bound="R10 alpha(lambda) full curve plus beta_bound=7.8e-05",
            pass_fail="BLOCKED_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
            claim_pass=False,
            **case,
        )
        for case in cases
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        {
            "decision_id": "DEC2516_0_progress",
            "decision": "R2FR_RELATIVE_ZERO_THEOREM_RECONFIRMED_IN_CURRENT_BRANCH",
            "rationale": "Nonlinear f(R) generically gives higher derivatives/scalar trace pole, so exact second-order/no-extra-scalar parent dynamics would kill it.",
            "status": "retained_derivation",
        },
        {
            "decision_id": "DEC2516_1_limit",
            "decision": "ABSOLUTE_MTS_ZERO_NOT_PROVEN",
            "rationale": "The parent activator still lacks no-bare-R2, no hidden curvature vertex, no measure/boundary/frame leakage, and response-bundle ownership.",
            "status": "claim_blocked",
        },
        {
            "decision_id": "DEC2516_2_formula",
            "decision": "SCALARON_FORMULA_AVAILABLE_NOT_A_PREDICTION",
            "rationale": "m_s, lambda_s and alpha_s maps are useful plumbing, but without c_R2_eff and regime they cannot be scored.",
            "status": "nonclaim_tooling",
        },
        {
            "decision_id": "DEC2516_3_bottleneck",
            "decision": "EFFECTIVE_COEFFICIENT_OWNER_SPLIT_IS_NOW_THE_BOTTLENECK",
            "rationale": "The next move is not more R10 data; it is splitting c_R2_eff into owned terms and trying to zero or bound them componentwise.",
            "status": "selected",
        },
        {
            "decision_id": "DEC2516_4_claim",
            "decision": "NO_R2FR_R10_BETA_OR_LOCAL_GR_CLAIM",
            "rationale": "No theorem-zero, coefficient, range, beta map, or claim-grade prediction row exists in this checkpoint.",
            "status": "enforced",
        },
    ]
    return [base_row(**decision) for decision in decisions]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2516_0_selected",
            selection_status="selected",
            target_file="2517-Y5-R2FR-cR2-effective-coefficient-owner-split-and-first-term-zero-or-bound.md",
            target_script="scripts/Y5_R2FR_cR2_effective_coefficient_owner_split_and_first_term_zero_or_bound_2517.py",
            objective="split c_R2_eff into c_bare, B^T L^-1 B, measure, boundary and frame-transfer terms; try to parent-zero c_bare first, otherwise create finite component rows with units and source paths",
            success_condition="each c_R2_eff component has theorem-zero evidence or a finite nonclaim row with units, sign, normalization, source path and observable link",
            do_not_do="do not cancel components by hand, do not backsolve from R10 bounds, and do not claim local GR from the relative f(R) theorem",
        ),
        base_row(
            route_id="NEXT2516_1_parallel_hold",
            selection_status="parallel_after_coefficient_split",
            target_file="2515b-Y5-R2FR-alpha3-source-exchange-current-owner-bound.md",
            target_script="scripts/Y5_R2FR_alpha3_source_exchange_current_owner_bound_2515b.py",
            objective="derive or bound alpha3 source-exchange/current-owner residual under the 4e-20 comparator",
            success_condition="alpha3 source-exchange row has current-owner theorem or finite coefficient/kernel rows",
            do_not_do="do not let R2/f(R) work erase preferred-frame/source-current debt",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("zero_attempt", OUTPUTS["zero_attempt"], BRANCH_COPIES["zero_attempt"]),
        ("scalaron_map", OUTPUTS["scalaron_map"], BRANCH_COPIES["scalaron_map"]),
        ("finite_inputs", OUTPUTS["finite_inputs"], BRANCH_COPIES["finite_inputs"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        ok, count, message = csv_rows_parse(destination)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(source.relative_to(ROOT)),
                destination=str(destination.relative_to(ROOT)),
                copied=destination.exists(),
                parse_ok=ok,
                row_count=count,
                parse_message=message,
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "accepted_for_scoring",
                "claim_pass",
            ):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    add("VAL2516_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2516_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2516_02_relative_theorem_present",
        any(row["step_id"] == "R2Z2516_5_relative_zero_theorem" and "RELATIVE_THEOREM_PROVEN" in row["result"] for row in rows_by_name["zero_attempt"]),
        "conditional f(R) zero theorem is retained",
    )
    add(
        "VAL2516_03_absolute_zero_blocked",
        any(row["step_id"] == "R2Z2516_7_verdict" and row["result"] == "ABSOLUTE_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in rows_by_name["zero_attempt"]),
        "absolute MTS R2/f(R) zero is not promoted",
    )
    add(
        "VAL2516_04_scalaron_formula_nonclaim",
        any(row["map_id"] == "SC2516_1_mass" and "1/(6 c_R2)" in row["formula_or_rule"] for row in rows_by_name["scalaron_map"])
        and any(row["map_id"] == "SC2516_6_verdict" and row["status"] == "NO_SCALARON_PREDICTION_CURRENT_CORPUS" for row in rows_by_name["scalaron_map"]),
        "scalaron formula is wired but not an MTS prediction",
    )
    add(
        "VAL2516_05_finite_inputs_rejected",
        len(rows_by_name["finite_inputs"]) >= 8
        and all(str(row["score_ready"]) == "False" and str(row["accepted_for_scoring"]) == "False" for row in rows_by_name["finite_inputs"]),
        "finite rows are schema only",
    )
    add(
        "VAL2516_06_dryruns_block_claims",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "dry run rejects formula-only, unsigned zero and backsolve paths",
    )
    add(
        "VAL2516_07_next_target",
        any(row["route_id"] == "NEXT2516_0_selected" and "cR2-effective-coefficient" in row["target_file"] for row in rows_by_name["next_target"]),
        "c_R2_eff owner split selected",
    )
    add("VAL2516_08_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2516_09_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2516*")) if formalization.exists() else []
    add(
        "VAL2516_10_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2516_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2516_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2516_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2516_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2516 proves the R2/f(R) zero theorem only conditionally, refuses absolute MTS promotion, stages scalaron beta/gamma/R10 inputs, and selects c_R2_eff owner split next",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2516 - R2/f(R) Scalar Mode Zero Theorem or Beta/Alpha Bound",
                "",
                "**Current verdict:** the R2/f(R) scalar mode is mathematically boxed, not killed. Nonlinear `f(R)` generically creates higher metric derivatives or a scalar trace pole, so an exact parent second-order/no-extra-scalar branch would zero it. The parent activator is still unsigned.",
                "",
                "**Main gain:** the scalaron route is now explicit in the current 2515 branch: `c_R2_eff`, `m_s`, `lambda_s`, `alpha_s`, gamma slip, beta second-order map, and R10 curve requirements are separated instead of blurred.",
                "",
                "**Claim discipline:** no R2/f(R), R10, beta, gamma, EH, Newton, PPN, local-GR, WEP, clock, orbit, or conservation claim is made here.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## R2/f(R) Zero Theorem Attempt",
                md_table(rows_by_name["zero_attempt"], ["step_id", "claim_attempted", "result", "mathematical_step", "blocking_input"]),
                "",
                "## Scalaron Map",
                md_table(rows_by_name["scalaron_map"], ["map_id", "map_piece", "formula_or_rule", "required_inputs", "status"]),
                "",
                "## Finite Input Rows",
                md_table(rows_by_name["finite_inputs"], ["input_id", "row_type", "quantity", "required_value_or_formula", "current_status", "observable_links"]),
                "",
                "## Bound Runner Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "result_status", "blocking_markers", "pass_fail", "claim_pass"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "zero_attempt": zero_attempt_rows(),
        "scalaron_map": scalaron_map_rows(),
        "finite_inputs": finite_input_rows(),
        "dryrun_results": dryrun_result_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()

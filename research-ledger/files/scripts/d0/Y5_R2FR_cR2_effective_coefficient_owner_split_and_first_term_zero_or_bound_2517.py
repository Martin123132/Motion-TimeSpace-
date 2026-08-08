from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_CR2_EFFECTIVE_COEFFICIENT_OWNER_SPLIT_2517"
CHECKPOINT_ID = "2517"
DOC = ROOT / "2517-Y5-R2FR-cR2-effective-coefficient-owner-split-and-first-term-zero-or-bound.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_SOURCE_REGISTER.csv",
    "component_split": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_CR2_COMPONENT_SPLIT.csv",
    "cbare_zero_attempt": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_CBARE_ZERO_ATTEMPT.csv",
    "cbare_finite_row": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_CBARE_FINITE_ROW.csv",
    "no_cancellation_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_NO_CANCELLATION_GATE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2517_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2517_VALIDATION.csv",
}

BRANCH_COPIES = {
    "component_split": ROOT
    / "source-intake"
    / "local_bounds"
    / "CR2_effective_component_split_2517_NONCLAIM.csv",
    "cbare_zero_attempt": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Cbare_zero_attempt_2517_NONCLAIM.csv",
    "cbare_finite_row": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2517_CBARE_FINITE_ROW_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2517_HIDDEN_CURVATURE_VERTEX_NEXT_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2517_0_2516_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2516_NEXT_TARGET.csv",
        "needles": ["NEXT2516_0_selected", "c_R2_eff"],
        "role": "authoritative handoff to c_R2_eff component split",
    },
    {
        "source_id": "SRC2517_1_2516_scalaron",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2516_R2FR_SCALARON_MAP.csv",
        "needles": ["SC2516_0_effective_coefficient", "c_bare"],
        "role": "effective coefficient law from the current branch",
    },
    {
        "source_id": "SRC2517_2_2516_zero_attempt",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2516_R2FR_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["R2Z2516_4_effective_coefficient_guard", "ZERO_SIGNATURE_REFINED_NOT_SIGNED"],
        "role": "no-cancellation guard for the full coefficient",
    },
    {
        "source_id": "SRC2517_3_2485_normal_form",
        "path": "source-intake/local_bounds/Parent_normal_form_contract_2485_NONCLAIM.csv",
        "needles": ["NF2485_0_parent_action_skeleton", "sum_i c_i O_i"],
        "role": "parent action skeleton retains residual operator slots",
    },
    {
        "source_id": "SRC2517_4_2485_coeff_slots",
        "path": "source-intake/local_bounds/Parent_coefficient_slot_ledger_2485_NONCLAIM.csv",
        "needles": ["CS2485_2_c_HD", "RETAIN_NONCLAIM"],
        "role": "higher-curvature coefficient slot remains retained",
    },
    {
        "source_id": "SRC2517_5_2485_derivative_grammar",
        "path": "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md",
        "needles": ["DG2485_3_higher_curvature", "RETAIN_AS_c_HD"],
        "role": "derivative grammar says higher-curvature terms need forbid-or-bound owner",
    },
    {
        "source_id": "SRC2517_6_964_countermodel",
        "path": "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
        "needles": ["CM964_0_EH_plus_R2", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
        "role": "EH plus epsilon R^2 remains legal without a parent no-extension theorem",
    },
    {
        "source_id": "SRC2517_7_2509_loop_guard",
        "path": "2509-Y5-R2FR-parent-constructor-exhaustion-from-MTS-primitives-or-source-weight-residual-pivot.md",
        "needles": ["PARENT_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED_PIVOT_REQUIRED", "LOOP_GUARD_ENFORCED"],
        "role": "do not restate constructor exhaustion as if it zeroed coefficients",
    },
    {
        "source_id": "SRC2517_8_2516_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2516_VALIDATION.csv",
        "needles": ["VAL2516_OVERALL", "PASS"],
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


def component_split_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "CR2C2517_0_cbare",
            "symbol": "c_bare",
            "definition": "bare local higher-curvature coefficient written directly in the parent public-geometry action",
            "required_zero_owner": "parent derivative grammar excludes R^2, f_extra(R), R Box R, and higher-curvature public operators except topological/boundary combinations",
            "current_status": "NOT_ZEROED_RETAIN_FINITE_ROW",
            "observable_links": "R10;PPN_gamma;PPN_beta;local_GR_operator",
            "next_action": "attempt c_bare zero theorem first; otherwise keep finite row",
        },
        {
            "component_id": "CR2C2517_1_hidden_vertex",
            "symbol": "1/2 B^T L^-1 B",
            "definition": "integrated-out hidden, memory, fibre, or auxiliary curvature-linear vertex contribution",
            "required_zero_owner": "B_X=0 or L^-1 decoupling/theorem-zero for every hidden curvature-linear vertex",
            "current_status": "OPEN_NEXT_AFTER_CBARE",
            "observable_links": "R10;PPN;Qnorm;clock_orbit",
            "next_action": "attack hidden curvature vertex after c_bare row",
        },
        {
            "component_id": "CR2C2517_2_measure",
            "symbol": "c_measure",
            "definition": "Jacobian, measure, local subtraction, or field-redefinition curvature-square residue",
            "required_zero_owner": "measure/readout/redefinition identity proving no observable residual",
            "current_status": "OPEN_RETAINED",
            "observable_links": "PPN;source_normalization;clock",
            "next_action": "defer until c_bare and hidden vertex are classified",
        },
        {
            "component_id": "CR2C2517_3_boundary",
            "symbol": "c_boundary",
            "definition": "boundary, corner, topological, reference, or no-flux leakage into the local operator",
            "required_zero_owner": "boundary class/topological/no-flux theorem including metric variation and source readout",
            "current_status": "OPEN_RETAINED",
            "observable_links": "beta;alpha3;xi;source_normalization",
            "next_action": "defer to boundary/projector branch if not zeroed earlier",
        },
        {
            "component_id": "CR2C2517_4_frame",
            "symbol": "c_frame",
            "definition": "observed-frame, coframe, conformal/disformal or readout transfer residue that mimics an f(R) coefficient",
            "required_zero_owner": "single observed coframe/frame-transfer theorem with variation-before-readout order",
            "current_status": "OPEN_RETAINED",
            "observable_links": "gamma;beta;clocks;preferred_frame",
            "next_action": "defer to observed-frame/readout branch after coefficient rows are split",
        },
        {
            "component_id": "CR2C2517_5_total",
            "symbol": "c_R2_eff",
            "definition": "componentwise effective coefficient entering scalaron range and Yukawa/PPN maps",
            "required_zero_owner": "all components zeroed individually or by a sourced Ward/topological identity; no cancellation by preference",
            "current_status": "MISSING_COMPONENT_VALUES_OR_ZERO_THEOREMS",
            "observable_links": "R2FR_scalaron;R10;PPN;local_GR",
            "next_action": "fill each limb in order",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, accepted_for_scoring=False, claim_pass=False, **row) for row in rows]


def cbare_zero_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "CBZ2517_0_target",
            "claim_attempted": "prove c_bare=0 from parent derivative grammar",
            "result": "TARGET_DEFINED",
            "logic": "c_bare is zero if the parent object language has no public higher-curvature operator slot beyond EH, Lambda and harmless topological/boundary terms",
            "blocking_gap": "2485 still writes sum_i c_i O_i and keeps c_HD retained",
        },
        {
            "attempt_id": "CBZ2517_1_allowed_operator_inventory",
            "claim_attempted": "restrict public local geometry to a0+a1 R only",
            "result": "CONDITIONAL_ROUTE_IDENTIFIED_NOT_SIGNED",
            "logic": "a strict derivative grammar plus local metric-only second-order premise would exclude R^2 and generic f(R)",
            "blocking_gap": "derivative grammar is a contract, not a derived parent action inventory",
        },
        {
            "attempt_id": "CBZ2517_2_constructor_exhaustion",
            "claim_attempted": "use ParentGenerate exhaustion to make c_bare unformable",
            "result": "REJECTED_LOOP_GUARD",
            "logic": "if c_bare is not in Image(ParentGenerate[q(Phi),theta,topological/universal data]), then it cannot appear",
            "blocking_gap": "2509 says ParentGenerate membership/no-extension is not derived and should not be repeated without new source",
        },
        {
            "attempt_id": "CBZ2517_3_topological_exception",
            "claim_attempted": "allow only topological/boundary higher-curvature combinations",
            "result": "SAFE_EXCEPTION_NOT_CURRENT_ROW",
            "logic": "a precise 4D Gauss-Bonnet/boundary class could be harmless if variation/readout silence is proved",
            "blocking_gap": "current R2/f(R) row is generic scalar curvature-square/f_extra(R), not a sourced topological combination",
        },
        {
            "attempt_id": "CBZ2517_4_countermodel",
            "claim_attempted": "exclude EH + epsilon R^2",
            "result": "COUNTERMODEL_REMAINS_LEGAL",
            "logic": "S = S_EH + epsilon int sqrt(-g) R^2 respects locality, 4D covariance and metric-only structure while violating second-order EH unless epsilon=0",
            "blocking_gap": "no parent no-extension/minimality theorem forbids epsilon",
        },
        {
            "attempt_id": "CBZ2517_5_verdict",
            "claim_attempted": "set c_bare=0 as MTS-owned",
            "result": "CBARE_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "logic": "conditional theorem is exact, but current evidence retains the c_HD/c_bare slot",
            "blocking_gap": "create finite c_bare row and move to hidden curvature vertex limb",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, claim_pass=False, **row) for row in rows]


def cbare_finite_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CBFIN2517_0_cbare_value",
            "quantity": "c_bare",
            "required_units": "length^2 or inverse_mass_squared after EH normalization",
            "required_value_or_formula": "numeric value or exact zero theorem with source path",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "observable_links": "R10;PPN_gamma;PPN_beta",
        },
        {
            "row_id": "CBFIN2517_1_normalization",
            "quantity": "EH normalization",
            "required_units": "declared a1/kappa convention",
            "required_value_or_formula": "coefficient must be normalized relative to the parent EH term a1 R",
            "current_status": "MISSING_A1_KAPPA_OWNER",
            "observable_links": "Newton;PPN;scalaron_mass",
        },
        {
            "row_id": "CBFIN2517_2_sign",
            "quantity": "sign(c_bare)",
            "required_units": "dimensionless sign with stability convention",
            "required_value_or_formula": "positive simple R+cR2 branch gives non-tachyonic scalaron; negative requires explicit stability treatment",
            "current_status": "MISSING_SIGN_AND_STABILITY_BRANCH",
            "observable_links": "R10;stability;local_branch",
        },
        {
            "row_id": "CBFIN2517_3_scalar_map",
            "quantity": "m_s;lambda_s;alpha_s",
            "required_units": "eV/meters/dimensionless",
            "required_value_or_formula": "m_s^2=1/(6c_bare) only if c_bare dominates c_R2_eff and simple unscreened metric-f(R) branch applies",
            "current_status": "MISSING_COMPONENT_DOMINANCE_AND_REGIME",
            "observable_links": "R10_alpha_lambda;gamma",
        },
        {
            "row_id": "CBFIN2517_4_beta_map",
            "quantity": "delta_beta_cbare",
            "required_units": "dimensionless",
            "required_value_or_formula": "second-order scalar/source/readout map in fixed observed-GM convention",
            "current_status": "MISSING_SECOND_ORDER_BETA_MAP",
            "observable_links": "PPN_beta_bound_7.8e-05",
        },
        {
            "row_id": "CBFIN2517_5_source_path",
            "quantity": "provenance",
            "required_units": "path/URL plus assumptions",
            "required_value_or_formula": "source path for coefficient, normalization, units and branch regime",
            "current_status": "MISSING_SOURCE_PATH",
            "observable_links": "all_future_scoring",
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


def no_cancellation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "NC2517_0_componentwise",
            "policy": "evaluate c_R2_eff by componentwise zero or bound rows",
            "forbidden_move": "set c_bare + hidden + measure + boundary + frame = 0 by tuning",
            "allowed_exception": "sourced Ward/topological/redefinition identity with source path and readout proof",
            "status": "ACTIVE",
        },
        {
            "gate_id": "NC2517_1_hidden_vertex",
            "policy": "do not cancel c_bare against B^T L^-1 B",
            "forbidden_move": "use opposite signs without parent identity",
            "allowed_exception": "derived Schur-complement identity or positive/zero theorem for each piece",
            "status": "ACTIVE",
        },
        {
            "gate_id": "NC2517_2_boundary_measure",
            "policy": "measure and boundary terms cannot silently remove public curvature residues",
            "forbidden_move": "call them gauge/topological without variation/readout silence",
            "allowed_exception": "boundary class plus no-flux plus variation-before-readout theorem",
            "status": "ACTIVE",
        },
        {
            "gate_id": "NC2517_3_claim",
            "policy": "no local-GR or scalaron score from an unsigned component split",
            "forbidden_move": "treat bookkeeping as evidence of a pass",
            "allowed_exception": "all components have real zero/bound rows and comparator maps",
            "status": "ACTIVE",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, claim_pass=False, **row) for row in rows]


def dryrun_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2517_0_derivative_taste",
            "case_description": "set c_bare=0 because higher derivatives are ugly",
            "result_status": "REFUSED_NO_DERIVATIVE_BY_TASTE",
            "blocking_markers": "MISSING_PARENT_DERIVATIVE_GRAMMAR_SIGNATURE",
        },
        {
            "case_id": "DRY2517_1_EH_import",
            "case_description": "use EH target branch to delete c_bare",
            "result_status": "REFUSED_EH_IMPORT_AS_COEFFICIENT_OWNER",
            "blocking_markers": "EH_PREMISES_UNSIGNED;C_HD_RETAINED",
        },
        {
            "case_id": "DRY2517_2_constructor_loop",
            "case_description": "repeat ParentGenerate exhaustion without new source",
            "result_status": "REFUSED_LOOP_GUARD",
            "blocking_markers": "PARENT_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED",
        },
        {
            "case_id": "DRY2517_3_finite_score",
            "case_description": "score finite c_bare row without value, units or beta/gamma/R10 map",
            "result_status": "REJECTED_MISSING_FINITE_INPUTS",
            "blocking_markers": "MISSING_VALUE;MISSING_UNITS;MISSING_MAPS;MISSING_SOURCE_PATH",
        },
        {
            "case_id": "DRY2517_4_component_cancellation",
            "case_description": "cancel c_bare against hidden/measure/boundary/frame terms",
            "result_status": "REFUSED_UNSOURCED_CANCELLATION",
            "blocking_markers": "NO_CANCELLATION_GATE_ACTIVE",
        },
        {
            "case_id": "DRY2517_5_future_complete_template",
            "case_description": "future c_bare row has theorem-zero or sourced numeric coefficient and maps",
            "result_status": "WOULD_ACCEPT_SCHEMA_IF_REAL_VALUES_AND_FILES_EXIST",
            "blocking_markers": "CURRENT_ROW_STILL_MISSING_REAL_INPUTS",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
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
            "decision_id": "DEC2517_0_split",
            "decision": "CR2_EFFECTIVE_COMPONENT_SPLIT_LOCKED",
            "rationale": "c_R2_eff is now split into c_bare, hidden Schur term, measure, boundary and frame limbs with separate owners.",
            "status": "retained_tooling",
        },
        {
            "decision_id": "DEC2517_1_cbare",
            "decision": "CBARE_ZERO_NOT_DERIVED",
            "rationale": "2485 still retains c_HD and 964's EH+R2 countermodel remains legal without a stronger parent derivative grammar.",
            "status": "claim_blocked",
        },
        {
            "decision_id": "DEC2517_2_finite",
            "decision": "CBARE_FINITE_ROW_STAGED_NONCLAIM",
            "rationale": "If c_bare survives, it needs value, units, sign, normalization, scalaron maps, beta map and source path before any scoring.",
            "status": "selected_nonclaim",
        },
        {
            "decision_id": "DEC2517_3_next",
            "decision": "ATTACK_HIDDEN_CURVATURE_VERTEX_NEXT",
            "rationale": "The next largest limb is the integrated-out hidden/memory/fibre term B^T L^-1 B, which can regenerate R2 even if c_bare is absent.",
            "status": "selected",
        },
        {
            "decision_id": "DEC2517_4_claim",
            "decision": "NO_CBARE_R2FR_OR_LOCAL_GR_CLAIM",
            "rationale": "No component has a claim-ready zero theorem or finite value; this checkpoint is coefficient discipline only.",
            "status": "enforced",
        },
    ]
    return [base_row(**decision) for decision in decisions]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2517_0_selected",
            selection_status="selected",
            target_file="2518-Y5-R2FR-hidden-curvature-vertex-BTLinvB-zero-or-finite-row.md",
            target_script="scripts/Y5_R2FR_hidden_curvature_vertex_BTLinvB_zero_or_finite_row_2518.py",
            objective="try to prove every hidden/memory/fibre curvature-linear vertex B_X vanishes or decouples; if not, create finite B_X, L_X, Z_X, M_X rows with units and observable maps",
            success_condition="B^T L^-1 B term is theorem-zero or each retained vertex has finite nonclaim coefficient, operator inverse/range, units, source path and R10/PPN/Qnorm link",
            do_not_do="do not assume c_bare=0 closes R2/f(R), do not cancel Schur terms by hand, and do not score symbolic B_X rows",
        ),
        base_row(
            route_id="NEXT2517_1_reentry",
            selection_status="reentry_only_if_new_source",
            target_file="2517b-Y5-R2FR-parent-derivative-grammar-new-source-reentry.md",
            target_script="scripts/Y5_R2FR_parent_derivative_grammar_new_source_reentry_2517b.py",
            objective="reopen c_bare zero only if a new source proves the parent derivative grammar excludes higher curvature from the constructor image",
            success_condition="new source path proves c_HD is unformable rather than retained",
            do_not_do="do not repeat 2485/2509/964 conditionals as fresh evidence",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("component_split", OUTPUTS["component_split"], BRANCH_COPIES["component_split"]),
        ("cbare_zero_attempt", OUTPUTS["cbare_zero_attempt"], BRANCH_COPIES["cbare_zero_attempt"]),
        ("cbare_finite_row", OUTPUTS["cbare_finite_row"], BRANCH_COPIES["cbare_finite_row"]),
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
    add("VAL2517_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2517_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2517_02_component_split",
        len(rows_by_name["component_split"]) == 6
        and any(row["symbol"] == "c_bare" for row in rows_by_name["component_split"])
        and any(row["symbol"] == "c_R2_eff" for row in rows_by_name["component_split"]),
        "c_R2_eff limbs are explicit",
    )
    add(
        "VAL2517_03_cbare_not_zeroed",
        any(row["attempt_id"] == "CBZ2517_5_verdict" and row["result"] == "CBARE_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in rows_by_name["cbare_zero_attempt"]),
        "bare higher-curvature zero theorem remains unsigned",
    )
    add(
        "VAL2517_04_finite_row_rejects",
        len(rows_by_name["cbare_finite_row"]) == 6
        and all(str(row["accepted_for_scoring"]) == "False" for row in rows_by_name["cbare_finite_row"]),
        "finite c_bare rows are schema-only",
    )
    add(
        "VAL2517_05_no_cancellation_gate",
        all(row["status"] == "ACTIVE" for row in rows_by_name["no_cancellation_gate"])
        and any(row["gate_id"] == "NC2517_0_componentwise" for row in rows_by_name["no_cancellation_gate"]),
        "component cancellation is forbidden without a parent identity",
    )
    add(
        "VAL2517_06_dryruns_block_claims",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "dry run rejects derivative-taste, EH import, loop and cancellation routes",
    )
    add(
        "VAL2517_07_next_target",
        any(row["route_id"] == "NEXT2517_0_selected" and "BTLinvB" in row["target_file"] for row in rows_by_name["next_target"]),
        "hidden curvature vertex selected next",
    )
    add("VAL2517_08_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2517_09_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2517*")) if formalization.exists() else []
    add(
        "VAL2517_10_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2517_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2517_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2517_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2517_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2517 splits c_R2_eff, refuses c_bare zero promotion, stages finite c_bare rows, and selects hidden curvature vertex B^T L^-1 B next",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2517 - c_R2 Effective Coefficient Owner Split and First-Term Zero/Bound",
                "",
                "**Current verdict:** `c_R2_eff` is now split into named limbs. The bare higher-curvature limb `c_bare` is not parent-zeroed because the current parent normal-form grammar still retains `c_HD` unless a stronger derivative-grammar/no-extension theorem is supplied.",
                "",
                "**Main gain:** this avoids circling the same R2/f(R) theorem. The next work can attack one coefficient limb at a time: bare slot, hidden Schur term, measure, boundary, and frame/readout transfer.",
                "",
                "**Claim discipline:** no R2/f(R), scalaron, beta, gamma, R10, EH, Newton, local-GR, WEP, clock, orbit, or conservation claim is made.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## c_R2_eff Component Split",
                md_table(rows_by_name["component_split"], ["component_id", "symbol", "definition", "required_zero_owner", "current_status", "next_action"]),
                "",
                "## c_bare Zero Attempt",
                md_table(rows_by_name["cbare_zero_attempt"], ["attempt_id", "claim_attempted", "result", "logic", "blocking_gap"]),
                "",
                "## c_bare Finite Row",
                md_table(rows_by_name["cbare_finite_row"], ["row_id", "quantity", "required_units", "required_value_or_formula", "current_status", "observable_links"]),
                "",
                "## No-Cancellation Gate",
                md_table(rows_by_name["no_cancellation_gate"], ["gate_id", "policy", "forbidden_move", "allowed_exception", "status"]),
                "",
                "## Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "result_status", "blocking_markers", "pass_fail"]),
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
        "component_split": component_split_rows(),
        "cbare_zero_attempt": cbare_zero_attempt_rows(),
        "cbare_finite_row": cbare_finite_rows(),
        "no_cancellation_gate": no_cancellation_rows(),
        "dryrun_results": dryrun_rows(),
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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2194"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2194-Y5-R2FR-parent-q_loc-alpha-coefficient-profile-or-theorem-zero.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2194_SOURCE_REGISTER.csv",
    "factorization_contract": OUT / "P8_Y5_PARENT_QLOC_2194_ALPHA_FACTORIZATION_CONTRACT.csv",
    "theorem_zero_gate": OUT / "P8_Y5_PARENT_QLOC_2194_THEOREM_ZERO_OR_FINITE_EXCHANGE_GATE.csv",
    "component_status": OUT / "P8_Y5_PARENT_QLOC_2194_THEORY_COMPONENT_STATUS.csv",
    "alpha_template": OUT / "P8_Y5_PARENT_QLOC_2194_R10_ALPHA_TEMPLATE_ROW.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2194_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2194_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2194_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2194_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2194_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2194_QLOC_ALPHA_FACTORISATION_CONTRACT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2194_THEORY_COMPONENT_STATUS_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_R10_ALPHA_TEMPLATE_2194_NONCLAIM.csv",
}


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
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def formalization_has_2194_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2194-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2194*",
        "*P8_Y5_BRR545_2194*",
        "*Y5_R2FR_parent_q_loc_alpha_coefficient_profile_or_theorem_zero_2194*",
        "*JR2194*",
        "*PARENT_QLOC_R10_ALPHA_TEMPLATE_2194*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2193_next",
            OUT / "P8_Y5_PARENT_QLOC_2193_NEXT_TARGET.csv",
            ["NEXT2193_0_2194", "c_q_alpha(lambda)", "do not set c_q_alpha=1"],
            "2193 selects theory-side q_loc alpha coefficient/profile derivation next.",
        ),
        (
            "2193_join_preview",
            OUT / "P8_Y5_PARENT_QLOC_2193_R10_JOIN_PREVIEW.csv",
            ["R10JOIN2193_0_component_seed_to_review_candidate", "MISSING_ALPHA_PREDICTED_FROM_QLOC", "nearest_alpha_bound"],
            "2193 supplies the external curve join preview and the missing theory-side alpha slot.",
        ),
        (
            "1035_kernel_audit",
            OUT / "P8_Y5_R10_1035_KERNEL_DERIVATION_AUDIT.csv",
            ["KXD1035_1_static_green_function", "G_lambda(r)=exp(-r/lambda)/(4 pi r)", "K_X^R10(lambda)=K_X^pt * F_ST(lambda) * Pi_R10"],
            "1035 derives the static Green-kernel and R10 profile factorization contract.",
        ),
        (
            "1035_kx_factorization",
            OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv",
            ["KXF1035_0_KX_point", "KXF1035_3_harmonic", "KXF1035_4_total"],
            "1035 names the exact K_X factors still missing.",
        ),
        (
            "1035_charge_split",
            OUT / "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
            ["BETA1035_0_product_law", "BETA1035_1_universal_weyl", "BETA1035_2_quotient_zero"],
            "1035 establishes source/test product, c_g-squared warning and quotient-zero branch.",
        ),
        (
            "1036_parent_X_audit",
            OUT / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv",
            ["PX1036_0_branch_extremum", "PX1036_4_source_test_betas", "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED"],
            "1036 audits the missing parent finite-X action row.",
        ),
        (
            "1036_beta_derivation",
            OUT / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
            ["BETA1036_2_R10_alpha_match", "alpha_X=s_X beta_s beta_t/(4*pi G_N Z_X)", "BETA1036_4_quotient_zero"],
            "1036 derives the finite-exchange alpha law and zero branch condition.",
        ),
        (
            "1036_branch_classification",
            OUT / "P8_Y5_R10_1036_BRANCH_CLASSIFICATION.csv",
            ["BR1036_0_no_physical_X_pole", "BR1036_2_sourced_finite_exchange", "BR1036_3_shadow_frame_marker"],
            "1036 classifies no-pole, finite-exchange and retained-tail routes.",
        ),
        (
            "1037_no_pole_audit",
            OUT / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv",
            ["NP1037_0_q_kernel", "NP1037_5_matter_readout", "NP1037_6_verdict"],
            "1037 gives the exact no-physical-pole certificate objects.",
        ),
        (
            "1037_beta_template",
            OUT / "P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
            ["BB1037_0_beta_source_geom", "BB1037_6_beta_abs_totals", "BB1037_7_beta_product_guard"],
            "1037 supplies no-cancellation beta envelope rows if no-pole fails.",
        ),
        (
            "1037_tail_envelope",
            OUT / "P8_Y5_R10_1037_ABSOLUTE_TAIL_ENVELOPE.csv",
            ["TAIL1037_0_alpha_envelope", "no cancellation credit", "CLAIM_BLOCKED"],
            "1037 enforces absolute tails and no cancellation.",
        ),
        (
            "2193_validation",
            OUT / "P8_Y5_BRR545_2193_VALIDATION.csv",
            ["VAL2193_OVERALL", "PASS", "private join/pressure work"],
            "2193 external curve admission passed while staying nonclaim.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def factorization_contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FAC2194_0_exact_finite_exchange",
            "finite physical local response mode",
            "alpha_predicted(lambda)=s_X K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda)",
            "K_X^R10(lambda)=K_X^pt F_ST(lambda) Pi_R10(lambda); K_X^pt=1/(4*pi*G_N*Z_X) if beta units do not absorb Z_X,G_N",
            "1035/1036",
            "CONDITIONAL_DERIVED_CONTRACT",
            "Z_X;sign_sX;lambda_X;beta_s;beta_t;F_ST;Pi_R10;epsilon_tail;unit convention",
        ),
        (
            "FAC2194_1_2192_product_form",
            "compatibility with 2192 c_q_alpha*q_profile schema",
            "alpha_R10_q(lambda)=c_q_alpha(lambda)*q_profile(lambda)+epsilon_tail(lambda)",
            "choose c_q_alpha=s_X/(4*pi*G_N*Z_X) and q_profile=F_ST Pi_R10 beta_s beta_t unless parent convention absorbs one or more factors",
            "2192/1035/1036",
            "SCHEMA_REFINED_NONCLAIM",
            "parent convention deciding which factors live in coefficient versus profile",
        ),
        (
            "FAC2194_2_universal_cg_warning",
            "universal Weyl/common matter-frame branch",
            "beta_s=c_g profile_s and beta_t=c_g profile_t, so alpha is proportional to c_g^2 not c_g",
            "a linear c_g R10 score is invalid unless Qbar_XH or q_profile explicitly already contains the other leg",
            "1035/1036/1037",
            "GUARDRAIL_ACTIVE",
            "source/test leg accounting and profile definitions",
        ),
        (
            "FAC2194_3_no_pole_zero",
            "quotient/gauge/constraint-only local response",
            "if no physical X pole exists, no local Yukawa Green kernel exists and alpha_predicted is zero/not_applicable",
            "requires q-kernel, action descent, first-class constraint, boundary silence, degree count and matter/readout descent",
            "1037",
            "BEST_DERIVATION_ROUTE_UNSIGNED",
            "all no-pole certificate clauses from one parent action",
        ),
        (
            "FAC2194_4_tail_envelope",
            "retained non-EH/disformal/marker/support tails",
            "|alpha_predicted| <= |K_X^R10|*(beta_s_abs beta_t_abs + abs_tail_source_test)",
            "unknown tails add in absolute value; no cancellation credit",
            "1037",
            "FALLBACK_BOUND_CONTRACT",
            "component theorem-zero or source-backed numeric bounds",
        ),
    ]
    return [
        base_row(
            factor_id=factor_id,
            branch=branch,
            alpha_form=alpha_form,
            normalization_rule=rule,
            source_pack=source_pack,
            current_status=status,
            missing_for_score=missing,
            score_ready=False,
        )
        for factor_id, branch, alpha_form, rule, source_pack, status, missing in specs
    ]


def theorem_zero_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "TZG2194_0_q_kernel",
            "Dq[v_X]=0 with q parent-defined before variation",
            "NP1037_0_q_kernel",
            "UNSIGNED",
            "without this, X can be physical rather than quotient-only",
        ),
        (
            "TZG2194_1_action_descent",
            "S_bulk[Phi]=S_red[q(Phi)] so Hessian has no invertible vertical Green operator",
            "NP1037_1_action_descent",
            "UNSIGNED",
            "without this, finite pole branch must remain",
        ),
        (
            "TZG2194_2_constraint_generator",
            "vertical X is generated by a first-class differentiable constraint with closed bracket",
            "NP1037_2_momentum_map",
            "UNSIGNED",
            "without this, apparent gauge direction may be second-class or physical",
        ),
        (
            "TZG2194_3_boundary_silence",
            "Q_X=0/exact/proper and K_boundary=0 locally",
            "NP1037_3_boundary_silence",
            "UNSIGNED",
            "without this, boundary/local charges can produce retained tails",
        ),
        (
            "TZG2194_4_degree_count",
            "constraints remove the local X pair from reduced phase space",
            "NP1037_4_degree_count",
            "UNSIGNED",
            "without this, local response is not eliminated",
        ),
        (
            "TZG2194_5_matter_readout",
            "ordinary matter/readout descends through q and no marker sees X",
            "NP1037_5_matter_readout",
            "UNSIGNED",
            "without this, beta_s/beta_t or marker tails survive",
        ),
        (
            "TZG2194_6_verdict",
            "all above clauses close from one parent action",
            "NP1037_6_verdict",
            "FAIL_CURRENT_CORPUS",
            "theorem-zero not proved; finite residual map stays active",
        ),
    ]
    return [
        base_row(
            gate_id=gate_id,
            required_clause=clause,
            source_row=source_row,
            current_status=status,
            failure_impact=impact,
            theorem_zero_ready=False,
        )
        for gate_id, clause, source_row, status, impact in specs
    ]


def component_status_rows() -> list[dict[str, Any]]:
    specs = [
        ("COMP2194_0_ZX", "Z_X", "K_X^pt denominator and ghost/elliptic sign", "MISSING_PARENT_KINETIC_RESIDUE", "PX1036_1_quadratic_residue;KXF1035_0_KX_point"),
        ("COMP2194_1_lambdaX", "lambda_X", "range where R10 bound is read", "RELATION_DERIVED_VALUES_MISSING", "PX1036_2_mass_gap_range;KXF1035_1_range"),
        ("COMP2194_2_beta_s", "beta_s(lambda)", "source leg of finite exchange", "MISSING_BETA_SOURCE_TEST_SPLIT", "BETA1036_0_point_particle_source;BB1037_0_beta_source_geom"),
        ("COMP2194_3_beta_t", "beta_t(lambda)", "test/readout leg of finite exchange", "MISSING_BETA_SOURCE_TEST_SPLIT", "BETA1036_0_point_particle_source;BB1037_1_beta_test_geom"),
        ("COMP2194_4_profile", "F_ST(lambda)", "finite source/test overlap", "SYMBOLIC_ONLY", "PROF1035_2_pair_overlap"),
        ("COMP2194_5_harmonic", "Pi_R10(lambda)", "R10 torque harmonic projection", "MISSING_EXPERIMENTAL_PROJECTION", "KXF1035_3_harmonic;PROF1035_3_R10_harmonic"),
        ("COMP2194_6_tail", "epsilon_tail(lambda)", "absolute retained tail envelope", "MISSING_NUMERIC_ENVELOPE", "TAIL1037_0_alpha_envelope"),
        ("COMP2194_7_bound_curve", "alpha_bound(lambda)", "external comparison wall", "REVIEW_CANDIDATE_NONCLAIM_AVAILABLE", "R10CURVE2193_0_review_candidate_admitted_to_q_loc_branch"),
    ]
    return [
        base_row(
            component_id=component_id,
            quantity=quantity,
            role=role,
            current_status=status,
            source_rows=source_rows,
            ready_for_score=False,
        )
        for component_id, quantity, role, status, source_rows in specs
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            model_id="MTS_q_loc_R10_alpha_template_2194",
            branch_id_template="finite_exchange_or_theorem_zero",
            lambda_value="MISSING_PARENT_LAMBDA_X",
            alpha_predicted="MISSING_PARENT_ALPHA_PREDICTED",
            alpha_bound_source="source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2193_R10_JOIN_PREVIEW.csv::nearest_alpha_bound",
            finite_exchange_formula="alpha_predicted(lambda)=s_X*K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            schema_2192_formula="alpha_R10_q(lambda)=c_q_alpha(lambda)*q_profile(lambda)+epsilon_tail(lambda)",
            c_q_alpha_lambda="MISSING_ZX_SIGN_AND_UNIT_CONVENTION",
            q_profile_lambda="MISSING_FST_PI_R10_BETA_SOURCE_BETA_TEST",
            theorem_zero_alternative="alpha_predicted=0 only if TZG2194_0..TZG2194_5 close from one parent action",
            failure_reasons="MISSING_ZX;MISSING_LAMBDA_X;MISSING_BETA_S;MISSING_BETA_T;MISSING_PROFILE;MISSING_PI_R10;MISSING_TAIL_ENVELOPE;THEOREM_ZERO_UNSIGNED;BOUND_CURVE_NONCLAIM",
            score_ready=False,
            row_status="derived_contract_nonclaim_values_missing",
        )
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2194_0_formula", "finite-exchange alpha formula exists as a contract", "PASS_NONCLAIM", "shape is derived from Green-kernel and source/test product rows"),
        ("CG2194_1_theorem_zero", "q_loc/R10 alpha is zero by parent theorem", "BLOCKED_NONCLAIM", "no-pole certificate clauses are unsigned"),
        ("CG2194_2_numeric_alpha", "alpha_predicted(lambda) is numeric/source-backed", "BLOCKED_NONCLAIM", "Z_X, lambda_X, beta_s, beta_t, profile, Pi_R10 and tails are missing"),
        ("CG2194_3_R10_score", "R10 pass/fail can be claimed", "BLOCKED_NONCLAIM", "theory side is missing and external curve is review-candidate nonclaim"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2194_0_gain",
            "QLOC_R10_ALPHA_MAP_DERIVED_AS_CONTRACT",
            "The vague coupling gap is now a precise fork: no-pole theorem-zero or finite exchange with K_X^R10 beta_s beta_t plus absolute tails.",
            "selected",
        ),
        (
            "DEC2194_1_limit",
            "NO_NUMERIC_OR_ZERO_ALPHA_YET",
            "The parent action does not yet sign the no-pole certificate or the finite-X coefficient/source-test rows.",
            "selected",
        ),
        (
            "DEC2194_2_next",
            "NO_POLE_CERTIFICATE_FIRST_THEN_BETA_ROWS",
            "The least-scrutinized route is to try to eliminate the physical pole; if that fails, fill bounded beta/source-test rows without cancellation.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2194_0_2195",
            selection_status="selected",
            target_file="2195-Y5-R2FR-parent-quotient-no-pole-certificate-or-first-beta-bound-row.md",
            target_script="scripts/Y5_R2FR_parent_quotient_no_pole_certificate_or_first_beta_bound_row_2195.py",
            objective="attempt the parent no-physical-pole certificate for the q_loc/R10 channel; if one clause cannot close, create the first bounded beta_s/beta_t row with absolute-tail policy",
            success_condition="one no-pole certificate clause is parent-signed/demoted, or one beta component row gets a source-backed bound; no alpha/R10/local-GR claim is made",
            do_not_do="do not invent Z_X, beta values, c_g, tau_R10, unity profiles, cancellation between tails, or a linear-c_g R10 score",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["factorization_contract"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["component_status"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["alpha_template"], BRANCH_COPIES["source_weight"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if truthy(row.get("claim_allowed", False)):
                return False
            if truthy(row.get("valid_for_claim", False)):
                return False
    return True


def all_score_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("score_ready", "ready_for_score", "theorem_zero_ready"):
                if key in row and truthy(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2194_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2194_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    factor_text = "\n".join(row["alpha_form"] + " " + row["normalization_rule"] for row in rows_by_name["factorization_contract"])
    factor_pass = "K_X^R10" in factor_text and "beta_s" in factor_text and "beta_t" in factor_text and "c_g^2" in factor_text and "no physical X pole" in factor_text
    validations.append(base_row(validation_id="VAL2194_02_factorization_contract", status="PASS" if factor_pass else "FAIL", detail="finite exchange, c_g^2 guard, 2192 schema mapping and no-pole branch are present"))

    theorem_rows = rows_by_name["theorem_zero_gate"]
    theorem_blocked = any(row["current_status"] == "FAIL_CURRENT_CORPUS" for row in theorem_rows) and all(not truthy(row["theorem_zero_ready"]) for row in theorem_rows)
    validations.append(base_row(validation_id="VAL2194_03_theorem_zero_blocked", status="PASS" if theorem_blocked else "FAIL", detail="no-pole theorem-zero clauses remain unsigned/nonclaim"))

    components = rows_by_name["component_status"]
    missing_components = [row for row in components if "MISSING" in row["current_status"] or "SYMBOLIC" in row["current_status"]]
    external_available = any(row["quantity"] == "alpha_bound(lambda)" and row["current_status"] == "REVIEW_CANDIDATE_NONCLAIM_AVAILABLE" for row in components)
    validations.append(base_row(validation_id="VAL2194_04_component_status", status="PASS" if len(missing_components) >= 6 and external_available else "FAIL", detail=f"missing_or_symbolic_components={len(missing_components)};external_review_candidate_available={external_available}"))

    alpha_row = rows_by_name["alpha_template"][0]
    alpha_pass = "K_X^R10" in alpha_row["finite_exchange_formula"] and "MISSING_PARENT_ALPHA_PREDICTED" in alpha_row["alpha_predicted"] and not truthy(alpha_row["score_ready"])
    validations.append(base_row(validation_id="VAL2194_05_alpha_template_nonclaim", status="PASS" if alpha_pass else "FAIL", detail=f"row_status={alpha_row['row_status']};score_ready={alpha_row['score_ready']}"))

    gate_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2194_06_claim_gate", status="PASS" if "PASS_NONCLAIM" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses else "FAIL", detail="formula contract passes only as nonclaim; zero/numeric/R10 claims blocked"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2194_07_decision", status="PASS" if "NO_POLE_CERTIFICATE_FIRST_THEN_BETA_ROWS" in decisions else "FAIL", detail="decision selects no-pole certificate before beta fallback"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2194_08_next_target", status="PASS" if "NEXT2194_0_2195" in routes else "FAIL", detail="2195 no-pole/beta-row target selected"))

    validations.append(base_row(validation_id="VAL2194_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    validations.append(base_row(validation_id="VAL2194_10_score_flags_false", status="PASS" if all_score_flags_false(rows_by_name) else "FAIL", detail="no generated row is score-ready or theorem-zero-ready"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2194_11_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2194_12_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2194_13_formalization_clean", status="PASS" if not formalization_has_2194_artifacts() else "FAIL", detail="formalization-workbench has no 2194 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2194_14_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2194_OVERALL", status=overall, detail="2194 derives the q_loc/R10 alpha map as a nonclaim contract, keeps theorem-zero unsigned, and selects no-pole certificate or beta-row fill next"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# 2194 - Y5/R2FR Parent q_loc Alpha Coefficient/Profile Or Theorem-Zero",
        "",
        "## Current Verdict",
        "",
        "2194 converts the loose word `coupling` into an exact fork.",
        "",
        "Either the local `q_loc`/R10 channel has **no physical pole** in the GR/Newton branch, in which case the Yukawa alpha is zero/not applicable, or a finite exchange branch survives and the private-test law is:",
        "",
        "`alpha_predicted(lambda)=s_X K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda)`.",
        "",
        "This is a derivation contract, not a score. The current corpus still lacks the parent-signed no-pole certificate and the finite-exchange inputs `Z_X`, `lambda_X`, `beta_s`, `beta_t`, `F_ST`, `Pi_R10`, and absolute tails.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Alpha Factorization Contract",
        "",
        md_table(rows_by_name["factorization_contract"], ["factor_id", "branch", "alpha_form", "normalization_rule", "current_status", "missing_for_score", "score_ready", "valid_for_claim"]),
        "",
        "## Theorem-Zero Or Finite Exchange Gate",
        "",
        md_table(rows_by_name["theorem_zero_gate"], ["gate_id", "required_clause", "source_row", "current_status", "failure_impact", "theorem_zero_ready", "valid_for_claim"]),
        "",
        "## Theory Component Status",
        "",
        md_table(rows_by_name["component_status"], ["component_id", "quantity", "role", "current_status", "source_rows", "ready_for_score", "valid_for_claim"]),
        "",
        "## R10 Alpha Template Row",
        "",
        md_table(rows_by_name["alpha_template"], ["model_id", "alpha_predicted", "finite_exchange_formula", "schema_2192_formula", "c_q_alpha_lambda", "q_profile_lambda", "theorem_zero_alternative", "failure_reasons", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "This is the sharpest shape of the local problem so far. We are not looking for a mystical coupling anymore. We are looking for either a parent quotient/no-pole certificate, or the first honest beta/source-test bound row. The `c_g` trap is also explicit: a universal source and test coupling contributes as `c_g^2`, not as a single linear `c_g`, unless one leg has already been absorbed into the profile convention.",
        "",
        "Best next attack: try to close the no-pole certificate clause-by-clause. If it fails at a named clause, immediately turn that failed clause into a bounded beta/tail acquisition row instead of circling.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "factorization_contract": factorization_contract_rows(),
        "theorem_zero_gate": theorem_zero_gate_rows(),
        "component_status": component_status_rows(),
        "alpha_template": alpha_template_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()

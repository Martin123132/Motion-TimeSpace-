from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2195"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2195-Y5-R2FR-parent-quotient-no-pole-certificate-or-first-beta-bound-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2195_SOURCE_REGISTER.csv",
    "no_pole_clause_attempt": OUT / "P8_Y5_PARENT_QLOC_2195_NO_POLE_CLAUSE_ATTEMPT.csv",
    "demotion_ledger": OUT / "P8_Y5_PARENT_QLOC_2195_NO_POLE_DEMOTION_LEDGER.csv",
    "beta_pressure_row": OUT / "P8_Y5_PARENT_QLOC_2195_FIRST_BETA_PRODUCT_PRESSURE_ROW.csv",
    "cg_squared_guard": OUT / "P8_Y5_PARENT_QLOC_2195_CG_SQUARED_GUARD.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2195_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2195_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2195_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2195_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2195_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2195_NO_POLE_DEMOTION_AND_BETA_PRESSURE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2195_FIRST_BETA_PRODUCT_PRESSURE_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_R10_BETA_PRODUCT_PRESSURE_2195_NONCLAIM.csv",
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


def safe_float(value: Any) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def formalization_has_2195_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2195-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2195*",
        "*P8_Y5_BRR545_2195*",
        "*Y5_R2FR_parent_quotient_no_pole_certificate_or_first_beta_bound_row_2195*",
        "*JR2195*",
        "*PARENT_QLOC_R10_BETA_PRODUCT_PRESSURE_2195*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2194_doc",
            ROOT / "2194-Y5-R2FR-parent-q_loc-alpha-coefficient-profile-or-theorem-zero.md",
            ["NEXT2194_0_2195", "alpha_predicted(lambda)=s_X K_X^R10(lambda)", "Best next attack"],
            "2194 selects no-pole certificate first and beta row fallback.",
        ),
        (
            "2194_theorem_gate",
            OUT / "P8_Y5_PARENT_QLOC_2194_THEOREM_ZERO_OR_FINITE_EXCHANGE_GATE.csv",
            ["TZG2194_0_q_kernel", "TZG2194_6_verdict", "FAIL_CURRENT_CORPUS"],
            "Current q_loc no-pole theorem clauses remain unsigned.",
        ),
        (
            "2194_factorization",
            OUT / "P8_Y5_PARENT_QLOC_2194_ALPHA_FACTORIZATION_CONTRACT.csv",
            ["FAC2194_0_exact_finite_exchange", "FAC2194_2_universal_cg_warning", "FAC2194_4_tail_envelope"],
            "Current q_loc R10 alpha factorization contract.",
        ),
        (
            "2193_join_preview",
            OUT / "P8_Y5_PARENT_QLOC_2193_R10_JOIN_PREVIEW.csv",
            ["R10JOIN2193_0_component_seed_to_review_candidate", "nearest_alpha_bound", "MISSING_ALPHA_PREDICTED"],
            "Review-candidate alpha wall at the 38.6 micrometer q_loc seed.",
        ),
        (
            "1023_demotion_doc",
            ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
            ["single `q/v_X/action` certificate does not close", "QVC1023_8_verdict", "fail_current_claim_demote_current_branch"],
            "Earlier certificate attempt demoted no-pole route to conditional-only for current corpus.",
        ),
        (
            "1023_validation",
            OUT / "P8_Y5_BRR545_1023_VALIDATION.csv",
            ["V1023_2_certificate_fails", "V1023_5_demotion_complete", "V1023_8_claim_gates_blocked"],
            "Validation of prior demotion and claim gates.",
        ),
        (
            "1027_qbar_bound",
            ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
            ["QZ1027_6_verdict", "FAIL_CURRENT_CLAIM", "bounded `qbar_XT` component schema"],
            "Matter source-zero fails and bounded coupling fallback is required.",
        ),
        (
            "1038_omega_audit",
            OUT / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv",
            ["ODC1038_0_parent_Omega", "ODC1038_5_bracket_closure", "ODC1038_6_degree_count"],
            "Parent Omega/DCX/degree-count gaps prevent no-pole claim.",
        ),
        (
            "1038_validation",
            OUT / "P8_Y5_BRR545_1038_VALIDATION.csv",
            ["V1038_1_closure_audit_blocks_claim", "V1038_4_beta_acquisition_staged_nonclaim", "V1038_5_linear_cg_quarantined"],
            "Validation of Omega/DCX failure and beta acquisition staging.",
        ),
        (
            "1041_owner_doc",
            ROOT / "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
            ["FAIL_CURRENT_CLAIM_THETAX_PX_OWNER_MISSING", "NFR1041_2_first_class_constraint", "DEC1041_0_parent_route_status"],
            "Theta_X/P_X route exists as template but parent owner is missing.",
        ),
        (
            "1087_matter_descent",
            ROOT / "1087-Y5-R10-parent-matter-descent-zero-current-or-DD-coefficient-source-pack.md",
            ["PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED", "DD coefficient source-pack is ready but empty", "CG1087_0_matter_descent"],
            "Matter/readout descent remains unsigned and forces finite source/test couplings to remain live.",
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


def no_pole_clause_attempt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NP2195_0_q_kernel",
            "Dq[v_X]=0 for the actual local X direction before variation",
            "1023 has a conditional q-map but actual local Xhat variations are not proved to equal an integrable parent null/relative-exact generator.",
            "DEMOTED_CURRENT_BRANCH_CONDITIONAL_ONLY",
            "finite beta/source-test row remains live",
        ),
        (
            "NP2195_1_action_descent",
            "S_parent[Phi]=S_red[q(Phi)] plus silent boundary/topological terms",
            "1023/1038 do not supply one parent Lagrangian with retained boundary/domain terms silent along v_X.",
            "DEMOTED_CURRENT_BRANCH_CONDITIONAL_ONLY",
            "finite Hessian/Green-kernel branch remains live",
        ),
        (
            "NP2195_2_first_class_generator",
            "i_v Omega = delta C_X with differentiable Q_X and closed bracket",
            "1038 names Omega_Y, D C_X, Q_X, bracket and degree count as missing objects.",
            "DEMOTED_CURRENT_BRANCH_CONDITIONAL_ONLY",
            "X cannot be treated as pure gauge/constraint",
        ),
        (
            "NP2195_3_boundary_silence",
            "Q_X=0/exact/proper and K_boundary=0 on compact local branch",
            "1038 and 1041 leave Q_X/K_boundary and boundary flux/source terms uncomputed.",
            "DEMOTED_CURRENT_BRANCH_CONDITIONAL_ONLY",
            "absolute tail/edge envelope remains live",
        ),
        (
            "NP2195_4_matter_readout",
            "ordinary matter/readout descends through q with no X-sensitive marker",
            "1087 says parent matter descent zero is not signed; 1027 keeps qbar_XT finite as fallback.",
            "DEMOTED_CURRENT_BRANCH_CONDITIONAL_ONLY",
            "beta_s/beta_t marker and geometry rows remain live",
        ),
        (
            "NP2195_5_degree_count",
            "rank/count removes the local X pair from reduced phase space",
            "1023/1038/1041 keep reduced rank and no-stabilizer check as an obligation, not a calculation.",
            "DEMOTED_CURRENT_BRANCH_CONDITIONAL_ONLY",
            "zero Hessian cannot be spent as gauge evidence",
        ),
        (
            "NP2195_6_verdict",
            "all no-pole clauses close from one parent action",
            "No inspected source signs the whole package; every clause is conditional, missing, or demoted.",
            "NO_POLE_NOT_CURRENTLY_CLAIMABLE",
            "proceed to first beta-product pressure row",
        ),
    ]
    return [
        base_row(
            clause_id=clause_id,
            required_statement=required,
            evidence_result=evidence,
            current_status=status,
            residual_impact=impact,
            theorem_zero_ready=False,
        )
        for clause_id, required, evidence, status, impact in specs
    ]


def demotion_ledger_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            demotion_id="DEM2195_0_no_pole_route",
            route="parent quotient/no-physical-pole q_loc/R10 route",
            demotion="closure_only_current_corpus",
            reason="the q-kernel, action descent, first-class generator, boundary silence, matter/readout descent and degree-count clauses do not close from one parent action",
            what_survives="future theorem target if a parent action supplies the whole certificate",
            what_must_not_be_done="do not set alpha_predicted=0 or K_X=0 from conditional quotient language",
        ),
        base_row(
            demotion_id="DEM2195_1_beta_fallback",
            route="finite source/test exchange fallback",
            demotion="active_nonclaim_residual_branch",
            reason="finite exchange is the honest branch if no-pole is unsigned",
            what_survives="alpha_predicted=s_X K_X^R10 beta_s beta_t + epsilon_tail with absolute no-cancellation policy",
            what_must_not_be_done="do not invent beta_s,beta_t,c_g,tau_R10,K_X or profile values",
        ),
    ]


def beta_pressure_rows() -> list[dict[str, Any]]:
    join = read_csv(OUT / "P8_Y5_PARENT_QLOC_2193_R10_JOIN_PREVIEW.csv")
    row = join[0] if join else {}
    nearest_alpha = safe_float(row.get("nearest_alpha_bound"))
    nearest_lambda = safe_float(row.get("nearest_lambda_m"))
    target_lambda = safe_float(row.get("target_lambda_m"))
    lambda_relative_error = safe_float(row.get("lambda_relative_error"))
    alpha_text = row.get("nearest_alpha_bound", "MISSING_ALPHA_BOUND")
    return [
        base_row(
            beta_row_id="BETA2195_0_R10_beta_product_pressure_at_38p6um",
            arena="R10_short_range",
            target_lambda_m=target_lambda if target_lambda is not None else "MISSING",
            nearest_curve_lambda_m=nearest_lambda if nearest_lambda is not None else "MISSING",
            lambda_relative_error=lambda_relative_error if lambda_relative_error is not None else "MISSING",
            alpha_bound_review_candidate=nearest_alpha if nearest_alpha is not None else "MISSING",
            alpha_bound_source=row.get("alpha_bound_source", "MISSING_ALPHA_BOUND_SOURCE"),
            source_join_row=row.get("join_id", "MISSING_JOIN_ROW"),
            pressure_quantity="abs(beta_s(lambda)*beta_t(lambda)) plus absolute tails",
            conditional_bound_formula=f"abs(beta_s*beta_t) <= ({alpha_text}-abs(epsilon_tail))/abs(K_X^R10(lambda)) if K_X^R10 is sourced and epsilon_tail is bounded",
            universal_cg_formula=f"abs(c_g) <= sqrt(({alpha_text}-abs(epsilon_tail))/(abs(K_X^R10)*abs(profile_s*profile_t))) only in a parent-signed universal Weyl source/test branch",
            source_leg_status="MISSING_BETA_SOURCE",
            test_leg_status="MISSING_BETA_TEST",
            kx_status="MISSING_KX_R10",
            tail_status="MISSING_ABSOLUTE_TAIL_ENVELOPE",
            curve_status="REVIEW_CANDIDATE_NONCLAIM",
            bound_status="source_backed_conditional_pressure_not_numeric_beta_bound",
            score_ready=False,
            notes="This is the first honest beta-product pressure row: the external alpha wall is real-shaped, but K_X/profile/tails are not known, so no beta value or R10 score is claimed.",
        )
    ]


def cg_squared_guard_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            guard_id="CGSQ2195_0_universal_weyl_two_leg_rule",
            branch="universal matter-frame/Weyl source-test response",
            wrong_form="alpha_R10 proportional to c_g",
            correct_form="alpha_R10 proportional to K_X^R10(lambda)*c_g^2*profile_s(lambda)*profile_t(lambda)+epsilon_tail(lambda)",
            exception="linear c_g is allowed only if one source/test leg is explicitly already absorbed into q_profile or Qbar_XH with source path and units",
            current_exception_status="NO_ABSORBED_LEG_SOURCE_DECLARED",
            guard_status="linear_cg_quarantined",
            score_ready=False,
        ),
        base_row(
            guard_id="CGSQ2195_1_no_cancellation_tail_rule",
            branch="retained tails and marker/disformal/support leakage",
            wrong_form="unknown tails can cancel beta_s beta_t",
            correct_form="unknown tails add in absolute value before comparison with alpha_bound(lambda)",
            exception="cancellation credit requires parent theorem-zero or source-backed signed correlation row",
            current_exception_status="NO_SIGNED_CORRELATION_ROW",
            guard_status="no_cancellation_policy_active",
            score_ready=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2195_0_no_pole", "no physical q_loc/R10 pole is proved", "BLOCKED_NONCLAIM", "all no-pole clauses are demoted to conditional-only for the current corpus"),
        ("CG2195_1_beta_pressure", "first beta product pressure row exists", "PASS_NONCLAIM", "source-backed review-candidate alpha wall gives a conditional pressure formula, not a beta value"),
        ("CG2195_2_numeric_beta", "numeric beta_s/beta_t bound is known", "BLOCKED_NONCLAIM", "K_X^R10, profile, source/test legs and tails are missing"),
        ("CG2195_3_R10_score", "R10 pass/fail can be claimed", "BLOCKED_NONCLAIM", "theory side remains conditional and the external curve is review-candidate nonclaim"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2195_0_no_pole_result",
            "NO_POLE_ROUTE_DEMOTED_CURRENT_BRANCH",
            "The no-pole path remains the cleanest future derivation, but current sources do not sign any claim-grade parent certificate.",
            "selected",
        ),
        (
            "DEC2195_1_beta_result",
            "FIRST_R10_BETA_PRODUCT_PRESSURE_ROW_WRITTEN",
            "The external review curve now puts a conditional pressure wall on beta_s beta_t without inventing K_X or beta values.",
            "selected",
        ),
        (
            "DEC2195_2_next",
            "ATTACK_KX_OR_BETA_LEG_SOURCE_NEXT",
            "The next non-circular move is to source/derive either K_X^R10 normalization or one source/test beta leg; otherwise the pressure row cannot become numeric.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2195_0_2196",
            selection_status="selected",
            target_file="2196-Y5-R2FR-KX-normalization-or-beta-leg-source-first-row.md",
            target_script="scripts/Y5_R2FR_KX_normalization_or_beta_leg_source_first_row_2196.py",
            objective="derive or source one missing term in the beta pressure row: K_X^R10 normalization, beta_s source leg, beta_t readout leg, or an absolute tail bound",
            success_condition="one factor in abs(beta_s beta_t)<=alpha_bound/abs(K_X) is parent-derived, source-backed, or explicitly demoted; no R10/local-GR claim is made",
            do_not_do="do not set K_X=1, do not set beta=1, do not use linear c_g, do not ignore tails, do not promote the review curve to claim-grade",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["demotion_ledger"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["beta_pressure_row"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["beta_pressure_row"], BRANCH_COPIES["source_weight"]),
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
            for key in ("score_ready", "theorem_zero_ready"):
                if key in row and truthy(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2195_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2195_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    no_pole_rows = rows_by_name["no_pole_clause_attempt"]
    no_pole_demoted = any(row["clause_id"] == "NP2195_6_verdict" and row["current_status"] == "NO_POLE_NOT_CURRENTLY_CLAIMABLE" for row in no_pole_rows)
    no_theorem_ready = all(not truthy(row.get("theorem_zero_ready", False)) for row in no_pole_rows)
    validations.append(base_row(validation_id="VAL2195_02_no_pole_demoted", status="PASS" if no_pole_demoted and no_theorem_ready else "FAIL", detail=f"no_pole_demoted={no_pole_demoted};no_theorem_ready={no_theorem_ready}"))

    demotion_ok = any(row["demotion"] == "closure_only_current_corpus" for row in rows_by_name["demotion_ledger"])
    validations.append(base_row(validation_id="VAL2195_03_demotion_ledger", status="PASS" if demotion_ok else "FAIL", detail="no-pole route demoted without deleting future theorem target"))

    beta_row = rows_by_name["beta_pressure_row"][0]
    alpha = safe_float(beta_row["alpha_bound_review_candidate"])
    beta_ok = (
        alpha is not None
        and alpha > 0
        and "abs(K_X^R10" in beta_row["conditional_bound_formula"]
        and beta_row["kx_status"] == "MISSING_KX_R10"
        and not truthy(beta_row["score_ready"])
    )
    validations.append(base_row(validation_id="VAL2195_04_beta_pressure_row", status="PASS" if beta_ok else "FAIL", detail=f"alpha={beta_row['alpha_bound_review_candidate']};kx_status={beta_row['kx_status']};score_ready={beta_row['score_ready']}"))

    cg_rows = rows_by_name["cg_squared_guard"]
    cg_guard_ok = any("c_g^2" in row["correct_form"] and row["guard_status"] == "linear_cg_quarantined" for row in cg_rows)
    tail_guard_ok = any(row["guard_status"] == "no_cancellation_policy_active" for row in cg_rows)
    validations.append(base_row(validation_id="VAL2195_05_cg_tail_guards", status="PASS" if cg_guard_ok and tail_guard_ok else "FAIL", detail=f"cg_squared_guard={cg_guard_ok};tail_guard={tail_guard_ok}"))

    gate_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2195_06_claim_gate", status="PASS" if "PASS_NONCLAIM" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses else "FAIL", detail="beta pressure passes only as nonclaim; no-pole/numeric/R10 claims blocked"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2195_07_decision", status="PASS" if "ATTACK_KX_OR_BETA_LEG_SOURCE_NEXT" in decisions else "FAIL", detail="decision selects K_X or beta leg source next"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2195_08_next_target", status="PASS" if "NEXT2195_0_2196" in routes else "FAIL", detail="2196 KX/beta-leg target selected"))

    validations.append(base_row(validation_id="VAL2195_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    validations.append(base_row(validation_id="VAL2195_10_score_flags_false", status="PASS" if all_score_flags_false(rows_by_name) else "FAIL", detail="no generated row is score-ready or theorem-zero-ready"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2195_11_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2195_12_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2195_13_formalization_clean", status="PASS" if not formalization_has_2195_artifacts() else "FAIL", detail="formalization-workbench has no 2195 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2195_14_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2195_OVERALL", status=overall, detail="2195 demotes current no-pole route to closure-only and writes the first source-backed conditional R10 beta-product pressure row without claims"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# 2195 - Y5/R2FR Parent Quotient No-Pole Certificate Or First Beta Bound Row",
        "",
        "## Current Verdict",
        "",
        "2195 takes the no-pole route seriously and rejects it as a **current claim**. The route is still the cleanest future derivation, but the present corpus does not parent-sign the q-kernel, action descent, first-class generator, boundary silence, matter/readout descent, and degree count together.",
        "",
        "The consequence is not defeat; it is discipline. Since `alpha_predicted=0` is not earned, the finite source/test branch remains active. The first honest pressure row is now:",
        "",
        "`abs(beta_s beta_t) <= (alpha_bound(lambda)-abs(epsilon_tail))/abs(K_X^R10(lambda))`",
        "",
        "using the 2193 review-candidate R10 alpha wall at the 38.6 micrometer seed. This is **not** a numeric beta bound yet because `K_X^R10`, source/test profiles, and tails are still missing.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## No-Pole Clause Attempt",
        "",
        md_table(rows_by_name["no_pole_clause_attempt"], ["clause_id", "required_statement", "current_status", "residual_impact", "theorem_zero_ready", "valid_for_claim"]),
        "",
        "## Demotion Ledger",
        "",
        md_table(rows_by_name["demotion_ledger"], ["demotion_id", "route", "demotion", "reason", "what_survives", "what_must_not_be_done", "valid_for_claim"]),
        "",
        "## First Beta Product Pressure Row",
        "",
        md_table(rows_by_name["beta_pressure_row"], ["beta_row_id", "arena", "target_lambda_m", "nearest_curve_lambda_m", "alpha_bound_review_candidate", "conditional_bound_formula", "source_leg_status", "test_leg_status", "kx_status", "tail_status", "bound_status", "score_ready", "valid_for_claim"]),
        "",
        "## c_g Squared And Tail Guard",
        "",
        md_table(rows_by_name["cg_squared_guard"], ["guard_id", "branch", "wrong_form", "correct_form", "exception", "current_exception_status", "guard_status", "score_ready", "valid_for_claim"]),
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
        "This is the point where we stop circling the word `coupling`. The no-pole path did not close in the present corpus, so the next practical derivation target is one factor in the pressure row: `K_X^R10`, `beta_s`, `beta_t`, or the absolute tail envelope. The review curve now tells us where the wall is; the theory side must tell us what is trying to hit it.",
        "",
        "Best next attack: derive/source `K_X^R10` normalization first if possible, because it turns the beta pressure row from a formal inequality into a quantitative target. If `K_X` stays unsigned, attack one beta leg with the same no-cancellation policy.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "no_pole_clause_attempt": no_pole_clause_attempt_rows(),
        "demotion_ledger": demotion_ledger_rows(),
        "beta_pressure_row": beta_pressure_rows(),
        "cg_squared_guard": cg_squared_guard_rows(),
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

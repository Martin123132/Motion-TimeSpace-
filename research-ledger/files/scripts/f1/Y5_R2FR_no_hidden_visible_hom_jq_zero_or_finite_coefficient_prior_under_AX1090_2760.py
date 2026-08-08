from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2760-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2760_SOURCE_REGISTER.csv",
    "theorem": MTS / "P8_Y5_R2FR_2760_NO_HIDDEN_VISIBLE_HOM_THEOREM_ATTEMPT.csv",
    "clauses": MTS / "P8_Y5_R2FR_2760_OPERATOR_DOMAIN_CLAUSE_LEDGER.csv",
    "countermodels": MTS / "P8_Y5_R2FR_2760_COUNTERMODEL_TO_JQ_MAP.csv",
    "priors": MTS / "P8_Y5_R2FR_2760_FINITE_COEFFICIENT_PRIOR_INTERFACE.csv",
    "arena": MTS / "P8_Y5_R2FR_2760_ARENA_IMPACT.csv",
    "decisions": MTS / "P8_Y5_R2FR_2760_DECISION_LEDGER.csv",
    "gates": MTS / "P8_Y5_R2FR_2760_CLAIM_GATES.csv",
    "refusal": MTS / "P8_Y5_R2FR_2760_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": MTS / "P8_Y5_R2FR_2760_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2760_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2760_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_queue": RAB_QUEUE / "JR2760_NO_HIDDEN_VISIBLE_HOM_THEOREM_ATTEMPT_NONCLAIM.csv",
    "prior_queue": RAB_QUEUE / "JR2760_FINITE_COEFFICIENT_PRIOR_INTERFACE_NONCLAIM.csv",
    "arena_beta": BETA_DOCS / "NO_HIDDEN_VISIBLE_HOM_LOCAL_ARENA_IMPACT_2760_NONCLAIM.csv",
    "arena_local": LOCAL_BOUNDS / "no_hidden_visible_hom_local_arena_impact_2760_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2760_COUPLING_SOURCE_ROW_NEXT_TARGET.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2760_00_2759_doc", "2759_doc", WORK / "2759-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack-under-AX1090.md", ["CMJ2759_5_hidden_visible_hom", "NEXT2759_0_2760"], "direct handoff: hidden-visible coupling is best next target"),
        ("SRC2760_01_2759_validation", "2759_validation", MTS / "P8_Y5_BRR545_2759_VALIDATION.csv", ["VAL2759_OVERALL"], "2759 validation"),
        ("SRC2760_02_2759_pack", "2759_finite_jq_pack", MTS / "P8_Y5_R2FR_2759_FINITE_JQ_SOURCE_PACK.csv", ["JQPACK2759_3_const", "JQPACK2759_4_shadow", "JQPACK2759_8_same_branch_lock"], "finite j_q source channels"),
        ("SRC2760_03_1090_doc", "1090_AX1090_doc", WORK / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md", ["AX1090_1_no_hidden_visible_hom", "DEC1090_2_best_next"], "AX1090 missing-axiom statement"),
        ("SRC2760_04_1091_doc", "1091_operator_domain_doc", WORK / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md", ["ODH1091_6_verdict", "FR1091_0_b_alpha"], "operator-domain theorem precedent"),
        ("SRC2760_05_1091_theorem", "1091_operator_domain_csv", MTS / "P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv", ["ODH1091_2_scalar_obstruction", "ODH1091_6_verdict"], "operator-domain theorem/counterexample csv"),
        ("SRC2760_06_2317_doc", "2317_hidden_visible_doc", WORK / "2317-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior.md", ["NHVH2317_5_verdict", "FCP2317_0_b_alpha"], "R2/f(R) hidden-visible theorem precedent"),
        ("SRC2760_07_2317_validation", "2317_validation", MTS / "P8_Y5_BRR545_2317_VALIDATION.csv", ["VAL2317_OVERALL"], "2317 validation"),
        ("SRC2760_08_2318_doc", "2318_functor_doc", WORK / "2318-Y5-R2FR-parent-coefficient-functor-construction-or-finite-coupling-prior-runner.md", ["PCF2318_5_verdict", "OBL2318_5_verdict"], "parent coefficient functor attempt"),
        ("SRC2760_09_2318_schema", "2318_prior_schema", MTS / "P8_Y5_PARENT_QLOC_2318_FINITE_COUPLING_PRIOR_RUNNER_SCHEMA.csv", ["SCHEMA2318_0_required_columns", "SCHEMA2318_3_nonclaim_first_rows"], "finite coupling prior schema"),
        ("SRC2760_10_2319_doc", "2319_source_rows_doc", WORK / "2319-Y5-R2FR-first-source-backed-finite-coupling-row-balpha-clock-or-deltaw.md", ["FCR2319_0_clock_product_best", "REF2319_3_local_GR"], "first source-backed nonclaim finite coupling rows"),
        ("SRC2760_11_2319_rows", "2319_source_rows_csv", MTS / "P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv", ["FCR2319_0_clock_product_best", "FCR2319_3_delta_w_missing_prediction"], "nonclaim product/proxy inputs"),
    ]
    rows = []
    for row_id, source_key, path, needles, role in specs:
        text = read_text(path)
        exists = path.exists()
        needles_found = exists and all(needle in text for needle in needles)
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle_spec": ";".join(needles),
            "needles_found": needles_found,
            "source_role": role,
        }))
    return rows


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NHVH2760_0_target",
            "claim_piece": "no hidden-visible coefficient hom theorem for j_q source silence",
            "formal_statement": "For visible coefficients c_i in {alpha_EM,m_A,y_A,binding_A,clock_i,w_A,A_A,B_A,readout_i,K_X}, require c_i=p_vis^*cbar_i(q_loc,representation,topology,Level_EM,declared_source_owner) with no hidden/representative scalar argument.",
            "proof_status": "TARGET_SHARPENED",
            "if_signed": "partial_q c_i=0 for every vertical q/hid generator in ker(Dp_vis), so j_const,j_shadow,j_weight,readout coefficient legs are theorem-zero",
            "current_gap": "parent action has not selected p_vis/F_coeff/target category as syntax",
        }),
        nonclaim({
            "row_id": "NHVH2760_1_exact_conditional_silence",
            "claim_piece": "vertical derivative silence",
            "formal_statement": "If c_i=p_vis^*cbar_i and v in ker(Dp_vis), then L_v c_i=d cbar_i(Dp_vis v)=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "if_signed": "visible coefficient source currents vanish without tuning or pair cancellation",
            "current_gap": "does not prove c_i is a pullback from p_vis",
        }),
        nonclaim({
            "row_id": "NHVH2760_2_hidden_scalar_counterexample",
            "claim_piece": "surviving hidden scalar defeats theorem",
            "formal_statement": "If I_hid is an invariant scalar with L_v I_hid neq 0 and coefficient targets include R or R_+, then c_i=c0+epsilon I_hid is an allowed hidden-visible Hom and contributes epsilon(L_v I_hid)O_i to j_q.",
            "proof_status": "COUNTEREXAMPLE_RETAINED",
            "if_signed": "not applicable; this is the obstruction",
            "current_gap": "hidden invariant algebra triviality/no-hair/profile-zero route remains unsigned",
        }),
        nonclaim({
            "row_id": "NHVH2760_3_source_target_exclusion",
            "claim_piece": "source-only coefficient target exclusion",
            "formal_statement": "F_coeff must forbid unowned R_+ active-source prefactors and species/source weights except one declared common calibration mode removed before local scoring.",
            "proof_status": "REQUIRED_BUT_UNSIGNED",
            "if_signed": "delta_w_A, source-label weights, and measured-G/source-normalization leakage become ill-typed",
            "current_gap": "source-target exclusion exists as a rule in earlier audits but is not derived from parent primitives",
        }),
        nonclaim({
            "row_id": "NHVH2760_4_effective_readout_closure",
            "claim_piece": "effective action and readout preserve coefficient domain",
            "formal_statement": "If S_bare obeys no hidden-visible Hom, then S_eff, thresholds, detector maps, material/source-worldtube selection, and clock readout must preserve that syntax.",
            "proof_status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "if_signed": "bare-theorem zeros would survive into PPN, clocks, WEP, R10, and orbital readouts",
            "current_gap": "post-variation/readout channels can regenerate finite j_q terms",
        }),
        nonclaim({
            "row_id": "NHVH2760_5_verdict",
            "claim_piece": "derive no hidden-visible Hom from current MTS corpus",
            "formal_statement": "NHVH2760_1 is exact if the parent coefficient functor is signed, but NHVH2760_2 through NHVH2760_4 remain live.",
            "proof_status": "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED",
            "if_signed": "the local q residual vector would lose the largest ordinary coefficient leak",
            "current_gap": "must either derive parent coefficient functor/trivial hidden invariant algebra/readout closure or source finite coupling priors",
        }),
    ]


def build_clause_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "ODC2760_0_parent_object", "clause": "single parent coefficient functor object", "required_statement": "ordinary visible coefficients are generated by one parent map before fitting/readout", "status": "NOT_PARENT_SIGNED", "blocks": "cannot tell theorem-zero from hygiene rule"}),
        nonclaim({"row_id": "ODC2760_1_visible_pullback", "clause": "visible coefficient pullback", "required_statement": "c_i=p_vis^*cbar_i for each EM/mass/clock/source/frame/readout coefficient", "status": "EXACT_CONDITIONAL_ONLY", "blocks": "hidden-visible derivatives remain legal"}),
        nonclaim({"row_id": "ODC2760_2_hidden_invariant_triviality", "clause": "hidden invariant algebra triviality", "required_statement": "O(C_hid)^inv=R or every surviving scalar is no-haired/bounded", "status": "COUNTEREXAMPLE_RETAINED", "blocks": "c_i=c0+epsilon I_hid construction"}),
        nonclaim({"row_id": "ODC2760_3_target_category", "clause": "coefficient target category excludes hidden/source-only targets", "required_statement": "Coeff(O_vis) has no hidden scalar R or source-only R_+ target except common calibration", "status": "TARGET_RULE_NOT_DERIVED", "blocks": "alpha, mass, shadow, and source prefactor channels"}),
        nonclaim({"row_id": "ODC2760_4_common_measure", "clause": "common measure/current owner", "required_statement": "one action/current/source normalization, no species-dependent Jacobian", "status": "COMMON_MEASURE_UNSIGNED", "blocks": "delta_w_A and source-normalization leakage"}),
        nonclaim({"row_id": "ODC2760_5_readout_order", "clause": "variation-before-readout closure", "required_statement": "empirical readout cannot manufacture q source after parent variation", "status": "READOUT_ORDER_UNSIGNED", "blocks": "detector/material/source-worldtube residuals"}),
        nonclaim({"row_id": "ODC2760_6_verdict", "clause": "all operator-domain clauses close", "required_statement": "ODC2760_0 through ODC2760_5 all parent-signed in one branch", "status": "OPERATOR_DOMAIN_NOT_CLOSED", "blocks": "no local-GR/Newton, PPN, WEP, clock, R10, or orbital claim"}),
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CM2760_0_alpha", "surviving_map": "alpha_EM(I_hid)", "j_q_channel": "j_const / EM kinetic", "minimal_counterexample": "f_alpha(I_hid) F_mu_nu F^mu_nu", "needed_to_kill": "alpha owner plus hidden invariant triviality plus radiative closure", "arena_risk": "clocks; WEP; R10; PPN_alpha"}),
        nonclaim({"row_id": "CM2760_1_mass", "surviving_map": "m_A(I_hid), y_A(I_hid), binding_A(I_hid)", "j_q_channel": "j_const / mass and material response", "minimal_counterexample": "m_A(I_hid) psibar_A psi_A", "needed_to_kill": "fixed constant/representation sector or sourced sensitivities", "arena_risk": "WEP; clocks; particle mass ratios"}),
        nonclaim({"row_id": "CM2760_2_source_weight", "surviving_map": "w_A(I_hid) or kappa_A(source_label)", "j_q_channel": "j_weight / source normalization", "minimal_counterexample": "sum_A w_A(I_hid) S_A", "needed_to_kill": "common action measure and source-target exclusion", "arena_risk": "Newton GM; WEP; orbital; R10 source leg"}),
        nonclaim({"row_id": "CM2760_3_shadow_frame", "surviving_map": "A_A(I_hid)^2 g_obs + B_A(I_hid) u_mu u_nu", "j_q_channel": "j_shadow / disformal frame", "minimal_counterexample": "species-dependent conformal/disformal matter frame", "needed_to_kill": "no-shadow domain theorem plus readout closure", "arena_risk": "PPN gamma; preferred frame; clocks"}),
        nonclaim({"row_id": "CM2760_4_readout", "surviving_map": "detector/material/source-worldtube coefficient after variation", "j_q_channel": "j_readout", "minimal_counterexample": "readout map R_i(I_hid,material) multiplying observable current", "needed_to_kill": "variation-before-readout theorem in same parent branch", "arena_risk": "clock calibration; WEP material basis; orbital source selection"}),
        nonclaim({"row_id": "CM2760_5_finite_range", "surviving_map": "K_X(I_hid), lambda_X(I_hid), source/test charges", "j_q_channel": "R10 finite operator leg", "minimal_counterexample": "alpha_X(lambda)=K_X Qbar_XH qbar_XT with hidden-sourced coefficient", "needed_to_kill": "finite operator owner or source-backed alpha(lambda) row", "arena_risk": "R10 short-range bound"}),
    ]


def build_prior_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "FCP2760_0_b_alpha", "symbol": "b_alpha", "sector": "EM_alpha", "definition": "vertical derivative of EM/gauge kinetic coefficient or fine-structure normalization", "units": "dimensionless vertical derivative", "current_status": "THEOREM_ZERO_UNSIGNED; standalone value missing", "best_source_row": "FCR2319_0_clock_product_best is product-only", "missing_for_score": "tau_clock_time, Xhat/chi_X normalization, WEP/R10 source-test projection, alpha owner", "arena_projection": "clock; WEP; R10; PPN_alpha", "score_ready": False}),
        nonclaim({"row_id": "FCP2760_1_b_mu", "symbol": "b_mu", "sector": "mass_ratio", "definition": "vertical derivative of mass ratio / Yukawa / QCD-linked coefficient", "units": "dimensionless vertical derivative", "current_status": "MISSING_SOURCE_BACKED_VALUE", "best_source_row": "none claim-ready in current chain", "missing_for_score": "mass-ratio sensitivities, tau/projection source rows, constant-sector owner", "arena_projection": "clocks; WEP; particle masses", "score_ready": False}),
        nonclaim({"row_id": "FCP2760_2_b_mA_b_nuc", "symbol": "b_mA;b_nuc", "sector": "material_nuclear", "definition": "vertical derivatives of species mass, nuclear binding, and composition response coefficients", "units": "dimensionless vertical derivative", "current_status": "MISSING_SOURCE_BACKED_VALUE", "best_source_row": "delta_w requirements from 2319/1490 are acquisition-only", "missing_for_score": "official material/source response vectors and same-branch tau_eff/readout transfer", "arena_projection": "WEP; Newton source normalization; clocks", "score_ready": False}),
        nonclaim({"row_id": "FCP2760_3_delta_w_A", "symbol": "delta_w_A", "sector": "source_weight", "definition": "relative active-source/action-scale weight after common mode removed", "units": "dimensionless", "current_status": "PREDICTION_MISSING; comparator bounds only", "best_source_row": "FCR2319_2_wep_comparator_bound exists but is not MTS prediction", "missing_for_score": "source/material vectors, tau_eff, readout transfer, no-cancellation group", "arena_projection": "WEP; Newton; R10 source leg; orbital GM", "score_ready": False}),
        nonclaim({"row_id": "FCP2760_4_shadow_frame", "symbol": "a_shadow;b_disformal", "sector": "frame_readout", "definition": "conformal/disformal/source-only frame derivatives entering local metric response", "units": "dimensionless or length^2 by operator normalization", "current_status": "NO_SHADOW_THEOREM_UNSIGNED", "best_source_row": "PPN vector proxy from 2319/2200 is not raw component owner", "missing_for_score": "component owner matrix, stress/source support, readout closure, same-branch normalization", "arena_projection": "PPN gamma/beta/preferred-frame; clocks; WEP", "score_ready": False}),
        nonclaim({"row_id": "FCP2760_5_readout_tau", "symbol": "Delta_tau_readout;tau_eff", "sector": "readout_clock_source", "definition": "post-variation readout/source-worldtube transfer into empirical residual", "units": "arena-dependent transfer factor", "current_status": "READOUT_ORDER_UNSIGNED", "best_source_row": "clock product has yr^-1 bound but not parent tau_clock_time", "missing_for_score": "variation-before-readout proof or source-backed transfer matrix", "arena_projection": "clocks; source normalization; orbital; WEP", "score_ready": False}),
        nonclaim({"row_id": "FCP2760_6_claim_gate", "symbol": "finite_coefficient_prior_gate", "sector": "all", "definition": "row may score only if theorem_zero_status=SIGNED_ZERO or numeric value, uncertainty, source path, projection, and no-cancellation group are real", "units": "guard", "current_status": "ALL_ROWS_NONCLAIM", "best_source_row": "2318 schema plus 2319 first nonclaim source rows", "missing_for_score": "same-branch finite coefficient rows for every surviving j_q leg", "arena_projection": "all local arenas blocked", "score_ready": False}),
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "ARENA2760_0_jq", "arena": "j_q numerator", "effect_if_theorem_signed": "j_const, j_weight, j_shadow, coefficient readout legs can be set to zero without tuning", "current_decision": "NOT_SIGNED_USE_FINITE_PRIORS", "remaining_vector": "j_boundary, j_curvature, q_loc, Q_R, delta_beta, source-normalization, readout tau", "score_ready": False}),
        nonclaim({"row_id": "ARENA2760_1_local_GR", "arena": "local GR/Newton", "effect_if_theorem_signed": "largest hidden-visible coupling leak removed from residual vector", "current_decision": "LOCAL_GR_NOT_CLAIMED", "remaining_vector": "operator-domain unsigned plus q_loc/Q_R/boundary/beta/GM/curvature closures not complete", "score_ready": False}),
        nonclaim({"row_id": "ARENA2760_2_PPN", "arena": "PPN gamma/beta/preferred-frame", "effect_if_theorem_signed": "alpha/mass/shadow/source coefficient channels shrink", "current_decision": "PPN_VECTOR_COMPONENT_RUNNER_REQUIRED", "remaining_vector": "component owner matrix and finite coefficient rows missing", "score_ready": False}),
        nonclaim({"row_id": "ARENA2760_3_WEP_clocks", "arena": "WEP and clocks", "effect_if_theorem_signed": "constant-sector and source-weight derivatives become zero/ill-typed", "current_decision": "CLOCK_PRODUCT_AND_WEP_BOUND_NONCLAIM_ONLY", "remaining_vector": "standalone b_alpha, tau_clock, material vectors, delta_w prediction missing", "score_ready": False}),
        nonclaim({"row_id": "ARENA2760_4_R10", "arena": "R10 short-range", "effect_if_theorem_signed": "hidden EM/source/test coupling channels reduce sharply", "current_decision": "R10_ALPHA_LAMBDA_STILL_BLOCKED", "remaining_vector": "real bound curve plus K_X,Qbar_XH,qbar_XT,lambda_X,source/test projections missing", "score_ready": False}),
        nonclaim({"row_id": "ARENA2760_5_orbital", "arena": "orbital/Newton source normalization", "effect_if_theorem_signed": "species/source hidden weights cannot mimic fitted GM", "current_decision": "ORBITAL_NOT_CLAIMED", "remaining_vector": "observed-GM ownership, source current, boundary/nocharge, readout transfer missing", "score_ready": False}),
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DEC2760_0_conditional_win", "decision": "the conditional no-hidden-visible-Hom theorem is exact", "because": "pullback coefficients have zero vertical derivative", "next_action": "keep theorem as a load-bearing route, not a claim"}),
        nonclaim({"row_id": "DEC2760_1_counterexample", "decision": "the current corpus cannot promote the theorem", "because": "surviving hidden scalars and unsigned target/readout clauses generate legal coefficient maps", "next_action": "do not zero b_alpha, b_mu, delta_w_A, shadow, or readout tau by assertion"}),
        nonclaim({"row_id": "DEC2760_2_coupling_gap", "decision": "the coupling gap is now localized", "because": "the main leak is not the q denominator but the coefficient-domain/source-current numerator", "next_action": "turn every surviving coefficient into a theorem-zero target or finite source-backed prior"}),
        nonclaim({"row_id": "DEC2760_3_best_route", "decision": "finite coefficient prior path is now necessary unless parent coefficient functor closes", "because": "2318/2319 already provide schema and first nonclaim product/proxy rows", "next_action": "build first same-branch coupling product row rather than repeating the functor contract"}),
        nonclaim({"row_id": "DEC2760_4_next", "decision": "NEXT_2761_FIRST_SAME_BRANCH_COUPLING_PRODUCT_ROW", "because": "we need one actual finite coefficient row tied to the local residual vector", "next_action": "try b_alpha*tau_clock normalization or delta_w material/source vector as the first same-branch nonclaim product"}),
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2760_0_sources", "gate": "source paths and needles valid", "passed": True, "claim_effect": "audit reproducible"}),
        nonclaim({"row_id": "CG2760_1_conditional_theorem", "gate": "conditional vertical-silence theorem stated", "passed": True, "claim_effect": "exact derivation route exists under premises"}),
        nonclaim({"row_id": "CG2760_2_parent_functor_signed", "gate": "parent coefficient functor/operator-domain signed", "passed": False, "claim_effect": "no hidden-visible Hom cannot be promoted"}),
        nonclaim({"row_id": "CG2760_3_hidden_scalar_closed", "gate": "hidden invariant scalar obstruction closed", "passed": False, "claim_effect": "counterexample remains live"}),
        nonclaim({"row_id": "CG2760_4_readout_closure", "gate": "effective/readout closure signed", "passed": False, "claim_effect": "bare theorem zeros cannot be safely transferred to tests"}),
        nonclaim({"row_id": "CG2760_5_finite_priors_score_ready", "gate": "finite coefficient priors source-backed and same-branch", "passed": False, "claim_effect": "local empirical scoring remains blocked"}),
        nonclaim({"row_id": "CG2760_6_local_GR_Newton", "gate": "derived local GR/Newton limit", "passed": False, "claim_effect": "no local-GR/Newton claim from 2760"}),
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REF2760_0_claim_theorem", "claim": "2760 derives the no-hidden-visible-Hom theorem", "allowed": False, "reason": "only the pullback lemma is exact; parent functor, hidden scalar triviality, source target, common measure, and readout closure are unsigned", "blocking_rows": "NHVH2760_5_verdict;ODC2760_6_verdict"}),
        nonclaim({"row_id": "REF2760_1_zero_coefficients", "claim": "b_alpha, b_mu, delta_w_A, shadow, and readout coefficients can be set to zero", "allowed": False, "reason": "zero is allowed only under signed theorem-zero rows; current rows are finite prior targets", "blocking_rows": "FCP2760_0_b_alpha;FCP2760_3_delta_w_A;FCP2760_6_claim_gate"}),
        nonclaim({"row_id": "REF2760_2_score_tests", "claim": "R10/PPN/WEP/clock/orbital tests can be scored from 2760", "allowed": False, "reason": "finite coefficient rows are not same-branch numeric predictions and several are still product/proxy/comparator only", "blocking_rows": "ARENA2760_2_PPN;ARENA2760_3_WEP_clocks;ARENA2760_4_R10"}),
        nonclaim({"row_id": "REF2760_3_local_GR", "claim": "MTS derives local GR/Newton after 2760", "allowed": False, "reason": "the coupling leak is narrowed, not closed; q_loc, boundary, beta, source normalization, curvature, and finite coefficient priors remain", "blocking_rows": "ARENA2760_1_local_GR;CG2760_6_local_GR_Newton"}),
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2760_0_2761",
            "next_target": "2761-Y5-R2FR-first-same-branch-coupling-product-row-balpha-clock-or-deltaw-under-AX1090.md",
            "script": "scripts/Y5_R2FR_first_same_branch_coupling_product_row_balpha_clock_or_deltaw_under_AX1090_2761.py",
            "why": "2760 cannot derive the parent operator-domain theorem, so the productive route is one same-branch finite coupling row tied to the local residual vector: either b_alpha*tau_clock with normalization or delta_w material/source vector.",
            "include": "source-backed product rows, branch locks, units, projection, no-cancellation group, refusal gates",
            "exclude": "setting coefficients to zero without theorem, transferring clock products to WEP/R10 without projection, local-GR claim, GitHub, formalization edits",
        })
    ]


def copy_branch_outputs(theorem: list[dict[str, Any]], priors: list[dict[str, Any]], arena: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("BR2760_0_theorem_queue", "theorem", theorem, OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_queue"], "RAB queue for no-hidden-visible-Hom theorem attempt"),
        ("BR2760_1_prior_queue", "priors", priors, OUTPUTS["priors"], BRANCH_OUTPUTS["prior_queue"], "RAB queue for finite coefficient priors"),
        ("BR2760_2_arena_beta", "arena", arena, OUTPUTS["arena"], BRANCH_OUTPUTS["arena_beta"], "beta/PPN/local arena impact"),
        ("BR2760_3_arena_local", "arena", arena, OUTPUTS["arena"], BRANCH_OUTPUTS["arena_local"], "local-bound arena impact"),
        ("BR2760_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for first same-branch coupling product"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "sources":
            continue
        for row in rows:
            value = str(row.get("valid_for_claim", "False")).lower()
            if value == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    theorem = rows_by_name["theorem"]
    clauses = rows_by_name["clauses"]
    countermodels = rows_by_name["countermodels"]
    priors = rows_by_name["priors"]
    arena = rows_by_name["arena"]
    gates = rows_by_name["gates"]
    refusal = rows_by_name["refusal"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2760_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2760_1_theorem_not_promoted", any(row["row_id"] == "NHVH2760_5_verdict" and row["proof_status"] == "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED" for row in theorem), "no-hidden-visible-Hom theorem remains non-promoted"),
        ("VAL2760_2_clause_ledger", any(row["row_id"] == "ODC2760_6_verdict" and row["status"] == "OPERATOR_DOMAIN_NOT_CLOSED" for row in clauses), "operator-domain clause ledger keeps closure blocked"),
        ("VAL2760_3_countermodels", len(countermodels) >= 6 and all("arena_risk" in row for row in countermodels), "major hidden-visible countermodels mapped to j_q channels"),
        ("VAL2760_4_prior_interface", all(any(row["row_id"] == key for row in priors) for key in ["FCP2760_0_b_alpha", "FCP2760_1_b_mu", "FCP2760_2_b_mA_b_nuc", "FCP2760_3_delta_w_A", "FCP2760_4_shadow_frame", "FCP2760_5_readout_tau", "FCP2760_6_claim_gate"]), "finite coefficient prior interface covers required coupling symbols"),
        ("VAL2760_5_arena_blocks", all(str(row["score_ready"]).lower() == "false" for row in arena), "all local arenas remain blocked/nonclaim"),
        ("VAL2760_6_claim_gates_block", any(row["row_id"] == "CG2760_6_local_GR_Newton" and row["passed"] is False for row in gates), "local GR/Newton gate remains blocked"),
        ("VAL2760_7_refusals_block", all(row["allowed"] is False for row in refusal), "refusal runner blocks premature claims"),
        ("VAL2760_8_next", any(row["row_id"] == "NEXT2760_0_2761" and "first-same-branch-coupling-product-row" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL2760_9_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2760_10_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2760_11_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true"),
        ("VAL2760_12_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2760_13_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2760_14_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    overall = all(row["passed"] for row in rows)
    rows.append({
        "validation_id": "VAL2760_OVERALL",
        "passed": overall,
        "detail": "2760 proves the pullback vertical-silence lemma conditionally, refuses no-hidden-visible-Hom promotion because parent coefficient functor/hidden scalar triviality/source target/common measure/readout closure remain unsigned, stages finite coefficient priors for b_alpha, b_mu, b_mA/b_nuc, delta_w_A, shadow-frame and readout tau channels, keeps every local arena nonclaim, and selects a first same-branch coupling product row as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2760 - Y5 R2/f(R): No Hidden-Visible Hom j_q Zero Or Finite Coefficient Prior Under AX1090",
        "## Private Verdict\n\nThe leap was worth taking, but it does not close yet. The exact bit is clean: if every visible coefficient is a pullback from quotient/representation/topology data, then vertical hidden/q motion has zero derivative on that coefficient. That would kill the nastiest coupling leak in `j_q` without tuning.\n\nThe problem is that the parent corpus still has not proved that visible coefficients must be pullbacks. A surviving hidden scalar can still generate `alpha_EM(I_hid)`, `m_A(I_hid)`, source weights, shadow frames, finite-range coefficients, or readout factors. So 2760 keeps the theorem as a conditional weapon and routes the live pieces into finite coefficient priors.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## No Hidden-Visible Hom Theorem Attempt\n\n" + markdown_table(rows_by_name["theorem"], ["row_id", "claim_piece", "formal_statement", "proof_status", "if_signed", "current_gap", "valid_for_claim"]),
        "## Operator-Domain Clause Ledger\n\n" + markdown_table(rows_by_name["clauses"], ["row_id", "clause", "required_statement", "status", "blocks", "valid_for_claim"]),
        "## Countermodel To j_q Map\n\n" + markdown_table(rows_by_name["countermodels"], ["row_id", "surviving_map", "j_q_channel", "minimal_counterexample", "needed_to_kill", "arena_risk", "valid_for_claim"]),
        "## Finite Coefficient Prior Interface\n\n" + markdown_table(rows_by_name["priors"], ["row_id", "symbol", "sector", "definition", "units", "current_status", "best_source_row", "missing_for_score", "arena_projection", "score_ready", "valid_for_claim"]),
        "## Arena Impact\n\n" + markdown_table(rows_by_name["arena"], ["row_id", "arena", "effect_if_theorem_signed", "current_decision", "remaining_vector", "score_ready", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decisions"], ["row_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "## Refusal Runner\n\n" + markdown_table(rows_by_name["refusal"], ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is a good narrowing, not a win lap. The coupling gap is now named with teeth: either the parent action proves coefficient-domain silence, or the theory must carry finite source-backed priors into every local test. The next best shot is not another abstract restatement; it is one same-branch finite coupling product row, probably `b_alpha*tau_clock_time` if we can normalize the parent tau, or `delta_w_A` if we can build the material/source vector.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    theorem = build_theorem_rows()
    clauses = build_clause_rows()
    countermodels = build_countermodel_rows()
    priors = build_prior_rows()
    arena = build_arena_rows()
    decisions = build_decision_rows()
    gates = build_gate_rows()
    refusal = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["clauses"], clauses)
    write_csv(OUTPUTS["countermodels"], countermodels)
    write_csv(OUTPUTS["priors"], priors)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(theorem, priors, arena, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "theorem": theorem,
        "clauses": clauses,
        "countermodels": countermodels,
        "priors": priors,
        "arena": arena,
        "decisions": decisions,
        "gates": gates,
        "refusal": refusal,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2760_OVERALL")
    print(f"2760 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

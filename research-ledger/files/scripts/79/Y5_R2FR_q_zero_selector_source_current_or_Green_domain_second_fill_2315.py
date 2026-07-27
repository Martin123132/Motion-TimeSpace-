from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_Q_ZERO_SELECTOR_OR_GREEN_DOMAIN_SECOND_FILL_2315"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2315-Y5-R2FR-q-zero-selector-source-current-or-Green-domain-second-fill.md"

PATHS = {
    "2314_doc": ROOT / "2314-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill.md",
    "2314_validation": OUT / "P8_Y5_BRR545_2314_VALIDATION.csv",
    "2314_first_fill": OUT / "P8_Y5_PARENT_QLOC_2314_FIRST_FILL_ROWS.csv",
    "2314_green": OUT / "P8_Y5_PARENT_QLOC_2314_GREEN_FUNCTION_NORMALIZATION_CONTRACT.csv",
    "2314_runner": OUT / "P8_Y5_PARENT_QLOC_2314_BOUND_RUNNER_UPDATE.csv",
    "2283_doc": ROOT / "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md",
    "2283_validation": OUT / "P8_Y5_BRR545_2283_VALIDATION.csv",
    "2283_owner": OUT / "P8_Y5_PARENT_QLOC_2283_RADIAL_CELL_OWNER_AUDIT.csv",
    "2283_finite": OUT / "P8_Y5_PARENT_QLOC_2283_FINITE_Q_RESIDUAL_INTAKE_CONTRACT.csv",
    "2284_doc": ROOT / "2284-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md",
    "2284_formula": OUT / "P8_Y5_PARENT_QLOC_2284_Q_RESIDUAL_FORMULA_LEDGER.csv",
    "2285_doc": ROOT / "2285-Y5-R2FR-finite-q-PPN-R10-projection-matrix-or-input-source-pack.md",
    "2285_state": OUT / "P8_Y5_PARENT_QLOC_2285_POBS_STATE_VECTOR.csv",
    "2285_projection": OUT / "P8_Y5_PARENT_QLOC_2285_PROJECTION_MATRIX_NONCLAIM.csv",
    "2285_pack": OUT / "P8_Y5_PARENT_QLOC_2285_COEFFICIENT_SOURCE_PACK.csv",
    "2296_nohair": OUT / "P8_Y5_PARENT_QLOC_2296_Q_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "2306_weyl": OUT / "P8_Y5_PARENT_QLOC_2306_SCHWARZSCHILD_WEYL2_PROJECTION_LAW.csv",
    "2308_coeff": OUT / "P8_Y5_PARENT_QLOC_2308_DQWEYL2_PARENT_COEFFICIENT_AUDIT.csv",
}

SOURCES = [
    ("SRC2315_00_2314_doc", "2314_doc", PATHS["2314_doc"], ["NEXT2314_0", "lambda_q=sqrt"], "2314 handoff: q operator partial fill and next target"),
    ("SRC2315_01_2314_validation", "2314_validation", PATHS["2314_validation"], ["VAL2314_OVERALL", "PASS"], "2314 validation"),
    ("SRC2315_02_2314_first_fill", "2314_first_fill", PATHS["2314_first_fill"], ["FF2314_2_lambda", "lambda_q = sqrt"], "machine-readable lambda_q=xi_q first fill"),
    ("SRC2315_03_2314_green", "2314_green", PATHS["2314_green"], ["GF2314_1_covariance_range", "lambda_q=xi_q"], "Green-domain normalization contract"),
    ("SRC2315_04_2314_runner", "2314_runner", PATHS["2314_runner"], ["RUN2314_6_score_gate", "CLAIM_AND_SCORE_BLOCKED"], "runner still blocked"),
    ("SRC2315_05_2283_doc", "2283_doc", PATHS["2283_doc"], ["NO_CURRENT_PARENT_OWNER_FOR_JQ_EQUALS_ONE", "finite residual physics"], "source-current selector exhaustion"),
    ("SRC2315_06_2283_validation", "2283_validation", PATHS["2283_validation"], ["VAL2283_OVERALL", "PASS"], "2283 validation"),
    ("SRC2315_07_2283_owner", "2283_owner", PATHS["2283_owner"], ["RCO2283_1_ordinary_current", "REJECTED_NO_CHARGE_OBSTRUCTION"], "radial cell source-current audit"),
    ("SRC2315_08_2283_finite", "2283_finite", PATHS["2283_finite"], ["FQI2283_1_jq", "MISSING_PARENT_SOURCE_COEFFICIENT"], "finite q numerator/source input gap"),
    ("SRC2315_09_2284_doc", "2284_doc", PATHS["2284_doc"], ["q_R=j_q/M_q^2", "MISSING_PARENT_SOURCE_COEFFICIENT"], "finite residual formula handoff"),
    ("SRC2315_10_2284_formula", "2284_formula", PATHS["2284_formula"], ["QRF2284_0_algebraic_parent_block", "q_R=j_q/M_q^2"], "algebraic q residual formula"),
    ("SRC2315_11_2285_doc", "2285_doc", PATHS["2285_doc"], ["gamma-1 = q_R", "P_obs projection matrix"], "projection matrix handoff"),
    ("SRC2315_12_2285_state", "2285_state", PATHS["2285_state"], ["STATE2285_2_lambda_q", "MISSING_OPERATOR_RANGE_INPUTS"], "pre-2315 state vector range gap"),
    ("SRC2315_13_2285_projection", "2285_projection", PATHS["2285_projection"], ["POBS2285_0_gamma", "gamma_minus_1 = 1*q_R"], "PPN projection matrix"),
    ("SRC2315_14_2285_pack", "2285_pack", PATHS["2285_pack"], ["PACK2285_0_qR", "MISSING_PARENT_COEFFICIENTS"], "coefficient source pack"),
    ("SRC2315_15_2296_nohair", "2296_nohair", PATHS["2296_nohair"], ["NH2296_3_zero_theorem", "CONDITIONAL_THEOREM_PROVED_PREMISES_UNSIGNED"], "conditional no-hair theorem"),
    ("SRC2315_16_2306_weyl", "2306_weyl", PATHS["2306_weyl"], ["PROJ2306_0_schwarzschild_identity", "EXACT_BACKGROUND_IDENTITY"], "Weyl2 background kernel"),
    ("SRC2315_17_2308_coeff", "2308_coeff", PATHS["2308_coeff"], ["DCO2308_3_verdict", "COEFFICIENT_UNSOURCED"], "curvature coefficient still missing"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2315_SOURCE_REGISTER.csv",
    "selector": OUT / "P8_Y5_PARENT_QLOC_2315_SELECTOR_REENTRY_AUDIT.csv",
    "green": OUT / "P8_Y5_PARENT_QLOC_2315_GREEN_DOMAIN_SECOND_FILL.csv",
    "formula": OUT / "P8_Y5_PARENT_QLOC_2315_FINITE_RESIDUAL_FORMULA_UPDATE.csv",
    "arena": OUT / "P8_Y5_PARENT_QLOC_2315_ARENA_READINESS_UPDATE.csv",
    "zero": OUT / "P8_Y5_PARENT_QLOC_2315_ZERO_THEOREM_LADDER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2315_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2315_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2315_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2315_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2315_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2315_0_selector", OUTPUTS["selector"], RAB_QUEUE / "JR2315_Q_ZERO_SELECTOR_REENTRY_AUDIT_NONCLAIM.csv"),
    ("COPY2315_1_green", OUTPUTS["green"], BETA_DOCS / "Q_GREEN_DOMAIN_SECOND_FILL_2315_NONCLAIM.csv"),
    ("COPY2315_2_formula", OUTPUTS["formula"], RAB_QUEUE / "JR2315_FINITE_RESIDUAL_FORMULA_UPDATE_NONCLAIM.csv"),
    ("COPY2315_3_arena", OUTPUTS["arena"], MICRO_RESIDUALS / "q_green_domain_arena_readiness_nonclaim_2315.csv"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        ok, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needles": ";".join(needles),
                "needles_found": b(ok),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_selector_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEL2315_0_identity",
            "selector_route": "q=0 / J_q=1 / R_AB=0 identity",
            "status": "EXACT_TARGET_IDENTITY_ONLY",
            "evidence": "2282 and 2283 identify q=0 iff T^2S=1 iff R_AB=0 and J_q=1, but identity is not dynamics.",
            "decision": "retain as target/closure benchmark only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEL2315_1_ordinary_current",
            "selector_route": "conserved radial source/current",
            "status": "REJECTED_BY_EXISTING_NO_CHARGE_OBSTRUCTION",
            "evidence": "2283 RCO2283_1: partial_r(W partial_r R_AB)=0 gives W R_AB'=Q_R, so Q_R hair survives unless a no-charge theorem is added.",
            "decision": "do not loop this route without new parent no-charge evidence",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEL2315_2_topological_no_charge",
            "selector_route": "topological/source representation zero charge",
            "status": "POSSIBLE_BUT_UNSUPPLIED",
            "evidence": "2283 RCO2283_2 leaves Q_R=0 as future contract only; no cohomology/source representation is present.",
            "decision": "eligible re-entry only if a concrete source-current theorem appears",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEL2315_3_first_class_or_psi",
            "selector_route": "first-class/gauge or psi quotient",
            "status": "CONTRACT_ONLY_NOT_PRESENT",
            "evidence": "2283 RCO2283_4/RCO2283_6 require generator, bracket, degree count, matter descent, or psi covariance quotient; current corpus does not supply them.",
            "decision": "keep closure label and finite-residual branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEL2315_4_verdict",
            "selector_route": "q-zero selector source/current re-entry",
            "status": "NO_NEW_SELECTOR_SOURCE_FOUND_USE_GREEN_DOMAIN_FILL",
            "evidence": "2315 finds no post-2283 source-current theorem; 2314 provides new operator/range structure instead.",
            "decision": "advance Green-domain and numerator/source-zero work; do not claim derived local GR",
            "valid_for_claim": "false",
        },
    ]


def build_green_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "GD2315_0_massive_kernel",
            "domain_piece": "massive covariance-Hessian branch",
            "formula": "L_q=-Z_q Delta+M_q^2, G_q(r)=exp(-r/xi_q)/(4*pi*Z_q*r) when Z_q=xi_q^2 M_q^2",
            "new_fill": "lambda_q is promoted from missing range input to exact conditional lambda_q=xi_q",
            "missing_for_score": "xi_q numeric/source; Z_q normalization; source vector S_q; boundary/domain; P_obs",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GD2315_1_compact_source_profile",
            "domain_piece": "compact source Green response",
            "formula": "q(x)=integral_D G_q(x,x') S_q(x') dV'; far field scales as Q_q^eff exp(-r/xi_q)/(4*pi Z_q r)",
            "new_fill": "profile shape is determined once xi_q and the effective source charge are parent-owned",
            "missing_for_score": "Q_q^eff from D_qWeyl2 C^2, J_q, boundary_tail with no-cancellation envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GD2315_2_algebraic_limit",
            "domain_piece": "algebraic/auxiliary limit",
            "formula": "if Z_q=0, q=S_q/M_q^2 and q_R=j_q/M_q^2 for weak-field source J_q=j_q L+O(L^2)",
            "new_fill": "using 2314 M_q^2=n_q H n_q gives q_R=j_q/(n_q H n_q) if the same branch is sourced",
            "missing_for_score": "j_q source leg, H_AB value, q normalization, source-normalization guard",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GD2315_3_boundary_hair",
            "domain_piece": "boundary/hair branch",
            "formula": "if reciprocal boundary momentum survives, R_AB has Q_R/r or Yukawa-tail hair depending on Z_q,M_q^2",
            "new_fill": "hair is now an explicit separate source channel, not hidden inside q=0 closure",
            "missing_for_score": "boundary variational class, Pi_R/Q_R source theorem or bound",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GD2315_4_closure_control",
            "domain_piece": "explicit q=0 closure benchmark",
            "formula": "q=0 remains a runnable regression control only",
            "new_fill": "closure control is separated from Green-domain finite residual predictions",
            "missing_for_score": "not scoreable as derivation; use only as labelled benchmark",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_formula_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FORM2315_0_Mq2",
            "quantity": "M_q^2",
            "formula": "M_q^2=n_q^A H_AB n_q^B",
            "source_basis": "2314 import of 2281 transverse Hessian",
            "upgrade_from": "missing parent Hessian",
            "remaining_gap": "H_AB and q=0 selector not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FORM2315_1_Zq",
            "quantity": "Z_q",
            "formula": "Z_q=xi_q^2 n_q^A H_AB n_q^B",
            "source_basis": "2314 import of 2281 finite smoothing expansion",
            "upgrade_from": "missing range operator input",
            "remaining_gap": "xi_q/smoothing kernel not source-backed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FORM2315_2_qR",
            "quantity": "q_R",
            "formula": "q_R=j_q/M_q^2=j_q/(n_q^A H_AB n_q^B)",
            "source_basis": "2284 q_R ratio plus 2314 M_q^2 fill",
            "upgrade_from": "ratio known but denominator blank",
            "remaining_gap": "j_q numerator/source leg is still missing; denominator not numeric",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FORM2315_3_zero_condition",
            "quantity": "q_R=0",
            "formula": "if M_q^2>0 and j_q=0 in the same normalization, then q_R=0",
            "source_basis": "algebraic residual formula",
            "upgrade_from": "vague finite residual zero condition",
            "remaining_gap": "need parent source-current/matter-descent theorem for j_q=0",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FORM2315_4_R10_range",
            "quantity": "R10 lambda input",
            "formula": "lambda_R10 = xi_q for the massive covariance-Hessian q branch",
            "source_basis": "2314 lambda_q=xi_q",
            "upgrade_from": "STATE2285_2_lambda_q MISSING_OPERATOR_RANGE_INPUTS",
            "remaining_gap": "R10 coupling K_q Qbar_qH qbar_qT and xi_q numeric/source still missing",
            "valid_for_claim": "false",
        },
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2315_0_PPN_gamma",
            "arena": "PPN gamma/light/Shapiro",
            "updated_input": "gamma-1=q_R=j_q/(nHn) plus retained source/q_loc channels",
            "improvement": "operator denominator now has conditional formula",
            "still_blocked_by": "j_q, source normalization, q_loc projection",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2315_1_PPN_beta_orbital",
            "arena": "PPN beta/perihelion/orbital",
            "updated_input": "perihelion keeps q_R and delta_beta channels; q_R denominator can be nHn conditionally",
            "improvement": "finite q channel is less foggy",
            "still_blocked_by": "delta_beta parent weak-field completion and Newton/source normalization",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2315_2_R10",
            "arena": "R10 short-range alpha(lambda)",
            "updated_input": "lambda_q=xi_q conditionally; alpha_q(lambda)=K_q Qbar_qH qbar_qT remains symbolic",
            "improvement": "range owner is narrowed to parent smoothing/correlation length",
            "still_blocked_by": "xi_q numeric/source, K_q, Qbar/qbar couplings, real bound curve/comparator",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2315_3_clocks_WEP",
            "arena": "clocks/WEP/matter",
            "updated_input": "matter q-source numerator j_q is now the highest-value zero theorem target",
            "improvement": "clear numerator-denominator split",
            "still_blocked_by": "matter/coframe descent and universal source-current theorem",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2315_4_boundary_force",
            "arena": "q_loc/boundary/local force residual",
            "updated_input": "boundary hair and q_loc remain separate residual channels",
            "improvement": "prevents hiding Q_R/q_loc inside the closure branch",
            "still_blocked_by": "boundary no-flux, Gamma/Khat action route, Helmholtz/metric response",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2315_0_selector",
            "target_zero": "q=0 from parent selector",
            "sufficient_conditions": "first-class/psi quotient or no-charge current theorem selects R_AB=0 before readout",
            "current_status": "BLOCKED_BY_2283_NO_OWNER",
            "next_best_attack": "do not loop unless new parent theorem appears",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2315_1_source_numerator",
            "target_zero": "j_q=0",
            "sufficient_conditions": "matter/source/current descent has no q numerator in the same observed coframe",
            "current_status": "OPEN_HIGHEST_VALUE_TARGET",
            "next_best_attack": "derive j_q source-leg zero or stage finite source pack",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2315_2_boundary_hair",
            "target_zero": "Q_R=0 / boundary q hair zero",
            "sufficient_conditions": "no-gradient/no-boundary-momentum theorem or source reciprocal neutrality",
            "current_status": "OPEN_BOUNDARY_TARGET",
            "next_best_attack": "pair with j_q source-leg proof; otherwise bound Q_R separately",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2315_3_curvature_source",
            "target_zero": "D_qWeyl2=0 or bounded",
            "sufficient_conditions": "no higher-curvature tower theorem or source-backed coefficient below bounds",
            "current_status": "OPEN_COEFFICIENT_TARGET",
            "next_best_attack": "do after j_q/Green-domain source channel or in parallel with R10",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2315_4_local_GR_Newton",
            "target_zero": "local GR/Newton residual vector",
            "sufficient_conditions": "selector or finite residual zeros plus source normalization and beta completion",
            "current_status": "NOT_DERIVED",
            "next_best_attack": "derive numerator/source zero first, then beta/source normalization",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2315_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2315_1_selector_reentry", "gate": "new source-current selector found", "passed": "false", "claim_effect": "q=0 remains closure/target, not parent theorem", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2315_2_green_domain_fill", "gate": "Green-domain second fill written", "passed": "true", "claim_effect": "workflow improves but remains nonclaim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2315_3_qR_parent_prediction", "gate": "q_R parent-predicted or theorem-zero", "passed": "false", "claim_effect": "PPN/local scoring blocked", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2315_4_R10_score_ready", "gate": "R10 range/coupling/projection ready", "passed": "false", "claim_effect": "R10 scoring blocked", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2315_5_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "still a target", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2315_0_reloop_current", "claim": "ordinary conserved radial current derives q=0", "allowed": "false", "reason": "2283 already rejected this route because Q_R hair survives", "blocking_rows": "SEL2315_1_ordinary_current", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2315_1_claim_lambda_numeric", "claim": "lambda_q=xi_q is a numeric R10 prediction", "allowed": "false", "reason": "xi_q is not sourced numerically and couplings/projection are missing", "blocking_rows": "ARENA2315_2_R10", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2315_2_score_ppn", "claim": "PPN/local tests can be scored now", "allowed": "false", "reason": "q_R numerator j_q and source-normalization channels remain missing", "blocking_rows": "FORM2315_2_qR;ARENA2315_0_PPN_gamma", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2315_3_local_gr", "claim": "MTS derives local GR/Newton after Green-domain fill", "allowed": "false", "reason": "Green-domain fill is a residual workflow, not a selector/source-zero theorem", "blocking_rows": "CG2315_5_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2315_0",
            "next_target": "2316-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md",
            "why": "after 2315, q_R=j_q/(nHn) is the cleanest local-residual formula; the numerator j_q is now the highest-value derivation target for local GR/PPN progress",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "row_count": len(read_csv_rows(dst)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    selector_rows: list[dict[str, Any]],
    green_rows: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, selector_rows, green_rows, formula_rows, arena_rows, zero_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    formalization_output_markers = (
        "2315-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2315",
        "P8_Y5_BRR545_2315",
        "JR2315_",
        "Q_GREEN_DOMAIN_SECOND_FILL_2315",
        "q_green_domain_arena_readiness_nonclaim_2315",
        "Y5_R2FR_q_zero_selector_source_current_or_Green_domain_second_fill_2315",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2315_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2315_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2315_02_selector_reentry_blocked", any(row["row_id"] == "SEL2315_4_verdict" and row["status"] == "NO_NEW_SELECTOR_SOURCE_FOUND_USE_GREEN_DOMAIN_FILL" for row in selector_rows), "selector/current re-entry is blocked by existing evidence"))
    checks.append(("VAL2315_03_green_domain_written", any(row["row_id"] == "GD2315_0_massive_kernel" and "lambda_q is promoted" in row["new_fill"] for row in green_rows), "Green-domain second fill records lambda_q=xi_q"))
    checks.append(("VAL2315_04_qR_formula_updated", any(row["row_id"] == "FORM2315_2_qR" and "j_q/(n_q^A H_AB n_q^B)" in row["formula"] for row in formula_rows), "q_R numerator/denominator formula updated"))
    checks.append(("VAL2315_05_R10_range_updated", any(row["row_id"] == "FORM2315_4_R10_range" and "xi_q" in row["formula"] for row in formula_rows), "R10 range input updated conditionally"))
    checks.append(("VAL2315_06_arena_blocks_preserved", all(row["score_ready"] == "false" for row in arena_rows), "all arena rows remain blocked/nonclaim"))
    checks.append(("VAL2315_07_zero_ladder", {"ZERO2315_1_source_numerator", "ZERO2315_2_boundary_hair", "ZERO2315_3_curvature_source"}.issubset({row["row_id"] for row in zero_rows}), "zero theorem ladder includes numerator, boundary, and curvature targets"))
    checks.append(("VAL2315_08_claims_blocked", any(row["row_id"] == "CG2315_5_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2315_09_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2315_10_next_target", any(row["row_id"] == "NEXT2315_0" and "2316-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md" in row["next_target"] for row in next_rows), "next target selected"))
    checks.append(("VAL2315_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2315_12_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2315_13_formalization_untouched_by_2315", len(formalization_hits) == 0, "no 2315 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2315_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2315 refuses to re-loop the source-current selector without new evidence, uses the 2314 lambda_q=xi_q result to fill the Green-domain/range lane conditionally, updates q_R to j_q/(nHn), keeps all arena scores blocked, and selects the j_q source-leg zero theorem as the next derivation target.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    selector_rows: list[dict[str, Any]],
    green_rows: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2315 - q-Zero Selector Source Current Or Green-Domain Second Fill",
        "",
        "## Summary",
        "",
        "2315 makes a deliberate route choice. The source-current selector for `q=0` was already audited in 2283: ordinary conservation leaves `Q_R` hair, and no parent no-charge/cohomology/first-class/psi-quotient theorem has appeared since. So this checkpoint refuses to re-loop that proof without new evidence.",
        "",
        "The forward gain comes from 2314. Since the conditional q Hessian gives `M_q^2=n_q H n_q`, `Z_q=xi_q^2 n_q H n_q`, and therefore `lambda_q=xi_q`, the Green-domain branch can now be written more sharply. The finite scalar residual becomes `q_R=j_q/(n_q H n_q)` on the same branch.",
        "",
        "That is not a local-GR claim. It is a cleaner target. The denominator has a conditional owner; the numerator `j_q` is now the highest-value derivation problem. If `j_q=0` and boundary hair/source-normalization channels also close, the local branch gets much closer to GR. If `j_q` is finite, it becomes a real residual to test.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Selector Re-Entry Audit",
        "",
        md_table(selector_rows, ["row_id", "selector_route", "status", "evidence", "decision", "valid_for_claim"]),
        "",
        "## Green-Domain Second Fill",
        "",
        md_table(green_rows, ["row_id", "domain_piece", "formula", "new_fill", "missing_for_score", "score_ready", "valid_for_claim"]),
        "",
        "## Finite Residual Formula Update",
        "",
        md_table(formula_rows, ["row_id", "quantity", "formula", "source_basis", "upgrade_from", "remaining_gap", "valid_for_claim"]),
        "",
        "## Arena Readiness Update",
        "",
        md_table(arena_rows, ["row_id", "arena", "updated_input", "improvement", "still_blocked_by", "score_ready", "valid_for_claim"]),
        "",
        "## Zero Theorem Ladder",
        "",
        md_table(zero_rows, ["row_id", "target_zero", "sufficient_conditions", "current_status", "next_best_attack", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = build_sources()
    selector_rows = build_selector_rows()
    green_rows = build_green_rows()
    formula_rows = build_formula_rows()
    arena_rows = build_arena_rows()
    zero_rows = build_zero_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["selector"], selector_rows)
    write_csv(OUTPUTS["green"], green_rows)
    write_csv(OUTPUTS["formula"], formula_rows)
    write_csv(OUTPUTS["arena"], arena_rows)
    write_csv(OUTPUTS["zero"], zero_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        selector_rows,
        green_rows,
        formula_rows,
        arena_rows,
        zero_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        selector_rows,
        green_rows,
        formula_rows,
        arena_rows,
        zero_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2315_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3223-Y5-R2FR-RQ-source-search-or-finite-alpha-runner-smoke-inputs-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3223_INPUTS.csv"
SEARCH = OUT / "P8_Y5_R2FR_3223_RQ_SOURCE_SEARCH.csv"
SCORE = OUT / "P8_Y5_R2FR_3223_RQ_CANDIDATE_SCORECARD.csv"
FORMULA = OUT / "P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv"
SMOKE = OUT / "P8_Y5_R2FR_3223_FINITE_ALPHA_SMOKE_INPUTS.csv"
RUNNER = OUT / "P8_Y5_R2FR_3223_ALPHA_SMOKE_RUNNER_RESULTS.csv"
DECISION = OUT / "P8_Y5_R2FR_3223_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3223_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def evidence(path: Path, terms: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:200]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3223_00_3222_doc",
        "location": "post_checkpoint",
        "relative_path": "3222-Y5-R2FR-defect-norm-parent-action-contract-or-finite-alpha-coefficient-runner-under-AX1090.md",
        "role": "3222 handoff and RQ target list",
        "terms": ["R_Z", "R_W", "R_H", "DEFECT_NORM_PARENT_ACTION_CONTRACT"],
    },
    {
        "input_id": "SRC3223_01_3222_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3222_PARENT_ACTION_DEFECT_NORM_CONTRACT.csv",
        "role": "parent-action defect-norm contract clauses",
        "terms": ["DNC3222_0_parent_object", "DNC3222_1_action_term", "DNC3222_7_verdict"],
    },
    {
        "input_id": "SRC3223_02_3222_candidates",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3222_RQ_CANDIDATE_ROUTES.csv",
        "role": "RQ candidate definitions",
        "terms": ["RQ3222_0_Ward_current_mismatch", "RQ3222_2_Hodge_descent_defect", "RQ3222_3_Maxwell_subblock_residual"],
    },
    {
        "input_id": "SRC3223_03_3222_runner",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3222_FINITE_ALPHA_RUNNER_SPEC.csv",
        "role": "finite alpha runner handoff",
        "terms": ["AR3222_0_theorem_zero_switch", "AR3222_5_arena_projection"],
    },
    {
        "input_id": "SRC3223_04_3218_ZA",
        "location": "post_checkpoint",
        "relative_path": "3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md",
        "role": "Z_A decomposition and countermodels",
        "terms": ["Z_A =", "C_P N_Q", "lambda_A", "f_m(m)"],
    },
    {
        "input_id": "SRC3223_05_3219_bound",
        "location": "post_checkpoint",
        "relative_path": "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md",
        "role": "off-root b_alpha and Hessian guard",
        "terms": ["ORB3219_0_balpha_offroot", "G_eff", "HES3219_1_coercivity_floor"],
    },
    {
        "input_id": "SRC3223_06_1055_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "role": "single parent action and EM owner contract",
        "terms": ["PAC1055_1_EM_owner", "PAC1055_5_radiative_readout_closure", "PAC1055_6_single_parent_action"],
    },
    {
        "input_id": "SRC3223_07_642_descent",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "role": "Maxwell descent and current status",
        "terms": ["MD642_1_Gauss_Ampere", "MD642_2_current_conservation", "MD642_4_alpha_constant"],
    },
    {
        "input_id": "SRC3223_08_765_mki",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "role": "Maxwell kinetic inheritance gates",
        "terms": ["MKI765_1_norm", "MKI765_2_unique_F2", "MKI765_4_readout", "MKI765_5_total"],
    },
    {
        "input_id": "SRC3223_09_988_emlock",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
        "role": "EM lock/readout theorem gates",
        "terms": ["EMLOCK988_1_unique_Maxwell_F2", "EMLOCK988_3_readout_descent", "EMLOCK988_5_theorem_verdict"],
    },
    {
        "input_id": "SRC3223_10_1057_unique",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "role": "unique Maxwell subblock",
        "terms": ["UMS1057_0_target", "UMS1057_2_no_independent_F2", "UMS1057_5_verdict"],
    },
    {
        "input_id": "SRC3223_11_1058_domain",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
        "role": "operator-domain exhaustion",
        "terms": ["VOE1058_0_target", "VOE1058_3_no_hidden_visible_hom", "VOE1058_5_verdict"],
    },
    {
        "input_id": "SRC3223_12_1091_domain",
        "location": "post_checkpoint",
        "relative_path": "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md",
        "role": "scalar obstruction and finite b_alpha route",
        "terms": ["ODH1091_2_scalar_obstruction", "FR1091_0_b_alpha", "ODH1091_6_verdict"],
    },
    {
        "input_id": "SRC3223_13_459B_phase",
        "location": "post_checkpoint",
        "relative_path": "459B-Andersen-charge-amplitude-phase-current-gate.md",
        "role": "phase-current conservation route",
        "terms": ["PC1_conserved_current", "PC4_Maxwell_limit", "theta_Q", "J_Q"],
    },
    {
        "input_id": "SRC3223_14_287_current",
        "location": "post_checkpoint",
        "relative_path": "287-boundary-current-charge-owner-attempt.md",
        "role": "relative boundary current",
        "terms": ["d_rel J_B", "Q_B", "No promotion yet"],
    },
    {
        "input_id": "SRC3223_15_288_level",
        "location": "post_checkpoint",
        "relative_path": "288-k9-Ward-index-level-attempt.md",
        "role": "level/index obstruction",
        "terms": ["rank is not a Ward identity", "Q_*", "integral periods"],
    },
    {
        "input_id": "SRC3223_16_alpha_clock",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "clock alpha product source anchor",
        "terms": ["alpha", "clock", "yr", "ACB1052"],
    },
    {
        "input_id": "SRC3223_17_alpha_WEP",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
        "role": "WEP alpha projection anchor",
        "terms": ["alpha", "WEP", "AWP1052", "Coulomb"],
    },
    {
        "input_id": "SRC3223_18_alpha_R10",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv",
        "role": "R10 alpha projection anchor",
        "terms": ["alpha", "R10", "RAP1052", "product"],
    },
]


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    evidence_by_id: dict[str, str] = {}
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        hit_text = evidence(path, source["terms"])
        evidence_by_id[source["input_id"]] = hit_text
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": hit_text,
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    search_rows = [
        {
            "search_id": "SRCSEARCH3223_RZ",
            "candidate": "R_Z = Z_A - C_P N_Q or unique Maxwell-subblock projection residual",
            "searched_sources": "3218;1055;765;988;1057;1058;1091",
            "positive_hits": "Z_A decomposition; EM owner contract; Maxwell kinetic inheritance; unique subblock target",
            "blocking_hits": "unique F2/operator-domain/readout clauses remain not derived; scalar f(I)F_Q^2 countermodel survives",
            "best_evidence": evidence_by_id["SRC3223_04_3218_ZA"] + " || " + evidence_by_id["SRC3223_10_1057_unique"],
            "source_signed": "false",
            "result": "RZ_TEMPLATE_FOUND_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "search_id": "SRCSEARCH3223_RW",
            "candidate": "R_W^nu = nabla_mu(Z_*F_Q^{mu nu}) - J_Q^nu",
            "searched_sources": "642;1055;459B;287;990/EM-lock gates through 3222",
            "positive_hits": "Maxwell equation closure and current conservation support exist",
            "blocking_hits": "current owner/source normalization and alpha kinetic coefficient are unsigned",
            "best_evidence": evidence_by_id["SRC3223_07_642_descent"] + " || " + evidence_by_id["SRC3223_13_459B_phase"],
            "source_signed": "false",
            "result": "RW_CURRENT_SUPPORT_NOT_KINETIC_OWNER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "search_id": "SRCSEARCH3223_RH",
            "candidate": "R_H = Hodge/coframe/readout descent residual",
            "searched_sources": "988;765;3222;3219",
            "positive_hits": "readout/Hodge channel is named and guarded",
            "blocking_hits": "observed Hodge/readout descent remains not parent-signed; Poynting channel remains separate",
            "best_evidence": evidence_by_id["SRC3223_09_988_emlock"] + " || " + evidence_by_id["SRC3223_08_765_mki"],
            "source_signed": "false",
            "result": "RH_STRESS_READOUT_GUARD_FOUND_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "search_id": "SRCSEARCH3223_RTHETA",
            "candidate": "R_theta = d_rel J_B or nabla_mu J_Q^mu",
            "searched_sources": "459B;287;288;642",
            "positive_hits": "relative/phase-current conservation support exists",
            "blocking_hits": "charge unit/level and Maxwell kinetic coefficient ownership are not derived",
            "best_evidence": evidence_by_id["SRC3223_14_287_current"] + " || " + evidence_by_id["SRC3223_15_288_level"],
            "source_signed": "false",
            "result": "RTHETA_CONSERVATION_SUPPORT_NOT_ALPHA_OWNER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "search_id": "SRCSEARCH3223_VERDICT",
            "candidate": "promote a source-signed R_Q",
            "searched_sources": "bounded source set from 3222 candidate list",
            "positive_hits": "several templates and conditional contracts exist",
            "blocking_hits": "no row supplies parent object + EM coefficient attachment + same-branch root + Hessian/stress/readout closure",
            "best_evidence": "all candidate rows remain nonclaim",
            "source_signed": "false",
            "result": "NO_RQ_SOURCE_SIGNED_BUILD_FINITE_ALPHA_SMOKE_INPUTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    score_rows = [
        {
            "candidate_id": "SCORE3223_RZ",
            "candidate": "R_Z coefficient residual",
            "parent_object": "partial",
            "coefficient_attachment": "best",
            "same_branch_root": "missing",
            "hessian_bound": "missing",
            "stress_readout": "missing",
            "overall": "best_alpha_owner_target_not_signed",
            "next_use": "first target if one more source hunt is attempted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "SCORE3223_RW",
            "candidate": "R_W Ward-current mismatch",
            "parent_object": "partial",
            "coefficient_attachment": "weak",
            "same_branch_root": "conditional",
            "hessian_bound": "missing",
            "stress_readout": "partial_current_only",
            "overall": "use_as_Maxwell_current_guard_not_alpha_owner",
            "next_use": "second-lane guard after R_Z",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "SCORE3223_RH",
            "candidate": "R_H Hodge/readout residual",
            "parent_object": "missing",
            "coefficient_attachment": "readout_only",
            "same_branch_root": "missing",
            "hessian_bound": "missing",
            "stress_readout": "best_stress_guard_target",
            "overall": "needed_for_Poynting_not_alpha_zero",
            "next_use": "stress/readout residual lane",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "SCORE3223_RTHETA",
            "candidate": "R_theta phase-current conservation",
            "parent_object": "partial",
            "coefficient_attachment": "missing",
            "same_branch_root": "conditional_conservation",
            "hessian_bound": "missing",
            "stress_readout": "not_enough",
            "overall": "charge_route_support_not_coupling_owner",
            "next_use": "charge/conservation branch, not immediate b_alpha zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    formula_rows = [
        {
            "formula_id": "FORM3223_0_exact_root",
            "quantity": "b_alpha_m at exact defect root",
            "formula": "b_alpha_m = partial_m ln Z_A = 0 if Delta Z_A=lambda_D ||R_Q||^2 and R_Q=0 exactly",
            "inputs_required": "source-signed R_Q, no linear defect, no independent coefficient, readout closure",
            "status": "THEOREM_SHAPE_ONLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "formula_id": "FORM3223_1_offroot_bound",
            "quantity": "finite off-root b_alpha_m",
            "formula": "|b_alpha_m| <= 2 |lambda_D| ||D_m R_Q||^2 |Delta m| / Z_min + O(Delta m^2)",
            "inputs_required": "lambda_D, ||D_m R_Q||, Delta m, Z_min, units, source paths",
            "status": "FINITE_BOUND_READY_FOR_INPUTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "formula_id": "FORM3223_2_alpha_residual",
            "quantity": "finite alpha residual",
            "formula": "|Delta alpha/alpha| <= |lambda_D| ||D_m R_Q||^2 Delta m^2 / Z_min + O(Delta m^3)",
            "inputs_required": "same finite inputs plus readout/radiative correction bound",
            "status": "FINITE_BOUND_READY_FOR_INPUTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "formula_id": "FORM3223_3_hessian_guard",
            "quantity": "defect-norm Hessian correction",
            "formula": "G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0",
            "inputs_required": "G_mem, lambda_D, ||D_m R_Q||, ||F_Q^2|| support norm, stress/readout bounds",
            "status": "FINITE_BOUND_READY_FOR_INPUTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    smoke_rows = [
        {
            "input_id": "SMOKE3223_0_balpha_zero_switch",
            "quantity": "b_alpha_m",
            "value": "0",
            "units": "dimensionless vertical slope",
            "source_path": "MISSING_SOURCE_SIGNED_RQ",
            "activation": "requires source-signed exact defect root",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "SMOKE3223_1_lambda_D",
            "quantity": "lambda_D",
            "value": "MISSING_NUMERIC_OR_THEOREM_FIXED",
            "units": "Z_A per ||R_Q||^2",
            "source_path": "MISSING_PARENT_ACTION_TERM",
            "activation": "finite off-root branch",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "SMOKE3223_2_DRQ_norm",
            "quantity": "||D_m R_Q||",
            "value": "MISSING_OPERATOR_NORM",
            "units": "R_Q per m",
            "source_path": "MISSING_LINEARIZED_DEFECT_MAP",
            "activation": "finite off-root and Hessian branch",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "SMOKE3223_3_delta_m",
            "quantity": "Delta m",
            "value": "MISSING_LOCAL_AMPLITUDE",
            "units": "m units",
            "source_path": "MISSING_SAME_BRANCH_LOCAL_LOCK_BOUND",
            "activation": "finite off-root branch",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "SMOKE3223_4_Z_min",
            "quantity": "Z_min",
            "value": "MISSING_POSITIVE_DENOMINATOR",
            "units": "EM kinetic normalization",
            "source_path": "MISSING_ALPHA_DENOMINATOR_OWNER",
            "activation": "finite off-root branch",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "SMOKE3223_5_tau_clock",
            "quantity": "tau_clock",
            "value": "MISSING_CLOCK_PROJECTION_FACTOR",
            "units": "time/projection units",
            "source_path": "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "activation": "clock comparison",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "SMOKE3223_6_tau_WEP_beta",
            "quantity": "tau_WEP and beta_source_alpha",
            "value": "MISSING_WEP_SOURCE_TEST_PROJECTION",
            "units": "dimensionless/projection units",
            "source_path": "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "activation": "WEP comparison",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "SMOKE3223_7_tau_R10",
            "quantity": "tau_R10",
            "value": "MISSING_R10_SOURCE_TEST_PROJECTION",
            "units": "length/projection units",
            "source_path": "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv",
            "activation": "R10 comparison",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "SMOKE3223_8_eta_stress_readout",
            "quantity": "eta_stress + eta_readout",
            "value": "MISSING_STRESS_READOUT_BOUND",
            "units": "operator/alpha correction units",
            "source_path": "MISSING_HODGE_STRESS_READOUT_SOURCE",
            "activation": "Maxwell stress and observed alpha guard",
            "schema_valid": "true",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    numeric_ready = sum(row["numeric_ready"] == "true" for row in smoke_rows)
    claim_ready = sum(row["valid_for_claim"] == "true" for row in smoke_rows)
    runner_rows = [
        {
            "run_id": "RUN3223_0_schema",
            "input_rows": len(smoke_rows),
            "schema_valid_rows": sum(row["schema_valid"] == "true" for row in smoke_rows),
            "numeric_ready_rows": numeric_ready,
            "claim_ready_rows": claim_ready,
            "comparison_status": "schema_smoke_only",
            "claim_allowed": "false",
            "reason": "finite alpha runner inputs are structurally staged but numeric/source-backed values are missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "run_id": "RUN3223_1_zero_switch",
            "input_rows": 1,
            "schema_valid_rows": 1,
            "numeric_ready_rows": 0,
            "claim_ready_rows": 0,
            "comparison_status": "inactive",
            "claim_allowed": "false",
            "reason": "R_Q exact root is not source-signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3223_0_result",
            "decision": "NO_RQ_SOURCE_SIGNED_FINITE_ALPHA_SMOKE_RUNNER_STAGED",
            "because": "bounded source search found templates/support for R_Z, R_W, R_H, and R_theta, but no candidate has parent object + EM coefficient attachment + same-branch root + Hessian/stress/readout closure",
            "claim_status": "NO_BALPHA_M_ZERO_NO_ALPHA_RUNNER_CLAIM_NO_MAXWELL_STRESS_NO_LOCAL_GR_CLAIM",
            "next_action": "turn finite formulas into a reusable alpha-bound propagator and start filling real values only when source-backed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3223_1_next_target",
            "decision": "3224-Y5-R2FR-finite-alpha-bound-propagator-clock-WEP-R10-under-AX1090",
            "because": "the derivation route is now exact but unsigned; practical progress is to make the finite branch executable without claims",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "implement a propagator for b_alpha_m bounds into clock/WEP/R10 products using only claim-valid numeric rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, search_rows, score_rows, formula_rows, smoke_rows, runner_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    search_rows: list[dict[str, object]],
    score_rows: list[dict[str, object]],
    formula_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, SEARCH, SCORE, FORMULA, SMOKE, RUNNER, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    source_signed_count = sum(row["source_signed"] == "true" for row in search_rows if "source_signed" in row)
    finite_formula = any(row["formula_id"] == "FORM3223_1_offroot_bound" for row in formula_rows)
    smoke_schema = all(row["schema_valid"] == "true" for row in smoke_rows)
    runner_refuses = all(row["claim_allowed"] == "false" for row in runner_rows)
    claim_true_count = 0
    for rows in [input_rows, search_rows, score_rows, formula_rows, smoke_rows, runner_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(FW not in [path, *path.parents] for path in out_paths + [DOC])

    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in out_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3223_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3223_01_no_RQ_source_signed", "pass": b(source_signed_count == 0), "detail": f"source_signed_count={source_signed_count}", "generated_utc": now},
        {"check_id": "VAL3223_02_candidates_scored", "pass": b(len(score_rows) >= 4), "detail": ";".join(row["candidate_id"] for row in score_rows), "generated_utc": now},
        {"check_id": "VAL3223_03_finite_formula_staged", "pass": b(finite_formula), "detail": "off-root b_alpha_m bound formula written", "generated_utc": now},
        {"check_id": "VAL3223_04_smoke_schema_valid", "pass": b(smoke_schema), "detail": f"smoke_rows={len(smoke_rows)}", "generated_utc": now},
        {"check_id": "VAL3223_05_runner_refuses_claim", "pass": b(runner_refuses), "detail": "claim_allowed=false for all runner rows", "generated_utc": now},
        {"check_id": "VAL3223_06_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3223_07_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3223_08_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3223_09_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3224-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    search_rows: list[dict[str, object]],
    score_rows: list[dict[str, object]],
    formula_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3223 - RQ Source Search Or Finite Alpha Runner Smoke Inputs under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3223 performs a bounded source search over the files that actually matter for the `R_Q` defect-norm route.

Result:

```text
No candidate R_Q is source-signed yet.
```

But the search is informative rather than empty:

```text
R_Z = Z_A - C_P N_Q
```

is still the best alpha/coupling owner target because it attaches directly to the EM kinetic coefficient. `R_W` and `R_H` are better treated as second-lane guards for current/stress/readout safety. `R_theta` supports the charge/conservation route but does not own the Maxwell kinetic coefficient.

Since no exact `R_Q` source row exists, 3223 stages the finite branch instead:

```text
|b_alpha_m| <= 2 |lambda_D| ||D_m R_Q||^2 |Delta m| / Z_min + O(Delta m^2).
```

The smoke runner deliberately refuses claims because all needed finite inputs remain placeholder/nonclaim.

Current verdict: `NO_RQ_SOURCE_SIGNED_FINITE_ALPHA_SMOKE_RUNNER_STAGED`.

## RQ Source Search

{md_table(search_rows, ["search_id", "candidate", "positive_hits", "blocking_hits", "result", "source_signed", "valid_for_claim"])}

## RQ Candidate Scorecard

{md_table(score_rows, ["candidate_id", "candidate", "parent_object", "coefficient_attachment", "same_branch_root", "hessian_bound", "stress_readout", "overall", "next_use", "valid_for_claim"])}

## Finite Alpha Bound Formula

{md_table(formula_rows, ["formula_id", "quantity", "formula", "inputs_required", "status", "valid_for_claim"])}

## Finite Alpha Smoke Inputs

{md_table(smoke_rows, ["input_id", "quantity", "value", "units", "source_path", "activation", "schema_valid", "numeric_ready", "valid_for_claim"])}

## Alpha Smoke Runner Results

{md_table(runner_rows, ["run_id", "input_rows", "schema_valid_rows", "numeric_ready_rows", "claim_ready_rows", "comparison_status", "claim_allowed", "reason", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_RQ_SOURCE_SEARCH.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_RQ_CANDIDATE_SCORECARD.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_FINITE_ALPHA_SMOKE_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_ALPHA_SMOKE_RUNNER_RESULTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, search_rows, score_rows, formula_rows, smoke_rows, runner_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (SEARCH, search_rows),
        (SCORE, score_rows),
        (FORMULA, formula_rows),
        (SMOKE, smoke_rows),
        (RUNNER, runner_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, search_rows, score_rows, formula_rows, smoke_rows, runner_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, search_rows, score_rows, formula_rows, smoke_rows, runner_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

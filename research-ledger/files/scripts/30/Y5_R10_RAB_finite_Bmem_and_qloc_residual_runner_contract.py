from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1350"
TITLE = "1350-Y5-R10-RAB-finite-Bmem-and-qloc-residual-runner-contract"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
RUNNER_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_SCHEMA.csv"
REQUIRED_INPUTS_PATH = OUT_DIR / f"{PACK_ID}_REQUIRED_INPUT_ROWS.csv"
OBSERVABLE_MAP_PATH = OUT_DIR / f"{PACK_ID}_OBSERVABLE_MAP.csv"
DRY_RUN_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_DRY_RUN.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1350_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def has_missing_token(value: object) -> bool:
    text = str(value).strip().lower()
    if not text:
        return True
    missing_tokens = [
        "missing",
        "missing_",
        "symbolic",
        "placeholder",
        "not_parent",
        "not_source",
        "not_instantiated",
        "unsigned",
        "closure_only",
        "blocked",
        "unknown",
    ]
    return any(token in text for token in missing_tokens)


def source_register() -> list[dict[str, object]]:
    source_rows = [
        {
            "source_id": "SRC1350_0_1349_doc",
            "source_path": "1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md",
            "required_anchor": "Current verdict",
            "purpose": "1349 verdict: K_MTS trace projection owner is not derived.",
        },
        {
            "source_id": "SRC1350_1_1349_residual_branch",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1349_FINITE_BMEM_RESIDUAL_BRANCH.csv",
            "required_anchor": "BMR1349_0_symbolic_input",
            "purpose": "finite B_mem and q_loc residual branch retained.",
        },
        {
            "source_id": "SRC1350_2_1349_claim_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1349_CLAIM_GATE.csv",
            "required_anchor": "GATE1349_2_local_GR",
            "purpose": "local-GR and B_mem zero claims remain blocked.",
        },
        {
            "source_id": "SRC1350_3_1010_q_loc_residual",
            "source_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "required_anchor": "q_loc residual",
            "purpose": "prior q_loc residual retention contract.",
        },
        {
            "source_id": "SRC1350_4_1011_bound_fill",
            "source_path": "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
            "required_anchor": "q_loc bound-fill rows",
            "purpose": "prior nonclaim q_loc bound-fill rows.",
        },
        {
            "source_id": "SRC1350_5_1348_bmem_extremum",
            "source_path": "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
            "required_anchor": "B_MEM_ZERO_NOT_PARENT_OWNED_CURRENT_CORPUS",
            "purpose": "conditional F1/B_mem zero route was not parent-owned.",
        },
    ]
    for row in source_rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return source_rows


def runner_schema() -> list[dict[str, object]]:
    return [
        {
            "field_name": "row_id",
            "required_for": "all_rows",
            "acceptance_rule": "unique nonempty identifier",
            "blocks_if_missing": True,
            "current_policy": "required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_name": "quantity",
            "required_for": "all_rows",
            "acceptance_rule": "one of B_mem,Z_mem,M2_mem,C_mem,J_mem,Q_boundary,Gamma_eff,K_hat,P_loc,q_loc,observable_map,bound",
            "blocks_if_missing": True,
            "current_policy": "required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_name": "numeric_value_or_theorem_zero",
            "required_for": "scored_rows",
            "acceptance_rule": "finite numeric value with units or theorem-zero certificate with source path",
            "blocks_if_missing": True,
            "current_policy": "symbolic-only rows reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_name": "units",
            "required_for": "scored_rows",
            "acceptance_rule": "dimensionful rows declare SI or natural-unit convention and conversion",
            "blocks_if_missing": True,
            "current_policy": "missing-unit rows reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_name": "parent_owner_source",
            "required_for": "derived_or_zero_rows",
            "acceptance_rule": "local source path proves parent action, variation, or theorem-zero clause",
            "blocks_if_missing": True,
            "current_policy": "closure-only rows reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_name": "normalization_and_sign",
            "required_for": "all_scored_rows",
            "acceptance_rule": "sign convention, Fourier/radial convention, and source/test normalization declared",
            "blocks_if_missing": True,
            "current_policy": "ambiguous sign/normalization rows reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_name": "observable_map",
            "required_for": "R10_PPN_clock_orbital_rows",
            "acceptance_rule": "maps residual quantity into the named measured observable with coefficient path",
            "blocks_if_missing": True,
            "current_policy": "no observable map, no score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_name": "bound_source",
            "required_for": "comparison_rows",
            "acceptance_rule": "source-backed constraint curve/table or explicitly noncurve anchor",
            "blocks_if_missing": True,
            "current_policy": "anchor-only rows cannot become claim rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def required_inputs() -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "REQ1350_0_Bmem",
            "quantity": "B_mem",
            "contract": "curvature-linear memory coupling in finite branch",
            "required_expression": "(-Z_mem nabla^2 + M2_mem) delta m = B_mem R_obs + C_mem T + J_mem + Q_boundary",
            "required_units": "units of memory-field equation source convention",
            "required_source": "parent action coefficient or theorem-zero certificate",
            "required_observable_map": "R10/PPN/clock/orbital coefficient map after solving profile",
            "current_status": "SYMBOLIC_NONCLAIM_ONLY",
        },
        {
            "input_id": "REQ1350_1_memory_operator",
            "quantity": "Z_mem;M2_mem;lambda_mem",
            "contract": "operator and range for memory profile",
            "required_expression": "lambda_mem = sqrt(Z_mem/M2_mem) after sign/unit convention is fixed",
            "required_units": "Z_mem and M2_mem compatible with chosen operator normalization",
            "required_source": "parent kinetic/mass operator source path",
            "required_observable_map": "range-to-lambda conversion for each arena",
            "current_status": "SYMBOLIC_NONCLAIM_ONLY",
        },
        {
            "input_id": "REQ1350_2_source_silence",
            "quantity": "C_mem;J_mem;Q_boundary",
            "contract": "ordinary matter, explicit current, and boundary source terms",
            "required_expression": "C_mem T + J_mem + Q_boundary is zero, bounded, or included",
            "required_units": "same source units as B_mem R_obs",
            "required_source": "parent pullback, Ward identity, or numeric bound source",
            "required_observable_map": "feeds q_loc and local fifth-force channels if nonzero",
            "current_status": "MISSING_ZERO_OR_BOUND_CERTIFICATE",
        },
        {
            "input_id": "REQ1350_3_Gamma_eff",
            "quantity": "Gamma_eff",
            "contract": "scalar density whose gradient enters q_loc",
            "required_expression": "Gamma_eff = parent-owned scalar-density functional, not a hand-set closure",
            "required_units": "declared density/scalar convention",
            "required_source": "K_MTS or parent variation source path",
            "required_observable_map": "gradient contribution to q_loc",
            "current_status": "MISSING_PARENT_OWNER",
        },
        {
            "input_id": "REQ1350_4_Khat",
            "quantity": "K_hat^{mu nu}",
            "contract": "metric response tensor paired with Gamma_eff",
            "required_expression": "K_hat = metric response of Gamma_eff including derivative and boundary terms",
            "required_units": "stress-response convention",
            "required_source": "Hilbert/metric variation source path",
            "required_observable_map": "divergence contribution to q_loc",
            "current_status": "MISSING_METRIC_RESPONSE_MATCH",
        },
        {
            "input_id": "REQ1350_5_Ploc",
            "quantity": "P_loc",
            "contract": "local projector selecting physical residual vector",
            "required_expression": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "required_units": "dimensionless projector or declared dimensionful map",
            "required_source": "local quotient/projection owner source path",
            "required_observable_map": "PPN/source-normalization/local-force vector",
            "current_status": "MISSING_PROJECTOR_OWNER",
        },
        {
            "input_id": "REQ1350_6_R10_map",
            "quantity": "alpha(lambda)",
            "contract": "map finite memory/local residual into Yukawa-style R10 comparison",
            "required_expression": "alpha_pred(lambda) = F_R10[B_mem,Z_mem,M2_mem,Gamma_eff,K_hat,P_loc,source]",
            "required_units": "dimensionless alpha, length lambda",
            "required_source": "observable coefficient derivation plus bound curve source",
            "required_observable_map": "R10 alpha-lambda bound",
            "current_status": "MISSING_R10_COEFFICIENT_MAP",
        },
        {
            "input_id": "REQ1350_7_PPN_map",
            "quantity": "Delta_PPN",
            "contract": "map q_loc residual into PPN vector",
            "required_expression": "Delta_PPN = F_PPN[q_loc,source,metric_solution]",
            "required_units": "dimensionless PPN vector",
            "required_source": "weak-field metric solution/source-normalization path",
            "required_observable_map": "gamma,beta,alpha_i,xi,Gdot constraints",
            "current_status": "MISSING_WEAK_FIELD_METRIC_MAP",
        },
        {
            "input_id": "REQ1350_8_clock_orbital_maps",
            "quantity": "clock;orbital residuals",
            "contract": "map q_loc profile into clocks and orbital systems",
            "required_expression": "delta_nu/nu and orbital residual vector from same q_loc profile",
            "required_units": "fractional frequency, acceleration/precession/time delay units",
            "required_source": "clock readout and orbital dynamics coefficient path",
            "required_observable_map": "clock, lunar/planetary, binary/orbital gates",
            "current_status": "MISSING_ARENA_PROJECTIONS",
        },
    ]

    for row in rows:
        row["runner_verdict"] = "REJECT_CURRENT_ROW"
        row["failure_reasons"] = "valid_for_claim_false;claim_allowed_false;" + str(row["current_status"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def observable_map() -> list[dict[str, object]]:
    rows = [
        {
            "observable_id": "OBS1350_0_R10",
            "arena": "R10 short-range gravity",
            "residual_input": "B_mem profile or q_loc profile",
            "observable_output": "alpha(lambda)",
            "must_have": "numeric coefficient map; source mass geometry; lambda convention; source-backed bound curve",
            "current_status": "MISSING_COEFFICIENT_MAP_AND_CLAIM_CURVE",
            "runner_policy": "reject",
        },
        {
            "observable_id": "OBS1350_1_PPN",
            "arena": "PPN/local weak-field",
            "residual_input": "q_loc^nu and metric solution",
            "observable_output": "gamma-1,beta-1,alpha_1,alpha_2,alpha_3,xi,Gdot/G",
            "must_have": "weak-field solution and source-normalization map",
            "current_status": "MISSING_WEAK_FIELD_MAP",
            "runner_policy": "reject",
        },
        {
            "observable_id": "OBS1350_2_clocks",
            "arena": "clock/readout tests",
            "residual_input": "Gamma_eff/Khat/P_loc residual and visible readout coupling",
            "observable_output": "delta_nu/nu or drift vector",
            "must_have": "clock readout coefficient and hidden-visible coupling theorem/bound",
            "current_status": "MISSING_CLOCK_READOUT_MAP",
            "runner_policy": "reject",
        },
        {
            "observable_id": "OBS1350_3_orbital",
            "arena": "orbital systems",
            "residual_input": "q_loc force/metric tail",
            "observable_output": "perihelion, Shapiro, ephemeris, binary timing residuals",
            "must_have": "radial profile, source geometry, metric/force law, data-bound source",
            "current_status": "MISSING_ORBITAL_PROJECTION",
            "runner_policy": "reject",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def evaluate_case(case: dict[str, object]) -> dict[str, object]:
    required_fields = [
        "numeric_value_or_theorem_zero",
        "units",
        "parent_owner_source",
        "normalization_and_sign",
        "observable_map",
        "bound_source",
    ]
    missing = [field for field in required_fields if has_missing_token(case.get(field, ""))]
    forbidden = []
    if "axiom" in str(case.get("parent_owner_source", "")).lower():
        forbidden.append("FORBIDDEN_PLATEAU_OR_CLOSURE_AXIOM")
    if str(case.get("hypothetical_complete", "False")).lower() == "true" and not missing and not forbidden:
        verdict = "WOULD_ACCEPT_IF_REAL_FILES_AND_VALUES_EXIST"
    else:
        verdict = "REJECT"
    case["missing_fields"] = ";".join(missing) if missing else "none"
    case["forbidden_reasons"] = ";".join(forbidden) if forbidden else "none"
    case["runner_verdict"] = verdict
    case["valid_for_claim"] = False
    case["claim_allowed"] = False
    return case


def dry_run_cases() -> list[dict[str, object]]:
    cases = [
        {
            "dry_run_id": "DRY1350_0_current_symbolic_Bmem",
            "candidate": "current finite B_mem row",
            "numeric_value_or_theorem_zero": "SYMBOLIC_B_mem",
            "units": "MISSING_UNITS",
            "parent_owner_source": "MISSING_PARENT_OWNER",
            "normalization_and_sign": "MISSING_NORMALIZATION",
            "observable_map": "MISSING_R10_PPN_CLOCK_ORBITAL_MAP",
            "bound_source": "MISSING_BOUND_SOURCE",
            "hypothetical_complete": False,
        },
        {
            "dry_run_id": "DRY1350_1_numeric_without_parent",
            "candidate": "numeric B_mem but no parent source",
            "numeric_value_or_theorem_zero": "0.0745331916",
            "units": "dimensionless_closure_proxy",
            "parent_owner_source": "MISSING_PARENT_OWNER",
            "normalization_and_sign": "closure_proxy_sign_only",
            "observable_map": "MISSING_R10_PPN_MAP",
            "bound_source": "MISSING_BOUND_SOURCE",
            "hypothetical_complete": False,
        },
        {
            "dry_run_id": "DRY1350_2_Gamma_without_Khat",
            "candidate": "Gamma_eff expression only",
            "numeric_value_or_theorem_zero": "formula_present",
            "units": "declared_scalar_density_units",
            "parent_owner_source": "Gamma_eff_candidate_but_Khat_missing",
            "normalization_and_sign": "normalization_partial",
            "observable_map": "MISSING_KHAT_RESPONSE_AND_PLOC_MAP",
            "bound_source": "MISSING_BOUND_SOURCE",
            "hypothetical_complete": False,
        },
        {
            "dry_run_id": "DRY1350_3_q_loc_zero_by_axiom",
            "candidate": "q_loc zero closure",
            "numeric_value_or_theorem_zero": "theorem_zero_claimed",
            "units": "dimensionless_vector",
            "parent_owner_source": "plateau_axiom_or_private_closure_only",
            "normalization_and_sign": "closure_convention",
            "observable_map": "not_needed_by_axiom",
            "bound_source": "not_needed_by_axiom",
            "hypothetical_complete": False,
        },
        {
            "dry_run_id": "DRY1350_4_future_complete_template",
            "candidate": "future real fully sourced row",
            "numeric_value_or_theorem_zero": "finite_numeric_value_or_parent_signed_theorem_zero",
            "units": "explicit_units_and_conversion",
            "parent_owner_source": "real_existing_parent_source_path_and_anchor",
            "normalization_and_sign": "explicit_sign_and_source_test_normalization",
            "observable_map": "real_existing_observable_coefficient_map",
            "bound_source": "real_existing_bound_curve_or_table",
            "hypothetical_complete": True,
        },
    ]
    return [evaluate_case(case) for case in cases]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1350_0_score_Bmem",
            "claim": "finite B_mem can be scored as local evidence",
            "allowed_if": "B_mem,Z_mem,M2_mem,C/J/boundary,units,source normalization, and observable maps are real",
            "current_status": "BLOCKED",
            "reason": "current B_mem is symbolic/closure-fit only",
        },
        {
            "gate_id": "GATE1350_1_q_loc_zero",
            "claim": "q_loc^nu vanishes locally",
            "allowed_if": "Gamma_eff,K_hat,P_loc,boundary,source currents, and Euler/Ward closure are parent-owned",
            "current_status": "BLOCKED",
            "reason": "q_loc zero remains closure/theorem target, not derived",
        },
        {
            "gate_id": "GATE1350_2_R10",
            "claim": "R10/Yukawa local-gravity pass",
            "allowed_if": "alpha(lambda) prediction and bound curve are both sourced and numeric",
            "current_status": "BLOCKED",
            "reason": "R10 coefficient map and claim-grade curve are missing",
        },
        {
            "gate_id": "GATE1350_3_PPN",
            "claim": "PPN/local-GR pass",
            "allowed_if": "weak-field metric solution maps q_loc into PPN vector below bounds",
            "current_status": "BLOCKED",
            "reason": "weak-field map and Khat response are missing",
        },
        {
            "gate_id": "GATE1350_4_clock_orbital",
            "claim": "clock/orbital consistency pass",
            "allowed_if": "same q_loc profile maps into clock and orbital residuals below sourced bounds",
            "current_status": "BLOCKED",
            "reason": "arena projections are missing",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1350_0_runner_contract_installed",
            "decision": "Finite B_mem/q_loc is now a runner-gated residual branch, not a free scoring branch.",
            "why": "1349 failed to parent-own K_MTS trace projection, so the honest default is finite symbolic residual retention.",
            "next_action": "feed only source-backed rows into future R10/PPN/local runners",
        },
        {
            "decision_id": "DEC1350_1_closure_not_public",
            "decision": "B_mem=0 may remain a private algebra closure but cannot be used as evidence.",
            "why": "F1=0 is conditional; the Gamma_eff/Khat/P_loc parent owner is not derived.",
            "next_action": "if closure is used, label it PRIVATE_CLOSURE_ONLY and keep claim gates false",
        },
        {
            "decision_id": "DEC1350_2_best_next_target",
            "decision": "The best next route is the minimal operator-owner bundle: Gamma_eff, K_hat, and P_loc.",
            "why": "Without that bundle, R10/PPN/clock/orbital maps are just bookkeeping coefficients.",
            "next_action": "try 1351 owner-bundle derivation before sourcing more empirical bound rows",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1350_0_1351",
            "target_file": "1351-Y5-R10-RAB-Gamma-Khat-Ploc-owner-bundle-or-q_loc-bound-row-fill.md",
            "target_script": "scripts/Y5_R10_RAB_Gamma_Khat_Ploc_owner_bundle_or_q_loc_bound_row_fill.py",
            "task": "try to parent-own the minimal q_loc operator bundle Gamma_eff, K_hat, and P_loc; if not, stage nonclaim q_loc bound rows for R10, PPN, clocks, and orbital arenas",
            "success_condition": "either a sourced operator-owner bundle or a source-ready residual-bound input pack that still refuses claims",
            "do_not": "do not score symbolic B_mem; do not set q_loc=0 by closure; do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate_outputs(
    sources: list[dict[str, object]],
    schema: list[dict[str, object]],
    inputs: list[dict[str, object]],
    dry_runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if status else "FAIL",
                "details": details,
            }
        )

    add(
        "VAL1350_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    required_schema = {
        "numeric_value_or_theorem_zero",
        "units",
        "parent_owner_source",
        "normalization_and_sign",
        "observable_map",
        "bound_source",
    }
    schema_fields = {str(row["field_name"]) for row in schema}
    add(
        "VAL1350_1_schema_has_claim_blockers",
        "runner schema contains all blockers needed before a claim can score",
        required_schema.issubset(schema_fields),
        f"missing={sorted(required_schema - schema_fields)}",
    )

    add(
        "VAL1350_2_required_inputs_reject_current",
        "all required current input rows reject and remain nonclaim",
        all(row["runner_verdict"] == "REJECT_CURRENT_ROW" and not row["valid_for_claim"] and not row["claim_allowed"] for row in inputs),
        f"rows={len(inputs)}",
    )

    current_dry_runs = [row for row in dry_runs if str(row["dry_run_id"]) != "DRY1350_4_future_complete_template"]
    add(
        "VAL1350_3_dry_run_rejects_bad_rows",
        "dry-run rejects symbolic, no-parent, partial-response, and axiom cases",
        all(row["runner_verdict"] == "REJECT" and not row["claim_allowed"] for row in current_dry_runs),
        ";".join(f"{row['dry_run_id']}={row['runner_verdict']}" for row in current_dry_runs),
    )

    future_row = next(row for row in dry_runs if str(row["dry_run_id"]) == "DRY1350_4_future_complete_template")
    add(
        "VAL1350_4_future_template_only",
        "complete future row is only a template, not a current claim",
        future_row["runner_verdict"] == "WOULD_ACCEPT_IF_REAL_FILES_AND_VALUES_EXIST"
        and not future_row["claim_allowed"]
        and not future_row["valid_for_claim"],
        str(future_row["runner_verdict"]),
    )

    add(
        "VAL1350_5_claim_gates_blocked",
        "all claim gates remain blocked",
        all(row["current_status"] == "BLOCKED" and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['current_status']}" for row in gates),
    )

    all_output_rows = sources + schema + inputs + observable_map() + dry_runs + gates + decision_rows() + next_target
    add(
        "VAL1350_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_output_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits = list(FORMALIZATION.rglob("*1350*")) if FORMALIZATION.exists() else []
    add(
        "VAL1350_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1350_8_next_target_1351",
        "next target routes to Gamma/Khat/Ploc owner bundle or q_loc bound fill",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1351-Y5-R10-RAB-Gamma-Khat-Ploc"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1350_9_overall",
        "overall 1350 validation",
        all(row["status"] == "PASS" for row in validations),
        "1350 installs strict nonclaim runner contract for finite B_mem/q_loc residual branch",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    schema: list[dict[str, object]],
    inputs: list[dict[str, object]],
    observables: list[dict[str, object]],
    dry_runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1350 does not make `B_mem` or `q_loc` evidence. It installs the opposite: a strict runner contract that rejects symbolic finite-memory and local-residual rows until units, parent owners, normalization, observable maps, and bound sources are real.",
            "**Main progress:** the live branch is now mechanically separated from the private closure branch. `B_mem=0` remains private closure only; finite `B_mem/q_loc` is retained as a nonclaim residual branch and cannot score R10, PPN, clock, or orbital tests without the required input bundle.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Runner schema",
            table(["field_name", "required_for", "acceptance_rule", "blocks_if_missing", "current_policy"], schema),
            "## Required input rows",
            table(["input_id", "quantity", "contract", "current_status", "runner_verdict", "failure_reasons"], inputs),
            "## Observable map gates",
            table(["observable_id", "arena", "residual_input", "observable_output", "current_status", "runner_policy"], observables),
            "## Dry-run rejection matrix",
            table(["dry_run_id", "candidate", "missing_fields", "forbidden_reasons", "runner_verdict", "claim_allowed"], dry_runs),
            "## Claim gates",
            table(["gate_id", "claim", "current_status", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    schema = runner_schema()
    inputs = required_inputs()
    observables = observable_map()
    dry_runs = dry_run_cases()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, schema, inputs, dry_runs, gates, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(RUNNER_SCHEMA_PATH, schema)
    write_csv(REQUIRED_INPUTS_PATH, inputs)
    write_csv(OBSERVABLE_MAP_PATH, observables)
    write_csv(DRY_RUN_PATH, dry_runs)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, schema, inputs, observables, dry_runs, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

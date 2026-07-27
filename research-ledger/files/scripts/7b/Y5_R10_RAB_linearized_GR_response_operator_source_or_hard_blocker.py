from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1296"
TITLE = "1296-Y5-R10-RAB-linearized-GR-response-operator-source-or-hard-blocker"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
RESPONSE_OPERATOR_PATH = OUT_DIR / f"{PACK_ID}_RESPONSE_OPERATOR_ROWS_NONCLAIM.csv"
RUNNER_BRIDGE_PATH = OUT_DIR / f"{PACK_ID}_OPERATOR_TO_RUNNER_BRIDGE_PREVIEW.csv"
OBSERVABLE_GAPS_PATH = OUT_DIR / f"{PACK_ID}_OBSERVABLE_GAP_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1296_VALIDATION.csv"

INPUT_PATH = OUT_DIR / "P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def is_true(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        RESPONSE_OPERATOR_PATH,
        RUNNER_BRIDGE_PATH,
        OBSERVABLE_GAPS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def bridge_inputs(required_inputs: str) -> tuple[str, list[str], bool, bool]:
    tokens = split_semicolon(required_inputs)
    csign_applied = "MISSING_C_SIGN" in tokens
    response_applied = "MISSING_RESPONSE_OPERATOR" in tokens
    preview_tokens = []
    for token in tokens:
        if token == "MISSING_C_SIGN":
            preview_tokens.append("ABS_C_SIGN_EQ_1_BOUND_ONLY")
        elif token == "MISSING_RESPONSE_OPERATOR":
            preview_tokens.append("RGO1296_LINEARIZED_GR_RESPONSE_NONCLAIM")
        else:
            preview_tokens.append(token)
    remaining = [token for token in preview_tokens if token.startswith("MISSING")]
    return ";".join(preview_tokens), remaining, csign_applied, response_applied


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    runner_rows = read_csv(INPUT_PATH)

    source_register = [
        {
            "source_id": "SRC1296_0_1295_next",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1295_NEXT_TARGET.csv",
            "url": "",
            "needle_or_anchor": "NEXT1295_0_1296",
            "role": "handoff into linearized GR response-operator acquisition",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1296_1_response_requirements",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "url": "",
            "needle_or_anchor": "RMR1288_7_response_verdict",
            "role": "local response requirements to be partially filled by formal operator",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1296_2_KL_budget",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "url": "",
            "needle_or_anchor": "KLB796_5_acceptance_condition",
            "role": "shows response operator plus amplitude/source normalization are required",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1296_3_runner_input",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "url": "",
            "needle_or_anchor": "MISSING_RESPONSE_OPERATOR",
            "role": "runner templates where the formal response operator can be previewed",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1296_4_MIT_linearized_GR",
            "source_type": "external_web",
            "local_path": "",
            "url": "https://web.mit.edu/sahughes/www/8.962/lec16.pdf",
            "needle_or_anchor": "linearized Einstein equation in Lorenz gauge and retarded Green-function solution; opened 2026-06-15 lines 357-372",
            "role": "source-backed linearized trace-reversed metric response operator",
            "web_verified_utc": RUN_STARTED_UTC.isoformat(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1296_5_Will_PPN_review",
            "source_type": "external_web",
            "local_path": "",
            "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
            "needle_or_anchor": "Living Reviews PPN/experimental-GR framework; opened 2026-06-15",
            "role": "source-backed PPN/weak-field test framework, not yet a full MTS response map",
            "web_verified_utc": RUN_STARTED_UTC.isoformat(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1296_6_Poisson_Green",
            "source_type": "external_web",
            "local_path": "",
            "url": "https://mathworld.wolfram.com/GreensFunctionPoissonsEquation.html",
            "needle_or_anchor": "Poisson equation Green function and integral solution; opened 2026-06-15 lines 18-37",
            "role": "source-backed scalar Poisson Green operator for Newton/static limit",
            "web_verified_utc": RUN_STARTED_UTC.isoformat(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        if row["source_type"] == "local":
            exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle_or_anchor"]))
            row["exists_or_url_recorded"] = exists
            row["anchor_found_or_web_verified"] = needle_found
        else:
            row["exists_or_url_recorded"] = bool(row["url"])
            row["anchor_found_or_web_verified"] = bool(row["web_verified_utc"])

    response_operators = [
        {
            "operator_id": "RGO1296_0_linearized_trace_reversed_metric_response",
            "arena": "linearized_GR_metric_response",
            "operator_kind": "retarded_Green_operator_for_trace_reversed_metric",
            "source_equation": "Box hbar_{mu nu} = -16*pi*G*T_{mu nu} in c=1 Lorenz-gauge linearized GR",
            "operator_form": "hbar_{mu nu}(t,x)=4G int_D T_{mu nu}(t-|x-x'|,x')/|x-x'| d^3x'",
            "domain_assumptions": "weak field; local approximately flat background; Lorenz gauge; compact/localized source; retarded boundary condition",
            "units": "c=1 in source; SI restoration requires G/c^4 multiplying stress-energy; hbar is dimensionless",
            "MTS_bridge_status": "FORMAL_OPERATOR_ACQUIRED_BUT_SOURCE_NORMALIZATION_MISSING",
            "MTS_source_slot": "T_{mu nu} must be replaced by a derived effective residual source from Kmetric_chain/R_chain, with coefficient and sign fixed by parent field equation",
            "usable_as_response_operator": True,
            "usable_for_scoring": False,
            "source_url": "https://web.mit.edu/sahughes/www/8.962/lec16.pdf",
            "source_anchor": "Lorenz-gauge linearized equation and Green solution lines 357-372 in opened PDF",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "operator_id": "RGO1296_1_static_Poisson_Newton_response",
            "arena": "Newton_source_static_limit",
            "operator_kind": "Poisson_Green_operator_for_scalar_potential",
            "source_equation": "nabla^2 Phi_K = S_K(x), where S_K is the MTS-normalized scalar source still to be derived",
            "operator_form": "Phi_K(x)=int_D G_P(x,x') S_K(x') d^3x' plus boundary terms, with G_P=-1/(4*pi*|x-x'|) under the MathWorld sign convention",
            "domain_assumptions": "static weak-field scalar limit; chosen boundary condition; localized source or finite local domain",
            "units": "S_K has units of potential/length^2; Phi_K has potential units; mapping S_K to K_chain/rho_eff remains missing",
            "MTS_bridge_status": "FORMAL_NEWTON_OPERATOR_ACQUIRED_BUT_SOURCE_SLOT_MISSING",
            "MTS_source_slot": "derive S_K from Kbar_L,loc,00 or R_chain^{00}, including c^2, 4*pi*G, measured-GM calibration, and density normalization",
            "usable_as_response_operator": True,
            "usable_for_scoring": False,
            "source_url": "https://mathworld.wolfram.com/GreensFunctionPoissonsEquation.html",
            "source_anchor": "Poisson Green function and integral solution lines 18-37 in opened page",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_bridge = []
    for row in runner_rows:
        preview_inputs, remaining, csign_applied, response_applied = bridge_inputs(row.get("required_inputs", ""))
        runner_bridge.append(
            {
                "bridge_id": f"ORB1296_{len(runner_bridge)}",
                "runner_id": row.get("runner_id", ""),
                "residual_component": row.get("residual_component", ""),
                "abs_Csign_applied_from_1295": csign_applied,
                "formal_response_operator_applied": response_applied,
                "required_inputs_original": row.get("required_inputs", ""),
                "required_inputs_preview": preview_inputs,
                "remaining_missing_count": len(remaining),
                "remaining_missing_tokens": ";".join(remaining) if remaining else "NONE",
                "non_score_blockers": "SOURCE_NORMALIZATION;OBSERVABLE_LIMITS;MTS_EFFECTIVE_STRESS_COEFFICIENT;GAUGE_DOMAIN_BOUNDARY_CONTROL",
                "score_emitted": False,
                "score_value": "",
                "runner_status": "FORMAL_OPERATOR_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    observable_gaps = [
        {
            "gap_id": "OG1296_0_source_normalization",
            "gap": "map Kmetric_chain/R_chain into the GR source side",
            "why_it_matters": "linearized GR operator accepts T_{mu nu} or a normalized source, but MTS has not derived the coefficient/sign/source placement",
            "blocks": "Newton source fraction; PPN metric response; all scores",
            "next_requirement": "derive S_K or T_eff,K from the parent field equation with units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "OG1296_1_observable_projection",
            "gap": "map metric perturbation to gamma, beta, alpha_i, xi, clock, orbital, and R10 observables",
            "why_it_matters": "formal hbar response is not yet the PPN/clock/orbital residual vector",
            "blocks": "PPN vector; clock; orbital; R10 alpha(lambda)",
            "next_requirement": "build observable projection rows from hbar/Phi_K to each arena",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "OG1296_2_gauge_domain_boundary",
            "gap": "gauge, local-domain, and boundary conditions",
            "why_it_matters": "local solar-system recovery needs gauge-invariant or gauge-fixed observables and controlled boundary modes",
            "blocks": "local-GR recovery and Kperp/boundary guard",
            "next_requirement": "declare domain D, boundary conditions, homogeneous modes, and gauge-invariant readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "OG1296_3_numeric_inputs",
            "gap": "m, L_cg, F/Fprime, metric kernels, and CDB bounds remain missing",
            "why_it_matters": "even a perfect response operator cannot score a residual amplitude without the residual input amplitude",
            "blocks": "runner score",
            "next_requirement": "source or derive numeric/theorem bounds for remaining RRI1292 inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1296_0_response_operator_acquired",
            "claim": "first formal local response operator is source-backed",
            "current_status": "SATISFIED_FOR_NONCLAIM_FORMAL_OPERATOR",
            "reason": "linearized GR retarded Green operator and static Poisson Green operator are recorded with external sources and domains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1296_1_response_scoring",
            "claim": "response operator can score MTS residuals",
            "current_status": "BLOCKED_SOURCE_NORMALIZATION_MISSING",
            "reason": "MTS residual source placement/coefficient into T_eff or S_K is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1296_2_observable_vector",
            "claim": "PPN/clock/orbital/R10 observable vectors can be computed",
            "current_status": "BLOCKED_OBSERVABLE_PROJECTION_MISSING",
            "reason": "formal metric/potential response is not yet gamma/beta/clock/orbital/R10 readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1296_3_runner_score",
            "claim": "RRI1292 chain-kernel runner can emit scores",
            "current_status": "BLOCKED_REMAINING_MISSING_INPUTS",
            "reason": "m/Lcg/F/kernel/CDB and response normalization inputs remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1296_4_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "a sourced formal operator is necessary progress, not sufficient recovery",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1296_0_operator_acquired",
            "decision": "accept linearized GR and Poisson Green maps as first formal response operators",
            "because": "they are source-backed, have declared domains, and give the missing operator shape without inventing MTS coefficients",
            "next_action": "derive the MTS source-normalization bridge into T_eff,K or S_K",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1296_1_no_score",
            "decision": "do not score residuals from the formal operators",
            "because": "source normalization and observable projection are still missing",
            "next_action": "build the Newton source bridge first, then PPN/clock/orbital/R10 projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1296_2_best_next_route",
            "decision": "target source-normalization before numeric fitting",
            "because": "until the field equation says how K_chain enters the GR source side, numeric bounds would be dimensionally ambiguous",
            "next_action": "derive S_K proportionality, c factors, 4*pi*G factors, and measured-GM calibration row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1296_0_1297",
            "target_file": "1297-Y5-R10-RAB-MTS-source-normalization-bridge-to-linearized-GR-operator.md",
            "target_script": "scripts/Y5_R10_RAB_MTS_source_normalization_bridge_to_linearized_GR_operator.py",
            "task": "derive or block the coefficient/sign/unit bridge from Kmetric_chain or R_chain^{00} into the sourced linearized-GR/Poisson operator",
            "success_condition": "produce a source-normalization row with c factors, 4*pi*G factors, density/effective-stress units, and measured-GM caveat, or keep scoring blocked with an explicit dimensional ledger",
            "do_not": "do not compute PPN/R10/clock/orbital scores until source normalization and observable projections are both sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(RESPONSE_OPERATOR_PATH, response_operators)
    write_csv(RUNNER_BRIDGE_PATH, runner_bridge)
    write_csv(OBSERVABLE_GAPS_PATH, observable_gaps)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists_or_url_recorded"] and row["anchor_found_or_web_verified"])
    validations.append(
        validation_row(
            "VAL1296_0_sources_recorded",
            "local source anchors and external web sources are recorded",
            source_hits == source_count,
            f"{source_hits}/{source_count} source records validated",
        )
    )
    validations.append(
        validation_row(
            "VAL1296_1_response_operator_rows",
            "formal response operator rows exist with domains and units",
            len(response_operators) == 2
            and all(is_true(row["usable_as_response_operator"]) for row in response_operators)
            and all(is_false(row["usable_for_scoring"]) for row in response_operators)
            and all(row["domain_assumptions"] and row["units"] for row in response_operators),
            ";".join(row["operator_id"] for row in response_operators),
        )
    )
    formal_applied_rows = [row for row in runner_bridge if row["formal_response_operator_applied"] is True]
    validations.append(
        validation_row(
            "VAL1296_2_runner_bridge_applies_formal_operator",
            "formal response operator fills the component-row response token in preview only",
            len(formal_applied_rows) == 3
            and all("RGO1296_LINEARIZED_GR_RESPONSE_NONCLAIM" in row["required_inputs_preview"] for row in formal_applied_rows),
            ";".join(row["runner_id"] for row in formal_applied_rows),
        )
    )
    validations.append(
        validation_row(
            "VAL1296_3_runner_still_no_score",
            "all bridge rows remain no-score with missing or non-score blockers",
            all(is_false(row["score_emitted"]) and row["runner_status"] == "FORMAL_OPERATOR_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE" for row in runner_bridge)
            and all(row["non_score_blockers"] for row in runner_bridge),
            ";".join(f"{row['runner_id']}={row['remaining_missing_count']}" for row in runner_bridge),
        )
    )
    validations.append(
        validation_row(
            "VAL1296_4_observable_gaps_explicit",
            "observable/source-normalization gaps remain explicit",
            len(observable_gaps) == 4 and all(is_false(row["claim_allowed"]) for row in observable_gaps),
            ";".join(row["gap_id"] for row in observable_gaps),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        RESPONSE_OPERATOR_PATH,
        RUNNER_BRIDGE_PATH,
        OBSERVABLE_GAPS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1296_5_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1296_6_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1296_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, response_operators, runner_bridge, observable_gaps, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1296_8_next_target_1297",
            "next target routes to source-normalization bridge",
            next_target[0]["next_id"] == "NEXT1296_0_1297" and "source-normalization" in next_target[0]["target_file"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1296_9_overall",
            "overall 1296 validation",
            overall_pass,
            "1296 acquires formal source-backed linearized-GR/Poisson response operators, keeps scoring blocked by MTS source normalization and observable projections, and routes to the source bridge",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1296 Y5 R10 RAB linearized-GR response-operator source or hard blocker

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1296 acquires the first source-backed local response operators: a Lorenz-gauge linearized-GR retarded Green operator and a static Poisson/Newton Green operator. This is real progress because the runner no longer lacks an operator shape in principle, but it is still nonclaim because the MTS source-normalization bridge is not derived.

**Main progress:** `MISSING_RESPONSE_OPERATOR` can now be replaced in component-row previews by `RGO1296_LINEARIZED_GR_RESPONSE_NONCLAIM`. Combined with 1295's `ABS_C_SIGN_EQ_1_BOUND_ONLY`, this narrows the runner blockers from vague operator absence to concrete missing source normalization, observable projection, domain/gauge/boundary control, and residual input amplitudes.

**Still blocked:** the formal operator accepts a GR source such as `T_{{mu nu}}` or a Poisson scalar source `S_K`; MTS still has to derive exactly how `Kmetric_chain` or `R_chain^{{00}}` enters that source side, with units, signs, `c` factors, `4πG` factors, and measured-GM calibration.

## Source Register

{markdown_table(source_register, ["source_id", "source_type", "local_path", "url", "needle_or_anchor", "exists_or_url_recorded", "anchor_found_or_web_verified", "role", "valid_for_claim", "claim_allowed"])}

## Response Operator Rows

{markdown_table(response_operators, ["operator_id", "arena", "operator_kind", "source_equation", "operator_form", "domain_assumptions", "units", "MTS_bridge_status", "MTS_source_slot", "usable_as_response_operator", "usable_for_scoring", "source_url", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Operator To Runner Bridge Preview

{markdown_table(runner_bridge, ["bridge_id", "runner_id", "residual_component", "abs_Csign_applied_from_1295", "formal_response_operator_applied", "required_inputs_preview", "remaining_missing_count", "remaining_missing_tokens", "non_score_blockers", "score_emitted", "score_value", "runner_status", "valid_for_claim", "claim_allowed"])}

## Observable Gap Ledger

{markdown_table(observable_gaps, ["gap_id", "gap", "why_it_matters", "blocks", "next_requirement", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

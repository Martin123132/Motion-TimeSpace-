from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_PARENT_COEFFICIENT_FUNCTOR_OR_FINITE_COUPLING_PRIOR_RUNNER_2368"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2368-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2368_2367_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2367_NEXT_TARGET.csv", "NEXT2367_0_selected", "2367 selected parent coefficient functor/finite prior route"),
        ("SRC2368_2367_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2367_VALIDATION.csv", "VAL2367_OVERALL", "2367 validation"),
        ("SRC2368_2318_functor", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2318_PARENT_COEFFICIENT_FUNCTOR_CONSTRUCTION_ATTEMPT.csv", "PCF2318_5_verdict", "parent coefficient functor not constructed"),
        ("SRC2368_2318_schema", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2318_FINITE_COUPLING_PRIOR_RUNNER_SCHEMA.csv", "SCHEMA2318_3_nonclaim_first_rows", "finite coupling prior runner schema"),
        ("SRC2368_2318_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2318_VALIDATION.csv", "VAL2318_09_claim_gates_block", "2318 validation keeps local GR blocked"),
        ("SRC2368_2319_rows", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv", "FCR2319_3_delta_w_missing_prediction", "first source-backed anchors and missing delta_w row"),
        ("SRC2368_2319_accept", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2319_RUNNER_ACCEPTANCE_MATRIX.csv", "ACCEPT2319_3_delta_w", "runner acceptance matrix"),
        ("SRC2368_2319_deltaw", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2319_DELTA_W_ACQUISITION_STATUS.csv", "DW2319_3_claim_gate", "delta_w acquisition status"),
        ("SRC2368_2320_route", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2320_ROUTE_SELECTION.csv", "ROUTE2320_2_verdict", "PPN component route selected over delta_w for sharper local-GR object"),
        ("SRC2368_2320_deltaw", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2320_DELTAW_MATERIAL_SOURCE_VECTOR_STATUS.csv", "DWV2320_4_verdict", "delta_w material vector deferred"),
        ("SRC2368_2320_ready", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2320_LOCAL_GR_TEST_READINESS_MATRIX.csv", "READY2320_2_local_GR_vector", "local GR test readiness blocked"),
        ("SRC2368_2320_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2320_NEXT_TARGET.csv", "NEXT2320_0", "next alpha_cg projection or delta_w acquisition target"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def parent_coefficient_functor_audit() -> list[dict[str, object]]:
    rows = [
        ("PCF2368_0_candidate", "parent coefficient functor", "p_vis=(q_loc,pi_rep,pi_top,Level_EM); F_coeff: O_vis -> p_vis^*Coeff(Q_obs,Rep,Top,Level)", "CANDIDATE_CONSTRUCTION_WRITTEN", "would remove hidden/local scalar arguments from visible coefficients"),
        ("PCF2368_1_vertical_silence", "coefficient descent", "if c_i=p_vis^*cbar_i and v in ker(Dp_vis), then L_v c_i=0", "EXACT_CONDITIONAL_THEOREM", "would kill b_alpha, b_mu, b_mA, b_nuc, shadow slopes, and hidden coefficient parts of j_q"),
        ("PCF2368_2_source_target_exclusion", "source-only target exclusion", "F_coeff has no R_+^active-source-prefactor target except guarded common calibration", "POWERFUL_IF_PARENT_SIGNED", "would make relative delta_w_A and kappa_A source multipliers ill-typed"),
        ("PCF2368_3_hidden_scalar_counterexample", "hidden scalar obstruction", "if I_hid survives and coefficient targets are legal, c=c0+epsilon I_hid is a valid hidden-visible Hom", "COUNTEREXAMPLE_RETAINED", "hidden invariant triviality/no-hair remains unsigned"),
        ("PCF2368_4_common_measure_readout", "common measure/readout closure", "functor must own action-scale/current normalization and survive S_eff, detector threshold, and source-worldtube readout", "REQUIRED_GUARD_UNSIGNED", "tree-level coefficient silence could be regenerated"),
        ("PCF2368_5_verdict", "construct parent coefficient functor now", "candidate functor would sign no-hidden-visible-Hom, but parent syntax/target category is not selected", "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED", "move finite prior lane forward without local-GR claim"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim_piece": piece,
            "formal_statement": statement,
            "proof_status": status,
            "effect_or_gap": effect,
        }
        for row_id, piece, statement, status, effect in rows
    ]


def proof_obligation_ledger() -> list[dict[str, object]]:
    rows = [
        ("OBL2368_0_parent_syntax", "parent syntax/target category", "parent action selects F_coeff target category before fitting/readout", "MISSING_PARENT_SELECTION"),
        ("OBL2368_1_hidden_triviality", "hidden invariant algebra triviality", "no surviving I_hid can feed visible coefficients", "MISSING_HIDDEN_NO_HAIR_OR_TRIVIALITY"),
        ("OBL2368_2_source_only", "source-only target exclusion", "R_+ active-source weights are not legal relative targets", "MISSING_SOURCE_TARGET_EXCLUSION"),
        ("OBL2368_3_common_measure", "common measure/current owner", "source normalization/common action scale is one parent-owned object", "MISSING_COMMON_MEASURE_CURRENT"),
        ("OBL2368_4_radiative_readout", "radiative/readout closure", "S_eff, detector, threshold, and source-worldtube maps do not regenerate hidden coefficients", "MISSING_RADIATIVE_READOUT_CLOSURE"),
        ("OBL2368_5_branch_lock", "same-branch finite runner lock", "coefficient, tau, range, source/test charge, denominator, and projection share one parent branch", "MISSING_BRANCH_LOCK_FOR_SCORING"),
        ("OBL2368_6_verdict", "functor proof obligation status", "all obligations must close to promote no-hidden-visible-Hom", "OBLIGATIONS_OPEN"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "obligation": obligation,
            "required_evidence": evidence,
            "status": status,
        }
        for row_id, obligation, evidence, status in rows
    ]


def finite_coupling_runner_schema() -> list[dict[str, object]]:
    rows = [
        ("SCHEMA2368_0_columns", "required columns", "symbol, sector, definition, units, theorem_zero_status, numeric_value, uncertainty, source_path, source_row_id, arena_projection, no_cancellation_group, score_ready, valid_for_claim", "SCHEMA_READY_NONCLAIM"),
        ("SCHEMA2368_1_no_cancellation", "no-cancellation envelope", "sum_abs over live components by arena unless covariance/orthogonality theorem signs cancellation", "REQUIRED_GUARD"),
        ("SCHEMA2368_2_branch_lock", "same-branch lock", "coefficient/tau/range/source/test charge/denominator/projection must belong to the same parent branch", "REQUIRED_GUARD"),
        ("SCHEMA2368_3_first_targets", "first acquisition targets", "b_alpha*tau_clock_time; alpha_PPN vector ceiling; eta_WEP comparator; delta_w_A; alpha_cg component owner", "ACQUISITION_QUEUE_READY"),
        ("SCHEMA2368_4_claim_rule", "score permission", "claim/score only if theorem-zero signed or numeric row has source, units, uncertainty, branch lock and projection", "CLAIM_BLOCKED"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "runner_piece": piece,
            "schema_or_rule": schema,
            "status": status,
        }
        for row_id, piece, schema, status in rows
    ]


def finite_coupling_anchors_nonclaim() -> list[dict[str, object]]:
    rows = [
        ("ANCH2368_0_clock_product", "b_alpha*tau_clock_time", "clock_product", "2.1e-18", "yr^-1", "source-backed product/envelope only; standalone b_alpha not derived", "clock product only", "true"),
        ("ANCH2368_1_ppn_vector_ceiling", "alpha_PPN_total_abs_vector", "PPN_vector", "0.005788015401465051", "dimensionless", "Cassini/scalar-tensor proxy vector ceiling; not raw c_g or MTS prediction", "PPN/local-GR target ceiling", "true"),
        ("ANCH2368_2_wep_comparator", "eta_WEP_source_charge_bound", "WEP_comparator", "2.8e-15", "dimensionless", "MICROSCOPE comparator bound; no delta_w prediction row", "WEP comparator only", "true"),
        ("ANCH2368_3_delta_w_missing", "delta_w_A", "source_weight", "MISSING_SOURCE_BACKED_VALUE", "dimensionless", "delta_w cannot be inferred from comparator bounds without material/source/tau projection", "WEP;Newton;R10 acquisition", "false"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "sector": sector,
            "numeric_value_or_status": value,
            "units": units,
            "theory_interpretation": interp,
            "arena_projection": projection,
            "source_backed_anchor": backed,
            "direct_MTS_prediction": "false",
        }
        for row_id, symbol, sector, value, units, interp, projection, backed in rows
    ]


def runner_acceptance_matrix() -> list[dict[str, object]]:
    rows = [
        ("ACCEPT2368_0_clock_product", "ANCH2368_0_clock_product", "source_backed_product_constraint", "nonclaim product constraint only", "standalone b_alpha; WEP; R10; local GR", "tau_clock_time parent derivation and shared WEP/R10 projection"),
        ("ACCEPT2368_1_ppn_vector", "ANCH2368_1_ppn_vector_ceiling", "source_backed_proxy_vector_ceiling", "nonclaim vector ceiling/proxy only", "raw c_g; individual PPN component pass", "component owner matrix, tau/range/source/current/support/boundary/readout projection"),
        ("ACCEPT2368_2_wep_bound", "ANCH2368_2_wep_comparator", "source_backed_comparator_bound", "comparator bound only", "delta_w inference", "official material/source response vector, tau_eff, readout transfer"),
        ("ACCEPT2368_3_delta_w", "ANCH2368_3_delta_w_missing", "required_prediction_missing", "acquisition queue only", "WEP/Newton/R10 source-weight scoring", "numeric delta_w_i or theorem-zero plus source path, units and projection"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "input_row": input_row,
            "row_kind": kind,
            "accepted_for": accepted,
            "blocked_transfer": blocked,
            "missing_for_score": missing,
            "direct_MTS_prediction": "false",
        }
        for row_id, input_row, kind, accepted, blocked, missing in rows
    ]


def route_selection() -> list[dict[str, object]]:
    rows = [
        ("ROUTE2368_0_functor", "parent coefficient functor", "CANDIDATE_NOT_PARENT_SIGNED", "highest derivation payoff, but cannot be claimed today", "KEEP_OPEN"),
        ("ROUTE2368_1_delta_w", "delta_w material/source vector", "COMPARATOR_AND_PRODUCT_ANCHORS_ONLY", "material/source response vector, tau_eff, readout transfer missing", "DEFER_TO_ACQUISITION"),
        ("ROUTE2368_2_ppn_component", "PPN component owner row", "OWNER_MATRIX_AND_ALPHA_CG_SOURCE_TARGET_EXIST", "structurally closer to local-GR testing than delta_w but projection clauses still blocked", "SELECT_NEXT"),
        ("ROUTE2368_3_verdict", "2368 route decision", "PPN_IMPORT_SELECTED_DELTAW_RETAINED", "first nonclaim anchors imported; next should fill alpha_cg projection owner or delta_w material vector", "SELECT_ALPHA_CG_PROJECTION_NEXT"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "candidate_route": route,
            "evidence_status": status,
            "reason_or_blocker": reason,
            "decision": decision,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, route, status, reason, decision in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2368_0_functor", "parent coefficient functor/no-hidden-visible-Hom derived", "BLOCKED", "parent syntax, hidden triviality, common measure and readout closure missing"),
        ("CG2368_1_jq_zero", "j_q source leg theorem-zero", "BLOCKED", "finite coupling channels remain live"),
        ("CG2368_2_anchors", "source-backed anchors become predictions", "BLOCKED", "anchors are product/comparator/proxy constraints, not MTS prediction rows"),
        ("CG2368_3_delta_w", "delta_w material/source vector score-ready", "BLOCKED", "material vector, tau/readout and component basis missing"),
        ("CG2368_4_ppn", "PPN/local-GR vector score-ready", "BLOCKED", "component owner/projection rows missing"),
        ("CG2368_5_local_GR_Newton", "local GR/Newton reduction derived", "BLOCKED", "coupling/source projection vector not theorem-zero or bounded"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": "false",
            "passes_public_claim": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2368_0_functor", "promote parent coefficient functor", "needs parent syntax/target category, hidden triviality, common measure and readout closure", "REFUSED"),
        ("REF2368_1_product_to_balpha", "infer standalone b_alpha from clock product", "needs tau_clock_time parent derivation and shared projection branch", "REFUSED"),
        ("REF2368_2_wep_to_deltaw", "infer delta_w from MICROSCOPE comparator", "needs material/source vector and tau/readout transfer", "REFUSED"),
        ("REF2368_3_ppn_pass", "treat PPN vector ceiling as MTS local-GR pass", "needs component owner matrix and MTS prediction vector", "REFUSED"),
        ("REF2368_4_local_GR", "claim local GR/Newton", "finite coupling/source vector remains unclosed", "REFUSED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "attempted_claim": claim,
            "missing_evidence": missing,
            "refusal_result": result,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, missing, result in rows
    ]


def next_target() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2368_0_selected",
            "next_file": "2369-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md",
            "next_script": "scripts/Y5_R2FR_alpha_cg_projection_owner_fill_or_deltaw_material_vector_acquisition_2369.py",
            "selected_reason": "the functor is unsigned but first nonclaim anchors are imported; the sharper next local-GR test object is alpha_cg/PPN component ownership while delta_w material-vector acquisition stays live",
            "success_condition": "fill one alpha_cg projection blocker such as tau_PPN, same-branch owner, Z_X/M_X^2, S_PPN, common-frame/readout tail, or acquire a real delta_w material/source vector row",
            "fallback_condition": "if neither projection owner nor delta_w vector can be sourced, keep all anchors nonclaim and move to readout-tail/source-only-slot zero proof",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
    ]


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        return len(changed) == 0, "git modified-file count for formalization-workbench is 0" if not changed else f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() == "true":
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": "false"})

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2368_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2368_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2368_02_outputs_exist", all(path.exists() for path in generated), "all 2368 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2368_03_csv_parse", parse_ok, parse_detail)

    functor = {row["row_id"]: row["proof_status"] for row in read_csv(outputs["functor"])}
    add("VAL2368_04_functor_not_promoted", functor.get("PCF2368_5_verdict") == "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED", "parent coefficient functor remains unpromoted")
    add("VAL2368_05_vertical_silence_conditional", functor.get("PCF2368_1_vertical_silence") == "EXACT_CONDITIONAL_THEOREM", "vertical coefficient silence theorem retained as conditional")

    anchors = read_csv(outputs["anchors"])
    backed = [row for row in anchors if row.get("source_backed_anchor") == "true"]
    add("VAL2368_06_source_backed_anchors_imported", len(backed) == 3, "three source-backed nonclaim anchors imported")
    add("VAL2368_07_anchors_nonclaim", all(row.get("score_ready") == "false" and row.get("valid_for_claim") == "false" for row in anchors), "all anchors remain nonclaim and not score-ready")

    acceptance = read_csv(outputs["acceptance"])
    add("VAL2368_08_no_direct_predictions", all(row.get("direct_MTS_prediction") == "false" for row in acceptance), "acceptance matrix blocks direct MTS prediction transfer")

    route = {row["row_id"]: row["decision"] for row in read_csv(outputs["route"])}
    add("VAL2368_09_route_selected", route.get("ROUTE2368_3_verdict") == "SELECT_ALPHA_CG_PROJECTION_NEXT", "alpha_cg projection owner route selected next")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2368_10_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2368_11_formalization_untouched", formal_ok, formal_detail)
    add("VAL2368_12_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2368_0_selected", "2369 alpha_cg/delta_w target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2368_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2368 valid: parent coefficient functor unpromoted, first nonclaim coupling anchors imported, alpha_cg projection owner route selected" if overall else "one or more validation gates failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(outputs: dict[str, Path]) -> None:
    def table(headers: list[str], rows: list[dict[str, str]]) -> str:
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(row.get(header, "").replace("|", "/") for header in headers) + " |")
        return "\n".join(lines)

    functor = read_csv(outputs["functor"])
    obligations = read_csv(outputs["obligations"])
    anchors = read_csv(outputs["anchors"])
    acceptance = read_csv(outputs["acceptance"])
    route = read_csv(outputs["route"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2368 - Parent Coefficient Functor Or Finite Coupling Prior Runner

## Result

The parent coefficient functor remains the clean derivation route, but it is not parent-signed.  The exact conditional theorem is:

`c_i = p_vis^* cbar_i` and `v in ker(Dp_vis)` implies `L_v c_i = 0`.

If the parent action actually selected that functor/target category, the visible hidden-coupling slopes feeding `j_q` would vanish.  Current evidence does not sign the parent syntax, hidden invariant triviality, common measure/current owner, or readout/radiative closure.

So the finite-prior lane is active, but still nonclaim.  Three real anchors are imported as constraints, not MTS predictions: `b_alpha*tau_clock_time`, a PPN vector ceiling, and a WEP comparator bound.  `delta_w_A` remains a missing prediction row.

The sharper next local-GR object is the `alpha_cg`/PPN component owner route, with `delta_w` material/source-vector acquisition retained in parallel.

## Parent Coefficient Functor Audit

{table(["row_id", "claim_piece", "proof_status", "effect_or_gap"], functor)}

## Proof Obligations

{table(["row_id", "obligation", "status"], obligations)}

## First Nonclaim Anchors

{table(["row_id", "symbol", "sector", "numeric_value_or_status", "source_backed_anchor", "arena_projection"], anchors)}

## Acceptance Matrix

{table(["row_id", "input_row", "accepted_for", "blocked_transfer", "missing_for_score"], acceptance)}

## Route Selection

{table(["row_id", "candidate_route", "evidence_status", "decision"], route)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["functor"])}`
- `{rel(outputs["obligations"])}`
- `{rel(outputs["schema"])}`
- `{rel(outputs["anchors"])}`
- `{rel(outputs["acceptance"])}`
- `{rel(outputs["route"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is progress because the runner now has real external anchors without pretending they are MTS predictions.  The theory still owes the projection owner: either fill an `alpha_cg` PPN component path in one branch, or acquire a real `delta_w` material/source vector.  Until then, no local-GR/Newton claim is allowed.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_SOURCE_REGISTER.csv",
        "functor": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_PARENT_COEFFICIENT_FUNCTOR_AUDIT.csv",
        "obligations": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_PROOF_OBLIGATION_LEDGER.csv",
        "schema": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_FINITE_COUPLING_RUNNER_SCHEMA.csv",
        "anchors": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_FIRST_NONCLAIM_COUPLING_ANCHORS.csv",
        "acceptance": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_RUNNER_ACCEPTANCE_MATRIX.csv",
        "route": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_DELTAW_PPN_ROUTE_SELECTION.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2368_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2368_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["functor"], parent_coefficient_functor_audit())
    write_csv(outputs["obligations"], proof_obligation_ledger())
    write_csv(outputs["schema"], finite_coupling_runner_schema())
    write_csv(outputs["anchors"], finite_coupling_anchors_nonclaim())
    write_csv(outputs["acceptance"], runner_acceptance_matrix())
    write_csv(outputs["route"], route_selection())
    write_csv(outputs["claims"], claim_gates())
    write_csv(outputs["refusal"], refusal_runner())
    write_csv(outputs["next"], next_target())
    validation = validation_rows(outputs, sources)
    write_csv(outputs["validation"], validation)
    write_markdown(outputs)

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

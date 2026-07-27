from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_ALPHA_CG_PROJECTION_OWNER_OR_DELTAW_MATERIAL_VECTOR_2369"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2369-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md"
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
        ("SRC2369_2368_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2368_NEXT_TARGET.csv", "NEXT2368_0_selected", "2368 selected alpha_cg/delta_w route"),
        ("SRC2369_2368_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2368_VALIDATION.csv", "VAL2368_OVERALL", "2368 validation"),
        ("SRC2369_2321_blockers", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2321_ALPHA_CG_PROJECTION_BLOCKER_AUDIT.csv", "ACG2321_6_verdict", "alpha_cg projection blockers"),
        ("SRC2369_2321_fills", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2321_CONDITIONAL_FILL_ROWS.csv", "CF2321_2_alpha_cg_normal_form", "conditional alpha_cg normal form"),
        ("SRC2369_2321_ready", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2321_SCORE_READINESS.csv", "READY2321_2_local_GR", "score readiness blocked"),
        ("SRC2369_2321_delta", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2321_DELTAW_MATERIAL_VECTOR_ACQUISITION_LEDGER.csv", "DWA2321_3_verdict", "delta_w acquisition ledger"),
        ("SRC2369_2322_tau", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2322_TAU_PPN_COMMON_FRAME_DERIVATION_AUDIT.csv", "TPA2322_4_verdict", "tau_PPN/common-frame audit"),
        ("SRC2369_2322_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2322_NEXT_TARGET.csv", "NEXT2322_0", "common-frame/readout target"),
        ("SRC2369_2323_frame", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2323_COMMON_FRAME_THEOREM_ATTEMPT.csv", "CFT2323_4_verdict", "common-frame theorem not derived"),
        ("SRC2369_2323_readout", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2323_ALPHA_READOUT_TAIL_ROW.csv", "ART2323_3_no_cancellation", "alpha_readout retained"),
        ("SRC2369_2323_feedback", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2323_SOURCE_FEEDBACK_COMMUTATOR_BRIDGE.csv", "SFC2323_2_countermodel", "source feedback commutator"),
        ("SRC2369_2323_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2323_NEXT_TARGET.csv", "NEXT2323_0", "readout-tail next target"),
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


def alpha_cg_projection_audit() -> list[dict[str, object]]:
    rows = [
        ("ACG2369_0_normal_form", "alpha_cg^PPN", "alpha_cg^PPN=tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)", "NORMAL_FORM_LOCKED_NONCLAIM", "raw c_g is forbidden as a score object"),
        ("ACG2369_1_common_frame", "universal common matter frame", "ordinary matter, rods, clocks, source masses, and Cassini/Shapiro readout use one parent-signed matter frame", "NOT_PARENT_SIGNED", "blocks treating alpha_cg as actual Cassini leg"),
        ("ACG2369_2_same_branch", "same-branch Xhat owner", "c_g, Z_X, M_X^2, lambda_X, S_PPN, tau_PPN and tails must belong to one branch", "MISSING_PARENT_OWNER", "prevents mixing closure and finite rows"),
        ("ACG2369_3_ZX", "canonical normalization", "N_X=1/sqrt(Z_X)", "RELATION_FILLED_VALUE_MISSING", "positive numeric/source-backed Z_X absent"),
        ("ACG2369_4_lambda_SPPN", "range/screening transfer", "lambda_X=sqrt(Z_X/M_X^2); screening is S_PPN(lambda_X,env)", "LAMBDA_RELATION_FILLED_SPPN_MISSING", "M_X^2 and Cassini geometry map absent"),
        ("ACG2369_5_tau_PPN", "PPN projection coefficient", "tau_PPN=1 only inside strict common-frame scalar-tensor branch", "EXACT_CONDITIONAL_NOT_ACTIVE", "active branch lacks common-frame/readout signature"),
        ("ACG2369_6_vector_tails", "other PPN vector tails", "disformal, non-Hilbert, support/domain, boundary, calibration and readout tails", "VECTOR_TAILS_UNCONTROLLED", "must be zero-proved or bounded"),
        ("ACG2369_7_verdict", "alpha_cg score-ready component", "normal form is locked but no score-ready local-GR component exists", "NOT_SCORE_READY", "move to common-frame/readout-tail proof or bound"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "projection_clause": clause,
            "formula_or_requirement": formula,
            "current_status": status,
            "effect_or_blocker": effect,
        }
        for row_id, clause, formula, status, effect in rows
    ]


def tau_common_frame_audit() -> list[dict[str, object]]:
    rows = [
        ("TAU2369_0_common_frame_premise", "universal common matter frame", "S_matter uses one metric/coframe for ordinary matter, clocks, source masses and readout", "CONDITIONAL_PREMISE_ONLY", "parent ordinary-matter signature not derived"),
        ("TAU2369_1_tau_one", "tau_PPN normalization", "standard scalar-tensor common-frame branch gives gamma-1=-2 alpha_eff^2/(1+alpha_eff^2), so tau_PPN=1 by definition", "EXACT_CONDITIONAL_TAU_EQUALS_ONE", "not active until common-frame branch is signed"),
        ("TAU2369_2_screening_split", "tau versus screening", "tau_PPN is projection normalization; finite range/screening belongs in S_PPN(lambda_X,env)", "DECOMPOSITION_LOCKED", "prevents hiding screening inside tau"),
        ("TAU2369_3_readout_tail", "observed PPN readout", "fixed-before-readout, measured-GM and PPN-gauge maps must not add alpha_readout/calibration tails", "NOT_DERIVED", "tail remains explicit"),
        ("TAU2369_4_verdict", "set tau_PPN=1 in active scoring", "allowed only inside parent-signed common-frame scalar-tensor branch", "NOT_ALLOWED_YET", "retain alpha_readout and projection blockers"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "target": target,
            "statement": statement,
            "result": result,
            "effect_or_gap": gap,
        }
        for row_id, target, statement, result, gap in rows
    ]


def delta_w_acquisition_status() -> list[dict[str, object]]:
    rows = [
        ("DWA2369_0_bound_anchor", "delta_w comparator/product anchor", "MICROSCOPE/source product ceiling exists", "ANCHOR_EXISTS_PREDICTION_MISSING", "MTS material/source prediction vector missing"),
        ("DWA2369_1_material_vector", "Ti/Pt or source-test material vector", "species/material basis, charge weights, nuclear/electronic/mass response decomposition", "ACQUISITION_REQUIRED", "parent-signed map from coefficient shifts to test-mass response missing"),
        ("DWA2369_2_tau_readout", "tau_WEP/readout transfer", "experiment geometry/readout projection and no-cancellation rule", "ACQUISITION_REQUIRED", "tau_WEP operator/readout tail theorem missing"),
        ("DWA2369_3_verdict", "delta_w score object", "held as fallback lane", "DEFERRED_NONCLAIM", "build after alpha_cg projection normal form path is settled"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "needed_object": obj,
            "current_evidence": evidence,
            "status": status,
            "missing_input": missing,
        }
        for row_id, obj, evidence, status, missing in rows
    ]


def readout_tail_matrix() -> list[dict[str, object]]:
    rows = [
        ("ART2369_0_alpha_readout", "alpha_readout", "alpha_readout = Pi_gamma[Delta_cal + Delta_PPN + C_feedback + C_protocol]", "RETAINED_NONCLAIM_COMPONENT", "numeric/source-backed tail values or theorem-zero certificates missing"),
        ("ART2369_1_source_feedback", "C_feedback", "D_v(Pi_A J_A)=[D_sigma Pi_A[J_A]+Pi_A D_sigma J_A]D_v sigma_A", "NORMAL_FORM_DERIVED_VALUES_MISSING", "operator norms and epsilon_sigma_A missing"),
        ("ART2369_2_protocol_tail", "C_protocol", "zero only if masks/support/orbit windows/boundary transport are fixed external protocol or q/e_obs descendants", "CLOSURE_OR_SOURCE_REQUIRED", "parent declaration or finite bound missing"),
        ("ART2369_3_commutator_zero", "source/readout commutator zero route", "if Pi_A and J_A descend through q/e_obs/theta, D_v(Pi_A J_A)=0 for v in ker(Dq)", "EXACT_CONDITIONAL_ZERO_UNSIGNED", "sector descent certificates missing"),
        ("ART2369_4_no_cancellation", "absolute PPN readout envelope", "abs(alpha_total)<=sum_abs(alpha_cg,alpha_dis,alpha_nonH,alpha_support,alpha_boundary,alpha_readout)", "ENVELOPE_ACTIVE_VALUES_MISSING", "all component values/theorem-zero rows missing"),
        ("ART2369_5_verdict", "active PPN obstruction", "common-frame theorem not derived; retain alpha_readout as explicit component", "READOUT_TAIL_SELECTED_NEXT", "next target is zero proof or first alpha_readout bound"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "component": component,
            "formula_or_statement": formula,
            "current_status": status,
            "missing_for_bound": missing,
        }
        for row_id, component, formula, status, missing in rows
    ]


def score_readiness() -> list[dict[str, object]]:
    rows = [
        ("READY2369_0_alpha_normal_form", "alpha_cg^PPN", "conditional normal form locked", "same-branch owner, Z_X, M_X^2, S_PPN, tau_PPN, common frame, vector tails"),
        ("READY2369_1_delta_w", "delta_w material/source vector", "acquisition lane retained", "material vector and tau/readout missing"),
        ("READY2369_2_readout_tail", "alpha_readout", "explicit PPN tail retained", "Delta_cal, Delta_PPN, C_feedback, C_protocol values or zero certificates missing"),
        ("READY2369_3_local_GR", "local GR/Newton recovery", "raw c_g loophole closed by normal-form rule", "full no-cancellation PPN/local residual vector not theorem-zero or bounded"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "test_object": obj,
            "progress": progress,
            "remaining_blocker": blocker,
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, obj, progress, blocker in rows
    ]


def route_selection() -> list[dict[str, object]]:
    rows = [
        ("DEC2369_0_alpha_cg", "alpha_cg PPN component owner", 1, "NORMAL_FORM_LOCKED_SCORE_BLOCKED", "best current local-GR test object, but projection owner/common-frame/readout blockers remain"),
        ("DEC2369_1_tau", "set tau_PPN=1", 3, "KEEP_CONDITIONAL_NOT_ACTIVE", "exact only in parent-signed common-frame scalar-tensor branch"),
        ("DEC2369_2_delta_w", "delta_w material/source vector", 2, "RETAIN_FALLBACK_ACQUISITION", "needs material vector and tau/readout transfer"),
        ("DEC2369_3_readout_tail", "alpha_readout zero proof or first bound", 1, "SELECT_NEXT_TARGET", "common-frame theorem stalls on readout/projector/support descent"),
        ("DEC2369_4_no_source_only", "NoSourceOnlySpeciesSlot syntax proof", 2, "PARALLEL_CLEANER_ROUTE", "could forbid relative source weights before they become readout tails"),
        ("DEC2369_5_empirical", "score local-GR vector", 5, "DEFER", "component vector is not theorem-zero or bounded"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "rank": rank,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2369_0_alpha_cg", "alpha_cg PPN component score-ready", "BLOCKED", "same branch owner/common frame/tau/readout/vector tail blockers remain"),
        ("CG2369_1_tau", "tau_PPN=1 active branch", "BLOCKED", "common-frame scalar-tensor branch not parent-signed"),
        ("CG2369_2_delta_w", "delta_w material/source vector score-ready", "BLOCKED", "material response tensor and tau/readout transfer missing"),
        ("CG2369_3_readout", "alpha_readout zero or bound ready", "BLOCKED", "readout/support/projector descent or numeric tail bound missing"),
        ("CG2369_4_local_GR", "local GR/Newton reduction derived", "BLOCKED", "PPN/local residual vector not closed"),
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
        ("REF2369_0_raw_cg", "score raw c_g", "raw c_g is not invariant under Xhat rescaling; use alpha_cg normal form", "REFUSED"),
        ("REF2369_1_tau_one", "set tau_PPN=1 now", "common-frame parent signature and readout-tail zero are unsigned", "REFUSED"),
        ("REF2369_2_cassini_pass", "treat PPN ceiling as local-GR pass", "MTS alpha_cg prediction vector not source-backed", "REFUSED"),
        ("REF2369_3_delta_w", "infer delta_w from WEP comparator", "material/source vector and tau/readout transfer missing", "REFUSED"),
        ("REF2369_4_local_GR", "claim local GR/Newton", "alpha_readout/readout/source tails remain open", "REFUSED"),
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
            "row_id": "NEXT2369_0_selected",
            "next_file": "2370-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md",
            "next_script": "scripts/Y5_R2FR_readout_tail_zero_proof_or_first_alpha_readout_bound_2370.py",
            "selected_reason": "alpha_cg normal form is locked but common-frame/readout signatures remain unsigned; alpha_readout is now the active PPN obstruction",
            "success_condition": "prove projector/support/readout descent enough to set alpha_readout=0, or fill a first source-backed alpha_readout tail bound row",
            "fallback_condition": "if readout zero/bound cannot be sourced, attempt the parallel NoSourceOnlySpeciesSlot syntax proof while keeping alpha_cg and delta_w nonclaim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2369_1_parallel",
            "next_file": "2370b-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-syntax-proof.md",
            "next_script": "scripts/Y5_R2FR_NoSourceOnlySpeciesSlot_parent_syntax_proof_2370b.py",
            "selected_reason": "parallel cleaner route: forbid relative source/species weights before they become readout/source tails",
            "success_condition": "derive parent syntax excluding source-only species slots, or stage finite delta_w/source-weight rows",
            "fallback_condition": "retain delta_w/source weights as nonclaim finite priors",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
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
    add("VAL2369_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2369_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2369_02_outputs_exist", all(path.exists() for path in generated), "all 2369 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2369_03_csv_parse", parse_ok, parse_detail)

    alpha = {row["row_id"]: row["current_status"] for row in read_csv(outputs["alpha"])}
    add("VAL2369_04_alpha_normal_form", alpha.get("ACG2369_0_normal_form") == "NORMAL_FORM_LOCKED_NONCLAIM", "alpha_cg normal form locked nonclaim")
    add("VAL2369_05_alpha_not_score_ready", alpha.get("ACG2369_7_verdict") == "NOT_SCORE_READY", "alpha_cg not score-ready")

    tau = {row["row_id"]: row["result"] for row in read_csv(outputs["tau"])}
    add("VAL2369_06_tau_conditional", tau.get("TAU2369_1_tau_one") == "EXACT_CONDITIONAL_TAU_EQUALS_ONE", "tau_PPN=1 retained only as conditional")
    add("VAL2369_07_tau_not_allowed", tau.get("TAU2369_4_verdict") == "NOT_ALLOWED_YET", "active tau_PPN claim blocked")

    readout = {row["row_id"]: row["current_status"] for row in read_csv(outputs["readout"])}
    add("VAL2369_08_readout_selected", readout.get("ART2369_5_verdict") == "READOUT_TAIL_SELECTED_NEXT", "alpha_readout/readout tail selected next")

    readiness = read_csv(outputs["ready"])
    add("VAL2369_09_readiness_nonclaim", all(row.get("score_ready") == "false" for row in readiness), "all readiness rows remain not score-ready")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2369_10_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2369_11_formalization_untouched", formal_ok, formal_detail)
    add("VAL2369_12_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2369_0_selected", "2370 readout-tail target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2369_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2369 valid: alpha_cg normal form locked, tau_PPN conditional only, alpha_readout/readout-tail route selected next" if overall else "one or more validation gates failed",
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

    alpha = read_csv(outputs["alpha"])
    tau = read_csv(outputs["tau"])
    delta = read_csv(outputs["delta"])
    readout = read_csv(outputs["readout"])
    decisions = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2369 - alpha_cg Projection Owner Fill Or delta_w Material Vector Acquisition

## Result

The local-GR score object is now narrowed:

`alpha_cg^PPN = tau_PPN * S_PPN(lambda_X, env) * c_g / sqrt(Z_X)`.

Raw `c_g` is forbidden because it is not invariant under `Xhat` rescaling.  This is a useful lock.  But it is not a pass: the same-branch owner, `Z_X`, `M_X^2`, `S_PPN`, common frame, and vector/readout tails remain open.

The best mathematical fill is `tau_PPN=1`, but only in a parent-signed common-frame scalar-tensor branch.  That branch is not signed here, so `tau_PPN=1` cannot be used in active scoring.  The active obstruction is now `alpha_readout`: calibration, PPN-gauge, source-feedback and protocol tails.

## alpha_cg Projection Audit

{table(["row_id", "projection_clause", "current_status", "effect_or_blocker"], alpha)}

## tau_PPN / Common Frame Audit

{table(["row_id", "target", "result", "effect_or_gap"], tau)}

## delta_w Acquisition Status

{table(["row_id", "needed_object", "status", "missing_input"], delta)}

## Readout Tail Matrix

{table(["row_id", "component", "current_status", "missing_for_bound"], readout)}

## Route Selection

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["alpha"])}`
- `{rel(outputs["tau"])}`
- `{rel(outputs["delta"])}`
- `{rel(outputs["readout"])}`
- `{rel(outputs["ready"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a good narrowing step.  We are no longer waving at PPN in general: the branch has a legal score object and a named obstruction.  Next target is to either prove the readout/support/projector tail is zero or put a first bound on `alpha_readout`.  `delta_w` remains a live fallback, not a shortcut.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_SOURCE_REGISTER.csv",
        "alpha": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_ALPHA_CG_PROJECTION_AUDIT.csv",
        "tau": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_TAU_PPN_COMMON_FRAME_AUDIT.csv",
        "delta": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_DELTAW_ACQUISITION_STATUS.csv",
        "readout": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_READOUT_TAIL_MATRIX.csv",
        "ready": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_SCORE_READINESS.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_DECISION_LEDGER.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2369_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2369_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["alpha"], alpha_cg_projection_audit())
    write_csv(outputs["tau"], tau_common_frame_audit())
    write_csv(outputs["delta"], delta_w_acquisition_status())
    write_csv(outputs["readout"], readout_tail_matrix())
    write_csv(outputs["ready"], score_readiness())
    write_csv(outputs["decision"], route_selection())
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

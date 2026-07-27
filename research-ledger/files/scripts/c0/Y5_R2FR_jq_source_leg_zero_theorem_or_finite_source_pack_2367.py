from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_JQ_SOURCE_LEG_ZERO_THEOREM_OR_FINITE_SOURCE_PACK_2367"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2367-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md"
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
        "numeric_value_present": "false",
        "source_backed": "false",
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
        ("SRC2367_2366_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2366_NEXT_TARGET.csv", "NEXT2366_0_selected", "2366 selected j_q numerator/source-leg route"),
        ("SRC2367_2366_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2366_VALIDATION.csv", "VAL2366_OVERALL", "2366 validation"),
        ("SRC2367_2316_zero", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2316_JQ_ZERO_THEOREM_TRANSFER.csv", "JQZ2316_3_current_corpus_verdict", "j_q zero theorem transferred but not promoted"),
        ("SRC2367_2316_pack", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2316_FINITE_JQ_SOURCE_PACK.csv", "JQPACK2316_8_same_branch_lock", "finite j_q component pack"),
        ("SRC2367_2316_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2316_NEXT_TARGET.csv", "NEXT2316_0", "old chain selects no-hidden-visible-Hom"),
        ("SRC2367_2317_theorem", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2317_NO_HIDDEN_VISIBLE_HOM_THEOREM_ATTEMPT.csv", "NHVH2317_5_verdict", "no-hidden-visible-Hom not parent derived"),
        ("SRC2367_2317_counter", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2317_HIDDEN_COUPLING_COUNTERMODEL_TO_JQ_MAP.csv", "HCJ2317_4_readout_regeneration", "hidden coupling countermodels mapped to j_q"),
        ("SRC2367_2317_prior", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2317_FINITE_COUPLING_PRIOR_INTERFACE.csv", "FCP2317_6_claim_gate", "finite coupling prior interface"),
        ("SRC2367_2317_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2317_NEXT_TARGET.csv", "NEXT2317_0", "old chain selects coefficient functor/finite runner"),
        ("SRC2367_2318_functor", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2318_PARENT_COEFFICIENT_FUNCTOR_CONSTRUCTION_ATTEMPT.csv", "PCF2318_5_verdict", "parent coefficient functor not constructed"),
        ("SRC2367_2318_schema", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2318_FINITE_COUPLING_PRIOR_RUNNER_SCHEMA.csv", "SCHEMA2318_3_nonclaim_first_rows", "finite coupling runner schema ready"),
        ("SRC2367_2318_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2318_VALIDATION.csv", "VAL2318_09_claim_gates_block", "2318 validation blocks local GR claim"),
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


def jq_zero_theorem_audit() -> list[dict[str, object]]:
    rows = [
        ("JQZ2367_0_definition", "j_q source numerator", "delta_q S_matter = int sqrt(g) j_q L q + O(L^2 q,q^2); q_R=j_q/(n_q^A H_AB n_q^B)", "DEFINITION_BRANCH_LOCKED", "sets the target; does not prove zero"),
        ("JQZ2367_1_matter_descent", "ordinary matter source silence", "if matter action, constants, clocks, source weights, and readout descend through the same observed coframe, then j_q^matter=0", "EXACT_CONDITIONAL_THEOREM", "strong but premises unsigned"),
        ("JQZ2367_2_qR_consequence", "matter part of q_R", "if n_q H n_q>0 and j_q^matter=0 in the same branch, then q_R^matter=0", "CONDITIONAL_ALGEBRAIC_CONSEQUENCE", "does not remove boundary/curvature/readout terms"),
        ("JQZ2367_3_same_branch_guard", "same branch lock", "denominator n_q H n_q, numerator j_* terms, q normalization, and P_obs must come from one parent branch", "REQUIRED_GUARD", "prevents denominator/source mixing"),
        ("JQZ2367_4_verdict", "promote j_q=0 now", "current corpus has conditional theorems only; finite source pack remains live", "ZERO_THEOREM_NOT_PROMOTED", "local GR/Newton and empirical scoring remain blocked"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "target": target,
            "formula_or_statement": statement,
            "status": status,
            "effect": effect,
        }
        for row_id, target, statement, status, effect in rows
    ]


def finite_jq_source_pack() -> list[dict[str, object]]:
    rows = [
        ("JQPACK2367_0_total", "j_q_total", "j_q = j_matter + j_const + j_weight + j_shadow + j_readout + j_boundary + j_curvature + j_tail", "SYMBOLIC_DECOMPOSITION_ONLY", "all local arenas"),
        ("JQPACK2367_1_matter", "j_matter", "ordinary-matter vertical source leg", "CONDITIONAL_ZERO_NOT_PROMOTED", "PPN;WEP;clock"),
        ("JQPACK2367_2_weight", "j_weight", "source/species/action-scale weighting contribution", "MISSING_PARENT_EXCLUSION_OR_VALUE", "WEP;source_normalization;R10"),
        ("JQPACK2367_3_const", "j_const", "constant-sector derivative from alpha_EM, masses, clocks, representation labels", "MISSING_CONSTANT_SUPERSELECTION_OR_VALUE", "EM;clocks;WEP;particle"),
        ("JQPACK2367_4_shadow", "j_shadow", "conformal/disformal/source-only frame contribution", "MISSING_NO_SHADOW_THEOREM_OR_VALUE", "PPN_gamma;WEP;clock;local_force"),
        ("JQPACK2367_5_readout", "j_readout", "post-variation material/readout/source-worldtube projection contribution", "MISSING_VARIATION_DOMAIN_ORDER_OR_VALUE", "PPN;orbital;source_normalization"),
        ("JQPACK2367_6_boundary", "j_boundary", "compact-source boundary/domain support, including possible Q_R hair", "MISSING_BOUNDARY_CLASS_OR_VALUE", "orbital;PPN;finite_range"),
        ("JQPACK2367_7_curvature", "j_curvature", "higher-curvature/Weyl2 coupling contribution", "MISSING_PARENT_COEFFICIENT_OR_BOUND", "R10;local_geometry;PPN"),
        ("JQPACK2367_8_tail", "j_tail", "history/projector/counterterm/calibration tail", "MISSING_TAIL_ZERO_OR_BOUND", "clock;R10;PPN;orbital"),
        ("JQPACK2367_9_claim_gate", "j_q_claim_gate", "all live terms must be theorem-zero or source-backed in a no-cancellation envelope", "CLAIM_BLOCKED", "all_local_arenas"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "coefficient": coeff,
            "definition": definition,
            "source_status": status,
            "observable_links": arena,
        }
        for row_id, coeff, definition, status, arena in rows
    ]


def hidden_visible_hom_audit() -> list[dict[str, object]]:
    rows = [
        ("HVH2367_0_target", "no hidden-visible coefficient Hom", "Hom(C_hid,Coeff(O_vis)) is absent or constant after quotient/constant projection", "TARGET_SHARP", "would kill j_const, j_shadow, j_hom, part of j_weight/readout"),
        ("HVH2367_1_descent", "descended coefficient silence", "if c_i=p^* cbar_i and v in ker(Dp), then L_v c_i=0", "EXACT_CONDITIONAL_THEOREM", "requires proof every visible coefficient descends"),
        ("HVH2367_2_counterexample", "hidden coefficient map", "c_i=c0+epsilon f(I_hid) sources j_q if I_hid survives", "COUNTERMODEL_SURVIVES", "hidden invariant triviality not proved"),
        ("HVH2367_3_target_exclusion", "source/frame/coefficient target exclusion", "source-only weights, EM/mass coefficients, frames, and readouts must not be legal hidden targets", "POWERFUL_CONDITIONAL_ROUTE", "parent coefficient functor not constructed"),
        ("HVH2367_4_readout_guard", "radiative/readout stability", "S_eff, detector thresholds, and source-worldtube maps cannot regenerate coefficient dependence", "REQUIRED_GUARD_UNSIGNED", "tree-level silence alone is insufficient"),
        ("HVH2367_5_verdict", "derive no-hidden-visible-Hom now", "conditional route exact, but operator-domain theorem, target exclusion, hidden invariant triviality, and readout closure remain unsigned", "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED", "finite coupling prior lane remains live"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim_piece": piece,
            "statement": statement,
            "proof_status": status,
            "impact": impact,
        }
        for row_id, piece, statement, status, impact in rows
    ]


def finite_coupling_prior_interface() -> list[dict[str, object]]:
    rows = [
        ("FCP2367_0_b_alpha", "b_alpha", "vertical derivative of EM/gauge kinetic or fine-structure coefficient", "MISSING_THEOREM_OR_NUMERIC_PRIOR", "clocks;WEP;R10;EM spectra"),
        ("FCP2367_1_b_mu", "b_mu", "vertical derivative of mass-ratio/spectrum coefficient", "MISSING_THEOREM_OR_NUMERIC_PRIOR", "clocks;WEP;composition"),
        ("FCP2367_2_b_mA_b_nuc", "b_mA;b_nuc", "vertical derivative of material mass and nuclear/electromagnetic binding", "MISSING_THEOREM_OR_NUMERIC_PRIOR", "WEP;R10;clock nuclear sensitivities"),
        ("FCP2367_3_delta_w", "delta_w_A", "relative active-source/action-scale weight after common mode removed", "MISSING_THEOREM_OR_REAL_SOURCE_BACKED_INPUT", "WEP;Newton source normalization;R10"),
        ("FCP2367_4_shadow_frame", "a_shadow;b_disformal", "hidden derivative of conformal/disformal/source-only matter frame", "MISSING_THEOREM_OR_NUMERIC_PRIOR", "PPN gamma;WEP;clock;local force"),
        ("FCP2367_5_tau_readout", "Delta_tau_readout", "arena-specific readout/calibration/source-worldtube residual", "MISSING_THEOREM_OR_REAL_SOURCE_BACKED_INPUT", "clocks;WEP;R10;PPN;orbital"),
        ("FCP2367_6_runner_schema", "finite coupling prior runner", "symbol, sector, definition, units, theorem-zero status, numeric value, uncertainty, source, projection, no-cancellation group", "SCHEMA_READY_NONCLAIM", "all local arenas"),
        ("FCP2367_7_claim_gate", "finite coupling score permission", "score only if theorem-zero or numeric value/uncertainty/source/projection are source-backed and branch-locked", "CLAIM_BLOCKED", "all local arenas"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "source_status": status,
            "observable_links": links,
        }
        for row_id, symbol, definition, status, links in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2367_0_jq_zero", "prove j_q=0", 1, "KEEP_AS_PRIMARY_DERIVATION_TARGET", "if parent descent/no-Hom closes, local matter-source q residual dies cleanly"),
        ("DEC2367_1_jq_claim", "claim j_q=0 now", 5, "REFUSE", "conditional theorem premises are unsigned"),
        ("DEC2367_2_finite_pack", "finite j_q component pack", 2, "STAGE_NONCLAIM", "needed if any coefficient/source/readout channel survives"),
        ("DEC2367_3_no_hidden_visible", "derive parent coefficient functor/no-hidden-visible-Hom", 1, "SELECT_NEXT_DERIVATION_ATTACK", "it attacks EM/constants/shadow/source/readout leakage at once"),
        ("DEC2367_4_first_numeric", "first finite coupling prior row", 3, "FALLBACK_AFTER_FUNCTOR_ATTEMPT", "schema is ready but no source-backed row should score yet"),
        ("DEC2367_5_empirical", "run PPN/R10/clock/orbital scoring", 5, "DEFER", "projection/coefficients are not claim-grade"),
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
        ("CG2367_0_jq_zero", "j_q=0 parent theorem signed", "BLOCKED", "matter/source/current/no-Hom/readout descent premises unsigned"),
        ("CG2367_1_jq_finite", "finite j_q pack score-ready", "BLOCKED", "no numeric/source-backed component rows"),
        ("CG2367_2_no_hidden_visible", "no-hidden-visible-Hom derived", "BLOCKED", "parent coefficient functor/target category not constructed"),
        ("CG2367_3_same_branch", "denominator/numerator/projection branch-lock proved", "BLOCKED", "source normalization and P_obs not source-backed"),
        ("CG2367_4_local_GR_Newton", "local GR/Newton reduction derived", "BLOCKED", "j_q and boundary/curvature/tail channels remain live"),
        ("CG2367_5_empirical", "R10/PPN/clock/orbital runner can score", "BLOCKED", "finite coupling prior rows are schema-only"),
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
        ("REF2367_0_jq_zero", "promote j_q=0", "needs parent matter/source/current descent and no-hidden-visible-Hom", "REFUSED"),
        ("REF2367_1_source_pack_score", "score finite j_q pack", "needs source-backed numeric/theorem rows, units, uncertainty, and P_arena", "REFUSED"),
        ("REF2367_2_cancel_components", "cancel b_alpha against delta_w/readout by fit", "no-cancellation envelope forbids unsourced sign cancellation", "REFUSED"),
        ("REF2367_3_local_GR", "claim local GR/Newton", "j_q, boundary, curvature and tail source channels remain open", "REFUSED"),
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
            "row_id": "NEXT2367_0_selected",
            "next_file": "2368-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md",
            "next_script": "scripts/Y5_R2FR_parent_coefficient_functor_or_finite_coupling_prior_runner_2368.py",
            "selected_reason": "j_q zero depends on killing hidden-visible coefficient maps across EM/constants/source weights/shadow/readout; the parent coefficient functor is the cleanest derivation attack, with finite coupling priors as fallback",
            "success_condition": "derive the coefficient target category/functor so visible coefficients descend and vertical derivatives vanish, or produce source-backed nonclaim finite coupling prior rows with units/projections",
            "fallback_condition": "if the functor remains unsigned, keep j_q finite and move to first source-backed coupling prior row without claiming local GR",
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
        "numeric_value_present",
        "source_backed",
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
    add("VAL2367_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2367_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2367_02_outputs_exist", all(path.exists() for path in generated), "all 2367 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2367_03_csv_parse", parse_ok, parse_detail)

    zero = {row["row_id"]: row["status"] for row in read_csv(outputs["zero"])}
    add("VAL2367_04_jq_defined", zero.get("JQZ2367_0_definition") == "DEFINITION_BRANCH_LOCKED", "j_q numerator definition recorded")
    add("VAL2367_05_zero_not_promoted", zero.get("JQZ2367_4_verdict") == "ZERO_THEOREM_NOT_PROMOTED", "j_q zero theorem remains unpromoted")

    pack = {row["row_id"]: row["source_status"] for row in read_csv(outputs["pack"])}
    add("VAL2367_06_finite_pack_live", pack.get("JQPACK2367_9_claim_gate") == "CLAIM_BLOCKED", "finite j_q source pack remains live and blocked")

    hom = {row["row_id"]: row["proof_status"] for row in read_csv(outputs["hom"])}
    add("VAL2367_07_no_hidden_unsigned", hom.get("HVH2367_5_verdict") == "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED", "no-hidden-visible-Hom remains unsigned")

    prior = {row["row_id"]: row["source_status"] for row in read_csv(outputs["prior"])}
    add("VAL2367_08_prior_schema_ready", prior.get("FCP2367_6_runner_schema") == "SCHEMA_READY_NONCLAIM", "finite coupling prior schema ready nonclaim")

    decisions = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2367_09_next_decision", decisions.get("DEC2367_3_no_hidden_visible") == "SELECT_NEXT_DERIVATION_ATTACK", "coefficient functor/no-hidden-visible route selected")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2367_10_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2367_11_formalization_untouched", formal_ok, formal_detail)
    add("VAL2367_12_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2367_0_selected", "2368 coefficient functor/finite prior target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2367_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2367 valid: j_q numerator defined, zero theorem unpromoted, finite source pack staged, coefficient-functor/no-Hom route selected" if overall else "one or more validation gates failed",
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

    zero = read_csv(outputs["zero"])
    pack = read_csv(outputs["pack"])
    hom = read_csv(outputs["hom"])
    prior = read_csv(outputs["prior"])
    decisions = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2367 - j_q Source-Leg Zero Theorem Or Finite Source Pack

## Result

The source numerator is now the live local-GR bottleneck.  On the current finite q branch:

`delta_q S_matter = int sqrt(g) j_q L q + O(L^2 q,q^2)`, and `q_R = j_q/(n_q^A H_AB n_q^B)`.

So after `2366`, the denominator is conditionally less vague, but the numerator decides whether the branch is harmless.  A clean zero is possible only if matter, constants, source weights, frames, clocks, readouts, and boundary/source terms descend through the same parent-observed coframe with no hidden-visible coefficient map.

That theorem is exact conditionally, but not signed.  The current status is therefore: no `j_q=0` claim, finite `j_q` source pack live, no cancellation, and no local-GR/Newton promotion.

## j_q Zero Theorem Audit

{table(["row_id", "target", "status", "effect"], zero)}

## Finite j_q Source Pack

{table(["row_id", "coefficient", "source_status", "observable_links"], pack)}

## Hidden-Visible Hom Audit

{table(["row_id", "claim_piece", "proof_status", "impact"], hom)}

## Finite Coupling Prior Interface

{table(["row_id", "symbol", "source_status", "observable_links"], prior)}

## Decision Ledger

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["zero"])}`
- `{rel(outputs["pack"])}`
- `{rel(outputs["hom"])}`
- `{rel(outputs["prior"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is the coupling fork.  If the parent coefficient functor/no-hidden-visible-Hom theorem can be derived, a whole family of bad source numerators dies together.  If not, the project must stop trying to win by grammar and start filling source-backed finite priors for `b_alpha`, mass/clock coefficients, active-source weights, shadow frames, readout tails, boundary hair, and curvature coupling.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_SOURCE_REGISTER.csv",
        "zero": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_JQ_ZERO_THEOREM_AUDIT.csv",
        "pack": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_FINITE_JQ_SOURCE_PACK.csv",
        "hom": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_HIDDEN_VISIBLE_HOM_AUDIT.csv",
        "prior": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_FINITE_COUPLING_PRIOR_INTERFACE.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_DECISION_LEDGER.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2367_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2367_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["zero"], jq_zero_theorem_audit())
    write_csv(outputs["pack"], finite_jq_source_pack())
    write_csv(outputs["hom"], hidden_visible_hom_audit())
    write_csv(outputs["prior"], finite_coupling_prior_interface())
    write_csv(outputs["decision"], decision_ledger())
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

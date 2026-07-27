from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2532"
BRANCH_ID = "MTS_R2FR_JQ_SOURCE_LEG_ZERO_THEOREM_OR_FINITE_SOURCE_PACK_2532"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2532-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2532_SOURCE_REGISTER.csv",
    "zero": RESIDUALS / "P8_Y5_NO_SHADOW_2532_JQ_ZERO_THEOREM_AUDIT.csv",
    "pack": RESIDUALS / "P8_Y5_NO_SHADOW_2532_FINITE_JQ_SOURCE_PACK.csv",
    "hom": RESIDUALS / "P8_Y5_NO_SHADOW_2532_HIDDEN_VISIBLE_HOM_AUDIT.csv",
    "prior": RESIDUALS / "P8_Y5_NO_SHADOW_2532_FINITE_COUPLING_PRIOR_INTERFACE.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2532_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2532_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2532_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2532_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2532_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2532_VALIDATION.csv",
}

BRANCH_COPIES = {
    "zero": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Jq_zero_theorem_audit_2532_NONCLAIM.csv",
    "pack": POST_ROOT / "source-intake" / "local_bounds" / "Finite_jq_source_pack_2532_NONCLAIM.csv",
    "prior": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "Finite_coupling_prior_interface_2532_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "PCF2532_NEXT_TARGET_NONCLAIM.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


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


SOURCE_SPECS = [
    ("SRC2532_0_2531_doc", "2531-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md", "NEXT2531_0_selected", "2531 selects j_q source numerator after D_qWeyl2/operator branch"),
    ("SRC2532_1_2531_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2531_VALIDATION.csv", "VAL2531_OVERALL,PASS", "2531 validation anchor"),
    ("SRC2532_2_2367_doc", "2367-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md", "JQZ2367_4_verdict", "j_q zero theorem precedent"),
    ("SRC2532_3_2367_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2367_VALIDATION.csv", "VAL2367_OVERALL,PASS", "2367 validation anchor"),
    ("SRC2532_4_2367_pack", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2367_FINITE_JQ_SOURCE_PACK.csv", "JQPACK2367_9_claim_gate", "finite j_q source pack precedent"),
    ("SRC2532_5_2367_hom", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2367_HIDDEN_VISIBLE_HOM_AUDIT.csv", "HVH2367_5_verdict", "hidden-visible Hom audit precedent"),
    ("SRC2532_6_2368_doc", "2368-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md", "PCF2368_5_verdict", "parent coefficient functor precedent"),
    ("SRC2532_7_2368_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2368_VALIDATION.csv", "VAL2368_OVERALL,PASS", "2368 validation anchor"),
    ("SRC2532_8_2368_anchors", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2368_FIRST_NONCLAIM_COUPLING_ANCHORS.csv", "ANCH2368_3_delta_w_missing", "nonclaim coupling anchors and missing delta_w row"),
    ("SRC2532_9_2368_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2368_NEXT_TARGET.csv", "NEXT2368_0_selected", "alpha_cg/PPN projection owner fallback route"),
]


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "source_id": source_id,
                    "source_path": source_path,
                    "needle": needle,
                    "role": role,
                    "path_exists": str(path.exists()).lower(),
                    "needle_found": str(contains(path, needle)).lower(),
                    "status": "SOURCE_OK" if path.exists() and contains(path, needle) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def jq_zero_theorem_audit() -> list[dict[str, object]]:
    rows = [
        ("JQZ2532_0_definition", "j_q source numerator", "delta_q S_matter = int sqrt(g) j_q L q + O(L^2 q,q^2); q_R = j_q/(n_q^A H_AB n_q^B)", "DEFINITION_BRANCH_LOCKED", "source numerator is the live local-GR bottleneck"),
        ("JQZ2532_1_matter_descent", "ordinary matter source silence", "if matter action, constants, clocks, source weights and readout all descend through the same observed coframe, then j_q^matter=0", "EXACT_CONDITIONAL_THEOREM", "strong theorem shape; premises still unsigned by parent action"),
        ("JQZ2532_2_qR_consequence", "matter part of q_R", "if n_q H n_q>0 and j_q^matter=0 in the same branch, then q_R^matter=0", "CONDITIONAL_ALGEBRAIC_CONSEQUENCE", "does not remove boundary, curvature, hidden coefficient, readout or tail terms"),
        ("JQZ2532_3_same_branch_guard", "same branch lock", "denominator n_q H n_q, numerator j_* terms, q normalization and P_obs must come from one parent branch", "REQUIRED_GUARD", "prevents false wins by mixing denominators and sources"),
        ("JQZ2532_4_verdict", "promote j_q=0 now", "conditional theorem exists but the corpus does not sign every source, constant, frame, readout and boundary premise", "ZERO_THEOREM_NOT_PROMOTED", "local GR/Newton and empirical scoring remain blocked"),
    ]
    return [
        {
            **no_claim(),
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
        ("JQPACK2532_0_total", "j_q_total", "j_q = j_matter + j_const + j_weight + j_shadow + j_readout + j_boundary + j_curvature + j_tail", "SYMBOLIC_DECOMPOSITION_ONLY", "all local arenas", "no cancellation allowed between live terms"),
        ("JQPACK2532_1_matter", "j_matter", "ordinary-matter vertical source leg", "CONDITIONAL_ZERO_NOT_PROMOTED", "PPN;WEP;clock", "matter descent not parent-signed across readout/source weights"),
        ("JQPACK2532_2_weight", "j_weight", "source/species/action-scale weighting contribution", "MISSING_PARENT_EXCLUSION_OR_VALUE", "WEP;source_normalization;R10", "delta_w_A remains missing"),
        ("JQPACK2532_3_const", "j_const", "constant-sector derivative from alpha_EM, masses, clocks and representation labels", "MISSING_CONSTANT_SUPERSELECTION_OR_VALUE", "EM;clocks;WEP;particle", "coefficient functor not constructed"),
        ("JQPACK2532_4_shadow", "j_shadow", "conformal/disformal/source-only frame contribution", "MISSING_NO_SHADOW_THEOREM_OR_VALUE", "PPN_gamma;WEP;clock;local_force", "no hidden-visible target exclusion"),
        ("JQPACK2532_5_readout", "j_readout", "post-variation material/readout/source-worldtube projection contribution", "MISSING_VARIATION_DOMAIN_ORDER_OR_VALUE", "PPN;orbital;source_normalization", "readout may regenerate finite source terms"),
        ("JQPACK2532_6_boundary", "j_boundary", "compact-source boundary/domain support, including possible Q_R hair", "MISSING_BOUNDARY_CLASS_OR_VALUE", "orbital;PPN;finite_range", "boundary silence not signed"),
        ("JQPACK2532_7_curvature", "j_curvature", "higher-curvature/Weyl2 coupling contribution", "MISSING_PARENT_COEFFICIENT_OR_BOUND", "R10;local_geometry;PPN", "D_qWeyl2 remains unsourced"),
        ("JQPACK2532_8_tail", "j_tail", "history/projector/counterterm/calibration tail", "MISSING_TAIL_ZERO_OR_BOUND", "clock;R10;PPN;orbital", "tails require theorem zero or sourced bound"),
        ("JQPACK2532_9_claim_gate", "j_q_claim_gate", "every live term must be theorem-zero or source-backed in a no-cancellation envelope", "CLAIM_BLOCKED", "all_local_arenas", "local branch cannot score while any row is symbolic"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "coefficient": coeff,
            "definition": definition,
            "source_status": status,
            "observable_links": links,
            "guard": guard,
        }
        for row_id, coeff, definition, status, links, guard in rows
    ]


def hidden_visible_hom_audit() -> list[dict[str, object]]:
    rows = [
        ("HVH2532_0_target", "no hidden-visible coefficient Hom", "Hom(C_hidden, Coeff(O_visible)) is absent or constant after quotient/constant projection", "TARGET_SHARP", "would kill j_const, j_shadow, j_hom and parts of j_weight/readout"),
        ("HVH2532_1_descent", "descended coefficient silence", "if c_i=pullback(cbar_i) and v in ker(Dp), then L_v c_i=0", "EXACT_CONDITIONAL_THEOREM", "requires proof every visible coefficient descends"),
        ("HVH2532_2_counterexample", "hidden coefficient map", "c_i=c0+epsilon f(I_hidden) sources j_q if I_hidden survives", "COUNTERMODEL_SURVIVES", "hidden invariant triviality not proved"),
        ("HVH2532_3_target_exclusion", "source/frame/coefficient target exclusion", "source-only weights, EM/mass coefficients, frames and readouts must not be legal hidden targets", "POWERFUL_CONDITIONAL_ROUTE", "parent coefficient functor not constructed"),
        ("HVH2532_4_readout_guard", "radiative/readout stability", "S_eff, detector thresholds and source-worldtube maps cannot regenerate coefficient dependence", "REQUIRED_GUARD_UNSIGNED", "tree-level silence alone is insufficient"),
        ("HVH2532_5_verdict", "derive no-hidden-visible-Hom now", "conditional route exact, but target category, operator-domain theorem, hidden invariant triviality and readout closure remain unsigned", "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED", "finite coupling prior lane remains live"),
    ]
    return [
        {
            **no_claim(),
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
        ("FCP2532_0_b_alpha", "b_alpha", "vertical derivative of EM/gauge kinetic or fine-structure coefficient", "MISSING_THEOREM_OR_NUMERIC_PRIOR", "clocks;WEP;R10;EM spectra", "must not be inferred from clock-product anchor alone"),
        ("FCP2532_1_b_mu", "b_mu", "vertical derivative of mass-ratio/spectrum coefficient", "MISSING_THEOREM_OR_NUMERIC_PRIOR", "clocks;WEP;composition", "requires source-backed sensitivity/projection"),
        ("FCP2532_2_b_mA_b_nuc", "b_mA;b_nuc", "vertical derivative of material mass and nuclear/electromagnetic binding", "MISSING_THEOREM_OR_NUMERIC_PRIOR", "WEP;R10;clock nuclear sensitivities", "composition rows not sourced"),
        ("FCP2532_3_delta_w", "delta_w_A", "relative active-source/action-scale weight after common mode removed", "MISSING_THEOREM_OR_REAL_SOURCE_BACKED_INPUT", "WEP;Newton;R10", "2368 records delta_w as missing, not bounded prediction"),
        ("FCP2532_4_shadow_frame", "a_shadow;b_disformal", "hidden derivative of conformal/disformal/source-only matter frame", "MISSING_THEOREM_OR_NUMERIC_PRIOR", "PPN gamma;WEP;clock;local force", "frame/no-shadow route unsigned"),
        ("FCP2532_5_tau_readout", "Delta_tau_readout", "arena-specific readout/calibration/source-worldtube residual", "MISSING_THEOREM_OR_REAL_SOURCE_BACKED_INPUT", "clocks;WEP;R10;PPN;orbital", "readout map not branch-locked"),
        ("FCP2532_6_runner_schema", "finite coupling prior runner", "symbol, sector, definition, units, theorem-zero status, numeric value, uncertainty, source, projection, no-cancellation group", "SCHEMA_READY_NONCLAIM", "all local arenas", "ready only as nonclaim"),
        ("FCP2532_7_claim_gate", "finite coupling score permission", "score only if theorem-zero or numeric value/uncertainty/source/projection are source-backed and branch-locked", "CLAIM_BLOCKED", "all local arenas", "symbolic priors cannot score"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "source_status": status,
            "observable_links": links,
            "guard": guard,
        }
        for row_id, symbol, definition, status, links, guard in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2532_0_jq_zero", "prove j_q=0", 1, "KEEP_AS_PRIMARY_DERIVATION_TARGET", "if parent descent/no-Hom closes, local matter-source q residual dies cleanly"),
        ("DEC2532_1_jq_claim", "claim j_q=0 now", 5, "REFUSE", "conditional theorem premises are unsigned"),
        ("DEC2532_2_finite_pack", "finite j_q component pack", 2, "STAGE_NONCLAIM", "needed if any coefficient/source/readout channel survives"),
        ("DEC2532_3_no_hidden_visible", "derive parent coefficient functor/no-hidden-visible-Hom", 1, "SELECT_NEXT_DERIVATION_ATTACK", "attacks EM/constants/shadow/source/readout leakage at once"),
        ("DEC2532_4_first_numeric", "first finite coupling prior row", 3, "FALLBACK_AFTER_FUNCTOR_ATTEMPT", "schema is ready but no source-backed row should score yet"),
        ("DEC2532_5_empirical", "run PPN/R10/clock/orbital scoring", 5, "DEFER", "projection/coefficients are not claim-grade"),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "route": route,
                "rank": rank,
                "decision": decision,
                "reason": reason,
            }
        )
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2532_0_jq_zero", "j_q=0 parent theorem signed", "BLOCKED", "matter/source/current/no-Hom/readout descent premises unsigned"),
        ("CG2532_1_jq_finite", "finite j_q pack score-ready", "BLOCKED", "no numeric/source-backed component rows"),
        ("CG2532_2_no_hidden_visible", "no-hidden-visible-Hom derived", "BLOCKED", "parent coefficient functor/target category not constructed"),
        ("CG2532_3_local_GR_Newton", "local GR/Newton reduction derived", "BLOCKED", "j_q and boundary/curvature/tail channels remain live"),
        ("CG2532_4_public_or_github", "public/GitHub claim allowed", "BLOCKED", "this is a private derivation checkpoint with nonclaim rows"),
        ("CG2532_5_empirical", "R10/PPN/clock/orbital runner can score", "BLOCKED", "finite coupling prior rows are schema-only"),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "gate_pass": "false",
                "passes_public_claim": "false",
            }
        )
        for row_id, claim, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2532_0_jq_zero", "promote j_q=0", "needs parent matter/source/current descent and no-hidden-visible-Hom", "REFUSED"),
        ("REF2532_1_source_pack_score", "score finite j_q pack", "needs source-backed numeric/theorem rows, units, uncertainty and P_arena", "REFUSED"),
        ("REF2532_2_cancel_components", "cancel b_alpha against delta_w/readout by fit", "no-cancellation envelope forbids unsourced sign cancellation", "REFUSED"),
        ("REF2532_3_local_GR", "claim local GR/Newton", "j_q, boundary, curvature and tail source channels remain open", "REFUSED"),
        ("REF2532_4_skip_functor", "skip coefficient functor and use anchors as predictions", "2368 anchors are imported constraints, not MTS predictions", "REFUSED"),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "attempted_claim": claim,
                "missing_evidence": missing,
                "refusal_result": result,
            }
        )
        for row_id, claim, missing, result in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "NEXT2532_0_selected",
            "priority": "selected",
            "next_file": "2533-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md",
            "next_script": "scripts/Y5_R2FR_parent_coefficient_functor_or_finite_coupling_prior_runner_2533.py",
            "selected_reason": "j_q zero depends on killing hidden-visible coefficient maps across EM/constants/source weights/shadow/readout; this is the cleanest derivation attack",
            "success_condition": "derive the coefficient target category/functor so visible coefficients descend and vertical derivatives vanish, or produce source-backed nonclaim finite coupling prior rows with units/projections",
            "fallback_condition": "if the functor remains unsigned, keep j_q finite and move to first source-backed coupling prior row without claiming local GR",
        },
        {
            "row_id": "NEXT2532_1_parallel_fallback",
            "priority": "fallback",
            "next_file": "2533b-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md",
            "next_script": "scripts/Y5_R2FR_alpha_cg_projection_owner_fill_or_deltaw_material_vector_acquisition_2533b.py",
            "selected_reason": "2368 already shows alpha_cg/PPN ownership and delta_w acquisition as the first finite-prior fallback",
            "success_condition": "fill tau_PPN, same-branch owner, Z_X/M_X^2, S_PPN, common-frame/readout tail, or a real delta_w material/source vector row",
            "fallback_condition": "if no row is source-backed, keep all anchors nonclaim",
        },
    ]
    return [stamp(row) for row in rows]


def branch_copy_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, destination in BRANCH_COPIES.items():
        source = OUTPUTS[key]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": key,
                    "source_path": rel(source),
                    "destination_path": rel(destination),
                    "destination_exists": str(destination.exists()).lower(),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


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
        rows.append(stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}))

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2532_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2532_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2532_02_outputs_exist", all(path.exists() for path in generated), "all 2532 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2532_03_csv_parse", parse_ok, parse_detail)

    zero = {row["row_id"]: row["status"] for row in read_csv(outputs["zero"])}
    add("VAL2532_04_jq_defined", zero.get("JQZ2532_0_definition") == "DEFINITION_BRANCH_LOCKED", "j_q numerator definition recorded")
    add("VAL2532_05_zero_not_promoted", zero.get("JQZ2532_4_verdict") == "ZERO_THEOREM_NOT_PROMOTED", "j_q zero theorem remains unpromoted")

    pack = {row["row_id"]: row["source_status"] for row in read_csv(outputs["pack"])}
    add("VAL2532_06_finite_pack_live", pack.get("JQPACK2532_9_claim_gate") == "CLAIM_BLOCKED", "finite j_q source pack remains live and blocked")

    hom = {row["row_id"]: row["proof_status"] for row in read_csv(outputs["hom"])}
    add("VAL2532_07_no_hidden_unsigned", hom.get("HVH2532_5_verdict") == "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED", "no-hidden-visible-Hom remains unsigned")

    prior = {row["row_id"]: row["source_status"] for row in read_csv(outputs["prior"])}
    add("VAL2532_08_prior_schema_ready", prior.get("FCP2532_6_runner_schema") == "SCHEMA_READY_NONCLAIM", "finite coupling prior schema ready nonclaim")
    add("VAL2532_09_delta_w_missing", prior.get("FCP2532_3_delta_w") == "MISSING_THEOREM_OR_REAL_SOURCE_BACKED_INPUT", "delta_w remains missing and nonclaim")

    decisions = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2532_10_next_decision", decisions.get("DEC2532_3_no_hidden_visible") == "SELECT_NEXT_DERIVATION_ATTACK", "coefficient functor/no-hidden-visible route selected")

    next_rows = read_csv(outputs["next"])
    add("VAL2532_11_next_selected", any(row.get("row_id") == "NEXT2532_0_selected" and "2533" in row.get("next_file", "") for row in next_rows), "2533 coefficient functor/finite prior target selected")

    copy_rows = read_csv(outputs["copies"])
    add("VAL2532_12_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2532_13_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2532_14_formalization_untouched", formal_ok, formal_detail)
    add("VAL2532_15_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2532_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2532 valid: j_q source numerator defined, zero theorem unpromoted, finite source pack staged, coupling functor/no-Hom route selected" if overall else "one or more validation gates failed",
            }
        )
    )
    return rows


def table(headers: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "").replace("|", "/") for header in headers) + " |")
    return "\n".join(lines)


def write_markdown(outputs: dict[str, Path]) -> None:
    zero = read_csv(outputs["zero"])
    pack = read_csv(outputs["pack"])
    hom = read_csv(outputs["hom"])
    prior = read_csv(outputs["prior"])
    decisions = read_csv(outputs["decision"])
    claims = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2532 - j_q Source-Leg Zero Theorem Or Finite Source Pack

**Current verdict:** the coupling/source numerator is now isolated as the live local-GR bottleneck. The clean zero theorem exists conditionally, but it is not parent-signed.

**Main gain:** the project no longer has to wave vaguely at "coupling". In this branch the exact object is `j_q`: the numerator in `q_R = j_q/(n_q^A H_AB n_q^B)`. If the parent action makes visible coefficients, source weights, frames, clocks, readouts and boundary/source terms descend through one observed coframe, `j_q` can vanish. The current corpus does not yet sign that contract.

**Claim discipline:** no local-GR/Newton/R10/PPN/clock/orbital/GitHub claim is allowed from 2532. This is a private derivation gate and all finite rows remain nonclaim.

## j_q Zero Theorem Audit

{table(["row_id", "target", "status", "effect"], zero)}

## Finite j_q Source Pack

{table(["row_id", "coefficient", "source_status", "observable_links", "guard"], pack)}

## Hidden-Visible Hom Audit

{table(["row_id", "claim_piece", "proof_status", "impact"], hom)}

## Finite Coupling Prior Interface

{table(["row_id", "symbol", "source_status", "observable_links", "guard"], prior)}

## Decision Ledger

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Claim Gates

{table(["row_id", "claim", "status", "reason"], claims)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

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
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is the coupling fork in its cleanest form. If the next checkpoint can construct the parent coefficient functor/no-hidden-visible-Hom rule, a family of bad local source terms dies together. If not, the route becomes honest finite-coupling work: source-backed rows for `b_alpha`, mass/clock coefficients, `delta_w_A`, shadow-frame leakage, readout tails, boundary hair and curvature coupling, with no cancellation games.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["zero"], jq_zero_theorem_audit())
    write_csv(OUTPUTS["pack"], finite_jq_source_pack())
    write_csv(OUTPUTS["hom"], hidden_visible_hom_audit())
    write_csv(OUTPUTS["prior"], finite_coupling_prior_interface())
    write_csv(OUTPUTS["decision"], decision_ledger())
    write_csv(OUTPUTS["claims"], claim_gates())
    write_csv(OUTPUTS["refusal"], refusal_runner())
    write_csv(OUTPUTS["next"], next_target())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

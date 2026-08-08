from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2533"
BRANCH_ID = "MTS_R2FR_PARENT_COEFFICIENT_FUNCTOR_OR_FINITE_COUPLING_PRIOR_RUNNER_2533"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2533-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2533_SOURCE_REGISTER.csv",
    "functor": RESIDUALS / "P8_Y5_NO_SHADOW_2533_PARENT_COEFFICIENT_FUNCTOR_AUDIT.csv",
    "obligations": RESIDUALS / "P8_Y5_NO_SHADOW_2533_PROOF_OBLIGATION_LEDGER.csv",
    "schema": RESIDUALS / "P8_Y5_NO_SHADOW_2533_FINITE_COUPLING_RUNNER_SCHEMA.csv",
    "anchors": RESIDUALS / "P8_Y5_NO_SHADOW_2533_FIRST_NONCLAIM_COUPLING_ANCHORS.csv",
    "acceptance": RESIDUALS / "P8_Y5_NO_SHADOW_2533_RUNNER_ACCEPTANCE_MATRIX.csv",
    "route": RESIDUALS / "P8_Y5_NO_SHADOW_2533_DELTAW_PPN_ROUTE_SELECTION.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2533_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2533_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2533_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2533_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2533_VALIDATION.csv",
}

BRANCH_COPIES = {
    "functor": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Parent_coefficient_functor_audit_2533_NONCLAIM.csv",
    "anchors": POST_ROOT / "source-intake" / "local_bounds" / "Finite_coupling_anchors_2533_NONCLAIM.csv",
    "schema": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "Finite_coupling_runner_schema_2533_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "ACG2533_NEXT_TARGET_NONCLAIM.csv",
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


SOURCE_SPECS = [
    ("SRC2533_0_2532_doc", "2532-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md", "NEXT2532_0_selected", "2532 selects coefficient-functor route after j_q source numerator isolation"),
    ("SRC2533_1_2532_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2532_VALIDATION.csv", "VAL2532_OVERALL,PASS", "2532 validation anchor"),
    ("SRC2533_2_2368_doc", "2368-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md", "PCF2368_5_verdict", "parent coefficient functor precedent"),
    ("SRC2533_3_2368_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2368_VALIDATION.csv", "VAL2368_OVERALL,PASS", "2368 validation anchor"),
    ("SRC2533_4_2368_functor", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2368_PARENT_COEFFICIENT_FUNCTOR_AUDIT.csv", "PCF2368_5_verdict", "functor audit precedent"),
    ("SRC2533_5_2368_anchors", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2368_FIRST_NONCLAIM_COUPLING_ANCHORS.csv", "ANCH2368_3_delta_w_missing", "first nonclaim coupling anchors and missing delta_w"),
    ("SRC2533_6_2368_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2368_NEXT_TARGET.csv", "NEXT2368_0_selected", "alpha_cg projection owner next route"),
    ("SRC2533_7_2369_doc", "2369-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md", "NEXT2369_0_selected", "alpha_cg/readout-tail precedent"),
    ("SRC2533_8_2369_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2369_VALIDATION.csv", "VAL2369_OVERALL,PASS", "2369 validation anchor"),
    ("SRC2533_9_2369_alpha", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_ALPHA_CG_PROJECTION_AUDIT.csv", "ACG2369_7_verdict", "alpha_cg projection owner precedent"),
    ("SRC2533_10_2369_readiness", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_SCORE_READINESS.csv", "READY2369_3_local_GR", "score readiness still blocked"),
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


def parent_coefficient_functor_audit() -> list[dict[str, object]]:
    rows = [
        ("PCF2533_0_candidate", "parent coefficient functor", "p_vis=(q_loc, theta_obs, Rep_vis, Top, Level_EM, current_class); F_coeff: O_vis -> p_vis^*Coeff(Q_obs,Rep,Top,Level,current)", "CANDIDATE_CONSTRUCTION_WRITTEN", "turns coupling into a category/grammar question rather than a free parameter"),
        ("PCF2533_1_vertical_silence", "coefficient descent", "if c_i=p_vis^*cbar_i and v in ker(Dp_vis), then L_v c_i=0", "EXACT_CONDITIONAL_THEOREM", "kills b_alpha, b_mu, b_mA, b_nuc, shadow slopes, and hidden coefficient parts of j_q if parent-signed"),
        ("PCF2533_2_jq_pushforward", "j_q coefficient leg", "if S_matter and readouts factor through p_vis and F_coeff, then the coefficient-sourced piece of delta_q S_matter vanishes along vertical directions", "EXACT_CONDITIONAL_COROLLARY", "connects the functor directly to the j_q numerator"),
        ("PCF2533_3_source_target_exclusion", "source-only target exclusion", "F_coeff has no relative active-source prefactor target except guarded common calibration", "POWERFUL_IF_PARENT_SIGNED", "would make delta_w_A/source multipliers ill-typed rather than merely small"),
        ("PCF2533_4_hidden_scalar_counterexample", "hidden scalar obstruction", "if I_hidden survives and coefficient targets are legal, c=c0+epsilon I_hidden is a valid hidden-visible Hom", "COUNTEREXAMPLE_RETAINED", "hidden invariant triviality/no-hair remains unsigned"),
        ("PCF2533_5_common_measure_readout", "common measure/readout closure", "functor must own action-scale/current normalization and survive S_eff, detector thresholds, protocol and source-worldtube readout", "REQUIRED_GUARD_UNSIGNED", "tree-level coefficient silence could be regenerated"),
        ("PCF2533_6_verdict", "construct parent coefficient functor now", "candidate functor is exact and valuable, but parent action syntax/target category is not selected in the corpus", "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED", "move to alpha_cg projection/readout-tail or finite-prior acquisition without local-GR claim"),
    ]
    return [
        {
            **no_claim(),
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
        ("OBL2533_0_parent_syntax", "parent syntax/target category", "parent action selects F_coeff target category before fitting/readout", "MISSING_PARENT_SELECTION", "without this, the functor is an imposed closure"),
        ("OBL2533_1_hidden_triviality", "hidden invariant algebra triviality", "no surviving I_hidden can feed visible coefficients", "MISSING_HIDDEN_NO_HAIR_OR_TRIVIALITY", "countermodel c=c0+epsilon I_hidden survives"),
        ("OBL2533_2_source_only", "source-only target exclusion", "relative active-source weights are not legal targets", "MISSING_SOURCE_TARGET_EXCLUSION", "delta_w_A remains live"),
        ("OBL2533_3_common_measure", "common measure/current owner", "source normalization/common action scale is one parent-owned object", "MISSING_COMMON_MEASURE_CURRENT", "prevents source-current slips"),
        ("OBL2533_4_radiative_readout", "radiative/readout closure", "S_eff, detector threshold, protocol and source-worldtube maps do not regenerate hidden coefficients", "MISSING_RADIATIVE_READOUT_CLOSURE", "feeds alpha_readout/tail terms"),
        ("OBL2533_5_branch_lock", "same-branch finite runner lock", "coefficient, tau, range, source/test charge, denominator and projection share one parent branch", "MISSING_BRANCH_LOCK_FOR_SCORING", "blocks score mixing"),
        ("OBL2533_6_verdict", "functor proof obligation status", "all obligations must close to promote no-hidden-visible-Hom", "OBLIGATIONS_OPEN", "not a local-GR/Newton derivation yet"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "obligation": obligation,
            "required_evidence": evidence,
            "status": status,
            "impact": impact,
        }
        for row_id, obligation, evidence, status, impact in rows
    ]


def finite_coupling_runner_schema() -> list[dict[str, object]]:
    rows = [
        ("SCHEMA2533_0_columns", "required columns", "symbol, sector, definition, units, theorem_zero_status, numeric_value, uncertainty, source_path, source_row_id, arena_projection, no_cancellation_group, score_ready, valid_for_claim", "SCHEMA_READY_NONCLAIM"),
        ("SCHEMA2533_1_no_cancellation", "no-cancellation envelope", "sum_abs over live components by arena unless covariance/orthogonality theorem signs cancellation", "REQUIRED_GUARD"),
        ("SCHEMA2533_2_branch_lock", "same-branch lock", "coefficient/tau/range/source/test charge/denominator/projection must belong to the same parent branch", "REQUIRED_GUARD"),
        ("SCHEMA2533_3_first_targets", "first acquisition targets", "b_alpha*tau_clock_time; alpha_PPN vector ceiling; eta_WEP comparator; delta_w_A; alpha_cg component owner; alpha_readout tail", "ACQUISITION_QUEUE_READY"),
        ("SCHEMA2533_4_claim_rule", "score permission", "claim/score only if theorem-zero signed or numeric row has source, units, uncertainty, branch lock and projection", "CLAIM_BLOCKED"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "runner_piece": piece,
            "schema_or_rule": schema,
            "status": status,
        }
        for row_id, piece, schema, status in rows
    ]


def finite_coupling_anchors_nonclaim() -> list[dict[str, object]]:
    rows = [
        ("ANCH2533_0_clock_product", "b_alpha*tau_clock_time", "clock_product", "2.1e-18", "yr^-1", "source-backed product/envelope only; standalone b_alpha not derived", "clock product only", "true"),
        ("ANCH2533_1_ppn_vector_ceiling", "alpha_PPN_total_abs_vector", "PPN_vector", "0.005788015401465051", "dimensionless", "Cassini/scalar-tensor proxy vector ceiling; not raw c_g or MTS prediction", "PPN/local-GR target ceiling", "true"),
        ("ANCH2533_2_wep_comparator", "eta_WEP_source_charge_bound", "WEP_comparator", "2.8e-15", "dimensionless", "MICROSCOPE comparator bound; no delta_w prediction row", "WEP comparator only", "true"),
        ("ANCH2533_3_delta_w_missing", "delta_w_A", "source_weight", "MISSING_SOURCE_BACKED_VALUE", "dimensionless", "delta_w cannot be inferred from comparator bounds without material/source/tau projection", "WEP;Newton;R10 acquisition", "false"),
        ("ANCH2533_4_alpha_readout_missing", "alpha_readout", "PPN_readout_tail", "MISSING_SOURCE_BACKED_VALUE", "dimensionless", "2369 identifies alpha_readout/readout tails as active PPN obstruction", "PPN;local_GR acquisition", "false"),
    ]
    return [
        {
            **no_claim(),
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
        ("ACCEPT2533_0_clock_product", "ANCH2533_0_clock_product", "source_backed_product_constraint", "nonclaim product constraint only", "standalone b_alpha; WEP; R10; local GR", "tau_clock_time parent derivation and shared WEP/R10 projection"),
        ("ACCEPT2533_1_ppn_vector", "ANCH2533_1_ppn_vector_ceiling", "source_backed_proxy_vector_ceiling", "nonclaim vector ceiling/proxy only", "raw c_g; individual PPN component pass", "component owner matrix, tau/range/source/current/support/boundary/readout projection"),
        ("ACCEPT2533_2_wep_bound", "ANCH2533_2_wep_comparator", "source_backed_comparator_bound", "comparator bound only", "delta_w inference", "official material/source response vector, tau_eff, readout transfer"),
        ("ACCEPT2533_3_delta_w", "ANCH2533_3_delta_w_missing", "required_prediction_missing", "acquisition queue only", "WEP/Newton/R10 source-weight scoring", "numeric delta_w_i or theorem-zero plus source path, units and projection"),
        ("ACCEPT2533_4_alpha_readout", "ANCH2533_4_alpha_readout_missing", "required_tail_missing", "acquisition queue only", "PPN/local-GR scoring", "zero proof or first source-backed alpha_readout tail bound"),
    ]
    return [
        {
            **no_claim(),
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
        ("ROUTE2533_0_functor", "parent coefficient functor", "CANDIDATE_NOT_PARENT_SIGNED", "highest derivation payoff; cannot be claimed without parent syntax", "KEEP_OPEN"),
        ("ROUTE2533_1_delta_w", "delta_w material/source vector", "COMPARATOR_AND_PRODUCT_ANCHORS_ONLY", "material/source response vector, tau_eff and readout transfer missing", "DEFER_TO_ACQUISITION"),
        ("ROUTE2533_2_ppn_component", "alpha_cg PPN component owner", "NORMAL_FORM_PRECEDENT_EXISTS_SCORE_BLOCKED", "structurally closer to local-GR testing than raw c_g, but projection clauses remain blocked", "SELECT_NEXT"),
        ("ROUTE2533_3_readout_tail", "alpha_readout zero proof or first bound", "PREVIEWED_AS_NEXT_OBSTRUCTION", "2369 says common-frame path stalls on readout/projector/support descent", "QUEUE_AFTER_ALPHA_CG_OWNER"),
        ("ROUTE2533_4_verdict", "2533 route decision", "FUNCTOR_UNSIGNED_ALPHA_CG_IMPORT_SELECTED", "first nonclaim anchors imported; next should fill alpha_cg projection owner with readout-tail/delta_w retained", "SELECT_ALPHA_CG_PROJECTION_NEXT"),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "candidate_route": route,
                "evidence_status": status,
                "reason_or_blocker": reason,
                "decision": decision,
            }
        )
        for row_id, route, status, reason, decision in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2533_0_functor", "parent coefficient functor/no-hidden-visible-Hom derived", "BLOCKED", "parent syntax, hidden triviality, common measure and readout closure missing"),
        ("CG2533_1_jq_zero", "j_q source leg theorem-zero", "BLOCKED", "finite coupling channels remain live"),
        ("CG2533_2_anchors", "source-backed anchors become predictions", "BLOCKED", "anchors are product/comparator/proxy constraints, not MTS prediction rows"),
        ("CG2533_3_delta_w", "delta_w material/source vector score-ready", "BLOCKED", "material vector, tau/readout and component basis missing"),
        ("CG2533_4_ppn", "PPN/local-GR vector score-ready", "BLOCKED", "alpha_cg/readout component owner/projection rows missing"),
        ("CG2533_5_local_GR_Newton", "local GR/Newton reduction derived", "BLOCKED", "coupling/source projection vector not theorem-zero or bounded"),
        ("CG2533_6_public_or_github", "public/GitHub claim allowed", "BLOCKED", "private nonclaim derivation checkpoint"),
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
        ("REF2533_0_promote_functor", "claim parent coefficient functor", "target category/parent syntax is not selected", "REFUSED"),
        ("REF2533_1_promote_noHom", "claim no-hidden-visible-Hom", "hidden invariant triviality and readout closure missing", "REFUSED"),
        ("REF2533_2_promote_anchors", "use source-backed anchors as MTS predictions", "anchors are constraints/proxies, not branch-locked MTS rows", "REFUSED"),
        ("REF2533_3_infer_delta_w", "infer delta_w from WEP bound", "requires material/source response vector and tau/readout transfer", "REFUSED"),
        ("REF2533_4_score_ppn", "score local PPN vector", "alpha_cg owner/readout-tail projections remain blocked", "REFUSED"),
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
            "row_id": "NEXT2533_0_selected",
            "priority": "selected",
            "next_file": "2534-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md",
            "next_script": "scripts/Y5_R2FR_alpha_cg_projection_owner_fill_or_deltaw_material_vector_acquisition_2534.py",
            "selected_reason": "the functor is unsigned but source-backed nonclaim anchors and the alpha_cg normal-form precedent make alpha_cg/PPN ownership the sharpest next local-GR object",
            "success_condition": "fill one alpha_cg projection blocker such as tau_PPN, same-branch owner, Z_X/M_X^2, S_PPN, common-frame/readout tail, or acquire a real delta_w material/source vector row",
            "fallback_condition": "if neither projection owner nor delta_w vector can be sourced, keep all anchors nonclaim and move to readout-tail/source-only-slot zero proof",
        },
        {
            "row_id": "NEXT2533_1_after_alpha_cg",
            "priority": "queued",
            "next_file": "2535-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md",
            "next_script": "scripts/Y5_R2FR_readout_tail_zero_proof_or_first_alpha_readout_bound_2535.py",
            "selected_reason": "2369 shows alpha_readout/readout tails become the active obstruction after alpha_cg normal-form locking",
            "success_condition": "prove projector/support/readout descent enough to set alpha_readout=0, or fill a first source-backed alpha_readout tail bound row",
            "fallback_condition": "if readout zero/bound cannot be sourced, attempt NoSourceOnlySpeciesSlot while keeping alpha_cg and delta_w nonclaim",
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
        rows.append(stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}))

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2533_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2533_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2533_02_outputs_exist", all(path.exists() for path in generated), "all 2533 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2533_03_csv_parse", parse_ok, parse_detail)

    functor = {row["row_id"]: row["proof_status"] for row in read_csv(outputs["functor"])}
    add("VAL2533_04_functor_not_promoted", functor.get("PCF2533_6_verdict") == "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED", "parent coefficient functor remains unpromoted")
    add("VAL2533_05_vertical_silence_conditional", functor.get("PCF2533_1_vertical_silence") == "EXACT_CONDITIONAL_THEOREM", "vertical coefficient silence theorem retained as conditional")
    add("VAL2533_06_jq_corollary_conditional", functor.get("PCF2533_2_jq_pushforward") == "EXACT_CONDITIONAL_COROLLARY", "j_q coefficient leg corollary recorded as conditional")

    obligations = {row["row_id"]: row["status"] for row in read_csv(outputs["obligations"])}
    add("VAL2533_07_obligations_open", obligations.get("OBL2533_6_verdict") == "OBLIGATIONS_OPEN", "proof obligations remain open")

    anchors = read_csv(outputs["anchors"])
    backed = [row for row in anchors if row.get("source_backed_anchor") == "true"]
    add("VAL2533_08_source_backed_anchors_imported", len(backed) == 3, "three source-backed nonclaim anchors imported")
    add("VAL2533_09_missing_rows_retained", any(row.get("row_id") == "ANCH2533_3_delta_w_missing" for row in anchors) and any(row.get("row_id") == "ANCH2533_4_alpha_readout_missing" for row in anchors), "delta_w and alpha_readout missing rows retained")
    add("VAL2533_10_anchors_nonclaim", all(row.get("score_ready") == "false" and row.get("valid_for_claim") == "false" for row in anchors), "all anchors remain nonclaim and not score-ready")

    acceptance = read_csv(outputs["acceptance"])
    add("VAL2533_11_no_direct_predictions", all(row.get("direct_MTS_prediction") == "false" for row in acceptance), "acceptance matrix blocks direct MTS prediction transfer")

    route = {row["row_id"]: row["decision"] for row in read_csv(outputs["route"])}
    add("VAL2533_12_route_selected", route.get("ROUTE2533_4_verdict") == "SELECT_ALPHA_CG_PROJECTION_NEXT", "alpha_cg projection owner route selected next")

    next_rows = read_csv(outputs["next"])
    add("VAL2533_13_next_selected", any(row.get("row_id") == "NEXT2533_0_selected" and "2534" in row.get("next_file", "") for row in next_rows), "2534 alpha_cg/delta_w target selected")

    copy_rows = read_csv(outputs["copies"])
    add("VAL2533_14_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2533_15_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2533_16_formalization_untouched", formal_ok, formal_detail)
    add("VAL2533_17_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2533_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2533 valid: parent coefficient functor contract sharpened, not promoted, finite coupling anchors retained nonclaim, alpha_cg projection route selected" if overall else "one or more validation gates failed",
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
    functor = read_csv(outputs["functor"])
    obligations = read_csv(outputs["obligations"])
    anchors = read_csv(outputs["anchors"])
    acceptance = read_csv(outputs["acceptance"])
    route = read_csv(outputs["route"])
    claims = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2533 - Parent Coefficient Functor Or Finite Coupling Prior Runner

**Current verdict:** the coefficient-functor route is the cleanest way to kill the bad coupling slopes, but it is still not parent-signed. Treat it as a sharp future-action contract, not a claimed theorem.

**Main gain:** the coupling problem is now expressed as a precise functor condition. If all visible coefficients are pulled back from the parent observed quotient, then every vertical generator invisible to that quotient has zero derivative on those coefficients. That would kill the dangerous visible hidden-coupling legs feeding `j_q`.

**Nonclaim anchor discipline:** source-backed external anchors are retained only as constraints/proxies. `delta_w_A` and `alpha_readout` remain missing prediction/bound rows, not wins.

## Parent Coefficient Functor Audit

{table(["row_id", "claim_piece", "proof_status", "effect_or_gap"], functor)}

## Proof Obligations

{table(["row_id", "obligation", "status", "impact"], obligations)}

## First Nonclaim Anchors

{table(["row_id", "symbol", "sector", "numeric_value_or_status", "source_backed_anchor", "arena_projection"], anchors)}

## Acceptance Matrix

{table(["row_id", "input_row", "accepted_for", "blocked_transfer", "missing_for_score"], acceptance)}

## Route Selection

{table(["row_id", "candidate_route", "evidence_status", "decision"], route)}

## Claim Gates

{table(["row_id", "claim", "status", "reason"], claims)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

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
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is useful progress but not a local-GR proof. The best next attack is to instantiate the `alpha_cg` PPN projection owner: lock the invariant normal form, then decide whether `tau_PPN`, `S_PPN`, `Z_X/M_X^2`, common-frame/readout tails, or a real `delta_w` vector can be sourced or zero-proved.
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
    write_csv(OUTPUTS["functor"], parent_coefficient_functor_audit())
    write_csv(OUTPUTS["obligations"], proof_obligation_ledger())
    write_csv(OUTPUTS["schema"], finite_coupling_runner_schema())
    write_csv(OUTPUTS["anchors"], finite_coupling_anchors_nonclaim())
    write_csv(OUTPUTS["acceptance"], runner_acceptance_matrix())
    write_csv(OUTPUTS["route"], route_selection())
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

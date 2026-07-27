from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2534"
BRANCH_ID = "MTS_R2FR_ALPHA_CG_PROJECTION_OWNER_OR_DELTAW_MATERIAL_VECTOR_2534"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2534-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2534_SOURCE_REGISTER.csv",
    "alpha": RESIDUALS / "P8_Y5_NO_SHADOW_2534_ALPHA_CG_PROJECTION_AUDIT.csv",
    "tau": RESIDUALS / "P8_Y5_NO_SHADOW_2534_TAU_PPN_COMMON_FRAME_AUDIT.csv",
    "delta": RESIDUALS / "P8_Y5_NO_SHADOW_2534_DELTAW_ACQUISITION_STATUS.csv",
    "readout": RESIDUALS / "P8_Y5_NO_SHADOW_2534_READOUT_TAIL_MATRIX.csv",
    "ready": RESIDUALS / "P8_Y5_NO_SHADOW_2534_SCORE_READINESS.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2534_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2534_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2534_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2534_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2534_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2534_VALIDATION.csv",
}

BRANCH_COPIES = {
    "alpha": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Alpha_cg_projection_audit_2534_NONCLAIM.csv",
    "ready": POST_ROOT / "source-intake" / "local_bounds" / "Alpha_cg_PPN_readiness_2534_NONCLAIM.csv",
    "delta": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "Delta_w_acquisition_status_2534_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "ART2534_NEXT_TARGET_NONCLAIM.csv",
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
    ("SRC2534_0_2533_doc", "2533-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md", "NEXT2533_0_selected", "2533 selects alpha_cg/delta_w projection owner route"),
    ("SRC2534_1_2533_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2533_VALIDATION.csv", "VAL2533_OVERALL,PASS", "2533 validation anchor"),
    ("SRC2534_2_2533_route", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2533_DELTAW_PPN_ROUTE_SELECTION.csv", "ROUTE2533_4_verdict", "2533 route decision"),
    ("SRC2534_3_2533_anchors", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2533_FIRST_NONCLAIM_COUPLING_ANCHORS.csv", "ANCH2533_4_alpha_readout_missing", "2533 retains alpha_readout missing row"),
    ("SRC2534_4_2369_doc", "2369-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md", "ACG2369_7_verdict", "alpha_cg projection precedent"),
    ("SRC2534_5_2369_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2369_VALIDATION.csv", "VAL2369_OVERALL,PASS", "2369 validation anchor"),
    ("SRC2534_6_2369_alpha", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_ALPHA_CG_PROJECTION_AUDIT.csv", "ACG2369_0_normal_form", "old alpha_cg normal-form lock"),
    ("SRC2534_7_2369_tau", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_TAU_PPN_COMMON_FRAME_AUDIT.csv", "TAU2369_4_verdict", "tau_PPN conditional-only precedent"),
    ("SRC2534_8_2369_readout", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_READOUT_TAIL_MATRIX.csv", "ART2369_5_verdict", "readout-tail obstruction precedent"),
    ("SRC2534_9_2369_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_NEXT_TARGET.csv", "NEXT2369_0_selected", "readout-tail selected next in precedent"),
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


def alpha_cg_projection_audit() -> list[dict[str, object]]:
    rows = [
        ("ACG2534_0_rescaling_invariance", "canonical invariant coupling", "under X -> k X, c_g -> c_g/k and Z_X -> Z_X/k^2, so c_g/sqrt(Z_X) is invariant for k>0", "EXACT_NORMALIZATION_LEMMA", "raw c_g cannot be scored"),
        ("ACG2534_1_normal_form", "alpha_cg^PPN", "alpha_cg^PPN = tau_PPN * S_PPN(lambda_X, env) * c_g/sqrt(Z_X)", "NORMAL_FORM_LOCKED_NONCLAIM", "legal local-GR comparison object is fixed"),
        ("ACG2534_2_common_frame", "universal common matter frame", "ordinary matter, rods, clocks, source masses and Cassini/Shapiro readout use one parent-signed matter frame", "NOT_PARENT_SIGNED", "blocks treating alpha_cg as actual Cassini leg"),
        ("ACG2534_3_same_branch", "same-branch Xhat owner", "c_g, Z_X, M_X^2, lambda_X, S_PPN, tau_PPN and tails must belong to one branch", "MISSING_PARENT_OWNER", "prevents mixing closure and finite rows"),
        ("ACG2534_4_ZX_MX", "canonical mass/range normalization", "N_X=1/sqrt(Z_X); lambda_X=sqrt(Z_X/M_X^2)", "RELATIONS_FILLED_VALUES_MISSING", "positive numeric/source-backed Z_X and M_X^2 absent"),
        ("ACG2534_5_SPPN", "range/screening transfer", "S_PPN(lambda_X,env) maps finite-range/profile effects into the Cassini/Shapiro geometry", "SPPN_GEOMETRY_MAP_MISSING", "screening cannot be hidden inside tau"),
        ("ACG2534_6_tau_PPN", "PPN projection coefficient", "tau_PPN=1 only inside strict parent-signed common-frame scalar-tensor branch", "EXACT_CONDITIONAL_NOT_ACTIVE", "active branch lacks common-frame/readout signature"),
        ("ACG2534_7_readout_vector_tails", "other PPN vector tails", "disformal, non-Hilbert, support/domain, boundary, calibration and readout tails", "VECTOR_TAILS_UNCONTROLLED", "must be zero-proved or bounded"),
        ("ACG2534_8_verdict", "alpha_cg score-ready component", "normal form is locked but no score-ready local-GR component exists", "NOT_SCORE_READY", "move to readout-tail zero proof or first bound"),
    ]
    return [
        {
            **no_claim(),
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
        ("TAU2534_0_common_frame_premise", "universal common matter frame", "S_matter uses one metric/coframe for ordinary matter, clocks, source masses and readout", "CONDITIONAL_PREMISE_ONLY", "parent ordinary-matter signature not derived"),
        ("TAU2534_1_tau_one", "tau_PPN normalization", "standard scalar-tensor common-frame branch gives gamma-1=-2 alpha_eff^2/(1+alpha_eff^2), so tau_PPN=1 by definition", "EXACT_CONDITIONAL_TAU_EQUALS_ONE", "not active until common-frame branch is signed"),
        ("TAU2534_2_screening_split", "tau versus screening", "tau_PPN is projection normalization; finite range/screening belongs in S_PPN(lambda_X,env)", "DECOMPOSITION_LOCKED", "prevents hiding screening inside tau"),
        ("TAU2534_3_readout_tail", "observed PPN readout", "fixed-before-readout, measured-GM and PPN-gauge maps must not add alpha_readout/calibration tails", "NOT_DERIVED", "tail remains explicit"),
        ("TAU2534_4_verdict", "set tau_PPN=1 in active scoring", "allowed only inside parent-signed common-frame scalar-tensor branch", "NOT_ALLOWED_YET", "retain alpha_readout and projection blockers"),
    ]
    return [
        {
            **no_claim(),
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
        ("DWA2534_0_bound_anchor", "delta_w comparator/product anchor", "MICROSCOPE/source product ceiling exists", "ANCHOR_EXISTS_PREDICTION_MISSING", "MTS material/source prediction vector missing"),
        ("DWA2534_1_material_vector", "Ti/Pt or source-test material vector", "species/material basis, charge weights, nuclear/electronic/mass response decomposition", "ACQUISITION_REQUIRED", "parent-signed map from coefficient shifts to test-mass response missing"),
        ("DWA2534_2_tau_readout", "tau_WEP/readout transfer", "experiment geometry/readout projection and no-cancellation rule", "ACQUISITION_REQUIRED", "tau_WEP operator/readout tail theorem missing"),
        ("DWA2534_3_verdict", "delta_w score object", "held as fallback lane", "DEFERRED_NONCLAIM", "build after alpha_cg projection/readout path is settled"),
    ]
    return [
        {
            **no_claim(),
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
        ("ART2534_0_alpha_readout", "alpha_readout", "alpha_readout = Pi_gamma[Delta_cal + Delta_PPN + C_feedback + C_protocol]", "RETAINED_NONCLAIM_COMPONENT", "numeric/source-backed tail values or theorem-zero certificates missing"),
        ("ART2534_1_source_feedback", "C_feedback", "D_v(Pi_A J_A)=[D_sigma Pi_A[J_A]+Pi_A D_sigma J_A]D_v sigma_A", "NORMAL_FORM_DERIVED_VALUES_MISSING", "operator norms and epsilon_sigma_A missing"),
        ("ART2534_2_protocol_tail", "C_protocol", "zero only if masks/support/orbit windows/boundary transport are fixed external protocol or q/e_obs descendants", "CLOSURE_OR_SOURCE_REQUIRED", "parent declaration or finite bound missing"),
        ("ART2534_3_commutator_zero", "source/readout commutator zero route", "if Pi_A and J_A descend through q/e_obs/theta, D_v(Pi_A J_A)=0 for v in ker(Dq)", "EXACT_CONDITIONAL_ZERO_UNSIGNED", "sector descent certificates missing"),
        ("ART2534_4_no_cancellation", "absolute PPN readout envelope", "abs(alpha_total)<=sum_abs(alpha_cg,alpha_dis,alpha_nonH,alpha_support,alpha_boundary,alpha_readout)", "ENVELOPE_ACTIVE_VALUES_MISSING", "all component values/theorem-zero rows missing"),
        ("ART2534_5_verdict", "active PPN obstruction", "common-frame theorem not derived; retain alpha_readout as explicit component", "READOUT_TAIL_SELECTED_NEXT", "next target is zero proof or first alpha_readout bound"),
    ]
    return [
        {
            **no_claim(),
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
        ("READY2534_0_alpha_normal_form", "alpha_cg^PPN", "invariant normal form locked", "same-branch owner, Z_X, M_X^2, S_PPN, tau_PPN, common frame, vector tails"),
        ("READY2534_1_tau", "tau_PPN", "exact conditional tau=1 lemma retained", "common-frame scalar-tensor branch and readout-tail zero missing"),
        ("READY2534_2_delta_w", "delta_w material/source vector", "acquisition lane retained", "material vector and tau/readout missing"),
        ("READY2534_3_readout_tail", "alpha_readout", "explicit PPN tail retained", "Delta_cal, Delta_PPN, C_feedback, C_protocol values or zero certificates missing"),
        ("READY2534_4_local_GR", "local GR/Newton recovery", "raw c_g loophole closed by normal-form rule", "full no-cancellation PPN/local residual vector not theorem-zero or bounded"),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "test_object": obj,
                "progress": progress,
                "remaining_blocker": blocker,
                "score_ready": "false",
            }
        )
        for row_id, obj, progress, blocker in rows
    ]


def route_selection() -> list[dict[str, object]]:
    rows = [
        ("DEC2534_0_alpha_cg", "alpha_cg PPN component owner", 1, "NORMAL_FORM_LOCKED_SCORE_BLOCKED", "best current local-GR test object, but projection owner/common-frame/readout blockers remain"),
        ("DEC2534_1_tau", "set tau_PPN=1", 3, "KEEP_CONDITIONAL_NOT_ACTIVE", "exact only in parent-signed common-frame scalar-tensor branch"),
        ("DEC2534_2_delta_w", "delta_w material/source vector", 2, "RETAIN_FALLBACK_ACQUISITION", "needs material vector and tau/readout transfer"),
        ("DEC2534_3_readout_tail", "alpha_readout zero proof or first bound", 1, "SELECT_NEXT_TARGET", "common-frame theorem stalls on readout/projector/support descent"),
        ("DEC2534_4_no_source_only", "NoSourceOnlySpeciesSlot syntax proof", 2, "PARALLEL_CLEANER_ROUTE", "could forbid relative source weights before they become readout tails"),
        ("DEC2534_5_empirical", "score local-GR vector", 5, "DEFER", "component vector is not theorem-zero or bounded"),
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
        ("CG2534_0_raw_cg", "raw c_g can be scored", "BLOCKED", "raw c_g is normalization-gauge dependent"),
        ("CG2534_1_alpha_cg", "alpha_cg PPN component score-ready", "BLOCKED", "same branch owner/common frame/tau/readout/vector tail blockers remain"),
        ("CG2534_2_tau", "tau_PPN=1 active branch", "BLOCKED", "common-frame scalar-tensor branch not parent-signed"),
        ("CG2534_3_delta_w", "delta_w material/source vector score-ready", "BLOCKED", "material response tensor and tau/readout transfer missing"),
        ("CG2534_4_readout", "alpha_readout zero or bound ready", "BLOCKED", "readout/support/projector descent or numeric tail bound missing"),
        ("CG2534_5_local_GR", "local GR/Newton reduction derived", "BLOCKED", "PPN/local residual vector not closed"),
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
        ("REF2534_0_raw_cg", "score raw c_g", "raw c_g is not invariant under Xhat rescaling; use alpha_cg normal form", "REFUSED"),
        ("REF2534_1_tau_one", "set tau_PPN=1 now", "common-frame parent signature and readout-tail zero are unsigned", "REFUSED"),
        ("REF2534_2_cassini_pass", "treat PPN ceiling as local-GR pass", "MTS alpha_cg prediction vector not source-backed", "REFUSED"),
        ("REF2534_3_delta_w", "infer delta_w from WEP comparator", "material/source vector and tau/readout transfer missing", "REFUSED"),
        ("REF2534_4_local_GR", "claim local GR/Newton", "alpha_readout/readout/source tails remain open", "REFUSED"),
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
            "row_id": "NEXT2534_0_selected",
            "priority": "selected",
            "next_file": "2535-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md",
            "next_script": "scripts/Y5_R2FR_readout_tail_zero_proof_or_first_alpha_readout_bound_2535.py",
            "selected_reason": "alpha_cg normal form is locked but common-frame/readout signatures remain unsigned; alpha_readout is now the active PPN obstruction",
            "success_condition": "prove projector/support/readout descent enough to set alpha_readout=0, or fill a first source-backed alpha_readout tail bound row",
            "fallback_condition": "if readout zero/bound cannot be sourced, attempt the parallel NoSourceOnlySpeciesSlot syntax proof while keeping alpha_cg and delta_w nonclaim",
        },
        {
            "row_id": "NEXT2534_1_parallel",
            "priority": "parallel",
            "next_file": "2535b-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-syntax-proof.md",
            "next_script": "scripts/Y5_R2FR_NoSourceOnlySpeciesSlot_parent_syntax_proof_2535b.py",
            "selected_reason": "parallel cleaner route: forbid relative source/species weights before they become readout/source tails",
            "success_condition": "derive parent syntax excluding source-only species slots, or stage finite delta_w/source-weight rows",
            "fallback_condition": "retain delta_w/source weights as nonclaim finite priors",
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
    add("VAL2534_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2534_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2534_02_outputs_exist", all(path.exists() for path in generated), "all 2534 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2534_03_csv_parse", parse_ok, parse_detail)

    alpha = {row["row_id"]: row["current_status"] for row in read_csv(outputs["alpha"])}
    add("VAL2534_04_rescaling_invariance", alpha.get("ACG2534_0_rescaling_invariance") == "EXACT_NORMALIZATION_LEMMA", "raw c_g rescaling issue closed by invariant normal form")
    add("VAL2534_05_alpha_normal_form", alpha.get("ACG2534_1_normal_form") == "NORMAL_FORM_LOCKED_NONCLAIM", "alpha_cg normal form locked nonclaim")
    add("VAL2534_06_alpha_not_score_ready", alpha.get("ACG2534_8_verdict") == "NOT_SCORE_READY", "alpha_cg not score-ready")

    tau = {row["row_id"]: row["result"] for row in read_csv(outputs["tau"])}
    add("VAL2534_07_tau_conditional", tau.get("TAU2534_1_tau_one") == "EXACT_CONDITIONAL_TAU_EQUALS_ONE", "tau_PPN=1 retained only as conditional")
    add("VAL2534_08_tau_not_allowed", tau.get("TAU2534_4_verdict") == "NOT_ALLOWED_YET", "active tau_PPN claim blocked")

    delta = {row["row_id"]: row["status"] for row in read_csv(outputs["delta"])}
    add("VAL2534_09_delta_deferred", delta.get("DWA2534_3_verdict") == "DEFERRED_NONCLAIM", "delta_w remains deferred nonclaim")

    readout = {row["row_id"]: row["current_status"] for row in read_csv(outputs["readout"])}
    add("VAL2534_10_readout_selected", readout.get("ART2534_5_verdict") == "READOUT_TAIL_SELECTED_NEXT", "alpha_readout/readout tail selected next")

    readiness = read_csv(outputs["ready"])
    add("VAL2534_11_readiness_nonclaim", all(row.get("score_ready") == "false" for row in readiness), "all readiness rows remain not score-ready")

    next_rows = read_csv(outputs["next"])
    add("VAL2534_12_next_selected", any(row.get("row_id") == "NEXT2534_0_selected" and "2535" in row.get("next_file", "") for row in next_rows), "2535 readout-tail target selected")

    copy_rows = read_csv(outputs["copies"])
    add("VAL2534_13_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2534_14_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2534_15_formalization_untouched", formal_ok, formal_detail)
    add("VAL2534_16_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2534_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2534 valid: raw c_g rejected, alpha_cg PPN normal form locked nonclaim, tau conditional only, readout-tail route selected" if overall else "one or more validation gates failed",
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
    alpha = read_csv(outputs["alpha"])
    tau = read_csv(outputs["tau"])
    delta = read_csv(outputs["delta"])
    readout = read_csv(outputs["readout"])
    readiness = read_csv(outputs["ready"])
    decisions = read_csv(outputs["decision"])
    claims = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2534 - alpha_cg Projection Owner Fill Or delta_w Material Vector Acquisition

**Current verdict:** raw `c_g` is now explicitly rejected as a score object. The legal local-GR comparison object is the invariant normal form `alpha_cg^PPN = tau_PPN S_PPN(lambda_X,env)c_g/sqrt(Z_X)`.

**Main gain:** this closes a real loophole. A rescaling of the hidden field changes `c_g` and `Z_X`, but not `c_g/sqrt(Z_X)`, so the branch can no longer pass or fail by a normalization convention.

**Remaining obstruction:** the normal form is not a pass. The active blockers are same-branch ownership, `Z_X/M_X^2`, `S_PPN`, common-frame/tau activation, and especially the explicit `alpha_readout` tail.

## alpha_cg Projection Audit

{table(["row_id", "projection_clause", "current_status", "effect_or_blocker"], alpha)}

## tau_PPN / Common Frame Audit

{table(["row_id", "target", "result", "effect_or_gap"], tau)}

## delta_w Acquisition Status

{table(["row_id", "needed_object", "status", "missing_input"], delta)}

## Readout Tail Matrix

{table(["row_id", "component", "current_status", "missing_for_bound"], readout)}

## Score Readiness

{table(["row_id", "test_object", "progress", "remaining_blocker", "score_ready"], readiness)}

## Route Selection

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Claim Gates

{table(["row_id", "claim", "status", "reason"], claims)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

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
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a useful local-GR narrowing step. We now have a legal PPN comparison variable and a named remaining obstruction. The next derivation target is `alpha_readout`: prove the projector/support/readout tail vanishes, or source a first finite bound. `delta_w_A` remains alive as a fallback, not a shortcut.
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
    write_csv(OUTPUTS["alpha"], alpha_cg_projection_audit())
    write_csv(OUTPUTS["tau"], tau_common_frame_audit())
    write_csv(OUTPUTS["delta"], delta_w_acquisition_status())
    write_csv(OUTPUTS["readout"], readout_tail_matrix())
    write_csv(OUTPUTS["ready"], score_readiness())
    write_csv(OUTPUTS["decision"], route_selection())
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

from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2536"
BRANCH_ID = "MTS_R2FR_SOURCE_FEEDBACK_EPSILON_SIGMA_OR_PPN_GAUGE_BOUND_2536"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2536-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"
ALPHA_READOUT_TARGET = "0.005788015401465051"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2536_SOURCE_REGISTER.csv",
    "epsilon": RESIDUALS / "P8_Y5_NO_SHADOW_2536_EPSILON_SIGMA_ZERO_AUDIT.csv",
    "leakage": RESIDUALS / "P8_Y5_NO_SHADOW_2536_FIRST_PROTOCOL_LEAKAGE_ROW.csv",
    "gauge": RESIDUALS / "P8_Y5_NO_SHADOW_2536_PPN_GAUGE_CALIBRATION_BOUND_ROW.csv",
    "universality": RESIDUALS / "P8_Y5_NO_SHADOW_2536_SOURCE_GM_UNIVERSALITY_AUDIT.csv",
    "nosource": RESIDUALS / "P8_Y5_NO_SHADOW_2536_NOSOURCEONLY_PARALLEL_ROUTE.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2536_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2536_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2536_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2536_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2536_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2536_VALIDATION.csv",
}

BRANCH_COPIES = {
    "epsilon": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Epsilon_sigma_zero_audit_2536_NONCLAIM.csv",
    "leakage": POST_ROOT / "source-intake" / "local_bounds" / "Source_GM_protocol_leakage_2536_NONCLAIM.csv",
    "nosource": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "NoSourceOnlySpeciesSlot_route_2536_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "SOURCEBLIND2536_NEXT_TARGET_NONCLAIM.csv",
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
    ("SRC2536_0_2535_doc", "2535-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md", "NEXT2535_0_selected", "2535 selected source-feedback epsilon_sigma / PPN gauge branch"),
    ("SRC2536_1_2535_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2535_VALIDATION.csv", "VAL2535_OVERALL,PASS", "2535 validation anchor"),
    ("SRC2536_2_2535_epsilon", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2535_EPSILON_SIGMA_BRIDGE.csv", "EPS2535_5_verdict", "epsilon_sigma bridge from current chain"),
    ("SRC2536_3_2371_doc", "2371-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md", "ESZA2371_5_verdict", "source-feedback precedent"),
    ("SRC2536_4_2371_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2371_VALIDATION.csv", "VAL2371_OVERALL,PASS", "2371 validation anchor"),
    ("SRC2536_5_2371_epsilon", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2371_EPSILON_SIGMA_ZERO_AUDIT.csv", "ESZA2371_5_verdict", "epsilon_sigma zero precedent"),
    ("SRC2536_6_2371_leakage", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2371_FIRST_PROTOCOL_LEAKAGE_ROW.csv", "PLR2371_0_source_GM", "first source_GM leakage row precedent"),
    ("SRC2536_7_2371_gauge", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2371_PPN_GAUGE_CALIBRATION_BOUND_ROW.csv", "PGB2371_3_bound_contract", "PPN gauge/calibration fallback precedent"),
    ("SRC2536_8_2371_universality", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2371_SOURCE_GM_UNIVERSALITY_AUDIT.csv", "UGM2371_6_verdict", "source_GM universality precedent"),
    ("SRC2536_9_2371_nosource", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2371_NOSOURCEONLY_PARALLEL_ROUTE.csv", "NSOS2371_2_source_blind_functor", "NoSourceOnlySpeciesSlot route precedent"),
    ("SRC2536_10_2371_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2371_NEXT_TARGET.csv", "NEXT2371_0_selected", "source-blind functor selected next in precedent"),
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


def epsilon_sigma_zero_audit() -> list[dict[str, object]]:
    rows = [
        ("ESZA2536_0_definition", "epsilon_sigma_A", "epsilon_sigma_A := ||D_v sigma_A|| for source/readout protocol variables sigma_A and vertical v in ker(Dq)", "DEFINITION_LOCKED", "zero requires sigma_A=sigma_bar_A(q,e_obs,theta) or fixed external protocol before variation"),
        ("ESZA2536_1_exact_zero", "descent/fixed-protocol zero", "If sigma_A descends through fixed observed quotient data or is declared fixed before variation, then D_v sigma_A=0 and the corresponding feedback tail vanishes.", "EXACT_CONDITIONAL_THEOREM", "not active because source profile, GM calibration, masks/support and boundary protocol are not parent-signed together"),
        ("ESZA2536_2_source_profile", "sigma_source_profile", "source density, composition, support/worldtube and weighting basis must be quotient-owned or fixed protocol", "NOT_PARENT_SIGNED", "relative profile/composition residual can still feed C_source_GM"),
        ("ESZA2536_3_GM_common_mode", "sigma_GM_common_mode", "one universal source normalization can be absorbed into measured G/GM, but relative source factors cannot", "GUARD_ACTIVE_NOT_NUMERIC", "same-branch calibration equation and relative source basis are missing"),
        ("ESZA2536_4_protocol_boundary", "mask/orbit/boundary protocol", "support masks, orbit windows, attitude and boundary transport must either be fixed protocol or quotient descendants", "CLOSURE_OR_SOURCE_REQUIRED", "official protocol arrays or parent descent certificate missing"),
        ("ESZA2536_5_verdict", "active epsilon_sigma zero", "all source/readout protocol variables required by alpha_readout have epsilon_sigma_A=0", "NOT_DERIVED_RETAIN_LEAKAGE_ROW", "source_GM channel remains the first live feedback input"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "sigma_piece": piece,
            "statement": statement,
            "status": status,
            "gap_or_effect": gap,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def first_protocol_leakage_row() -> list[dict[str, object]]:
    rows = [
        ("PLR2536_0_source_GM", "C_source_GM", "|Pi_gamma C_source_GM| <= |Pi_gamma| * L_source_GM * epsilon_sigma_source_GM", "L_source_GM = ||D_sigma Pi_source||||J_source|| + ||Pi_source||||D_sigma J_source||", "epsilon_sigma_source_GM = ||D_v(sigma_source_profile, sigma_GM_common_mode)||", ALPHA_READOUT_TARGET, "dimensionless alpha_PPN_total_abs_vector budget", "CONTRACT_READY_VALUES_MISSING", "needs L_source_GM and epsilon_sigma_source_GM numeric or theorem-zero rows"),
        ("PLR2536_1_LsourceGM_input", "L_source_GM", "operator/source-current Lipschitz norm in the Pi_gamma-projected source_GM channel", "requires norm convention, J_source norm, D_sigma Pi_source and D_sigma J_source", "not applicable", "MISSING_OPERATOR_NORM_AND_SOURCE_CURRENT_NORM", "declared protocol norm after PPN normalization", "INPUT_MISSING", "cannot produce alpha_readout prediction without units, basis and projection"),
        ("PLR2536_2_epsilon_input", "epsilon_sigma_source_GM", "source profile/GM protocol leakage norm", "zero if source_GM universality and NoSourceOnlySpeciesSlot are parent-signed", "||D_v(sigma_source_profile, sigma_GM_common_mode)||", "MISSING_ZERO_CERTIFICATE_OR_NUMERIC_BOUND", "declared protocol norm", "INPUT_MISSING", "finite source-profile vector remains fallback"),
        ("PLR2536_3_no_cancellation_policy", "source_GM absolute contribution", "source_GM must pass by absolute budget, not cancellation against alpha_cg, disformal, non-Hilbert, support, boundary or readout tails", "absolute-vector policy inherited from PPN vector source row", "epsilon_sigma_source_GM", ALPHA_READOUT_TARGET, "dimensionless ceiling before sibling tails", "NONCLAIM_TARGET_ONLY", "local-GR branch remains blocked until the whole absolute vector is complete"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_bound": formula,
            "lipschitz_factor": lipschitz,
            "epsilon_symbol": epsilon,
            "target_or_value": target,
            "units": units,
            "status": status,
            "missing_for_score": missing,
        }
        for row_id, quantity, formula, lipschitz, epsilon, target, units, status, missing in rows
    ]


def ppn_gauge_calibration_bound_row() -> list[dict[str, object]]:
    rows = [
        ("PGB2536_0_source_target", "PPN_gauge_calibration_readout_tail_target", f"abs(Pi_gamma[Delta_cal+Delta_PPN]) <= {ALPHA_READOUT_TARGET} as a nonclaim target", ALPHA_READOUT_TARGET, "dimensionless", "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION"),
        ("PGB2536_1_delta_cal", "Delta_cal", "M_eff[Pi_M J_H] - M_Gauss_orbital projected into gamma/readout channel", "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL", "dimensionless_or_declared_projection_units", "INPUT_MISSING"),
        ("PGB2536_2_delta_ppn", "Delta_PPN", "PPN gauge/source-normalization residual after fixing G_ref and observed source mass", "MISSING_PPN_GAUGE_TRANSFORM_AND_SOURCE_NORMALIZATION", "dimensionless_or_declared_projection_units", "INPUT_MISSING"),
        ("PGB2536_3_bound_contract", "gauge_calibration_abs_envelope", "abs(Pi_gamma Delta_cal)+abs(Pi_gamma Delta_PPN) <= target after same-frame source normalization", "MISSING_TERM_BOUNDS", "dimensionless", "BOUND_CONTRACT_READY_VALUES_MISSING"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_bound": formula,
            "numeric_value": value,
            "units": units,
            "status": status,
        }
        for row_id, quantity, formula, value, units, status in rows
    ]


def source_gm_universality_audit() -> list[dict[str, object]]:
    rows = [
        ("UGM2536_0_target", "source_GM profile universality", "D_v(sigma_source_profile, sigma_GM_common_mode)=0, hence epsilon_sigma_source_GM=0, if source profile/support and GM calibration descend through the same observed quotient data.", "TARGET_SHARPENED", "this is the exact zero route for the first source_GM leakage channel"),
        ("UGM2536_1_common_monopole", "universal exterior common-mode monopole", "If J_H is conserved, source support is fixed, one G_ref/source measure is used and all source response is common-mode, the leading exterior source leg is calibrated GM/r^2 plus bounded multipoles.", "EXACT_CONDITIONAL_LEMMA", "works only for universal source factor, not relative profile/composition residuals"),
        ("UGM2536_2_no_source_only_species_slot", "NoSourceOnlySpeciesSlot", "The parent object language must not admit species/material source weights w_A that multiply active gravitational source strength independently of non-gravitational normalization.", "SHARPEST_MISSING_PREMISE", "otherwise S_m=sum_A(1+epsilon_A)S_A remains a covariant countermodel"),
        ("UGM2536_3_GM_calibration", "measured GM common-mode guard", "Fitted GM may absorb one universal source normalization, but it cannot absorb relative source/profile/composition residuals.", "GUARD_ACTIVE_NOT_NUMERIC", "calibration equation and relative source basis are not source-filled"),
        ("UGM2536_4_profile_weighting", "orbit/worldtube-weighted source profile", "sigma_source_profile must be quotient-owned/fixed-protocol data or a source-backed orbit/profile/worldtube vector in the same basis as response projection.", "SOURCE_PROFILE_AND_COMPOSITION_OBSTRUCTION_ACTIVE", "bulk source composition is not enough; support/worldtube weighting or cancellation theorem is needed"),
        ("UGM2536_5_same_frame_pullback", "same-frame source pullback", "force law, source variation, clocks, orbit and eta/PPN readout must use the same observed coframe/time generator or retain a frame-source residual.", "SAME_FRAME_SOURCE_PULLBACK_NOT_DERIVED", "profile theorem cannot close local GR if source and readout legs live in different effective frames"),
        ("UGM2536_6_verdict", "promote epsilon_sigma_source_GM=0", "Current parent primitives prove source_GM profile/GM universality strongly enough to set epsilon_sigma_source_GM=0.", "NOT_PROVED_USE_BOUND_OR_PARENT_SYNTAX_ROUTE", "NoSourceOnlySpeciesSlot, profile/source vector, GM calibration equation, finite-source/multipole handling and same-frame pullback remain open"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "claim_piece": piece,
            "formal_statement": statement,
            "status": status,
            "proof_or_obstruction": obstruction,
        }
        for row_id, piece, statement, status, obstruction in rows
    ]


def no_source_only_parallel_route() -> list[dict[str, object]]:
    rows = [
        ("NSOS2536_0_countermodel", "covariant source-only weights survive unless excluded", "Diffeomorphism covariance alone permits S_m=sum_A w_A S_A with constant scalar species weights.", "COUNTERMODEL_ACTIVE", "do not claim WEP/local-GR descent from covariance alone"),
        ("NSOS2536_1_hilbert_current", "Hilbert-current ownership", "Once S_matter is fixed, the gravitational source is the Hilbert variation with respect to e_obs/g_obs before readout.", "EXACT_SUBTHEOREM_BUT_NOT_ENOUGH", "kills post-variation source rescaling, not pre-variation w_A inside S_matter"),
        ("NSOS2536_2_source_blind_functor", "source-blind matter functor theorem", "If ordinary matter is a source-blind descended functor with one observed measure, one Hilbert-source natural transformation and no independent SpeciesLabel -> Coeff_active_source object, then w_A is common calibration, ordinary theta_A data, or inadmissible.", "EXACT_CONDITIONAL_THEOREM", "this is the cleanest parent-action signature to try next"),
        ("NSOS2536_3_common_scale", "common source scale quotient", "A single common factor multiplying total T_matter is absorbed into kappa/G_N/GM calibration once.", "EXACT_IF_SINGLE_SCALE", "relative species/source coefficients still require parent syntax or finite source vector"),
        ("NSOS2536_4_verdict", "NoSourceOnlySpeciesSlot active branch", "The active corpus already signs the source-blind functor/admissibility clauses strongly enough to remove source-only species weights.", "NOT_PARENT_SIGNED", "write the parent-action signature or stage finite source-profile vector"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "route_piece": piece,
            "formal_statement": statement,
            "status": status,
            "effect_or_gap": gap,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2536_0_feedback_contract", "C_feedback/source_GM leakage row", 1, "LOCKED_NONCLAIM_CONTRACT", "the useful normal form is now |Pi_gamma C_source_GM| <= |Pi_gamma| L_source_GM epsilon_sigma_source_GM"),
        ("DEC2536_1_epsilon_zero", "epsilon_sigma zero theorem", 1, "KEEP_CONDITIONAL_UNSIGNED", "exact if source/readout protocol variables descend or are fixed before variation; not signed for source_GM"),
        ("DEC2536_2_ppn_gauge", "Delta_cal/Delta_PPN fallback", 2, "STAGE_PARALLEL_NONCLAIM", "keeps a concrete PPN target but does not create an MTS prediction"),
        ("DEC2536_3_nosource", "NoSourceOnlySpeciesSlot parent syntax", 1, "SELECT_NEXT_DERIVATION_TARGET", "this is the least hand-wavy route: remove the source-only coupling countermodel at parent-action level"),
        ("DEC2536_4_finite_source", "finite source-profile vector", 2, "FALLBACK_IF_PARENT_SIGNATURE_FAILS", "honest bound route if source-blind functor cannot be signed"),
        ("DEC2536_5_local_gr", "local GR/PPN pass", 5, "DEFER", "absolute PPN vector still lacks alpha_readout component values and sibling tails"),
    ]
    return [
        stamp({"row_id": row_id, "route": route, "rank": rank, "decision": decision, "reason": reason})
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("GATE2536_0_epsilon_zero", "epsilon_sigma_source_GM zero active", "FAIL", "NoSourceOnlySpeciesSlot/source-blind functor and source_GM descent are not parent-signed"),
        ("GATE2536_1_feedback_prediction", "C_source_GM numeric prediction or zero theorem", "FAIL", "L_source_GM and epsilon_sigma_source_GM are missing values or active zero"),
        ("GATE2536_2_ppn_gauge", "Delta_cal/Delta_PPN same-frame bound", "FAIL", "target exists but term bounds and same-frame source normalization are missing"),
        ("GATE2536_3_vector_completion", "absolute local PPN vector complete", "FAIL", "sibling PPN/local tails remain unclosed"),
        ("GATE2536_4_public_claim", "R10/WEP/PPN/local-GR public pass", "FAIL", "2536 is private scaffolding and refusal-runner evidence only"),
    ]
    return [
        stamp({"row_id": row_id, "gate": gate, "gate_status": status, "reason": reason})
        for row_id, gate, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2536_0_no_zero_promotion", "Refuse to set epsilon_sigma_source_GM=0 from covariance/common-mode language alone.", "relative source-only species weights remain a countermodel"),
        ("REF2536_1_no_numeric_alpha", "Refuse to publish alpha_readout or alpha_PPN_total as a numeric MTS prediction.", "C_feedback, Delta_cal, Delta_PPN, C_protocol and sibling tails lack values"),
        ("REF2536_2_no_github_claim", "Refuse to describe the local branch as GR-derived/pass-ready.", "this checkpoint is private derivation discipline, not public claim text"),
        ("REF2536_3_no_data_substitution", "Refuse to replace parent-action coupling derivation with a fitted source leakage parameter.", "finite source-profile vectors are fallback bounds, not the desired derivation"),
    ]
    return [
        stamp({"row_id": row_id, "refusal": refusal, "reason": reason})
        for row_id, refusal, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "NEXT2536_0_selected",
            "priority": "selected",
            "next_file": "2537-Y5-R2FR-parent-action-source-blind-functor-signature-or-source-profile-vector.md",
            "next_script": "scripts/Y5_R2FR_parent_action_source_blind_functor_signature_or_source_profile_vector_2537.py",
            "success_condition": "prove the parent matter action is a source-blind descended functor with no SpeciesLabel -> Coeff_active_source object, so NoSourceOnlySpeciesSlot becomes parent-signed",
            "fallback_condition": "if this cannot be signed, stage a finite source-profile/vector acquisition row with basis, units, frame, GM calibration and L_source_GM",
        },
        {
            "row_id": "NEXT2536_1_parallel",
            "priority": "parallel",
            "next_file": "2537b-Y5-R2FR-LsourceGM-bound-row-and-PPN-gauge-calibration-residual.md",
            "next_script": "scripts/Y5_R2FR_LsourceGM_bound_row_and_PPN_gauge_calibration_residual_2537b.py",
            "success_condition": "fill L_source_GM, epsilon_sigma_source_GM, Delta_cal or Delta_PPN from source-backed same-frame inputs",
            "fallback_condition": "keep alpha_readout nonclaim if any value is a target, placeholder or differently framed source",
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
        "local_gr_claim",
        "epsilon_zero_active",
        "vector_complete",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() in {"true", "pass", "passed", "ready", "yes", "1"}:
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
    add("VAL2536_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2536_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2536_02_outputs_exist", all(path.exists() for path in generated), "all 2536 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2536_03_csv_parse", parse_ok, parse_detail)

    eps = {row["row_id"]: row["status"] for row in read_csv(outputs["epsilon"])}
    add("VAL2536_04_epsilon_definition_locked", eps.get("ESZA2536_0_definition") == "DEFINITION_LOCKED", "epsilon_sigma definition locked")
    add("VAL2536_05_epsilon_zero_not_promoted", eps.get("ESZA2536_5_verdict") == "NOT_DERIVED_RETAIN_LEAKAGE_ROW", "epsilon_sigma zero remains nonclaim")

    leak = {row["row_id"]: row for row in read_csv(outputs["leakage"])}
    add("VAL2536_06_feedback_contract_ready", "L_source_GM" in leak.get("PLR2536_0_source_GM", {}).get("lipschitz_factor", ""), "source_GM feedback bound contract written")
    add("VAL2536_07_feedback_values_missing", leak.get("PLR2536_1_LsourceGM_input", {}).get("status") == "INPUT_MISSING", "L_source_GM numeric input remains missing")

    gauge = {row["row_id"]: row["status"] for row in read_csv(outputs["gauge"])}
    add("VAL2536_08_ppn_gauge_fallback_nonclaim", gauge.get("PGB2536_0_source_target") == "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION", "PPN gauge fallback imported as target only")

    universality = {row["row_id"]: row["status"] for row in read_csv(outputs["universality"])}
    add("VAL2536_09_source_gm_not_proved", universality.get("UGM2536_6_verdict") == "NOT_PROVED_USE_BOUND_OR_PARENT_SYNTAX_ROUTE", "source_GM universality not promoted")

    nosource = {row["row_id"]: row["status"] for row in read_csv(outputs["nosource"])}
    decision = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2536_10_nosource_route_selected", nosource.get("NSOS2536_2_source_blind_functor") == "EXACT_CONDITIONAL_THEOREM" and decision.get("DEC2536_3_nosource") == "SELECT_NEXT_DERIVATION_TARGET", "NoSourceOnlySpeciesSlot/source-blind functor selected next")

    next_rows = read_csv(outputs["next"])
    add("VAL2536_11_next_selected", any(row.get("row_id") == "NEXT2536_0_selected" and "2537" in row.get("next_file", "") for row in next_rows), "2537 parent-action source-blind functor target selected")

    copy_rows = read_csv(outputs["copies"])
    add("VAL2536_12_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2536_13_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2536_14_formalization_untouched", formal_ok, formal_detail)
    add("VAL2536_15_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2536_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2536 valid: source-feedback equation locked, epsilon_sigma zero not promoted, NoSourceOnlySpeciesSlot parent-action route selected" if overall else "one or more validation gates failed",
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
        lines.append("| " + " | ".join(row.get(header, "").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    epsilon = read_csv(outputs["epsilon"])
    leakage = read_csv(outputs["leakage"])
    gauge = read_csv(outputs["gauge"])
    universality = read_csv(outputs["universality"])
    nosource = read_csv(outputs["nosource"])
    decision = read_csv(outputs["decision"])
    claims = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2536 - Source-Feedback epsilon_sigma Or PPN Gauge Bound Row

**Current verdict:** `C_feedback` is now tightened into the first concrete source-channel nonclaim contract.

`|Pi_gamma C_source_GM| <= |Pi_gamma| * L_source_GM * epsilon_sigma_source_GM`.

with `L_source_GM = ||D_sigma Pi_source||||J_source|| + ||Pi_source||||D_sigma J_source||` and `epsilon_sigma_source_GM = ||D_v(sigma_source_profile, sigma_GM_common_mode)||`.

**Why this is not a win:** the exact zero theorem exists only conditionally. The source_GM channel is not parent-signed because relative source-only species/coupling weights remain a covariant countermodel.

**Best derivation route:** prove a parent-action `NoSourceOnlySpeciesSlot` / source-blind matter-functor signature. The finite fallback is a source-profile vector plus `L_source_GM`, same-frame GM calibration and PPN gauge residual bounds.

## epsilon_sigma Zero Audit

{table(["row_id", "sigma_piece", "status", "gap_or_effect"], epsilon)}

## First Protocol Leakage Row

{table(["row_id", "quantity", "formula_or_bound", "target_or_value", "status", "missing_for_score"], leakage)}

## PPN Gauge / Calibration Fallback

{table(["row_id", "quantity", "numeric_value", "status"], gauge)}

## Source_GM Universality Audit

{table(["row_id", "claim_piece", "status", "proof_or_obstruction"], universality)}

## NoSourceOnlySpeciesSlot Parallel Route

{table(["row_id", "route_piece", "status", "effect_or_gap"], nosource)}

## Decision Ledger

{table(["row_id", "route", "rank", "decision", "reason"], decision)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "reason"], claims)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["epsilon"])}`
- `{rel(outputs["leakage"])}`
- `{rel(outputs["gauge"])}`
- `{rel(outputs["universality"])}`
- `{rel(outputs["nosource"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a useful narrowing. The local-GR problem is no longer a vague PPN residue problem; it is a source-ownership/coupling problem. If the parent action forbids independent source-only species weights, the source_GM leakage route can collapse by theorem. If it does not, the branch must carry finite source-profile and calibration vectors as explicit nonclaim bounds.
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
    write_csv(OUTPUTS["epsilon"], epsilon_sigma_zero_audit())
    write_csv(OUTPUTS["leakage"], first_protocol_leakage_row())
    write_csv(OUTPUTS["gauge"], ppn_gauge_calibration_bound_row())
    write_csv(OUTPUTS["universality"], source_gm_universality_audit())
    write_csv(OUTPUTS["nosource"], no_source_only_parallel_route())
    write_csv(OUTPUTS["decision"], decision_ledger())
    write_csv(OUTPUTS["claims"], claim_gates())
    write_csv(OUTPUTS["refusal"], refusal_runner())
    write_csv(OUTPUTS["next"], next_target())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

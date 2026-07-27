from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1230"
TITLE = "1230-Y5-R10-universal-action-scale-measure-owner-theorem-or-finite-delta-w-prior"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ACTION_SCALE_OWNER_PATH = OUT_DIR / f"{PACK_ID}_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv"
MEASURE_DESCENT_PATH = OUT_DIR / f"{PACK_ID}_MEASURE_DESCENT_PROOF_STACK.csv"
FAILURE_MODE_PATH = OUT_DIR / f"{PACK_ID}_OWNER_FAILURE_MODE_LEDGER.csv"
FINITE_DELTA_PATH = OUT_DIR / f"{PACK_ID}_FINITE_DELTA_W_PRIOR_CONTRACT.csv"
LOCAL_GR_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_SOURCE_COUPLING_GATE_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1230_VALIDATION.csv"


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
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1230_0_1229_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1229_NEXT_TARGET.csv",
            "needle": "NEXT1229_0_1230",
            "purpose": "1229 handoff to action-scale/measure owner theorem or finite Delta_w contract",
        },
        {
            "source_id": "SRC1230_1_1229_clause_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
            "needle": "CLC1229_0_single_action_scale",
            "purpose": "universal source-coupling clause audit",
        },
        {
            "source_id": "SRC1230_2_1229_measure_clause",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
            "needle": "CLC1229_4_measure_coframe_connection_descent",
            "purpose": "species-blind measure/coframe/connection descent clause",
        },
        {
            "source_id": "SRC1230_3_1067_action_scale",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
            "needle": "ASO1067_5_verdict",
            "purpose": "prior action-scale owner attempt",
        },
        {
            "source_id": "SRC1230_4_1067_hbar_measure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
            "needle": "HMO1067_4_verdict",
            "purpose": "hbar/measure owner audit",
        },
        {
            "source_id": "SRC1230_5_1078_measure_attempt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
            "needle": "AM1078_4_verdict",
            "purpose": "action-measure proof attempt",
        },
        {
            "source_id": "SRC1230_6_1220_typed_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "needle": "PTOL1220_4_action_scale_measure_owner",
            "purpose": "parent typed signature action-scale owner gap",
        },
        {
            "source_id": "SRC1230_7_1219_typed_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
            "needle": "TVC1219_1_typed_domain_theorem",
            "purpose": "exact conditional typing theorem",
        },
        {
            "source_id": "SRC1230_8_1055_parent_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "purpose": "single parent action candidate",
        },
        {
            "source_id": "SRC1230_9_1224_delta_w",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
            "needle": "FSW1224_1_delta_w",
            "purpose": "finite Delta_w input gap",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    action_scale_owner = [
        {
            "owner_id": "UAS1230_0_target",
            "claim": "universal action-scale owner for ordinary matter",
            "formal_statement": "Ordinary matter actions are sections of one parent action-density line L_action with one hbar_parent; sector labels are fields/representations, not automorphisms of L_action.",
            "proof_step": "replace separate sector normalizations with one line-bundle owner before variation/readout",
            "result": "TARGET_SHARPENED",
            "missing_for_claim": "parent construction of L_action and ordinary matter category",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "UAS1230_1_connected_naturality_lemma",
            "claim": "connected matter category forces common source scale",
            "formal_statement": "If w is a natural positive automorphism of the matter action-density functor over a connected ordinary-matter category C_matter, then w_A=w_* for every object A.",
            "proof_step": "for any morphism A->B, naturality gives w_B F(f)=F(f) w_A; on nonzero action-density lines this implies w_B=w_A, and connectedness propagates equality",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "C_matter connectedness and action-density functor are not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "UAS1230_2_common_factor_absorption",
            "claim": "one common source scale is harmless",
            "formal_statement": "If w_A=w_* for all ordinary matter, T_eff=w_* sum_A T_A and w_* can be absorbed into the empirical normalization of G_N without composition-dependent residuals.",
            "proof_step": "only relative source weights survive local tests; a common multiplier renormalizes the coupling constant",
            "result": "EXACT_IF_UAS1230_1_SIGNED",
            "missing_for_claim": "does not handle relative w_A if category is disconnected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "UAS1230_3_measure_owner_extension",
            "claim": "same owner must cover path measure and Hilbert current",
            "formal_statement": "The action-density owner must also fix the quantum/statistical measure and Hilbert-current normalization; otherwise a Jacobian J_A or hbar_A recreates w_A.",
            "proof_step": "extend line-owner theorem from action syntax to measure and current extraction",
            "result": "REQUIRED_EXTENSION_NOT_PARENT_SIGNED",
            "missing_for_claim": "species-blind measure/coframe descent and current owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "UAS1230_4_current_corpus_signature",
            "claim": "current corpus signs the universal action-scale theorem",
            "formal_statement": "MTS already derives one connected matter category, one action-density line, one hbar_parent, and species-blind measure descent.",
            "proof_step": "audit 1055, 1067, 1078, 1220, and 1229 sources",
            "result": "NOT_PARENT_SIGNED",
            "missing_for_claim": "single parent object-language certificate and connected matter category remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "UAS1230_5_verdict",
            "claim": "Delta_w theorem-zero from universal action-scale owner",
            "formal_statement": "UAS1230_1 plus species-blind measure/current/readout descent would give Delta_w_AB=0 for ordinary matter source coupling.",
            "proof_step": "conditional theorem assembled; promotion denied until parent signs its premises",
            "result": "CONDITIONAL_THEOREM_ONLY_NOT_CLAIMABLE",
            "missing_for_claim": "derive C_matter connectedness, L_action owner, hbar/measure owner, source-label forgetting, and readout descent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    measure_descent = [
        {
            "measure_id": "MDS1230_0_parent_measure_line",
            "required_clause": "one parent density/measure line dmu_parent for ordinary matter",
            "exact_condition": "D_A log dmu_parent has no source-only species component after quotient",
            "status": "CONDITIONAL_NOT_DERIVED",
            "failure_if_missing": "measure factor J_A mimics source multiplier w_A",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "measure_id": "MDS1230_1_quotient_jacobian",
            "required_clause": "quotient Jacobian from parent variables to observed coframe is species-blind",
            "exact_condition": "J_q(Phi) depends on q(Phi), geometry, and universal constants, not on A or source labels",
            "status": "UNSIGNED_DESCENT",
            "failure_if_missing": "hidden representative measure leakage reopens local source residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "measure_id": "MDS1230_2_hbar_parent",
            "required_clause": "one hbar_parent/phase normalization for all ordinary matter histories",
            "exact_condition": "exp(i S_matter/hbar_parent) has no sector-specific hbar_A or w_A S_A slot",
            "status": "OWNER_NOT_DERIVED",
            "failure_if_missing": "species action-scale factors are physical in quantum/statistical weighting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "measure_id": "MDS1230_3_current_extraction",
            "required_clause": "Hilbert stress/current is extracted from the total matter action before species/readout selection",
            "exact_condition": "T_total=(2/sqrt(-g)) delta S_matter/delta g with no post-variation source weights",
            "status": "CONDITIONAL_READOUT_UNSIGNED",
            "failure_if_missing": "readout/projector maps can create effective source weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "measure_id": "MDS1230_4_verdict",
            "required_clause": "measure/current descent closes CLC1229_4",
            "exact_condition": "MDS1230_0 through MDS1230_3 all parent-signed",
            "status": "NOT_CLOSED",
            "failure_if_missing": "finite Delta_w branch remains mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    failure_modes = [
        {
            "failure_id": "FAIL1230_0_disconnected_category",
            "construction": "C_matter splits into disconnected species components with independent action-line automorphisms",
            "why_it_survives": "naturality only forces common weights inside each connected component",
            "kills_theorem_clause": "UAS1230_1",
            "status": "ACTIVE_UNTIL_PARENT_CATEGORY_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FAIL1230_1_source_only_scalar",
            "construction": "w_A is a source-only scalar attached to species/source labels",
            "why_it_survives": "ordinary covariance does not ban scalar-density multipliers",
            "kills_theorem_clause": "UAS1230_0;MDS1230_3",
            "status": "ACTIVE_UNTIL_TYPED_GRAMMAR_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FAIL1230_2_measure_jacobian",
            "construction": "species-dependent J_A in measure/coframe/quotient descent",
            "why_it_survives": "bare action equality is not enough to fix descended measure normalization",
            "kills_theorem_clause": "MDS1230_0;MDS1230_1",
            "status": "ACTIVE_UNTIL_MEASURE_DESCENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FAIL1230_3_hbar_A",
            "construction": "sector-specific hbar_A or statistical weight",
            "why_it_survives": "classical EOM cannot see overall action-scale multipliers",
            "kills_theorem_clause": "MDS1230_2",
            "status": "ACTIVE_UNTIL_HBAR_OWNER_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FAIL1230_4_readout_reentry",
            "construction": "post-variation readout/projection introduces source-weight kernel",
            "why_it_survives": "MICROSCOPE/source-worldtube readout is still data-pending",
            "kills_theorem_clause": "MDS1230_3",
            "status": "ACTIVE_UNTIL_READOUT_DESCENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_delta = [
        {
            "input_id": "FDW1230_0_Delta_w_TiPt",
            "quantity": "Delta_w_TiPt",
            "required_form": "numeric signed or absolute Ti/Pt relative source-normalization residual in the same convention as tau_WEP",
            "current_value_or_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "source_requirement": "parent-derived prior, material model, or explicit phenomenological prior clearly marked nonclaim",
            "feeds": "FR1229_3_WEP_product;PROD1224_0_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FDW1230_1_Delta_w_source_profile",
            "quantity": "Delta_w_source_profile",
            "required_form": "source-body composition/profile-weighted residual, not a bulk-composition shortcut",
            "current_value_or_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source_requirement": "Earth/source worldtube and material response in observed local frame",
            "feeds": "FR1229_1_Tres;FR1229_2_qsource",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FDW1230_2_tau_WEP",
            "quantity": "tau_WEP",
            "required_form": "official MICROSCOPE/CMSM projection factor from source residual to reported eta channel",
            "current_value_or_status": "DATA_PENDING_SYMBOLIC_ONLY",
            "source_requirement": "accepted files through 1228 intake gates plus parser/schema/provenance",
            "feeds": "FR1229_3_WEP_product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FDW1230_3_tau_PPN",
            "quantity": "tau_PPN",
            "required_form": "projection from source residual stress to PPN residual vector",
            "current_value_or_status": "PLACEHOLDER_CONTRACT_ONLY",
            "source_requirement": "local metric map and PPN bound source",
            "feeds": "FR1229_4_PPN_product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FDW1230_4_no_claim_guard",
            "quantity": "finite Delta_w branch",
            "required_form": "all products remain nonclaim until Delta_w, tau arena projections, bounds, and source paths are real",
            "current_value_or_status": "GUARD_ACTIVE",
            "source_requirement": "no MISSING markers, no placeholders, no surrogate data",
            "feeds": "claim gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_gr_update = [
        {
            "update_id": "LGU1230_0_CLC1229_0",
            "prior_clause": "CLC1229_0_single_action_scale",
            "update": "exact conditional connected-naturality theorem written",
            "new_status": "PARTIAL_EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "remaining_blocker": "derive connected ordinary matter category and action-density line owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "LGU1230_1_CLC1229_4",
            "prior_clause": "CLC1229_4_measure_coframe_connection_descent",
            "update": "measure descent clauses separated into parent measure, quotient Jacobian, hbar, and current extraction",
            "new_status": "SHARPENED_NOT_CLOSED",
            "remaining_blocker": "species-blind measure/current/readout descent proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "LGU1230_2_CLC1229_1",
            "prior_clause": "CLC1229_1_connected_matter_category",
            "update": "promoted to next root blocker because it is the decisive premise of UAS1230_1",
            "new_status": "NEXT_PRIMARY_DERIVATION_TARGET",
            "remaining_blocker": "prove ordinary matter category connectedness/source-label forgetting or retain disconnected-component Delta_w",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "LGU1230_3_local_GR",
            "prior_clause": "CLC1229_8_verdict",
            "update": "local GR source-coupling gate remains blocked",
            "new_status": "BLOCKED_NONCLAIM",
            "remaining_blocker": "UAS1230_5 verdict is conditional only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1230_0_conditional_win",
            "decision": "keep the connected-naturality theorem as the cleanest derivation route",
            "because": "if the parent matter category is connected and owns one action-density line, relative source weights collapse to one common factor",
            "next_action": "derive connected matter category/source-label forgetting directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1230_1_no_claim",
            "decision": "do not promote Delta_w=0 or local GR",
            "because": "the current corpus still lacks parent-signed category, hbar/measure, and readout descent premises",
            "next_action": "treat theorem as exact conditional only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1230_2_finite_backstop",
            "decision": "retain finite Delta_w prior contract",
            "because": "disconnected category, source-only scalar, measure Jacobian, hbar_A, and readout reentry counterexamples remain active",
            "next_action": "only score finite branch after sourced Delta_w and tau projections exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1230_0_action_scale_owner",
            "claim": "universal action-scale owner theorem",
            "status": "BLOCKED",
            "reason": "conditional theorem lacks parent-signed connected category and action-density line",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1230_1_measure_owner",
            "claim": "species-blind measure/coframe/current descent",
            "status": "BLOCKED",
            "reason": "MDS1230_4 verdict not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1230_2_Delta_w_zero",
            "claim": "Delta_w_AB=0 for ordinary matter",
            "status": "BLOCKED",
            "reason": "UAS1230_5 is conditional only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1230_3_finite_score",
            "claim": "finite Delta_w branch score",
            "status": "BLOCKED",
            "reason": "FDW1230 inputs still contain MISSING/PLACEHOLDER statuses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1230_4_local_GR",
            "claim": "derived local GR/Newton source-coupling pass",
            "status": "BLOCKED",
            "reason": "source-coupling theorem not parent-signed and finite branch not sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1230_0_1231",
            "target_file": "1231-Y5-R10-parent-matter-category-connectedness-or-source-label-residual-map.md",
            "target_script": "scripts/Y5_R10_parent_matter_category_connectedness_or_source_label_residual_map.py",
            "task": "try to prove the ordinary matter category/source functor is connected and source-label-forgetting before gravity sees it; if not, make the disconnected-component Delta_w residual map explicit",
            "success_condition": "either UAS1230_1 receives its parent category premise, or each disconnected matter component gets an explicit nonclaim residual slot",
            "do_not_do": "do not claim Delta_w=0, local GR, WEP, PPN, or public source-coupling closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        ACTION_SCALE_OWNER_PATH,
        MEASURE_DESCENT_PATH,
        FAILURE_MODE_PATH,
        FINITE_DELTA_PATH,
        LOCAL_GR_UPDATE_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(ACTION_SCALE_OWNER_PATH, action_scale_owner)
    write_csv(MEASURE_DESCENT_PATH, measure_descent)
    write_csv(FAILURE_MODE_PATH, failure_modes)
    write_csv(FINITE_DELTA_PATH, finite_delta)
    write_csv(LOCAL_GR_UPDATE_PATH, local_gr_update)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            action_scale_owner,
            measure_descent,
            failure_modes,
            finite_delta,
            local_gr_update,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    conditional_theorem_present = any(
        row["owner_id"] == "UAS1230_1_connected_naturality_lemma" and row["result"] == "EXACT_CONDITIONAL_THEOREM"
        for row in action_scale_owner
    )
    verdict_not_claimable = any(
        row["owner_id"] == "UAS1230_5_verdict" and row["result"] == "CONDITIONAL_THEOREM_ONLY_NOT_CLAIMABLE"
        for row in action_scale_owner
    )
    measure_not_closed = any(row["measure_id"] == "MDS1230_4_verdict" and row["status"] == "NOT_CLOSED" for row in measure_descent)
    active_failures = len([row for row in failure_modes if row["status"].startswith("ACTIVE")])
    finite_inputs_blocked = all(
        "MISSING" in row["current_value_or_status"]
        or "PLACEHOLDER" in row["current_value_or_status"]
        or "DATA_PENDING" in row["current_value_or_status"]
        or "GUARD_ACTIVE" in row["current_value_or_status"]
        for row in finite_delta
    )
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1231 = next_target[0]["target_file"].startswith("1231-Y5-R10-parent-matter-category")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1230_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1230_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1230_2_conditional_theorem",
            "connected-naturality theorem is written exactly as conditional",
            conditional_theorem_present,
            "UAS1230_1 result=EXACT_CONDITIONAL_THEOREM",
        ),
        validation_row(
            "VAL1230_3_verdict_not_claimable",
            "Delta_w theorem-zero is not promoted",
            verdict_not_claimable,
            "UAS1230_5 verdict blocks claim",
        ),
        validation_row(
            "VAL1230_4_measure_not_closed",
            "measure descent remains open",
            measure_not_closed,
            "MDS1230_4_verdict=NOT_CLOSED",
        ),
        validation_row(
            "VAL1230_5_failure_modes_active",
            "counterexamples/failure modes remain explicit",
            active_failures >= 5,
            f"active_failures={active_failures}",
        ),
        validation_row(
            "VAL1230_6_finite_inputs_blocked",
            "finite Delta_w rows remain blocked/nonclaim",
            finite_inputs_blocked,
            "all FDW1230 rows are missing, pending, placeholder, or guard-only",
        ),
        validation_row(
            "VAL1230_7_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1230_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1230_9_next_target_1231",
            "next target attacks matter-category connectedness",
            next_is_1231,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1230_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1230_11_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1230_12_overall",
            "overall 1230 validation",
            all(row["status"] == "PASS" for row in validation),
            "1230 converts the coupling root into an exact conditional connected-naturality theorem plus nonclaim finite Delta_w fallback",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1230 gets a real mathematical foothold but does **not** close the local-GR source-coupling theorem. If ordinary matter forms a connected parent category with one action-density line and one species-blind measure/current owner, then all source multipliers are forced to one common factor. The corpus has not yet parent-signed those premises.",
        "",
        "**Main progress:** the coupling problem is now reduced to a clean fork: prove parent matter-category connectedness plus measure descent, or retain explicit finite `Delta_w` residual inputs. This is better than vague coupling trouble; it is a target with teeth.",
        "",
        "**No-claim guard:** no `Delta_w=0`, WEP, PPN, clock, orbital, local-GR, or public claim is promoted by this checkpoint.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Action-Scale Owner Theorem Attempt",
        markdown_table(action_scale_owner, list(action_scale_owner[0].keys())),
        "",
        "## Measure Descent Proof Stack",
        markdown_table(measure_descent, list(measure_descent[0].keys())),
        "",
        "## Owner Failure Mode Ledger",
        markdown_table(failure_modes, list(failure_modes[0].keys())),
        "",
        "## Finite Delta-w Prior Contract",
        markdown_table(finite_delta, list(finite_delta[0].keys())),
        "",
        "## Local-GR Source-Coupling Gate Update",
        markdown_table(local_gr_update, list(local_gr_update[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

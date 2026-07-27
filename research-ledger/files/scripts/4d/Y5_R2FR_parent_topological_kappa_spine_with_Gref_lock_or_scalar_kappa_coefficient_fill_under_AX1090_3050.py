from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3050"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3050-Y5-R2FR-parent-topological-kappa-spine-with-Gref-lock-or-scalar-kappa-coefficient-fill-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3050_00_3049_doc": ROOT / "3049-Y5-R2FR-scalar-kappa-first-bound-runner-dryrun-or-parent-adoption-review-under-AX1090.md",
    "SRC3050_01_3049_adoption_review": RESIDUALS / "P8_Y5_R2FR_3049_TOPOLOGICAL_ADOPTION_REVIEW.csv",
    "SRC3050_02_3049_dryrun": RESIDUALS / "P8_Y5_R2FR_3049_SCALAR_KAPPA_DRYRUN_RESULTS.csv",
    "SRC3050_03_3049_claim_status": RESIDUALS / "P8_Y5_R2FR_3049_LOCAL_CLAIM_STATUS.csv",
    "SRC3050_04_3049_unlock_map": RESIDUALS / "P8_Y5_R2FR_3049_UNLOCK_CONDITION_MAP.csv",
    "SRC3050_05_3049_next": RESIDUALS / "P8_Y5_R2FR_3049_NEXT_TARGET.csv",
    "SRC3050_06_topological_clause": RESIDUALS / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
    "SRC3050_07_global_contract": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
    "SRC3050_08_constant_kappa_contract": RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
    "SRC3050_09_3046_gref": RESIDUALS / "P8_Y5_R2FR_3046_GREF_GEFF_REFERENCE_LOCK_ATTEMPT.csv",
    "SRC3050_10_3046_epsilon": RESIDUALS / "P8_Y5_R2FR_3046_EPSILON_GREF_COMPONENT_ROW.csv",
    "SRC3050_11_3045_aw_law": RESIDUALS / "P8_Y5_R2FR_3045_AW_COEFFICIENT_RATIO_LAW.csv",
    "SRC3050_12_3044_poisson": RESIDUALS / "P8_Y5_R2FR_3044_AW_SOURCE_AMPLITUDE_THEOREM_ATTEMPT.csv",
    "SRC3050_13_bound_matrix": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
    "SRC3050_14_fill_queue": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3050_SOURCE_REGISTER.csv",
    "candidate_spine": RESIDUALS / "P8_Y5_R2FR_3050_PARENT_TOPOLOGICAL_KAPPA_SPINE_CANDIDATE.csv",
    "variation_audit": RESIDUALS / "P8_Y5_R2FR_3050_VARIATION_AND_LOCAL_LIMIT_AUDIT.csv",
    "gref_lock": RESIDUALS / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv",
    "signature_gates": RESIDUALS / "P8_Y5_R2FR_3050_PARENT_SIGNATURE_GATES.csv",
    "fallback": RESIDUALS / "P8_Y5_R2FR_3050_SCALAR_COEFFICIENT_FALLBACK_SELECTION.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3050_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3050_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3050_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3050_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3050_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "candidate_spine_copy": PARENT_ACTION / "parent_topological_kappa_spine_candidate_3050_CONDITIONAL_NONCLAIM.csv",
    "variation_copy": PARENT_ACTION / "variation_and_local_limit_audit_3050_CONDITIONAL_NONCLAIM.csv",
    "gref_copy": PARENT_ACTION / "Gref_AW_normalization_lock_3050_CONDITIONAL_NONCLAIM.csv",
    "signature_copy": PARENT_ACTION / "parent_signature_gates_3050_NOT_SIGNED.csv",
    "fallback_copy": LOCAL_BOUNDS / "scalar_coefficient_fallback_selection_3050_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3050_SOURCE_FRAME_STRESS_TEST_OR_DOTG_COEFFICIENT_FILL_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: as_str(output_row.get(key, "")) for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, str]]) -> bool:
    claim_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "claim_active"}
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        values = []
        for column in columns:
            value = as_str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


source_register = [
    base(
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "parse_ok": csv_ok(path) if path.suffix.lower() == ".csv" and path.exists() else "",
            "row_count": len(rows(path)) if path.suffix.lower() == ".csv" and path.exists() else "",
            "role": source_id.split("_", 2)[-1],
            "status": "PRESENT" if path.exists() else "MISSING_BLOCKER",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

candidate_spine_rows = [
    base(
        {
            "clause_id": "SPINE3050_0_fields",
            "object": "parent fields",
            "candidate_form": "g_munu, matter fields psi, topological 3-form A_3, zero-form/global label kappa_eff",
            "mathematical_role": "A_3 enforces local constancy of kappa_eff; kappa_eff is the Einstein/source coupling label",
            "status": "CANDIDATE_PARENT_SPINE_WRITTEN_NOT_ADOPTED",
            "missing_for_active_claim": "explicit parent-action adoption",
        }
    ),
    base(
        {
            "clause_id": "SPINE3050_1_action",
            "object": "minimal action",
            "candidate_form": "S_parent = (1/(2*kappa_eff))*integral_M epsilon_g R + integral_M kappa_eff dA_3 + S_matter[g,psi] + S_boundary",
            "mathematical_role": "EH term supplies Einstein equation; topological term supplies d kappa_eff=0",
            "status": "CONDITIONAL_ACTION_CANDIDATE",
            "missing_for_active_claim": "boundary term and allowed variations must be signed in parent corpus",
        }
    ),
    base(
        {
            "clause_id": "SPINE3050_2_source_readout",
            "object": "matter/source coupling",
            "candidate_form": "S_matter depends on g_obs and psi but carries no species/source/range/frame dependence of kappa_eff",
            "mathematical_role": "prevents WEP/source-charge/range/frame scalar-kappa leakage",
            "status": "REQUIRED_CLAUSE_NOT_DERIVED_HERE",
            "missing_for_active_claim": "source-frame/matter descent audit",
        }
    ),
    base(
        {
            "clause_id": "SPINE3050_3_reference",
            "object": "observed G reference",
            "candidate_form": "G_ref := kappa_eff c^4/(8*pi)",
            "mathematical_role": "turns A_W = kappa_eff c^4/(8*pi*G_ref) into A_W=1 by definition/readout, not by fitting",
            "status": "CANDIDATE_REFERENCE_LOCK",
            "missing_for_active_claim": "parent ownership of G_ref and same-frame W/Phi readout",
        }
    ),
]

variation_rows = [
    base(
        {
            "variation_id": "VAR3050_0_A3",
            "variation": "delta A_3",
            "calculation": "delta_A3 integral kappa_eff dA_3 = - integral d kappa_eff wedge delta A_3 + boundary",
            "result": "d kappa_eff = 0 on connected local domains if variations are admissible",
            "status": "DERIVED_IF_PARENT_SECTOR_ADOPTED",
            "claim_effect": "would close time/radial/range kappa running",
        }
    ),
    base(
        {
            "variation_id": "VAR3050_1_metric",
            "variation": "delta g_munu",
            "calculation": "with d kappa_eff=0, delta_g[(1/(2*kappa_eff))*integral epsilon_g R + S_matter] gives G_munu = kappa_eff T_munu up to fixed convention",
            "result": "local Einstein equation with constant coupling",
            "status": "CONDITIONAL_NORMALIZATION_PROOF",
            "claim_effect": "would connect parent action to GR field equation",
        }
    ),
    base(
        {
            "variation_id": "VAR3050_2_kappa",
            "variation": "delta kappa_eff",
            "calculation": "delta_kappa S gives a companion global/topological equation involving dA_3 and the EH density",
            "result": "A_3 must absorb the global constraint without adding local stress/source hair",
            "status": "OPEN_GLOBAL_CONSTRAINT_AUDIT",
            "claim_effect": "blocks adoption until no local representative force is reintroduced",
        }
    ),
    base(
        {
            "variation_id": "VAR3050_3_weak_field",
            "variation": "weak-field 00 equation",
            "calculation": "G_00 approx 2 nabla^2 Phi/c^2 and T_00 approx rho c^2, so nabla^2 Phi = (kappa_eff c^4/2) rho = 4*pi*G_ref*rho",
            "result": "G_ref = kappa_eff c^4/(8*pi)",
            "status": "CONDITIONAL_NEWTON_LIMIT_LOCK",
            "claim_effect": "would close A_W if same observed frame and source normalization are signed",
        }
    ),
]

gref_rows = [
    base(
        {
            "lock_id": "GLOCK3050_0_definition",
            "identity": "G_ref := kappa_eff c^4/(8*pi)",
            "derivation": "from weak-field limit of G_munu = kappa_eff T_munu",
            "closes": "epsilon_Gref = kappa_eff c^4/(8*pi*G_ref)-1",
            "status": "CONDITIONAL_PARENT_READOUT_LOCK",
            "missing_for_claim": "same-frame W/Phi/source readout and parent adoption",
        }
    ),
    base(
        {
            "lock_id": "GLOCK3050_1_AW",
            "identity": "A_W = kappa_eff c^4/(8*pi*G_ref) = 1",
            "derivation": "substitute G_ref lock into 3045 coefficient ratio law",
            "closes": "Newton amplitude mismatch between W and Phi_metric",
            "status": "CONDITIONAL_NOT_ACTIVE",
            "missing_for_claim": "no independent G_ref denominator and no source/frame split",
        }
    ),
    base(
        {
            "lock_id": "GLOCK3050_2_residuals",
            "identity": "D_t G_ref = partial_r G_ref = partial_lambda G_ref = partial_A G_ref = 0",
            "derivation": "follows if kappa_eff is global/topological and matter/source labels act trivially",
            "closes": "Gdot, radial, R10 range, source-charge, frame split",
            "status": "REQUIRES_SOURCE_LABEL_BLINDNESS",
            "missing_for_claim": "GS2-GS5/CU2-CU5 signatures",
        }
    ),
]

signature_gate_rows = [
    base(
        {
            "gate_id": "SIG3050_0_active_parent_action",
            "requirement": "S_parent includes the EH/topological kappa spine as active theory, not just a candidate",
            "current_status": "FAILED_NOT_ADOPTED",
            "blocks_claim": "true",
            "next_action": "make explicit parent-spine adoption decision or keep as conditional theorem",
        }
    ),
    base(
        {
            "gate_id": "SIG3050_1_boundary_variation",
            "requirement": "A_3 boundary variation is fixed/topological so delta_A3 implies d kappa_eff=0",
            "current_status": "UNSIGNED",
            "blocks_claim": "true",
            "next_action": "write boundary condition and local patch admissibility clause",
        }
    ),
    base(
        {
            "gate_id": "SIG3050_2_metric_stress_silence",
            "requirement": "the kappa/A_3 topological sector adds no local non-EH stress or preferred-frame term",
            "current_status": "UNSIGNED",
            "blocks_claim": "true",
            "next_action": "audit delta_g integral kappa_eff dA_3 and companion equation",
        }
    ),
    base(
        {
            "gate_id": "SIG3050_3_matter_source_blindness",
            "requirement": "matter/source action cannot carry species, range, frame, domain or marker dependence of kappa_eff",
            "current_status": "UNSIGNED",
            "blocks_claim": "true",
            "next_action": "test source-frame/matter descent under the candidate spine",
        }
    ),
    base(
        {
            "gate_id": "SIG3050_4_Gref_same_frame",
            "requirement": "G_ref readout, W, Phi_metric and T_obs live in the same observed/source frame",
            "current_status": "UNSIGNED",
            "blocks_claim": "true",
            "next_action": "bind G_ref readout to W/Phi/source normalization map",
        }
    ),
    base(
        {
            "gate_id": "SIG3050_5_second_order_PPN",
            "requirement": "source-normalized second-order beta/residual vector is silent",
            "current_status": "DEFERRED",
            "blocks_claim": "true",
            "next_action": "only after first-order coupling gates close",
        }
    ),
]

fallback_rows = [
    base(
        {
            "fallback_id": "FALL3050_0_primary",
            "if_clause": "parent topological spine remains unsigned",
            "selected_residual": "dln_Geff_dt",
            "target_file": str(RESIDUALS / "P8_time_drift_residual_or_zero.csv"),
            "reason": "highest-impact scalar-kappa coefficient with clock/orbital/local-GR link and existing bound target",
            "required_fill": "parent zero theorem or numeric dln_Geff_dt coefficient in yr^-1",
            "status": "SELECTED_ONLY_IF_3051_PARENT_STRESS_TEST_FAILS",
        }
    ),
    base(
        {
            "fallback_id": "FALL3050_1_r10",
            "if_clause": "range/radial source hair survives parent stress test",
            "selected_residual": "alpha(lambda)",
            "target_file": str(RESIDUALS / "R10_alpha_lambda_curve_MTS_source_normalization.csv"),
            "reason": "finite range leakage directly threatens inverse-square/Newton limit",
            "required_fill": "real alpha_bound(lambda) curve plus MTS alpha_predicted(lambda)",
            "status": "SECOND_FALLBACK",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3050_0_parent_spine",
            "claim": "candidate parent topological kappa spine exists",
            "status": "YES_CANDIDATE_CONTRACT_WRITTEN",
            "claim_active": "false",
            "reason": "action/variation/readout contract is explicit, but not adopted into active theory",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3050_1_constant_kappa",
            "claim": "d kappa_eff=0 is proven for active MTS",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "depends on active S_kappa_top and boundary/stress clauses",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3050_2_AW_Newton",
            "claim": "A_W=1/Newton coefficient is derived",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "requires G_ref same-frame parent lock and source normalization silence",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3050_3_local_GR",
            "claim": "local GR/PPN pass",
            "status": "NO_REMAINS_BLOCKED",
            "claim_active": "false",
            "reason": "first-order coupling gates and second-order PPN residual vector are not all signed",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3050_0_theorem_attempt",
            "question": "Can we write a clean parent action that would derive constant kappa and G_ref?",
            "answer": "YES_AS_CONDITIONAL_CANDIDATE",
            "reason": "EH plus topological kappa/A3 sector gives a compact derivation route",
            "action": "keep as parent-spine candidate; do not claim active theorem",
        }
    ),
    base(
        {
            "decision_id": "DEC3050_1_promotion",
            "question": "Can 3050 promote Newton/local GR?",
            "answer": "NO",
            "reason": "source-frame matter descent, boundary/stress silence, and second-order PPN are unsigned",
            "action": "select 3051 source-frame/stress test",
        }
    ),
    base(
        {
            "decision_id": "DEC3050_2_fallback",
            "question": "If the parent-spine test fails, which coefficient gets filled first?",
            "answer": "dln_Geff_dt",
            "reason": "it is the first scalar-kappa leak with direct clock/orbital/local-GR relevance",
            "action": "use FALL3050_0 if 3051 fails",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3050_0_3051",
            "next_checkpoint": "3051-Y5-R2FR-source-frame-stress-test-of-topological-kappa-spine-or-first-dotG-coefficient-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_source_frame_stress_test_of_topological_kappa_spine_or_first_dotG_coefficient_fill_under_AX1090_3051.py",
            "mission": "stress-test the 3050 candidate parent spine against matter/source blindness, same-frame G_ref/W/Phi readout, topological stress silence, and the kappa companion equation; if a clause fails, fill the first dln_Geff_dt coefficient row instead",
            "starting_equation": "S_parent = (1/(2*kappa_eff))*integral epsilon_g R + integral kappa_eff dA_3 + S_matter, with G_ref = kappa_eff c^4/(8*pi)",
            "claim_policy": "no Newton/local-GR claim unless every signature gate and residual dryrun gate closes",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["candidate_spine"], candidate_spine_rows)
write_csv(OUTPUTS["variation_audit"], variation_rows)
write_csv(OUTPUTS["gref_lock"], gref_rows)
write_csv(OUTPUTS["signature_gates"], signature_gate_rows)
write_csv(OUTPUTS["fallback"], fallback_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["candidate_spine"], BRANCH_OUTPUTS["candidate_spine_copy"])
copy_csv(OUTPUTS["variation_audit"], BRANCH_OUTPUTS["variation_copy"])
copy_csv(OUTPUTS["gref_lock"], BRANCH_OUTPUTS["gref_copy"])
copy_csv(OUTPUTS["signature_gates"], BRANCH_OUTPUTS["signature_copy"])
copy_csv(OUTPUTS["fallback"], BRANCH_OUTPUTS["fallback_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3050 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["candidate_spine"],
    OUTPUTS["variation_audit"],
    OUTPUTS["gref_lock"],
    OUTPUTS["signature_gates"],
    OUTPUTS["fallback"],
    OUTPUTS["claim_status"],
    OUTPUTS["decision"],
    OUTPUTS["next"],
    OUTPUTS["branches"],
    *BRANCH_OUTPUTS.values(),
]

all_output_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_output_rows.extend(rows(path))

generated_paths = [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
formalization_generated_hits = [path for path in generated_paths if FORMALIZATION.exists() and under(path, FORMALIZATION)]

signature_blocks = [row for row in signature_gate_rows if boolish(row["blocks_claim"])]

validation_rows = [
    base({"validation_id": "VAL3050_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3050_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3050_02_spine_written", "passed": any(row["clause_id"] == "SPINE3050_1_action" and "integral_M kappa_eff dA_3" in row["candidate_form"] for row in candidate_spine_rows), "requirement": "candidate parent action with topological kappa term is written", "evidence": OUTPUTS["candidate_spine"].name}),
    base({"validation_id": "VAL3050_03_variation_derives_constancy", "passed": any(row["variation_id"] == "VAR3050_0_A3" and row["result"].startswith("d kappa_eff = 0") for row in variation_rows), "requirement": "delta A3 route derives conditional constant kappa", "evidence": OUTPUTS["variation_audit"].name}),
    base({"validation_id": "VAL3050_04_gref_lock_written", "passed": any(row["lock_id"] == "GLOCK3050_0_definition" and "kappa_eff c^4/(8*pi)" in row["identity"] for row in gref_rows), "requirement": "G_ref lock and A_W normalization are made explicit", "evidence": OUTPUTS["gref_lock"].name}),
    base({"validation_id": "VAL3050_05_signature_gates_block_claim", "passed": len(signature_blocks) >= 5, "requirement": "unsigned parent/source/frame/PPN gates block claim", "evidence": OUTPUTS["signature_gates"].name}),
    base({"validation_id": "VAL3050_06_fallback_selected", "passed": fallback_rows[0]["selected_residual"] == "dln_Geff_dt", "requirement": "fallback coefficient target is selected if parent route fails", "evidence": OUTPUTS["fallback"].name}),
    base({"validation_id": "VAL3050_07_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active flags"}),
    base({"validation_id": "VAL3050_08_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "candidate theorem is not promoted as active local-GR claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3050_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3050_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3050_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3050_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3051-"), "requirement": "next target stress-tests source/frame/stress or fills dotG coefficient", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3050_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3050 - Parent Topological Kappa Spine with Gref Lock or Scalar-Kappa Coefficient Fill

Status: `Y5_R2FR_3050_parent_topological_kappa_spine_candidate_written_not_claimed`

Generated: `{RUN_UTC}`

## Verdict

3050 gets us closer to the GR/Newton reduction target by writing the exact parent-action spine that would make the coupling route work:

`S_parent = (1/(2*kappa_eff))*integral_M epsilon_g R + integral_M kappa_eff dA_3 + S_matter[g,psi] + S_boundary`

The useful derivation chain is now explicit:

`delta_A3 S_parent -> d kappa_eff = 0`

`delta_g S_parent -> G_munu = kappa_eff T_munu`

`G_00 weak field -> G_ref = kappa_eff c^4/(8*pi)`

`A_W = kappa_eff c^4/(8*pi*G_ref) = 1`

That is the serious route. But 3050 does **not** claim local GR, because the route is still a candidate parent spine. The unsigned clauses are exactly the things a hostile reader would hit: active adoption, A3 boundary variation, topological stress silence, matter/source blindness, same-frame G_ref/W/Phi readout, and later second-order PPN.

## Candidate Parent Spine

{md_table(candidate_spine_rows, ["clause_id", "object", "candidate_form", "mathematical_role", "status", "missing_for_active_claim"])}

## Variation and Local Limit Audit

{md_table(variation_rows, ["variation_id", "variation", "calculation", "result", "status", "claim_effect"])}

## Gref Lock and AW Normalization

{md_table(gref_rows, ["lock_id", "identity", "derivation", "closes", "status", "missing_for_claim"])}

## Parent Signature Gates

{md_table(signature_gate_rows, ["gate_id", "requirement", "current_status", "blocks_claim", "next_action"])}

## Scalar Coefficient Fallback

{md_table(fallback_rows, ["fallback_id", "if_clause", "selected_residual", "target_file", "reason", "required_fill", "status"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "status", "claim_active", "reason"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "parse_ok", "row_count", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "row_count", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3050 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: parent topological kappa spine candidate written; local GR remains unclaimed")

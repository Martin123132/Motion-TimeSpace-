from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2858-Y5-R2FR-minimal-amplitude-doublet-action-consistency-gate-or-reject-under-AX1090.md"

SRC_2857_DOC = ROOT / "2857-Y5-R2FR-vertical-generator-source-hunt-or-minimal-action-construction-under-AX1090.md"
SRC_2857_NEXT = RESIDUALS / "P8_Y5_R2FR_2857_NEXT_TARGET.csv"
SRC_2857_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2857_VALIDATION.csv"
SRC_2857_ANSATZ = RESIDUALS / "P8_Y5_R2FR_2857_MINIMAL_DOUBLET_ACTION_ANSATZ.csv"
SRC_2857_ALGEBRA = RESIDUALS / "P8_Y5_R2FR_2857_ANSATZ_ALGEBRA_CHECK.csv"
SRC_2857_OWNERSHIP = RESIDUALS / "P8_Y5_R2FR_2857_PARENT_OWNERSHIP_GATE.csv"
SRC_2857_HUNT = RESIDUALS / "P8_Y5_R2FR_2857_EXISTING_GENERATOR_HUNT.csv"
SRC_2857_CLAIMS = RESIDUALS / "P8_Y5_R2FR_2857_CLAIM_GATES.csv"
SRC_727_DCDAGGER = RESIDUALS / "P8_Y5_R10_727_DCDAGGER_VERTICAL_MAP.csv"
SRC_670_CERT = RESIDUALS / "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv"
SRC_1022_VERTICAL_QUOTIENT = RESIDUALS / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv"
SRC_1045_VERTICAL_LIFT = RESIDUALS / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv"
SRC_1505_DQ_TESTS = RESIDUALS / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv"
SRC_781_ACTION = RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv"
SRC_783_FIELD_MAP = RESIDUALS / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv"
SRC_1282_DOUBLET = RESIDUALS / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2853_RUNNER = RESIDUALS / "P8_Y5_R2FR_2853_STRICT_RUNNER_RESULTS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2858_SOURCE_REGISTER.csv",
    "consistency": RESIDUALS / "P8_Y5_R2FR_2858_CONSISTENCY_GATE_MATRIX.csv",
    "nontuning": RESIDUALS / "P8_Y5_R2FR_2858_NON_TUNING_AUDIT.csv",
    "quotient": RESIDUALS / "P8_Y5_R2FR_2858_QUOTIENT_COMPATIBILITY_AUDIT.csv",
    "degree": RESIDUALS / "P8_Y5_R2FR_2858_DEGREE_COUNT_AND_HESSIAN_AUDIT.csv",
    "fallback": RESIDUALS / "P8_Y5_R2FR_2858_FINITE_FALLBACK_REQUIREMENTS.csv",
    "verdict": RESIDUALS / "P8_Y5_R2FR_2858_VERDICT_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2858_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2858_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2858_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2858_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2858_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "gate_copy": LOCAL_BOUNDS / "RAB_MINIMAL_DOUBLET_CONSISTENCY_GATE_2858_NONCLAIM.csv",
    "verdict_copy": SOURCE_WEIGHT / "RAB_UAMP_ACTION_VERDICT_2858_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2858_Uamp_parent_origin_or_fallback_NEXT.csv",
    "fallback_copy": BETA_DOCS / "RAB_FINITE_FALLBACK_REQUIREMENTS_2858_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
            "control_only": True,
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2858_0_2857_doc", SRC_2857_DOC, "U_amp = delta_R - sigma_R C_AB;NEXT2857_0_2858;VAL2857_OVERALL", "2857 verdict and handoff"),
        ("SRC2858_1_2857_next", SRC_2857_NEXT, "NEXT2857_0_2858", "2858 selected"),
        ("SRC2858_2_2857_validation", SRC_2857_VALIDATION, "VAL2857_OVERALL", "2857 validation"),
        ("SRC2858_3_2857_ansatz", SRC_2857_ANSATZ, "ANS2857_2_quotient_invariant;ANS2857_7_claim_guard", "minimal doublet ansatz"),
        ("SRC2858_4_2857_algebra", SRC_2857_ALGEBRA, "ALG2857_0_invariant;ALG2857_5_tuning_guard", "ansatz algebra check"),
        ("SRC2858_5_2857_ownership", SRC_2857_OWNERSHIP, "OWN2857_0_sigma;OWN2857_6_full_vector", "ownership gates"),
        ("SRC2858_6_2857_hunt", SRC_2857_HUNT, "HUNT2857_0_dcdagger_map;HUNT2857_4_minimal_action_contract", "generator hunt"),
        ("SRC2858_7_2857_claims", SRC_2857_CLAIMS, "CG2857_2_generator_claim;CG2857_4_local_GR_Newton", "blocked claim gates"),
        ("SRC2858_8_727_dcdagger", SRC_727_DCDAGGER, "DVM727_3_precise_map;DVM727_4_raise_index", "formal generator map"),
        ("SRC2858_9_670_cert", SRC_670_CERT, "VGC670_0_parent_Omega;VGC670_6_matter_quotient", "vertical generator certificate"),
        ("SRC2858_10_1022_quotient", SRC_1022_VERTICAL_QUOTIENT, "VQC1022_0_q_map;VQC1022_7_verdict", "quotient construction"),
        ("SRC2858_11_1045_lift", SRC_1045_VERTICAL_LIFT, "VLG1045_1_gauge_lift;VLG1045_4_verdict", "vertical lift descent"),
        ("SRC2858_12_1505_dq", SRC_1505_DQ_TESTS, "DQT1505_2_apply_Dq;DQT1505_8_acceptance", "Dq tests"),
        ("SRC2858_13_781_action", SRC_781_ACTION, "MPC781_3_matter_action;MPC781_7_contract_verdict", "minimal action contract"),
        ("SRC2858_14_783_field_map", SRC_783_FIELD_MAP, "FM783_1_Q;FM783_7_q_loc", "field map"),
        ("SRC2858_15_1282_doublet", SRC_1282_DOUBLET, "RCM1282_4_PPN_vector_lock;RCM1282_6_verdict", "full vector component map"),
        ("SRC2858_16_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign", "amplitude contract"),
        ("SRC2858_17_2853_runner", SRC_2853_RUNNER, "REFUSED_MISSING_PROVENANCE_OR_INPUTS", "strict finite fallback runner"),
    ]
    return [source_row(*spec) for spec in specs]


def consistency_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2858_0_algebra", "U_amp invariant and source split algebra", "PASS_CONDITIONAL", "2857 algebra gives a consistent current identity", "not enough for claim without ownership"),
        ("GATE2858_1_sigma_owner", "sigma_R fixed by parent kinetic/Green operator before readout", "FAIL_OPEN", "CONTRACT2844_5_sign remains missing", "blocks non-tuning"),
        ("GATE2858_2_quotient_owner", "q(Phi_parent) makes v_amp vertical and U_amp quotient/physical", "FAIL_OPEN", "VQC1022/FM783 keep q map conditional", "blocks quotient compatibility"),
        ("GATE2858_3_generator_owner", "v_amp equals Omega^{-1} DCdagger X in parent phase space", "FAIL_OPEN", "DVM727 gives formal map but Omega/DC not supplied", "blocks parent generator claim"),
        ("GATE2858_4_action_origin", "S_amp depends on U_amp because of parent symmetry", "FAIL_OPEN", "action is an ansatz not an adopted parent action", "blocks action derivation"),
        ("GATE2858_5_boundary", "K_amp/B terms vanish, are exact, or are included in Q definitions", "FAIL_OPEN", "boundary differentiability/silence missing", "blocks integrated zero"),
        ("GATE2858_6_matter_descent", "matter/source/readout see quotient variables only", "FAIL_OPEN", "matter descent and source weights unsigned", "blocks Newton/source-side derivation"),
        ("GATE2858_7_full_vector", "same branch closes full PPN/local vector", "FAIL_OPEN", "RCM1282 keeps full residual vector lock open", "blocks local-GR claim"),
    ]
    return [
        nonclaim(
            {
                "gate_id": gate_id,
                "test": test,
                "status": status,
                "evidence": evidence,
                "effect_if_open": effect,
                "gate_passed_for_claim": False,
                "control_only": True,
            }
        )
        for gate_id, test, status, evidence, effect in specs
    ]


def nontuning_rows() -> list[dict[str, Any]]:
    specs = [
        ("NT2858_0_before_readout", "U_amp and sigma_R defined before A_total/PPN readout", "OPEN", "need timestamp/source hierarchy proving U_amp is parent-derived before cancellation target"),
        ("NT2858_1_no_free_ratio", "ratio in v_amp is fixed, not adjustable", "OPEN", "normalization guard says b/a=sigma_R must be parent-owned"),
        ("NT2858_2_source_not_rescaled", "J_CAB/J_R split comes from one J_U", "CONDITIONAL_PASS", "algebra passes if S_src=-<J_U,U_amp> is parent-owned"),
        ("NT2858_3_no_hidden_counterterm", "boundary/improvement is not chosen after fit", "OPEN", "K_amp and B terms unsourced"),
        ("NT2858_4_independent_sector_survival", "galaxy/cosmology sectors are not accidentally erased", "OPEN", "domain guard and full field map not checked in this ansatz"),
        ("NT2858_5_verdict", "non-tuning gate", "FAIL_CURRENT_CLAIM", "too many parent-owner clauses are arbitrary/open"),
    ]
    return [
        nonclaim(
            {
                "nontuning_id": nontuning_id,
                "test": test,
                "status": status,
                "reason": reason,
                "non_tuning_proven": False,
                "control_only": True,
            }
        )
        for nontuning_id, test, status, reason in specs
    ]


def quotient_rows() -> list[dict[str, Any]]:
    specs = [
        ("QCA2858_0_coordinate_split", "parent amplitude coordinates split into U_amp plus a vertical coordinate V_amp", "CONDITIONAL", "requires parent field chart naming C_AB/delta_R as doublet components"),
        ("QCA2858_1_Dq", "Dq[v_amp]=0 while Dq[U_amp] is retained or physical", "OPEN", "DQT1505 says Dq computation is missing"),
        ("QCA2858_2_matter_visibility", "ordinary matter/readout cannot see V_amp", "OPEN", "VLG1045 says fixed/gauge lift is not parent-signed"),
        ("QCA2858_3_boundary_visibility", "boundary/edge cannot see V_amp as a charge", "OPEN", "VGC670 boundary differentiability not derived"),
        ("QCA2858_4_full_vector", "U_amp projection does not leave beta/preferred/source/clock/orbital residues", "OPEN", "RCM1282 full-vector lock not closed"),
        ("QCA2858_5_verdict", "quotient compatibility", "FAIL_CURRENT_CLAIM", "needs q/Dq/matter/boundary/full-vector closure"),
    ]
    return [
        nonclaim(
            {
                "quotient_id": quotient_id,
                "test": test,
                "status": status,
                "reason": reason,
                "quotient_closed": False,
                "control_only": True,
            }
        )
        for quotient_id, test, status, reason in specs
    ]


def degree_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEG2858_0_rank_one_hessian", "S_amp[U_amp] gives a rank-one Hessian in (C_AB,delta_R)", "CONDITIONAL_PASS", "one orthogonal amplitude direction is null if action truly depends only on U_amp"),
        ("DEG2858_1_null_direction", "null direction is v_amp=partial_C+sigma_R partial_R", "CONDITIONAL_PASS", "matches the desired current identity direction"),
        ("DEG2858_2_constraint_class", "null direction is first-class/proper gauge rather than second-class underdetermination", "OPEN", "bracket closure/reduced Omega not checked"),
        ("DEG2858_3_boundary_charge", "null direction has zero/improper boundary charge", "OPEN", "edge charge can make a gauge-looking mode physical"),
        ("DEG2858_4_no_extra_pole", "no physical finite local pole remains in V_amp", "OPEN", "no-pole theorem not proven"),
        ("DEG2858_5_verdict", "degree-count consistency", "FAIL_CURRENT_CLAIM", "rank-one algebra is not enough without constraint class and boundary proof"),
    ]
    return [
        nonclaim(
            {
                "degree_id": degree_id,
                "test": test,
                "status": status,
                "reason": reason,
                "degree_count_closed": False,
                "control_only": True,
            }
        )
        for degree_id, test, status, reason in specs
    ]


def fallback_rows() -> list[dict[str, Any]]:
    specs = [
        ("FB2858_0_Q_CAB", "Q_CAB", "source-backed finite row or theorem-zero owner", "still required if U_amp is not parent-owned"),
        ("FB2858_1_q_R_eff", "q_R_eff", "same convention finite row", "still required if U_amp is not parent-owned"),
        ("FB2858_2_sigma_R", "sigma_R", "operator/Green sign source", "required for either theorem route or finite scoring"),
        ("FB2858_3_boundary", "K_amp/B_CAB/B_R", "zero/exact/included or finite bound", "required before integrated cancellation"),
        ("FB2858_4_GM", "measured GM glue", "worldtube/source measure and metric 1/r readout", "required for local Newton comparison"),
        ("FB2858_5_full_vector", "full PPN/local vector", "beta/preferred/source/clock/orbital/q_loc rows", "required before local-GR claim"),
        ("FB2858_6_runner", "2853 strict runner", str(SRC_2853_RUNNER), "fallback scorer remains the honest path if theorem route fails"),
    ]
    return [
        nonclaim(
            {
                "fallback_id": fallback_id,
                "quantity": quantity,
                "required_input": required,
                "why_needed": why,
                "fallback_active": True,
                "control_only": True,
            }
        )
        for fallback_id, quantity, required, why in specs
    ]


def verdict_rows() -> list[dict[str, Any]]:
    specs = [
        ("VER2858_0_algebra", "Minimal doublet algebra is internally consistent.", "SURVIVES_AS_CANDIDATE", "U_amp gives the desired source identity without independent source rescaling if parent-owned"),
        ("VER2858_1_consistency_gate", "The action is not yet parent-owned.", "FAIL_CURRENT_CLAIM", "sigma/q/Omega/action/boundary/matter/full-vector gates remain open"),
        ("VER2858_2_rejection", "Reject theorem-zero as a claim for now.", "REJECT_CLAIM_NOT_MATH", "do not use U_amp to claim local GR/Newton until origin is derived"),
        ("VER2858_3_best_next", "Next work should attack the origin of U_amp directly.", "SELECTED_2859", "derive U_amp from parent quotient/action or demote to finite-source fallback"),
    ]
    return [
        nonclaim(
            {
                "verdict_id": verdict_id,
                "verdict": verdict,
                "status": status,
                "because": because,
                "control_only": True,
            }
        )
        for verdict_id, verdict, status, because in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2858_0_algebra_candidate", "minimal doublet algebra is viable", "PASS_CONTROL_ONLY", "candidate mechanism survives algebraic sanity check"),
        ("CG2858_1_non_tuning", "U_amp action is non-tunable", "BLOCKED", "origin of sigma and U_amp not parent-owned"),
        ("CG2858_2_quotient", "v_amp is quotient vertical", "BLOCKED", "q/Dq computation missing"),
        ("CG2858_3_integrated_zero", "Q_CAB + sigma_R q_R_eff = 0 theorem", "BLOCKED", "boundary and ownership gates open"),
        ("CG2858_4_local_Newton_GR", "local Newton/GR reduction", "BLOCKED", "matter descent, GM glue, and full vector remain open"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2858_0_keep", "Keep U_amp as the leading candidate mechanism.", "it is the first clean route that makes the amplitude cancellation structural rather than numeric if parent-owned"),
        ("DEC2858_1_no_claim", "Do not claim theorem-zero/local-GR.", "every hard ownership gate remains open"),
        ("DEC2858_2_next", "Move to parent-origin hunt for U_amp.", "the fastest way forward is proving or rejecting that the doublet/invariant already lives in the parent theory"),
        ("DEC2858_3_fallback", "Keep finite runner fallback live.", "if U_amp origin fails, the theory must score finite residuals honestly"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "control_only": True,
            }
        )
        for decision_id, decision, reason in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2858_0_2859",
                "status": "selected_primary",
                "target_doc": "2859-Y5-R2FR-Uamp-parent-origin-or-finite-source-fallback-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Uamp_parent_origin_or_finite_source_fallback_under_AX1090_2859.py",
                "mission": "try to derive U_amp=delta_R-sigma_R C_AB from existing parent quotient/action/sign structure before any amplitude readout; if the origin cannot be sourced, demote the doublet action to closure-only and route back to finite source rows",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2858_0_gate", OUTPUTS["consistency"], BRANCH_OUTPUTS["gate_copy"], "minimal doublet consistency gate nonclaim copy"),
        ("COPY2858_1_verdict", OUTPUTS["verdict"], BRANCH_OUTPUTS["verdict_copy"], "U_amp verdict nonclaim copy"),
        ("COPY2858_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2859"),
        ("COPY2858_3_fallback", OUTPUTS["fallback"], BRANCH_OUTPUTS["fallback_copy"], "finite fallback requirements copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "gate_passed",
        "gate_passed_for_claim",
        "non_tuning_proven",
        "quotient_closed",
        "degree_count_closed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2858_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2858_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2858_2_consistency_matrix", len(rows_by_name["consistency"]) >= 8, "consistency gate matrix covers algebra/sign/quotient/generator/action/boundary/matter/full-vector"),
        ("VAL2858_3_candidate_survives_only_conditionally", any(row["status"] == "PASS_CONDITIONAL" for row in rows_by_name["consistency"]) and any(row["status"] == "FAIL_OPEN" for row in rows_by_name["consistency"]), "candidate algebra passes but owner gates fail open"),
        ("VAL2858_4_nontuning_not_proven", not any(row["non_tuning_proven"] for row in rows_by_name["nontuning"]), "non-tuning is not proven"),
        ("VAL2858_5_quotient_not_closed", not any(row["quotient_closed"] for row in rows_by_name["quotient"]), "quotient compatibility is not closed"),
        ("VAL2858_6_degree_not_closed", not any(row["degree_count_closed"] for row in rows_by_name["degree"]), "degree-count/gauge status is not closed"),
        ("VAL2858_7_fallback_active", all(row["fallback_active"] for row in rows_by_name["fallback"]), "finite fallback requirements remain active"),
        ("VAL2858_8_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2858_9_next_target_2859", any(row["next_id"] == "NEXT2858_0_2859" and row["selected"] for row in rows_by_name["next"]), "2859 U_amp parent-origin target selected"),
        ("VAL2858_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2858_11_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2858_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2858_13_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2858_14_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2858_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2858_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2858_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2858_OVERALL",
            "passed": overall,
            "detail": "2858 keeps the U_amp doublet mechanism as a serious conditional candidate, refuses claim status because ownership gates remain open, and selects a parent-origin or finite-fallback target for 2859.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2858 - Y5 R2FR Minimal Amplitude Doublet Action Consistency Gate Or Reject Under AX1090

Status: `Y5_R2FR_2858_Uamp_candidate_survives_conditionally_claim_rejected_parent_origin_next`

## Private Verdict

The minimal amplitude-doublet mechanism survives as a serious candidate, not as a claim.

The good part is real: if the parent theory owns

`U_amp = delta_R - sigma_R C_AB`

and the amplitude action is

`S_amp = 1/2 <U_amp, L_U U_amp> - <J_U, U_amp> + boundary`

then the source split is structural:

`J_CAB = -sigma_R J_U`, `J_R = J_U`, so `J_CAB + sigma_R J_R = 0`

That is exactly the kind of mechanism we wanted: not a fitted cancellation, but a possible quotient/action identity.

The bad part is equally clear: current evidence does not yet prove the parent owns `sigma_R`, `U_amp`, `v_amp`, the quotient map, the boundary term, matter descent, or the full PPN/local vector. So this checkpoint rejects theorem-zero/local-GR claim status while keeping the mechanism alive as the best candidate route.

The next target is therefore not more decorative algebra. It is the origin test: derive `U_amp` from existing parent quotient/action/sign structure before any amplitude readout, or demote the route to finite-source fallback.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Consistency Gate Matrix

{markdown_table(rows["consistency"], ["gate_id", "test", "status", "evidence", "effect_if_open", "gate_passed_for_claim", "valid_for_claim"])}

## Non-Tuning Audit

{markdown_table(rows["nontuning"], ["nontuning_id", "test", "status", "reason", "non_tuning_proven", "valid_for_claim"])}

## Quotient Compatibility Audit

{markdown_table(rows["quotient"], ["quotient_id", "test", "status", "reason", "quotient_closed", "valid_for_claim"])}

## Degree Count And Hessian Audit

{markdown_table(rows["degree"], ["degree_id", "test", "status", "reason", "degree_count_closed", "valid_for_claim"])}

## Finite Fallback Requirements

{markdown_table(rows["fallback"], ["fallback_id", "quantity", "required_input", "why_needed", "fallback_active", "valid_for_claim"])}

## Verdict Ledger

{markdown_table(rows["verdict"], ["verdict_id", "verdict", "status", "because", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["consistency"] = consistency_rows()
    rows["nontuning"] = nontuning_rows()
    rows["quotient"] = quotient_rows()
    rows["degree"] = degree_rows()
    rows["fallback"] = fallback_rows()
    rows["verdict"] = verdict_rows()
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "consistency", "nontuning", "quotient", "degree", "fallback", "verdict", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2858_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2858_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

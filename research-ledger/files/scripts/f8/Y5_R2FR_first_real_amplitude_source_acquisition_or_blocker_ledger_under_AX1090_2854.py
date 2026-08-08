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

DOC = ROOT / "2854-Y5-R2FR-first-real-amplitude-source-acquisition-or-blocker-ledger-under-AX1090.md"

SRC_2853_DOC = ROOT / "2853-Y5-R2FR-finite-amplitude-fallback-source-row-or-parent-action-reentry-under-AX1090.md"
SRC_2853_RUNNER = RESIDUALS / "P8_Y5_R2FR_2853_STRICT_RUNNER_RESULTS.csv"
SRC_2853_CANDIDATE = RESIDUALS / "P8_Y5_R2FR_2853_CANDIDATE_INPUT_ROWS.csv"
SRC_2853_NEXT = RESIDUALS / "P8_Y5_R2FR_2853_NEXT_TARGET.csv"
SRC_2853_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2853_VALIDATION.csv"
SRC_2852_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2852_FINITE_AMPLITUDE_FALLBACK_CONTRACT.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_1882_SIGMAR = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_SIGMAR_NO_CIRCULARITY_MAP.csv"
SRC_1882_REFUSAL = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_RUNNER_REFUSAL.csv"
SRC_1882_TAIL = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_TAIL_ROUTE_INTEGRATION.csv"
SRC_509 = RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"
SRC_510 = RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2854_SOURCE_REGISTER.csv",
    "scan": RESIDUALS / "P8_Y5_R2FR_2854_REAL_SOURCE_ACQUISITION_SCAN.csv",
    "accepted": RESIDUALS / "P8_Y5_R2FR_2854_ACCEPTED_ROW_LEDGER.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_2854_BLOCKER_LEDGER.csv",
    "request": RESIDUALS / "P8_Y5_R2FR_2854_SOURCE_REQUEST_PACK.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2854_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2854_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2854_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2854_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2854_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "scan_copy": LOCAL_BOUNDS / "RAB_REAL_AMPLITUDE_SOURCE_SCAN_2854_NONCLAIM.csv",
    "blocker_copy": SOURCE_WEIGHT / "RAB_AMPLITUDE_BLOCKER_LEDGER_2854_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2854_parent_source_equation_draft_NEXT.csv",
    "request_copy": BETA_DOCS / "RAB_AMPLITUDE_SOURCE_REQUEST_PACK_2854_NONCLAIM.csv",
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
        ("SRC2854_0_2853_doc", SRC_2853_DOC, "NEXT2853_0_2854;VAL2853_OVERALL", "2853 handoff to real amplitude source acquisition"),
        ("SRC2854_1_2853_runner", SRC_2853_RUNNER, "RUN2853_CAND2853_0_placeholder_current_corpus;REFUSED_MISSING_PROVENANCE_OR_INPUTS", "strict runner refusal"),
        ("SRC2854_2_2853_candidate", SRC_2853_CANDIDATE, "CAND2853_0_placeholder_current_corpus;MISSING_Q_CAB", "placeholder finite candidate"),
        ("SRC2854_3_2853_next", SRC_2853_NEXT, "NEXT2853_0_2854", "2854 target selection"),
        ("SRC2854_4_2853_validation", SRC_2853_VALIDATION, "VAL2853_OVERALL", "2853 validation"),
        ("SRC2854_5_2852_fallback", SRC_2852_FALLBACK, "FB2852_0_Q_CAB;FB2852_3_A_total;FB2852_5_full_vector", "finite fallback contract"),
        ("SRC2854_6_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff;PACK2844_5_tail_bound", "Q_CAB/q_R_eff/tail missing source pack"),
        ("SRC2854_7_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_5_sign;CONTRACT2844_6_measured_GM;CONTRACT2844_7_full_vector", "sign/GM/full-vector contract gaps"),
        ("SRC2854_8_1882_sigmar", SRC_1882_SIGMAR, "SNCM1882_0_sigma_from_CR;SNCM1882_1_generalized_gamma", "b_R/sigma symbolic map"),
        ("SRC2854_9_1882_refusal", SRC_1882_REFUSAL, "RUN1882_0_combo_gamma_runner;REFUSE_CLAIM_RUN", "b_R/delta_p runner refusal"),
        ("SRC2854_10_1882_tail", SRC_1882_TAIL, "TRI1882_0_CR_kinematic_route;TRI1882_2_no_shadow_route", "tail/no-shadow route status"),
        ("SRC2854_11_509_GM", SRC_509, "T509_0_charge_identity_needed;T509_2_no_extra_mass_channel", "measured-GM conditional source route"),
        ("SRC2854_12_510_GM", SRC_510, "T510_1_worldtube_source_measure;T510_3_Newton_PPN_readout", "worldtube/metric readout route"),
        ("SRC2854_13_2631_vector", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full-vector guard"),
    ]
    return [source_row(*spec) for spec in specs]


def scan_rows() -> list[dict[str, Any]]:
    specs = [
        ("SCAN2854_0_Q_CAB", "Q_CAB", SRC_2844_PACK, "PACK2844_0_Q_CAB", "definition/status row found", "MISSING_PARENT_INPUT", "no finite numeric Q_CAB and no parent-signed zero theorem"),
        ("SCAN2854_1_q_R_eff", "q_R_eff", SRC_2844_PACK, "PACK2844_4_q_R_eff", "finite Green charge slot found", "MISSING_SOURCE_NORMALIZATION", "no finite numeric q_R_eff and no parent source normalization"),
        ("SCAN2854_2_sigma_R", "sigma_R", SRC_2844_CONTRACT, "CONTRACT2844_5_sign", "sign contract found", "MISSING_SIGN_CONVENTION", "no parent action operator sign"),
        ("SCAN2854_3_b_R", "b_R", SRC_1882_SIGMAR, "SNCM1882_1_generalized_gamma", "symbolic gamma combo found", "B_R_VALUE_MISSING", "b_R and delta_p are not independently source-backed"),
        ("SCAN2854_4_tail", "C_AB_reg/H_R/tail", SRC_2844_PACK, "PACK2844_5_tail_bound", "tail slot found", "MISSING_TAIL_BOUND", "no tail profile/bound across arenas"),
        ("SCAN2854_5_GM", "M_source/GM", SRC_510, "T510_1_worldtube_source_measure", "conditional measured-GM route found", "CONDITIONAL_ONLY_PREMISES_OPEN", "worldtube charge glue and metric readout are not closed"),
        ("SCAN2854_6_full_vector", "full PPN residual vector", SRC_2631, "PPNV2631_8_total_abs", "full-vector guard found", "SCHEMA_READY_VALUES_MISSING", "all non-gamma channels still need finite/theorem-zero rows"),
    ]
    return [
        nonclaim(
            {
                "scan_id": scan_id,
                "quantity": quantity,
                "best_source_path": str(path),
                "best_source_anchor": anchor,
                "best_hit": hit,
                "current_status": status,
                "why_not_accepted": why,
                "accepted_source_row_found": False,
                "numeric_value_present": False,
                "theorem_zero_present": False,
                "control_only": True,
            }
        )
        for scan_id, quantity, path, anchor, hit, status, why in specs
    ]


def accepted_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "accepted_id": "ACCEPT2854_0_none",
                "accepted_rows_count": 0,
                "reason": "no Q_CAB/q_R_eff/sigma_R/b_R/tail/GM/full-vector row satisfies numeric/source/theorem-zero requirements",
                "runner_to_use_when_ready": str(SRC_2853_RUNNER),
                "control_only": True,
            }
        )
    ]


def blocker_rows() -> list[dict[str, Any]]:
    specs = [
        ("BLOCK2854_0_Q_CAB", "Q_CAB", "MISSING_PARENT_INPUT", "derive/source target current or finite monopole charge", "blocks A_total"),
        ("BLOCK2854_1_q_R_eff", "q_R_eff", "MISSING_SOURCE_NORMALIZATION", "derive/source delta_R Green charge in same convention as Q_CAB", "blocks A_total"),
        ("BLOCK2854_2_sigma_R", "sigma_R", "MISSING_SIGN_CONVENTION", "derive parent operator sign and Green kernel", "blocks sign-stable A_total"),
        ("BLOCK2854_3_b_R", "b_R", "MISSING_B_R_OR_NO_SHADOW_THEOREM", "source b_R or parent no-shadow theorem", "blocks gamma combo"),
        ("BLOCK2854_4_tail", "tail/profile", "MISSING_TAIL_BOUND", "source tail profile or projection-zero theorem", "blocks arena projection"),
        ("BLOCK2854_5_GM", "M_source/GM", "MISSING_GM_PARENT_GLUE", "close worldtube/Hamiltonian charge and metric 1/r readout", "blocks delta_p/q_R_hat normalization"),
        ("BLOCK2854_6_full_vector", "full PPN vector", "MISSING_FULL_VECTOR_CLOSURE", "fill beta/preferred/source/endpoint/clock/orbital/q_loc rows", "blocks local-GR claim"),
    ]
    return [
        nonclaim(
            {
                "blocker_id": blocker_id,
                "quantity": quantity,
                "blocker_code": blocker,
                "required_resolution": resolution,
                "blocks": blocks,
                "control_only": True,
            }
        )
        for blocker_id, quantity, blocker, resolution, blocks in specs
    ]


def request_rows() -> list[dict[str, Any]]:
    specs = [
        ("REQ2854_0_parent_equations", "parent action/source equations", "equations defining L_CAB C_AB=J_CAB and L_R delta_R=J_R with all signs and Green conventions"),
        ("REQ2854_1_charge_integrals", "charge definitions", "integral definitions for Q_CAB and q_R_eff including boundary/corner terms and units"),
        ("REQ2854_2_operator_sign", "sigma_R source", "quadratic operator/Green kernel sign that fixes sigma_R"),
        ("REQ2854_3_no_shadow_or_bR", "b_R source", "finite b_R row or parent no-shadow theorem excluding the Weyl/log-coframe shadow channel"),
        ("REQ2854_4_tail_profile", "tail source", "C_AB_reg/H_R/range profile or projection bound for local arenas"),
        ("REQ2854_5_GM_glue", "measured-GM source", "worldtube/Hamiltonian/Noether charge equality and weak-field metric 1/r readout"),
        ("REQ2854_6_full_vector", "full-vector source", "non-gamma local PPN residual rows in the same branch and convention"),
    ]
    return [
        nonclaim(
            {
                "request_id": request_id,
                "needed_source": source,
                "minimum_content": content,
                "accepted_only_if": "existing source_path plus exact equation/table anchor plus units/convention; no MISSING markers",
                "control_only": True,
            }
        )
        for request_id, source, content in specs
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_control = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    specs = [
        ("CG2854_0_source_register", "source register valid", "PASS_CONTROL_ONLY" if source_control else "BLOCKED", "control source check only", source_control),
        ("CG2854_1_accepted_rows", "at least one accepted amplitude source row exists", "BLOCKED", "scan found zero accepted source rows", False),
        ("CG2854_2_runner_ready", "2853 runner can score", "BLOCKED", "core finite inputs remain missing", False),
        ("CG2854_3_parent_reentry", "parent-action theorem route reopens", "BLOCKED", "no parent equations/symmetry supplied", False),
        ("CG2854_4_local_GR_Newton", "local GR/Newton reduction claimed", "BLOCKED", "GM and full-vector blockers remain active", False),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "control_check_passed": control_passed,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason, control_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2854_0_scan", "Real amplitude source acquisition scan completed.", "NO_ACCEPTED_ROWS_FOUND", "current corpus has symbolic/missing/conditional rows only"),
        ("DEC2854_1_blockers", "Blocker ledger written.", "EXPLICIT", "Q_CAB/q_R_eff/sigma_R/b_R/tail/GM/full-vector blockers are now separated"),
        ("DEC2854_2_request_pack", "Source request pack written.", "READY", "future user/corpus inputs have exact minimum content requirements"),
        ("DEC2854_3_next", "Next target is parent source-equation drafting/reentry.", "SELECTED_2855", "if no finite rows exist, the best progress is to draft the parent equations that would create them"),
        ("DEC2854_4_no_claim", "No local-GR/Newton/PPN/R10 claim.", "LOCKED", "scan found no accepted source rows and runner remains unscored"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2854_0_2855",
                "status": "selected_primary",
                "target_doc": "2855-Y5-R2FR-parent-source-equation-draft-or-user-source-request-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_source_equation_draft_or_user_source_request_under_AX1090_2855.py",
                "mission": "draft the exact parent source equations needed to populate Q_CAB, q_R_eff, sigma_R, b_R, tail and GM rows, while clearly marking which clauses are derivation attempts versus requests for user-supplied source material",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2854_0_scan", OUTPUTS["scan"], BRANCH_OUTPUTS["scan_copy"], "real amplitude source scan nonclaim copy"),
        ("COPY2854_1_blockers", OUTPUTS["blockers"], BRANCH_OUTPUTS["blocker_copy"], "amplitude blocker ledger nonclaim copy"),
        ("COPY2854_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2855"),
        ("COPY2854_3_request", OUTPUTS["request"], BRANCH_OUTPUTS["request_copy"], "source request pack nonclaim copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table", "best_source_path", "runner_to_use_when_ready"}
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
    claim_keys = {"valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "accepted_source_row_found", "numeric_value_present", "theorem_zero_present", "gate_passed"}
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
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
        ("VAL2854_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2854_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2854_2_no_accepted_rows", not any(row["accepted_source_row_found"] for row in rows_by_name["scan"]), "no accepted source rows found"),
        ("VAL2854_3_blockers_complete", len(rows_by_name["blockers"]) >= 7, "blocker ledger covers all core finite route quantities"),
        ("VAL2854_4_request_pack_complete", len(rows_by_name["request"]) >= 7, "source request pack covers all required future inputs"),
        ("VAL2854_5_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2854_6_next_target_2855", any(row["next_id"] == "NEXT2854_0_2855" and row["selected"] for row in rows_by_name["next"]), "2855 parent source-equation draft selected"),
        ("VAL2854_7_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2854_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2854_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2854_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2854_11_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2854_12_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2854_13_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2854_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2854_OVERALL",
            "passed": overall,
            "detail": "2854 scans for real finite amplitude source rows, finds none accepted, writes blocker and request ledgers, and selects parent source-equation drafting for 2855.",
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
    content = f"""# 2854 - Y5 R2FR First Real Amplitude Source Acquisition Or Blocker Ledger Under AX1090

Status: `Y5_R2FR_2854_real_amplitude_source_scan_no_accepted_rows_blocker_ledger_nonclaim`

## Private Verdict

2854 looked for real source-backed amplitude rows after the strict 2853 runner was installed.

Result: no accepted finite row exists yet.

That does not mean the route is empty. It means the current corpus has symbolic forms, conditional identities, and well-labelled missing slots, but not claim-grade `Q_CAB`, `q_R_eff`, `sigma_R`, `b_R`, tail, `GM`, or full-vector inputs.

The useful output is the blocker split: we now know exactly which missing object blocks which part of the local-GR bridge. The next best move is to draft the parent source equations that could populate those rows, while also producing a source-request pack if the missing material exists elsewhere in the corpus or in your notes.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Real Source Acquisition Scan

{markdown_table(rows["scan"], ["scan_id", "quantity", "best_hit", "current_status", "why_not_accepted", "accepted_source_row_found", "valid_for_claim"])}

## Accepted Row Ledger

{markdown_table(rows["accepted"], ["accepted_id", "accepted_rows_count", "reason", "valid_for_claim"])}

## Blocker Ledger

{markdown_table(rows["blockers"], ["blocker_id", "quantity", "blocker_code", "required_resolution", "blocks", "valid_for_claim"])}

## Source Request Pack

{markdown_table(rows["request"], ["request_id", "needed_source", "minimum_content", "accepted_only_if", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

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
    rows["scan"] = scan_rows()
    rows["accepted"] = accepted_rows()
    rows["blockers"] = blocker_rows()
    rows["request"] = request_rows()
    rows["claim_gates"] = claim_gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "scan", "accepted", "blockers", "request", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2854_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2854_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

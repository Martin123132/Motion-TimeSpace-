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

DOC = ROOT / "2860-Y5-R2FR-finite-source-row-acquisition-after-Uamp-demotion-under-AX1090.md"

SRC_2859_DOC = ROOT / "2859-Y5-R2FR-Uamp-parent-origin-or-finite-source-fallback-under-AX1090.md"
SRC_2859_NEXT = RESIDUALS / "P8_Y5_R2FR_2859_NEXT_TARGET.csv"
SRC_2859_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2859_VALIDATION.csv"
SRC_2859_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2859_FINITE_SOURCE_FALLBACK_QUEUE.csv"
SRC_2859_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2859_CLOSURE_DEMOTION_LEDGER.csv"
SRC_2859_ORIGIN = RESIDUALS / "P8_Y5_R2FR_2859_PARENT_ORIGIN_SCAN.csv"
SRC_2854_SCAN = RESIDUALS / "P8_Y5_R2FR_2854_REAL_SOURCE_ACQUISITION_SCAN.csv"
SRC_2854_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2854_BLOCKER_LEDGER.csv"
SRC_2854_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2854_SOURCE_REQUEST_PACK.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2853_CANDIDATE = RESIDUALS / "P8_Y5_R2FR_2853_CANDIDATE_INPUT_ROWS.csv"
SRC_2853_RUNNER = RESIDUALS / "P8_Y5_R2FR_2853_STRICT_RUNNER_RESULTS.csv"
SRC_2853_REENTRY = RESIDUALS / "P8_Y5_R2FR_2853_PARENT_ACTION_REENTRY_HOOK.csv"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"
SRC_1882_SIGMAR = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_SIGMAR_NO_CIRCULARITY_MAP.csv"
SRC_509 = RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"
SRC_510 = RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2860_SOURCE_REGISTER.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_2860_FINITE_SOURCE_ACQUISITION_PACK.csv",
    "template": RESIDUALS / "P8_Y5_R2FR_2860_STRICT_RUNNER_IMPORT_TEMPLATE_NONCLAIM.csv",
    "preflight": RESIDUALS / "P8_Y5_R2FR_2860_STRICT_IMPORT_PREFLIGHT.csv",
    "handoff": RESIDUALS / "P8_Y5_R2FR_2860_RUNNER_HANDOFF_LEDGER.csv",
    "evidence": RESIDUALS / "P8_Y5_R2FR_2860_BLOCKER_TO_EVIDENCE_MAP.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2860_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2860_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2860_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2860_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2860_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "acquisition_copy": LOCAL_BOUNDS / "RAB_FINITE_SOURCE_ACQUISITION_PACK_2860_NONCLAIM.csv",
    "preflight_copy": SOURCE_WEIGHT / "RAB_STRICT_IMPORT_PREFLIGHT_2860_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2860_QCAB_qReff_sigma_first_source_rows_NEXT.csv",
    "template_copy": BETA_DOCS / "RAB_STRICT_RUNNER_IMPORT_TEMPLATE_2860_NONCLAIM.csv",
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
        ("SRC2860_0_2859_doc", SRC_2859_DOC, "NEXT2859_0_2860;VAL2859_OVERALL", "2859 verdict and handoff"),
        ("SRC2860_1_2859_next", SRC_2859_NEXT, "NEXT2859_0_2860", "2860 selected"),
        ("SRC2860_2_2859_validation", SRC_2859_VALIDATION, "VAL2859_OVERALL", "2859 validation"),
        ("SRC2860_3_2859_fallback", SRC_2859_FALLBACK, "FSQ2859_0_Q_CAB;FSQ2859_6_strict_runner", "finite fallback queue"),
        ("SRC2860_4_2859_demotion", SRC_2859_DEMOTION, "DEM2859_1_claim_status;DEM2859_2_runner_status", "closure demotion"),
        ("SRC2860_5_2859_origin", SRC_2859_ORIGIN, "ORG2859_0_direct_parent_uamp;ORG2859_6_matter_full_vector_origin", "U_amp origin failure"),
        ("SRC2860_6_2854_scan", SRC_2854_SCAN, "SCAN2854_0_Q_CAB;SCAN2854_6_full_vector", "real source acquisition scan"),
        ("SRC2860_7_2854_blockers", SRC_2854_BLOCKERS, "BLOCK2854_0_Q_CAB;BLOCK2854_6_full_vector", "blocker ledger"),
        ("SRC2860_8_2854_requests", SRC_2854_REQUESTS, "REQ2854_0_parent_equations;REQ2854_6_full_vector", "source request pack"),
        ("SRC2860_9_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_5_tail_bound", "amplitude source pack"),
        ("SRC2860_10_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_5_sign;CONTRACT2844_6_measured_GM", "amplitude contract"),
        ("SRC2860_11_2853_candidate", SRC_2853_CANDIDATE, "CAND2853_0_placeholder_current_corpus;MISSING_Q_CAB", "strict runner candidate shape"),
        ("SRC2860_12_2853_runner", SRC_2853_RUNNER, "REFUSED_MISSING_PROVENANCE_OR_INPUTS", "strict runner refusal"),
        ("SRC2860_13_2853_reentry", SRC_2853_REENTRY, "RE2853_0_parent_source_equation;RE2853_3_full_vector", "parent theorem reentry hooks"),
        ("SRC2860_14_2631", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full vector guard"),
        ("SRC2860_15_1882_sigmar", SRC_1882_SIGMAR, "SNCM1882_1_generalized_gamma", "symbolic sigma/b_R map"),
        ("SRC2860_16_509", SRC_509, "T509_0_charge_identity_needed;T509_2_no_extra_mass_channel", "source-measure theorem"),
        ("SRC2860_17_510", SRC_510, "T510_1_worldtube_source_measure;T510_3_Newton_PPN_readout", "worldtube source-measure theorem"),
    ]
    return [source_row(*spec) for spec in specs]


def acquisition_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ACQ2860_0_Q_CAB",
            "Q_CAB",
            "source-backed finite monopole charge",
            "real number in same charge convention as q_R_eff",
            "source_path; equation_anchor; units; boundary policy; sign convention",
            "SCAN2854_0_Q_CAB;BLOCK2854_0_Q_CAB;PACK2844_0_Q_CAB",
            "MISSING_PARENT_INPUT",
            "first_core_row",
        ),
        (
            "ACQ2860_1_q_R_eff",
            "q_R_eff",
            "source-backed finite curvature Green charge",
            "real number in same charge convention as Q_CAB",
            "source_path; equation_anchor; Green normalization; units; boundary policy",
            "SCAN2854_1_q_R_eff;BLOCK2854_1_q_R_eff;PACK2844_4_q_R_eff",
            "MISSING_SOURCE_NORMALIZATION",
            "first_core_row",
        ),
        (
            "ACQ2860_2_sigma_R",
            "sigma_R",
            "parent operator/Green sign",
            "numeric sign or signed convention row",
            "source_path; equation_anchor; metric signature; Green orientation; operator sign",
            "SCAN2854_2_sigma_R;BLOCK2854_2_sigma_R;CONTRACT2844_5_sign",
            "MISSING_SIGN_CONVENTION",
            "first_core_row",
        ),
        (
            "ACQ2860_3_b_R",
            "b_R",
            "finite b_R or no-shadow theorem",
            "real coefficient or theorem-zero owner",
            "source_path; equation_anchor; no-shadow theorem or finite derivative definition",
            "SCAN2854_3_b_R;BLOCK2854_3_b_R;SNCM1882_1_generalized_gamma",
            "MISSING_B_R_OR_NO_SHADOW_THEOREM",
            "second_core_row",
        ),
        (
            "ACQ2860_4_boundary_tail",
            "K_amp/B_CAB/B_R/tail",
            "boundary/tail zero, exact, included, or finite bound",
            "bound or theorem-zero certificate",
            "source_path; equation_anchor; compact support/domain; included charge definition",
            "SCAN2854_4_tail;BLOCK2854_4_tail;PACK2844_5_tail_bound",
            "MISSING_TAIL_BOUND",
            "second_core_row",
        ),
        (
            "ACQ2860_5_GM",
            "M_source/GM",
            "measured-GM glue",
            "worldtube/Hamiltonian mass equals weak-field 1/r metric mass",
            "source_path; equation_anchor; no extra mass channel; metric readout convention",
            "SCAN2854_5_GM;BLOCK2854_5_GM;T510_1_worldtube_source_measure",
            "CONDITIONAL_ONLY_PREMISES_OPEN",
            "third_core_row",
        ),
        (
            "ACQ2860_6_full_vector",
            "full PPN/local vector",
            "same-branch non-gamma residual rows",
            "finite or theorem-zero rows for beta/preferred/source/clock/orbital/q_loc",
            "source_path; equation_anchor; branch id; convention; residual vector components",
            "SCAN2854_6_full_vector;BLOCK2854_6_full_vector;PPNV2631_8_total_abs",
            "SCHEMA_READY_VALUES_MISSING",
            "third_core_row",
        ),
    ]
    return [
        nonclaim(
            {
                "acquisition_id": acquisition_id,
                "quantity": quantity,
                "required_object": required_object,
                "minimum_value": minimum_value,
                "minimum_provenance": provenance,
                "source_anchors": anchors,
                "current_blocker": blocker,
                "priority": priority,
                "accepted_source_present": False,
                "numeric_or_theorem_zero_present": False,
                "ready_for_strict_runner": False,
                "control_only": True,
            }
        )
        for acquisition_id, quantity, required_object, minimum_value, provenance, anchors, blocker, priority in specs
    ]


def template_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "candidate_id": "CAND2860_0_finite_source_import_template_nonclaim",
                "branch_id": "R2FR_local_PPN_constant_limit_after_Uamp_demotion",
                "Q_CAB_value": "MISSING_Q_CAB",
                "q_R_eff_value": "MISSING_q_R_eff",
                "sigma_R_value": "MISSING_sigma_R",
                "GM_value": "MISSING_GM",
                "b_R_value": "MISSING_b_R",
                "tail_status": "MISSING_TAIL_PROFILE",
                "full_vector_status": "MISSING_FULL_VECTOR",
                "Q_CAB_source_path": "",
                "q_R_eff_source_path": "",
                "sigma_R_source_path": "",
                "GM_source_path": "",
                "green_convention": "MISSING_GREEN_CONVENTION",
                "sign_convention": "MISSING_SIGN_CONVENTION",
                "GM_convention": "MISSING_GM_CONVENTION",
                "parent_theorem_zero": False,
                "theorem_zero_authority": "UAMP_DEMOTED_CLOSURE_ONLY",
                "numeric_value_present": False,
                "control_only": True,
            }
        )
    ]


def preflight_rows(template: list[dict[str, Any]]) -> list[dict[str, Any]]:
    row = template[0]
    checks = [
        ("PF2860_0_Q_CAB_value", "Q_CAB_value", row["Q_CAB_value"], "finite numeric"),
        ("PF2860_1_q_R_eff_value", "q_R_eff_value", row["q_R_eff_value"], "finite numeric"),
        ("PF2860_2_sigma_R_value", "sigma_R_value", row["sigma_R_value"], "finite numeric/sign"),
        ("PF2860_3_GM_value", "GM_value", row["GM_value"], "finite numeric"),
        ("PF2860_4_Q_CAB_source", "Q_CAB_source_path", row["Q_CAB_source_path"], "existing source path"),
        ("PF2860_5_q_R_eff_source", "q_R_eff_source_path", row["q_R_eff_source_path"], "existing source path"),
        ("PF2860_6_sigma_R_source", "sigma_R_source_path", row["sigma_R_source_path"], "existing source path"),
        ("PF2860_7_GM_source", "GM_source_path", row["GM_source_path"], "existing source path"),
        ("PF2860_8_conventions", "green/sign/GM conventions", f"{row['green_convention']};{row['sign_convention']};{row['GM_convention']}", "no MISSING convention markers"),
        ("PF2860_9_b_R_tail_vector", "b_R/tail/full_vector", f"{row['b_R_value']};{row['tail_status']};{row['full_vector_status']}", "b_R plus tail plus full vector filled"),
    ]
    rows: list[dict[str, Any]] = []
    for check_id, field, value, requirement in checks:
        missing = value == "" or "MISSING" in str(value)
        rows.append(
            nonclaim(
                {
                    "preflight_id": check_id,
                    "field": field,
                    "value_or_marker": value,
                    "requirement": requirement,
                    "passed": not missing,
                    "failure_reason": "MISSING_OR_PLACEHOLDER_INPUT" if missing else "",
                    "control_only": True,
                }
            )
        )
    rows.append(
        nonclaim(
            {
                "preflight_id": "PF2860_OVERALL",
                "field": "strict_import_template",
                "value_or_marker": "template remains placeholder-only",
                "requirement": "all finite source rows and conventions present",
                "passed": False,
                "failure_reason": "REFUSED_MISSING_PROVENANCE_OR_INPUTS",
                "control_only": True,
            }
        )
    )
    return rows


def handoff_rows() -> list[dict[str, Any]]:
    specs = [
        ("HAND2860_0_runner", "2853 strict runner", str(SRC_2853_RUNNER), "do not rerun as claim until preflight passes"),
        ("HAND2860_1_template", "2860 import template", str(OUTPUTS["template"]), "template is schema-ready but intentionally invalid"),
        ("HAND2860_2_first_rows", "Q_CAB/q_R_eff/sigma_R first-row target", str(OUTPUTS["acquisition"]), "fill first_core_row before any A_total attempt"),
        ("HAND2860_3_claim_guard", "U_amp theorem-zero route", "DEMOTED_CLOSURE_ONLY", "cannot substitute for finite rows"),
    ]
    return [
        nonclaim(
            {
                "handoff_id": handoff_id,
                "object": obj,
                "target": target,
                "instruction": instruction,
                "runner_allowed": False,
                "control_only": True,
            }
        )
        for handoff_id, obj, target, instruction in specs
    ]


def evidence_rows(acquisition: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "evidence_id": row["acquisition_id"].replace("ACQ", "EVID"),
                "quantity": row["quantity"],
                "current_blocker": row["current_blocker"],
                "source_anchors": row["source_anchors"],
                "minimum_provenance": row["minimum_provenance"],
                "accepted_source_present": row["accepted_source_present"],
                "control_only": True,
            }
        )
        for row in acquisition
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2860_0_acquisition_pack", "finite-source acquisition pack exists", "PASS_CONTROL_ONLY", "pack is written but contains no accepted source values"),
        ("CG2860_1_import_template", "strict runner import template exists", "PASS_CONTROL_ONLY", "template is schema-ready but invalid by design"),
        ("CG2860_2_preflight", "strict runner preflight passes", "BLOCKED", "placeholder/missing inputs remain"),
        ("CG2860_3_A_total_score", "A_total can be computed", "BLOCKED", "Q_CAB/q_R_eff/sigma_R missing"),
        ("CG2860_4_Newton_PPN", "local Newton/PPN claim", "BLOCKED", "GM and full vector missing"),
        ("CG2860_5_Uamp_zero", "U_amp theorem-zero route can replace finite rows", "BLOCKED", "U_amp demoted to closure-only"),
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
        ("DEC2860_0_pack", "Finite-source acquisition pack written.", "The local branch now has a concrete row-by-row acquisition queue."),
        ("DEC2860_1_template", "Strict runner import template written as nonclaim.", "The schema is ready, but missing values correctly block scoring."),
        ("DEC2860_2_no_score", "No A_total/PPN/local-GR score attempted.", "Preflight refuses placeholders and U_amp theorem-zero remains demoted."),
        ("DEC2860_3_next", "Next target is first-row source extraction.", "Q_CAB/q_R_eff/sigma_R are the smallest set needed before any finite A_total attempt."),
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
                "next_id": "NEXT2860_0_2861",
                "status": "selected_primary",
                "target_doc": "2861-Y5-R2FR-QCAB-qReff-sigma-first-source-rows-or-retain-missing-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_QCAB_qReff_sigma_first_source_rows_or_retain_missing_under_AX1090_2861.py",
                "mission": "extract or reject the first finite-source rows Q_CAB, q_R_eff, and sigma_R from existing parent/source materials; if they remain unsourced, emit exact source requests and keep the 2853 runner blocked",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2860_0_acquisition", OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_copy"], "finite source acquisition pack nonclaim copy"),
        ("COPY2860_1_preflight", OUTPUTS["preflight"], BRANCH_OUTPUTS["preflight_copy"], "strict import preflight nonclaim copy"),
        ("COPY2860_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2861"),
        ("COPY2860_3_template", OUTPUTS["template"], BRANCH_OUTPUTS["template_copy"], "strict runner template nonclaim copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table", "target"}
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
        "accepted_source_present",
        "numeric_or_theorem_zero_present",
        "ready_for_strict_runner",
        "ready_for_runner",
        "runner_allowed",
        "gate_passed",
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
        ("VAL2860_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2860_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2860_2_acquisition_complete", len(rows_by_name["acquisition"]) >= 7, "acquisition pack covers Q_CAB/q_R_eff/sigma/b_R/tail/GM/full-vector"),
        ("VAL2860_3_template_written", len(rows_by_name["template"]) == 1, "strict runner import template written"),
        ("VAL2860_4_preflight_refuses", any(row["preflight_id"] == "PF2860_OVERALL" and row["passed"] is False for row in rows_by_name["preflight"]), "preflight refuses placeholder import"),
        ("VAL2860_5_no_ready_rows", not any(row["ready_for_strict_runner"] for row in rows_by_name["acquisition"]), "no acquisition row is marked runner-ready"),
        ("VAL2860_6_handoff_blocked", not any(row["runner_allowed"] for row in rows_by_name["handoff"]), "runner handoff remains blocked"),
        ("VAL2860_7_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2860_8_next_target_2861", any(row["next_id"] == "NEXT2860_0_2861" and row["selected"] for row in rows_by_name["next"]), "2861 first-row source extraction selected"),
        ("VAL2860_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2860_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2860_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2860_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2860_13_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2860_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2860_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2860_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2860_OVERALL",
            "passed": overall,
            "detail": "2860 builds the finite-source acquisition pack and strict nonclaim runner import template after U_amp demotion; placeholders are refused and first-row source extraction is selected for 2861.",
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
    content = f"""# 2860 - Y5 R2FR Finite Source Row Acquisition After Uamp Demotion Under AX1090

Status: `Y5_R2FR_2860_finite_source_pack_built_strict_import_template_refused_nonclaim`

## Private Verdict

After `U_amp` was demoted to closure-only for claim purposes, 2860 moves the local branch back onto the honest finite-source path.

This checkpoint does not score `A_total`, `gamma`, Newton, PPN, R10, or local GR. It builds the acquisition pack and runner import template that would make scoring possible later.

The strict template is intentionally invalid right now. It still contains `MISSING_Q_CAB`, `MISSING_q_R_eff`, `MISSING_sigma_R`, `MISSING_GM`, missing source paths, missing conventions, missing tail, and missing full-vector rows. The preflight correctly refuses it.

The next target is the smallest useful finite step: extract or reject the first three source rows, `Q_CAB`, `q_R_eff`, and `sigma_R`. Without those three, there is no honest finite `A_total` attempt.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Finite Source Acquisition Pack

{markdown_table(rows["acquisition"], ["acquisition_id", "quantity", "required_object", "current_blocker", "priority", "ready_for_strict_runner", "valid_for_claim"])}

## Strict Runner Import Template

{markdown_table(rows["template"], ["candidate_id", "branch_id", "Q_CAB_value", "q_R_eff_value", "sigma_R_value", "GM_value", "tail_status", "full_vector_status", "valid_for_claim"])}

## Strict Import Preflight

{markdown_table(rows["preflight"], ["preflight_id", "field", "requirement", "passed", "failure_reason", "valid_for_claim"])}

## Runner Handoff Ledger

{markdown_table(rows["handoff"], ["handoff_id", "object", "target", "instruction", "runner_allowed", "valid_for_claim"])}

## Blocker To Evidence Map

{markdown_table(rows["evidence"], ["evidence_id", "quantity", "current_blocker", "source_anchors", "accepted_source_present", "valid_for_claim"])}

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
    rows["acquisition"] = acquisition_rows()
    rows["template"] = template_rows()
    rows["preflight"] = preflight_rows(rows["template"])
    rows["handoff"] = handoff_rows()
    rows["evidence"] = evidence_rows(rows["acquisition"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "acquisition", "template", "preflight", "handoff", "evidence", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2860_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2860_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

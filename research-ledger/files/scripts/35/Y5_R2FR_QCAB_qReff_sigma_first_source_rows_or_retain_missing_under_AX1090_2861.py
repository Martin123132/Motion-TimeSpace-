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

DOC = ROOT / "2861-Y5-R2FR-QCAB-qReff-sigma-first-source-rows-or-retain-missing-under-AX1090.md"

SRC_2860_DOC = ROOT / "2860-Y5-R2FR-finite-source-row-acquisition-after-Uamp-demotion-under-AX1090.md"
SRC_2860_NEXT = RESIDUALS / "P8_Y5_R2FR_2860_NEXT_TARGET.csv"
SRC_2860_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2860_VALIDATION.csv"
SRC_2860_ACQ = RESIDUALS / "P8_Y5_R2FR_2860_FINITE_SOURCE_ACQUISITION_PACK.csv"
SRC_2860_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2860_STRICT_RUNNER_IMPORT_TEMPLATE_NONCLAIM.csv"
SRC_2860_PREFLIGHT = RESIDUALS / "P8_Y5_R2FR_2860_STRICT_IMPORT_PREFLIGHT.csv"
SRC_2853_RUNNER = RESIDUALS / "P8_Y5_R2FR_2853_STRICT_RUNNER_RESULTS.csv"
SRC_2855_EQUATIONS = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"
SRC_2855_STATUS = RESIDUALS / "P8_Y5_R2FR_2855_DERIVATION_STATUS_MATRIX.csv"
SRC_2839_DOC = ROOT / "2839-Y5-R2FR-finite-RAB-residual-green-kernel-normalization-or-first-source-backed-row-under-AX1090.md"
SRC_2840_DOC = ROOT / "2840-Y5-R2FR-first-finite-RAB-normalization-pack-or-parent-zero-certificate-under-AX1090.md"
SRC_2840_FILL = RESIDUALS / "P8_Y5_R2FR_2840_FIRST_PACK_FILL_ATTEMPT_NONCLAIM.csv"
SRC_2840_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_2844_DOC = ROOT / "2844-Y5-R2FR-CAB-one-over-r-amplitude-law-or-parent-cancellation-theorem-under-AX1090.md"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_CANCEL = RESIDUALS / "P8_Y5_R2FR_2844_CAB_CANCELLATION_THEOREM_ATTEMPT.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_1882_SIGMAR = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_SIGMAR_NO_CIRCULARITY_MAP.csv"
SRC_1882_DOC = ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2861_SOURCE_REGISTER.csv",
    "scan": RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_SOURCE_SCAN.csv",
    "collisions": RESIDUALS / "P8_Y5_R2FR_2861_SIGMA_SYMBOL_COLLISION_AUDIT.csv",
    "acceptance": RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_ACCEPTANCE_TEST.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2861_EXACT_SOURCE_REQUESTS.csv",
    "template": RESIDUALS / "P8_Y5_R2FR_2861_STRICT_TEMPLATE_UPDATE_NONCLAIM.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2861_RUNNER_STATUS_UPDATE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2861_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2861_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2861_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2861_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2861_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "scan_copy": LOCAL_BOUNDS / "RAB_FIRST_ROW_SOURCE_SCAN_2861_NONCLAIM.csv",
    "collision_copy": SOURCE_WEIGHT / "RAB_SIGMA_SYMBOL_COLLISION_2861_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2861_sigma_disambiguation_source_request_NEXT.csv",
    "request_copy": BETA_DOCS / "RAB_FIRST_ROW_EXACT_SOURCE_REQUESTS_2861_NONCLAIM.csv",
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
        ("SRC2861_0_2860_doc", SRC_2860_DOC, "NEXT2860_0_2861;VAL2860_OVERALL", "2860 handoff"),
        ("SRC2861_1_2860_next", SRC_2860_NEXT, "NEXT2860_0_2861", "2861 selected"),
        ("SRC2861_2_2860_validation", SRC_2860_VALIDATION, "VAL2860_OVERALL", "2860 validation"),
        ("SRC2861_3_2860_acquisition", SRC_2860_ACQ, "ACQ2860_0_Q_CAB;ACQ2860_2_sigma_R", "first-row acquisition pack"),
        ("SRC2861_4_2860_template", SRC_2860_TEMPLATE, "CAND2860_0_finite_source_import_template_nonclaim;MISSING_Q_CAB", "strict template"),
        ("SRC2861_5_2860_preflight", SRC_2860_PREFLIGHT, "PF2860_OVERALL;REFUSED_MISSING_PROVENANCE_OR_INPUTS", "preflight refusal"),
        ("SRC2861_6_2853_runner", SRC_2853_RUNNER, "REFUSED_MISSING_PROVENANCE_OR_INPUTS", "strict runner refusal"),
        ("SRC2861_7_2855_equations", SRC_2855_EQUATIONS, "PEQ2855_0_CAB_source;PEQ2855_2_sigma_sign", "draft source equations"),
        ("SRC2861_8_2855_status", SRC_2855_STATUS, "STAT2855_0_CAB_source;STAT2855_2_sigma_sign", "draft source status"),
        ("SRC2861_9_2839_doc", SRC_2839_DOC, "KER2839_4_compact_body;ZOS2839_4_first_source_row", "Green-kernel q_R_eff grammar"),
        ("SRC2861_10_2840_doc", SRC_2840_DOC, "FILL2840_0_first_RAB_finite_pack;PACK2840_1_amplitude", "normalization pack checkpoint"),
        ("SRC2861_11_2840_fill", SRC_2840_FILL, "FILL2840_0_first_RAB_finite_pack;MISSING_Q_R_EFF", "first pack fill failure"),
        ("SRC2861_12_2840_contract", SRC_2840_CONTRACT, "PACK2840_1_amplitude;PACK2840_2_sign", "normalization contract"),
        ("SRC2861_13_2844_doc", SRC_2844_DOC, "FLUX2844_4_local_ppn_amplitude;CANCEL2844_5_verdict", "CAB amplitude checkpoint"),
        ("SRC2861_14_2844_flux", SRC_2844_FLUX, "FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "A_total flux law"),
        ("SRC2861_15_2844_cancel", SRC_2844_CANCEL, "CANCEL2844_1_parent_source_identity;CANCEL2844_5_verdict", "cancellation theorem attempt"),
        ("SRC2861_16_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff", "amplitude source pack"),
        ("SRC2861_17_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign", "parent amplitude contract"),
        ("SRC2861_18_1882_sigmar", SRC_1882_SIGMAR, "SNCM1882_0_sigma_from_CR;SNCM1882_1_generalized_gamma", "sigma_R profile collision evidence"),
        ("SRC2861_19_1882_doc", SRC_1882_DOC, "sigma_R=b_R C_R;SNCM1882_1_generalized_gamma", "sigma_R profile doc"),
    ]
    return [source_row(*spec) for spec in specs]


def scan_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SCAN2861_0_Q_CAB",
            "Q_CAB",
            "FLUX2844_2_source_charge;FLUX2844_4_local_ppn_amplitude;PACK2844_0_Q_CAB",
            "symbolic charge law exists: Q_CAB=4*pi*A_CAB, with A_CAB from a surface/source integral",
            "MISSING_FINITE_NUMERIC_OR_PARENT_ZERO_ROW",
            "requires finite Q_CAB value or parent-zero owner plus source path/anchor/units/boundary/sign convention",
        ),
        (
            "SCAN2861_1_q_R_eff",
            "q_R_eff",
            "KER2839_4_compact_body;PACK2840_1_amplitude;PACK2844_4_q_R_eff",
            "symbolic Green charge exists: q_R_eff=-integral_body S_R/Z_R d^3x with length units",
            "MISSING_Q_R_EFF_VALUE_AND_NORMALIZATION",
            "requires ell_R/q_R_eff/source sign/Green normalization/source path/arena projection",
        ),
        (
            "SCAN2861_2_sigma_R_source_sign",
            "sigma_R_source_sign",
            "PACK2840_2_sign;PEQ2855_2_sigma_sign;CONTRACT2844_5_sign",
            "a source-sign/Green-convention slot exists",
            "MISSING_OPERATOR_GREEN_SIGN_OWNER",
            "requires metric signature, Green orientation, operator sign and exact parent source anchor",
        ),
        (
            "SCAN2861_3_sigma_R_profile_collision",
            "sigma_R_profile",
            "SNCM1882_0_sigma_from_CR;SNCM1882_1_generalized_gamma",
            "sigma_R is also used for a PPN conformal/log-coframe profile sigma_R=b_R*C_R or s_R*U/c^2",
            "SYMBOL_COLLISION_NOT_ACCEPTED_AS_SOURCE_SIGN",
            "must be renamed/canonicalized before strict runner import",
        ),
    ]
    return [
        nonclaim(
            {
                "scan_id": scan_id,
                "quantity": quantity,
                "best_source_anchors": anchors,
                "best_evidence": evidence,
                "current_status": status,
                "required_resolution": resolution,
                "accepted_source_row": False,
                "finite_numeric_value": False,
                "parent_zero_owner": False,
                "control_only": True,
            }
        )
        for scan_id, quantity, anchors, evidence, status, resolution in specs
    ]


def collision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "COL2861_0_runner_sigma",
            "sigma_R_source_sign",
            "sign/Green convention multiplying q_R_eff in A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)",
            "needed by 2853/2860 strict runner",
            "MISSING_SIGN_CONVENTION",
        ),
        (
            "COL2861_1_profile_sigma",
            "sigma_R_profile",
            "weak-field conformal/log-coframe profile sigma_R=b_R*C_R or s_R*U/c^2",
            "appears in 1882 PPN gamma map",
            "DERIVED_SYMBOLIC_PROFILE_NONCLAIM",
        ),
        (
            "COL2861_2_decision",
            "sigma_R canonicalization",
            "these cannot be treated as the same source row without an explicit bridge",
            "rename or split in future import template",
            "DISAMBIGUATION_REQUIRED_BEFORE_SCORING",
        ),
    ]
    return [
        nonclaim(
            {
                "collision_id": collision_id,
                "canonical_symbol": symbol,
                "meaning": meaning,
                "source_context": context,
                "status": status,
                "resolved": False,
                "control_only": True,
            }
        )
        for collision_id, symbol, meaning, context, status in specs
    ]


def acceptance_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACC2861_0_Q_CAB_numeric", "Q_CAB has finite numeric or theorem-zero owner", False, "only symbolic identities and missing source pack rows found"),
        ("ACC2861_1_q_R_eff_numeric", "q_R_eff has finite numeric plus normalization pack", False, "2839/2840 define required pack but value remains MISSING_Q_R_EFF"),
        ("ACC2861_2_sigma_sign", "sigma_R_source_sign has parent operator/Green sign owner", False, "CONTRACT2844_5_sign remains MISSING_SIGN_CONVENTION"),
        ("ACC2861_3_sigma_disambiguated", "sigma_R source sign is disambiguated from sigma_R profile", False, "1882 uses sigma_R for profile/coframe response"),
        ("ACC2861_4_source_paths", "all first rows have source paths and anchors", False, "template/source rows still missing source paths"),
        ("ACC2861_5_runner_ready", "first three rows can feed 2853/2860 strict runner", False, "first row set remains blocked"),
    ]
    return [
        nonclaim(
            {
                "acceptance_id": acceptance_id,
                "test": test,
                "passed": passed,
                "reason": reason,
                "control_only": True,
            }
        )
        for acceptance_id, test, passed, reason in specs
    ]


def request_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "REQ2861_0_Q_CAB",
            "Q_CAB",
            "finite value or parent-zero theorem for Q_CAB=4*pi*A_CAB",
            "equation/table anchor for A_CAB or rho_CAB integral; units; sign; boundary/corner treatment; source path",
        ),
        (
            "REQ2861_1_q_R_eff",
            "q_R_eff",
            "finite compact-source Green charge in same convention as Q_CAB",
            "ell_R or long-range limit; q_R_eff value; source density normalization S_R/Z_R; units; source path; arena projection",
        ),
        (
            "REQ2861_2_sigma_source_sign",
            "sigma_R_source_sign",
            "operator/Green sign convention for A_total source term",
            "metric signature; operator sign; Green orientation; exact parent action/source equation anchor",
        ),
        (
            "REQ2861_3_sigma_bridge_or_rename",
            "sigma_R canonical split",
            "explicit bridge or rename between sigma_R_source_sign and sigma_R_profile",
            "if no bridge exists, runner template must use separate fields and reject profile rows as sign rows",
        ),
    ]
    return [
        nonclaim(
            {
                "request_id": request_id,
                "quantity": quantity,
                "needed_source": needed,
                "minimum_content": content,
                "status": "OPEN_EXACT_SOURCE_REQUEST",
                "accepted_only_if": "source_path exists; equation_anchor exists; no MISSING markers; semantics match runner field",
                "control_only": True,
            }
        )
        for request_id, quantity, needed, content in specs
    ]


def template_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "candidate_id": "CAND2861_0_first_rows_retained_missing_nonclaim",
                "branch_id": "R2FR_local_PPN_constant_limit_after_Uamp_demotion",
                "Q_CAB_value": "MISSING_Q_CAB",
                "q_R_eff_value": "MISSING_q_R_eff",
                "sigma_R_source_sign": "MISSING_sigma_R_source_sign",
                "sigma_R_profile_status": "SYMBOL_COLLISION_NOT_ACCEPTED_AS_SOURCE_SIGN",
                "Q_CAB_source_path": "",
                "q_R_eff_source_path": "",
                "sigma_R_source_sign_path": "",
                "green_convention": "MISSING_GREEN_CONVENTION",
                "sign_convention": "MISSING_SIGN_CONVENTION",
                "first_rows_ready": False,
                "control_only": True,
            }
        )
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "runner_update_id": "RUNSTAT2861_0_first_rows_blocked",
                "runner": str(SRC_2853_RUNNER),
                "status": "BLOCKED",
                "reason": "Q_CAB/q_R_eff/sigma_R_source_sign remain unsourced and sigma_R profile collision is unresolved",
                "rerun_allowed": False,
                "control_only": True,
            }
        )
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2861_0_scan_done", "first-row source scan completed", "PASS_CONTROL_ONLY", "symbolic sources reviewed"),
        ("CG2861_1_Q_CAB", "Q_CAB accepted", "BLOCKED", "no finite numeric or parent-zero source row"),
        ("CG2861_2_q_R_eff", "q_R_eff accepted", "BLOCKED", "normalization pack missing q_R_eff/ell/source sign"),
        ("CG2861_3_sigma", "sigma_R source sign accepted", "BLOCKED", "operator/Green sign missing and profile collision unresolved"),
        ("CG2861_4_runner", "strict runner can run", "BLOCKED", "first rows not ready"),
        ("CG2861_5_local_GR", "local Newton/GR claim", "BLOCKED", "no A_total, GM, tail, or full-vector closure"),
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
        ("DEC2861_0_no_first_rows", "No accepted first finite-source rows were found.", "Q_CAB/q_R_eff/sigma_R remain symbolic or missing."),
        ("DEC2861_1_sigma_collision", "Split sigma_R semantics before scoring.", "sigma_R_source_sign and sigma_R_profile are not interchangeable."),
        ("DEC2861_2_runner", "Keep 2853/2860 strict runner blocked.", "template remains missing first rows and source paths."),
        ("DEC2861_3_next", "Next target is exact source-request pack plus sigma canonicalization.", "without semantic split and source rows, the finite route cannot become testable."),
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
                "next_id": "NEXT2861_0_2862",
                "status": "selected_primary",
                "target_doc": "2862-Y5-R2FR-first-row-source-request-pack-and-sigmaR-disambiguation-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_row_source_request_pack_and_sigmaR_disambiguation_under_AX1090_2862.py",
                "mission": "split sigma_R_source_sign from sigma_R_profile in the strict runner contract, write exact source-request rows for Q_CAB/q_R_eff/sigma_R_source_sign, and keep the runner blocked until real sources are supplied",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2861_0_scan", OUTPUTS["scan"], BRANCH_OUTPUTS["scan_copy"], "first-row source scan nonclaim copy"),
        ("COPY2861_1_collision", OUTPUTS["collisions"], BRANCH_OUTPUTS["collision_copy"], "sigma symbol collision nonclaim copy"),
        ("COPY2861_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2862"),
        ("COPY2861_3_requests", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "exact source requests copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table", "runner"}
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
        "accepted_source_row",
        "finite_numeric_value",
        "parent_zero_owner",
        "resolved",
        "first_rows_ready",
        "rerun_allowed",
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
        ("VAL2861_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2861_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2861_2_scan_complete", len(rows_by_name["scan"]) >= 4, "scan covers Q_CAB/q_R_eff/sigma source sign/sigma profile collision"),
        ("VAL2861_3_no_accepted_rows", not any(row["accepted_source_row"] for row in rows_by_name["scan"]), "no first finite-source row accepted"),
        ("VAL2861_4_sigma_collision_recorded", any(row["canonical_symbol"] == "sigma_R_profile" for row in rows_by_name["collisions"]), "sigma_R profile collision recorded"),
        ("VAL2861_5_acceptance_failed", not any(row["passed"] for row in rows_by_name["acceptance"]), "all first-row acceptance tests fail as expected"),
        ("VAL2861_6_requests_complete", len(rows_by_name["requests"]) >= 4, "exact source requests emitted"),
        ("VAL2861_7_runner_blocked", not any(row["rerun_allowed"] for row in rows_by_name["runner"]), "strict runner remains blocked"),
        ("VAL2861_8_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2861_9_next_target_2862", any(row["next_id"] == "NEXT2861_0_2862" and row["selected"] for row in rows_by_name["next"]), "2862 sigma/source-request target selected"),
        ("VAL2861_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2861_11_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2861_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2861_13_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2861_14_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2861_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2861_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2861_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2861_OVERALL",
            "passed": overall,
            "detail": "2861 reviews the first finite rows Q_CAB/q_R_eff/sigma_R, finds no accepted source rows, records sigma_R symbol collision, keeps the runner blocked, and selects source requests plus sigma disambiguation for 2862.",
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
    content = f"""# 2861 - Y5 R2FR Q_CAB/q_R_eff/sigma First Source Rows Or Retain Missing Under AX1090

Status: `Y5_R2FR_2861_first_rows_not_found_sigmaR_collision_runner_blocked`

## Private Verdict

2861 tried to extract the first finite-source rows: `Q_CAB`, `q_R_eff`, and `sigma_R`.

The result is disciplined but not glamorous:

- `Q_CAB` has a symbolic Gauss/source identity, but no finite numeric/source-backed row.
- `q_R_eff` has a Green-kernel normalization grammar, but no sourced `q_R_eff`, `ell_R`, source sign, or arena projection.
- `sigma_R` is worse than merely missing: the symbol is overloaded. The runner needs a source-sign/Green-convention `sigma_R_source_sign`, while 1882 uses `sigma_R` for a conformal/log-coframe PPN profile.

So the strict runner stays blocked. The next step must split the sigma semantics and write exact source-request rows. Otherwise we risk feeding the runner a profile coefficient where it expects a Green-kernel sign.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## First Row Source Scan

{markdown_table(rows["scan"], ["scan_id", "quantity", "best_evidence", "current_status", "required_resolution", "accepted_source_row", "valid_for_claim"])}

## Sigma Symbol Collision Audit

{markdown_table(rows["collisions"], ["collision_id", "canonical_symbol", "meaning", "source_context", "status", "resolved", "valid_for_claim"])}

## First Row Acceptance Test

{markdown_table(rows["acceptance"], ["acceptance_id", "test", "passed", "reason", "valid_for_claim"])}

## Exact Source Requests

{markdown_table(rows["requests"], ["request_id", "quantity", "needed_source", "minimum_content", "status", "valid_for_claim"])}

## Strict Template Update

{markdown_table(rows["template"], ["candidate_id", "Q_CAB_value", "q_R_eff_value", "sigma_R_source_sign", "sigma_R_profile_status", "first_rows_ready", "valid_for_claim"])}

## Runner Status Update

{markdown_table(rows["runner"], ["runner_update_id", "status", "reason", "rerun_allowed", "valid_for_claim"])}

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
    rows["scan"] = scan_rows()
    rows["collisions"] = collision_rows()
    rows["acceptance"] = acceptance_rows()
    rows["requests"] = request_rows()
    rows["template"] = template_rows()
    rows["runner"] = runner_rows()
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "scan", "collisions", "acceptance", "requests", "template", "runner", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2861_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2861_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

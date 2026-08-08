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

DOC = ROOT / "2862-Y5-R2FR-first-row-source-request-pack-and-sigmaR-disambiguation-under-AX1090.md"

SRC_2861_DOC = ROOT / "2861-Y5-R2FR-QCAB-qReff-sigma-first-source-rows-or-retain-missing-under-AX1090.md"
SRC_2861_NEXT = RESIDUALS / "P8_Y5_R2FR_2861_NEXT_TARGET.csv"
SRC_2861_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2861_VALIDATION.csv"
SRC_2861_SCAN = RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_SOURCE_SCAN.csv"
SRC_2861_COLLISIONS = RESIDUALS / "P8_Y5_R2FR_2861_SIGMA_SYMBOL_COLLISION_AUDIT.csv"
SRC_2861_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2861_EXACT_SOURCE_REQUESTS.csv"
SRC_2861_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2861_STRICT_TEMPLATE_UPDATE_NONCLAIM.csv"
SRC_2861_RUNNER = RESIDUALS / "P8_Y5_R2FR_2861_RUNNER_STATUS_UPDATE.csv"
SRC_2860_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2860_STRICT_RUNNER_IMPORT_TEMPLATE_NONCLAIM.csv"
SRC_2853_RUNNER = RESIDUALS / "P8_Y5_R2FR_2853_STRICT_RUNNER_RESULTS.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2840_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_1882_SIGMAR = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_SIGMAR_NO_CIRCULARITY_MAP.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2862_SOURCE_REGISTER.csv",
    "canonical": RESIDUALS / "P8_Y5_R2FR_2862_SIGMA_CANONICAL_DICTIONARY.csv",
    "schema": RESIDUALS / "P8_Y5_R2FR_2862_STRICT_RUNNER_SCHEMA_SPLIT.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2862_FIRST_ROW_SOURCE_REQUEST_PACK.csv",
    "rejections": RESIDUALS / "P8_Y5_R2FR_2862_SEMANTIC_REJECTION_RULES.csv",
    "preflight": RESIDUALS / "P8_Y5_R2FR_2862_SPLIT_PREFLIGHT.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2862_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2862_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2862_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2862_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2862_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "canonical_copy": LOCAL_BOUNDS / "RAB_SIGMA_CANONICAL_DICTIONARY_2862_NONCLAIM.csv",
    "schema_copy": SOURCE_WEIGHT / "RAB_STRICT_RUNNER_SCHEMA_SPLIT_2862_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2862_QCAB_first_source_or_parent_zero_NEXT.csv",
    "request_copy": BETA_DOCS / "RAB_FIRST_ROW_SOURCE_REQUEST_PACK_2862_NONCLAIM.csv",
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
        ("SRC2862_0_2861_doc", SRC_2861_DOC, "NEXT2861_0_2862;VAL2861_OVERALL", "2861 handoff"),
        ("SRC2862_1_2861_next", SRC_2861_NEXT, "NEXT2861_0_2862", "2862 selected"),
        ("SRC2862_2_2861_validation", SRC_2861_VALIDATION, "VAL2861_OVERALL", "2861 validation"),
        ("SRC2862_3_2861_scan", SRC_2861_SCAN, "SCAN2861_0_Q_CAB;SCAN2861_3_sigma_R_profile_collision", "first-row scan"),
        ("SRC2862_4_2861_collisions", SRC_2861_COLLISIONS, "COL2861_0_runner_sigma;COL2861_2_decision", "sigma collision audit"),
        ("SRC2862_5_2861_requests", SRC_2861_REQUESTS, "REQ2861_0_Q_CAB;REQ2861_3_sigma_bridge_or_rename", "exact source requests"),
        ("SRC2862_6_2861_template", SRC_2861_TEMPLATE, "CAND2861_0_first_rows_retained_missing_nonclaim;SYMBOL_COLLISION_NOT_ACCEPTED_AS_SOURCE_SIGN", "strict template split draft"),
        ("SRC2862_7_2861_runner", SRC_2861_RUNNER, "RUNSTAT2861_0_first_rows_blocked;BLOCKED", "runner blocked status"),
        ("SRC2862_8_2860_template", SRC_2860_TEMPLATE, "CAND2860_0_finite_source_import_template_nonclaim;MISSING_sigma_R", "pre-split template"),
        ("SRC2862_9_2853_runner", SRC_2853_RUNNER, "REFUSED_MISSING_PROVENANCE_OR_INPUTS", "strict runner refusal"),
        ("SRC2862_10_2844_flux", SRC_2844_FLUX, "FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "A_total formula"),
        ("SRC2862_11_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff", "amplitude source pack"),
        ("SRC2862_12_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign", "parent amplitude contract"),
        ("SRC2862_13_2840_contract", SRC_2840_CONTRACT, "PACK2840_1_amplitude;PACK2840_2_sign", "normalization pack contract"),
        ("SRC2862_14_1882_sigma", SRC_1882_SIGMAR, "SNCM1882_0_sigma_from_CR;SNCM1882_1_generalized_gamma", "profile sigma evidence"),
    ]
    return [source_row(*spec) for spec in specs]


def canonical_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SIG2862_0_source_sign",
            "sigma_R_source_sign",
            "runner_sign",
            "dimensionless sign/convention multiplying q_R_eff in A_total=(sigma_R_source_sign*q_R_eff+Q_CAB)/(4*pi)",
            "PACK2840_2_sign;CONTRACT2844_5_sign;SCAN2861_2_sigma_R_source_sign",
            "MISSING_OPERATOR_GREEN_SIGN_OWNER",
            "accepted only from parent operator/Green/source convention",
        ),
        (
            "SIG2862_1_profile",
            "sigma_R_profile",
            "weak_field_profile",
            "dimensionless weak-field conformal/log-coframe profile, e.g. sigma_R_profile=b_R*C_R=s_R*U/c^2",
            "SNCM1882_0_sigma_from_CR;SNCM1882_1_generalized_gamma",
            "DERIVED_SYMBOLIC_PROFILE_NONCLAIM",
            "not accepted as runner source sign unless an explicit bridge is sourced",
        ),
        (
            "SIG2862_2_bridge",
            "sigma_R_bridge",
            "semantic_bridge",
            "optional equation proving a source-sign convention maps into the weak-field profile convention without circularity",
            "REQ2861_3_sigma_bridge_or_rename",
            "MISSING_BRIDGE",
            "if absent, profile rows are rejected from first-row runner import",
        ),
    ]
    return [
        nonclaim(
            {
                "canonical_id": canonical_id,
                "canonical_symbol": symbol,
                "semantic_role": role,
                "definition": definition,
                "source_anchors": anchors,
                "current_status": status,
                "acceptance_rule": rule,
                "accepted_for_runner": False,
                "control_only": True,
            }
        )
        for canonical_id, symbol, role, definition, anchors, status, rule in specs
    ]


def schema_rows() -> list[dict[str, Any]]:
    specs = [
        ("SCHEMA2862_0_Q_CAB_value", "Q_CAB_value", "finite numeric or theorem-zero token", "MISSING_Q_CAB", "required before A_total"),
        ("SCHEMA2862_1_q_R_eff_value", "q_R_eff_value", "finite numeric Green charge", "MISSING_q_R_eff", "required before A_total"),
        ("SCHEMA2862_2_sigma_source_sign", "sigma_R_source_sign", "operator/Green/source sign convention", "MISSING_sigma_R_source_sign", "replaces ambiguous sigma_R_value"),
        ("SCHEMA2862_3_sigma_profile", "sigma_R_profile", "weak-field profile row from PPN/coframe sector", "REJECT_FOR_RUNNER_IMPORT_UNLESS_BRIDGED", "kept separate from sign"),
        ("SCHEMA2862_4_sigma_bridge", "sigma_R_bridge_source_path", "optional bridge source path", "", "required only if profile is used to infer source sign"),
        ("SCHEMA2862_5_rejection_flag", "profile_as_sign_rejected", "boolean guard", True, "blocks profile coefficient from sign slot"),
    ]
    return [
        nonclaim(
            {
                "schema_id": schema_id,
                "field": field,
                "meaning": meaning,
                "current_value_or_marker": value,
                "runner_rule": rule,
                "field_ready": False if "MISSING" in str(value) or value == "" or value is True else False,
                "control_only": True,
            }
        )
        for schema_id, field, meaning, value, rule in specs
    ]


def request_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "REQ2862_0_Q_CAB",
            "Q_CAB",
            "finite value or parent-zero theorem for Q_CAB=4*pi*A_CAB",
            "source_path; equation_anchor for surface flux or rho_CAB integral; units; boundary/corner convention; sign convention; branch id",
            "ACCEPT_FINITE_OR_THEOREM_ZERO_ONLY",
        ),
        (
            "REQ2862_1_q_R_eff",
            "q_R_eff",
            "finite compact-source Green charge in same convention as Q_CAB",
            "source_path; equation_anchor for q_R_eff=-integral S_R/Z_R d^3x; ell_R or long-range limit; units; source sign; arena projection",
            "ACCEPT_FINITE_NORMALIZATION_PACK_ONLY",
        ),
        (
            "REQ2862_2_sigma_R_source_sign",
            "sigma_R_source_sign",
            "operator/Green sign multiplying q_R_eff in A_total",
            "source_path; equation_anchor; parent operator sign; metric signature; Green orientation; source equation convention",
            "ACCEPT_SIGN_CONVENTION_ONLY",
        ),
        (
            "REQ2862_3_sigma_R_profile",
            "sigma_R_profile",
            "weak-field profile retained only as profile evidence",
            "source_path; equation_anchor; profile formula; b_R/delta_p definitions; explicit non-use as source sign",
            "REJECT_FOR_RUNNER_SIGN_SLOT",
        ),
        (
            "REQ2862_4_sigma_bridge",
            "sigma_R_bridge",
            "optional bridge from source sign to profile convention",
            "source_path; equation_anchor; derivation showing no circular use of gamma/PPN bound; units and orientation",
            "ACCEPT_ONLY_IF_PARENT_DERIVED",
        ),
    ]
    return [
        nonclaim(
            {
                "request_id": request_id,
                "quantity": quantity,
                "needed_source": needed,
                "minimum_content": minimum,
                "acceptance_mode": mode,
                "status": "OPEN_SOURCE_REQUEST",
                "control_only": True,
            }
        )
        for request_id, quantity, needed, minimum, mode in specs
    ]


def rejection_rows() -> list[dict[str, Any]]:
    specs = [
        ("REJ2862_0_profile_as_sign", "sigma_R_profile supplied where sigma_R_source_sign is required", "REJECT", "profile is a weak-field response, not a Green-kernel sign convention"),
        ("REJ2862_1_symbol_only", "symbol name sigma_R matches but semantic_role differs", "REJECT", "same glyph is insufficient evidence"),
        ("REJ2862_2_gamma_bound_backsolve", "infer sigma_R_source_sign from Cassini/gamma bound", "REJECT", "would import an empirical bound as a parent convention"),
        ("REJ2862_3_Uamp_zero", "use U_amp closure to skip first rows", "REJECT", "U_amp is demoted to closure-only"),
        ("REJ2862_4_placeholder", "MISSING_* marker in any first-row field", "REJECT", "strict runner remains blocked"),
    ]
    return [
        nonclaim(
            {
                "rejection_id": rejection_id,
                "attempt": attempt,
                "status": status,
                "reason": reason,
                "control_only": True,
            }
        )
        for rejection_id, attempt, status, reason in specs
    ]


def preflight_rows() -> list[dict[str, Any]]:
    checks = [
        ("SPLIT2862_0_dictionary", "canonical dictionary defines source_sign/profile/bridge", True, ""),
        ("SPLIT2862_1_schema", "strict schema no longer has ambiguous sigma_R_value as accepted field", True, ""),
        ("SPLIT2862_2_profile_rejected", "sigma_R_profile rejected for runner sign slot", True, ""),
        ("SPLIT2862_3_Q_CAB_missing", "Q_CAB real source row present", False, "MISSING_Q_CAB"),
        ("SPLIT2862_4_q_R_eff_missing", "q_R_eff real source row present", False, "MISSING_q_R_eff"),
        ("SPLIT2862_5_sigma_sign_missing", "sigma_R_source_sign real source row present", False, "MISSING_sigma_R_source_sign"),
        ("SPLIT2862_6_runner", "strict runner may run", False, "FIRST_ROWS_STILL_MISSING"),
    ]
    return [
        nonclaim(
            {
                "preflight_id": check_id,
                "check": check,
                "passed": passed,
                "failure_reason": reason,
                "control_only": True,
            }
        )
        for check_id, check, passed, reason in checks
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2862_0_sigma_split", "sigma semantics split", "PASS_CONTROL_ONLY", "dictionary and schema split are written"),
        ("CG2862_1_source_requests", "first-row source requests written", "PASS_CONTROL_ONLY", "requests are exact but unsatisfied"),
        ("CG2862_2_first_rows", "first rows accepted", "BLOCKED", "Q_CAB/q_R_eff/sigma_R_source_sign still missing"),
        ("CG2862_3_runner", "strict runner can run", "BLOCKED", "first rows missing and profile-as-sign rejected"),
        ("CG2862_4_A_total", "A_total can be scored", "BLOCKED", "no finite first rows"),
        ("CG2862_5_local_GR", "local GR/Newton claim", "BLOCKED", "no A_total, GM, tail, or full-vector closure"),
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
        ("DEC2862_0_split", "Split sigma_R into sigma_R_source_sign and sigma_R_profile.", "prevents profile coefficients from being fed into the Green-sign slot"),
        ("DEC2862_1_requests", "Exact first-row source requests written.", "future rows now have a clear acceptance contract"),
        ("DEC2862_2_runner", "Keep runner blocked.", "source requests are not source rows"),
        ("DEC2862_3_next", "Attack Q_CAB first.", "it is the target-map charge side of A_total and can be tested for finite row or parent-zero owner independently"),
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
                "next_id": "NEXT2862_0_2863",
                "status": "selected_primary",
                "target_doc": "2863-Y5-R2FR-QCAB-first-source-row-or-parent-zero-owner-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_QCAB_first_source_row_or_parent_zero_owner_under_AX1090_2863.py",
                "mission": "try to extract a real Q_CAB finite source row or parent-zero owner from the target-map/source-current materials; if no source row exists, keep Q_CAB missing and move to q_R_eff with an explicit blocker",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2862_0_canonical", OUTPUTS["canonical"], BRANCH_OUTPUTS["canonical_copy"], "sigma canonical dictionary nonclaim copy"),
        ("COPY2862_1_schema", OUTPUTS["schema"], BRANCH_OUTPUTS["schema_copy"], "strict runner schema split nonclaim copy"),
        ("COPY2862_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2863"),
        ("COPY2862_3_requests", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "first-row source request pack copy"),
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
        "accepted_for_runner",
        "field_ready",
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
        ("VAL2862_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2862_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2862_2_canonical_split", len(rows_by_name["canonical"]) >= 3, "sigma source/profile/bridge canonical rows written"),
        ("VAL2862_3_profile_rejected", any(row["attempt"] == "sigma_R_profile supplied where sigma_R_source_sign is required" for row in rows_by_name["rejections"]), "profile-as-sign rejection is explicit"),
        ("VAL2862_4_requests_complete", len(rows_by_name["requests"]) >= 5, "first-row and sigma bridge requests complete"),
        ("VAL2862_5_preflight_blocks_runner", any(row["preflight_id"] == "SPLIT2862_6_runner" and row["passed"] is False for row in rows_by_name["preflight"]), "preflight keeps runner blocked"),
        ("VAL2862_6_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2862_7_next_target_2863", any(row["next_id"] == "NEXT2862_0_2863" and row["selected"] for row in rows_by_name["next"]), "2863 Q_CAB source/zero target selected"),
        ("VAL2862_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2862_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2862_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2862_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2862_12_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2862_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2862_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2862_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2862_OVERALL",
            "passed": overall,
            "detail": "2862 splits sigma_R_source_sign from sigma_R_profile, writes exact first-row source requests, rejects profile-as-sign import, keeps the runner blocked, and selects Q_CAB source/zero extraction for 2863.",
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
    content = f"""# 2862 - Y5 R2FR First Row Source Request Pack And sigma_R Disambiguation Under AX1090

Status: `Y5_R2FR_2862_sigma_split_source_requests_runner_blocked_QCAB_next`

## Private Verdict

2862 fixes the `sigma_R` symbol trap.

From now on the strict local runner must distinguish:

- `sigma_R_source_sign`: the operator/Green/source sign multiplying `q_R_eff` in `A_total=(sigma_R_source_sign*q_R_eff+Q_CAB)/(4*pi)`.
- `sigma_R_profile`: the weak-field conformal/log-coframe profile used in the 1882 PPN map, e.g. `sigma_R_profile=b_R*C_R=s_R*U/c^2`.

Those are not interchangeable. A profile row is explicitly rejected if someone tries to import it into the source-sign slot without a parent-derived bridge.

The source requests for `Q_CAB`, `q_R_eff`, and `sigma_R_source_sign` are now exact. The runner remains blocked because requests are not evidence rows.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Sigma Canonical Dictionary

{markdown_table(rows["canonical"], ["canonical_id", "canonical_symbol", "semantic_role", "definition", "current_status", "accepted_for_runner", "valid_for_claim"])}

## Strict Runner Schema Split

{markdown_table(rows["schema"], ["schema_id", "field", "meaning", "current_value_or_marker", "runner_rule", "field_ready", "valid_for_claim"])}

## First Row Source Request Pack

{markdown_table(rows["requests"], ["request_id", "quantity", "needed_source", "minimum_content", "acceptance_mode", "status", "valid_for_claim"])}

## Semantic Rejection Rules

{markdown_table(rows["rejections"], ["rejection_id", "attempt", "status", "reason", "valid_for_claim"])}

## Split Preflight

{markdown_table(rows["preflight"], ["preflight_id", "check", "passed", "failure_reason", "valid_for_claim"])}

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
    rows["canonical"] = canonical_rows()
    rows["schema"] = schema_rows()
    rows["requests"] = request_rows()
    rows["rejections"] = rejection_rows()
    rows["preflight"] = preflight_rows()
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "canonical", "schema", "requests", "rejections", "preflight", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2862_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2862_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

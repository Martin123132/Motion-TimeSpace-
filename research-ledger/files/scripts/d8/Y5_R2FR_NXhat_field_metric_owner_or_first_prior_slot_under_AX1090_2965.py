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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE_1848 = ROOT / "source-intake" / "microscope" / "quarantine" / "1848"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2965"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2965-Y5-R2FR-NXhat-field-metric-owner-or-first-prior-slot-under-AX1090.md"

SRC_2964_DOC = ROOT / "2964-Y5-R2FR-Xhat-ZX-MX2-lambda-or-source-current-first-value-under-AX1090.md"
SRC_2964_NEXT = RESIDUALS / "P8_Y5_R2FR_2964_NEXT_TARGET.csv"
SRC_2964_SLOTS = RESIDUALS / "P8_Y5_R2FR_2964_FIRST_VALUE_SLOTS_NONCLAIM.csv"
SRC_2964_XPAYLOAD = RESIDUALS / "P8_Y5_R2FR_2964_XHAT_ZX_MX2_LAMBDA_PAYLOAD_GATE.csv"
SRC_2963_PROMOTION = RESIDUALS / "P8_Y5_R2FR_2963_PROMOTION_RULES.csv"
SRC_2962_XHAT = PARENT_ACTION / "canonical_Xhat_source_current_gate_2962_NOT_DERIVED.csv"
SRC_2954_FIELD = PARENT_ACTION / "field_space_law_audit_2954_NONCLAIM.csv"
SRC_2953_BETA = PARENT_ACTION / "field_space_beta_blocker_2953_NONCLAIM.csv"
SRC_2951_COEFF = PARENT_ACTION / "ZX_MX2_source_row_attempt_2951_BLOCKED.csv"
SRC_2951_OWNER = PARENT_ACTION / "parent_X_owner_contract_2951_NONCLAIM.csv"
SRC_2197_ZX = BETA_SOURCE / "PARENT_QLOC_ZX_RESIDUE_OWNER_CONTRACT_2197_NONCLAIM.csv"
SRC_2663_KX = SOURCE_WEIGHT / "R10_SOURCE_TEST_CHARGE_NORMALIZATION_2663_NONCLAIM.csv"
SRC_2157_METRIC = SOURCE_WEIGHT / "AFRAME_PARENT_METRIC_TRACE_2157_NONCLAIM.csv"
SRC_1847_LOCKS = RESIDUALS / "P8_Y5_PARENT_QLOC_1847_FIELD_NORMALIZATION_LOCKS.csv"
SRC_1848_METRIC = QUARANTINE_1848 / "P8_Y5_PARENT_QLOC_1848_PARENT_METRIC_ATTEMPT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2965_SOURCE_REGISTER.csv",
    "owner_gate": RESIDUALS / "P8_Y5_R2FR_2965_NXHAT_FIELD_METRIC_OWNER_GATE.csv",
    "rescaling": RESIDUALS / "P8_Y5_R2FR_2965_RESCALING_GUARD_AUDIT.csv",
    "prior_slot": RESIDUALS / "P8_Y5_R2FR_2965_NXHAT_FIRST_PRIOR_SLOT_NONCLAIM.csv",
    "runner_patch": RESIDUALS / "P8_Y5_R2FR_2965_RUNNER_PATCH_ROWS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2965_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2965_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2965_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2965_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2965_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_gate_copy": PARENT_ACTION / "NXhat_field_metric_owner_gate_2965_NOT_DERIVED.csv",
    "prior_slot_copy": LOCAL_BOUNDS / "NXhat_first_prior_slot_2965_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2965_ZX_FX_FIELD_METRIC_OR_NXHAT_PRIOR_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def all_semicolon_paths_exist(paths: str) -> bool:
    return all(Path(path).exists() for path in paths.split(";") if path)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2965_00_2964_doc", SRC_2964_DOC, "NEXT2964_0_2965;SLOT2964_0_N_Xhat", "2964 handoff"),
        ("SRC2965_01_2964_next", SRC_2964_NEXT, "NEXT2964_0_2965", "machine-readable 2965 target"),
        ("SRC2965_02_2964_slots", SRC_2964_SLOTS, "SLOT2964_0_N_Xhat;SLOT2964_1_lambda_X", "first slot ordering"),
        ("SRC2965_03_2964_xpayload", SRC_2964_XPAYLOAD, "XPL2964_4_NXhat;XPL2964_5_verdict", "Xhat payload blocker"),
        ("SRC2965_04_2963_promotion", SRC_2963_PROMOTION, "PROM2963_1_Xhat;PROM2963_6_verdict", "runner promotion rule"),
        ("SRC2965_05_2962_xhat", SRC_2962_XHAT, "XHAT2962_1_field_metric;XHAT2962_3_rescaling_guard;XHAT2962_4_verdict", "canonical Xhat gate"),
        ("SRC2965_06_2954_field", SRC_2954_FIELD, "LAW2954_2_canonical_metric_contract;LAW2954_3_rescaling_guard;LAW2954_6_verdict", "field-space law"),
        ("SRC2965_07_2953_beta", SRC_2953_BETA, "BETA2953_1_field_metric;BETA2953_4_verdict", "field metric beta blocker"),
        ("SRC2965_08_2951_coeff", SRC_2951_COEFF, "COEFF2951_0_ZX_formula;COEFF2951_4_lambdaX", "Z_X/M_X/lambda formula-only state"),
        ("SRC2965_09_2951_owner", SRC_2951_OWNER, "OWN2951_3_field_normalization;OWN2951_4_ZX_owner;OWN2951_5_MX2_owner", "parent X owner contract"),
        ("SRC2965_10_2197_ZX", SRC_2197_ZX, "ZOC2197_3_metric_lock;ZOC2197_5_verdict", "Z_X residue owner contract"),
        ("SRC2965_11_2663_KX", SRC_2663_KX, "KX2663_4_rescaling;KX2663_5_verdict", "R10 charge normalization guard"),
        ("SRC2965_12_2157_metric", SRC_2157_METRIC, "PML2157_0_parent_metric_object;PML2157_5_verdict", "parent metric trace"),
        ("SRC2965_13_1847_locks", SRC_1847_LOCKS, "FNL1847_1_canonical_metric;FNL1847_4_CX_tie", "field normalization locks"),
        ("SRC2965_14_1848_metric", SRC_1848_METRIC, "PM1848_0_metric_target;PM1848_6_verdict", "parent metric attempt"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def owner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FM2965_0_conditional_canonical_map",
            "N_Xhat",
            "If the parent quadratic block supplies a positive field metric G_X or kinetic residue Z_X, the canonical local coordinate is Xhat=N_Xhat X with N_Xhat=sqrt(G_X) up to the declared field-unit convention.",
            "DERIVED_CONDITIONALLY",
            "standard second-variation normalization; usable only after parent owner signs G_X/Z_X and units",
            True,
            False,
            "does not itself identify the parent object",
        ),
        (
            "FM2965_1_parent_metric_object",
            "G_X=M_AB e_X^A e_X^B",
            "one parent field-space metric M_AB and normalized X direction e_X are selected before local readout",
            "TARGET_DEFINED_NOT_OWNED",
            "2157/1848 define the right invariant object but do not derive it from one parent action",
            True,
            False,
            "M_AB, e_X, f_X, units and stress variation missing",
        ),
        (
            "FM2965_2_ZX_fX_product",
            "Z_X f_X^2",
            "field metric/amplitude product is parent-owned; canonical vacuum lock candidate is Z_X f_X^2=rho_vac^(1/2)",
            "CLEAN_CONTRACT_NOT_SIGNED",
            "2954/2157/1847 agree on the clean contract, but no Ward/metric theorem signs it",
            True,
            False,
            "parent Ward/current norm or defect metric theorem missing",
        ),
        (
            "FM2965_3_same_branch_lambda",
            "lambda_X",
            "lambda_X=sqrt(Z_X/M_X^2) using Z_X and M_X^2 from the same field metric and Hessian branch",
            "BLOCKED_BY_ZX_MX2",
            "2951 keeps Z_X and M_X^2 formula-only and not parent-signed",
            True,
            False,
            "positive kinetic sign, mass gap and zero-mode policy missing",
        ),
        (
            "FM2965_4_source_charge_same_units",
            "beta_source/test in Xhat units",
            "source/test charges are derivatives with respect to the same canonical Xhat used by Z_X, lambda_X and K_X",
            "BLOCKED_BY_CURRENT_OWNER",
            "2964/2663 keep source charge normalization blocked until N_Xhat is owned",
            True,
            False,
            "source-current owner and source/test projections missing",
        ),
        (
            "FM2965_5_verdict",
            "N_Xhat field-metric owner",
            "FM2965_0 through FM2965_4 close from one parent branch",
            "NXHAT_OWNER_NOT_DERIVED",
            "the map is mathematically clear, but the corpus still lacks a parent-signed owner for the metric/amplitude product",
            True,
            False,
            "emit first nonclaim N_Xhat prior/source slot instead of claiming local-GR/R10 readiness",
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "owner_acquired": acquired,
                "missing_for_claim": missing,
            }
        )
        for gate_id, obj, statement, status, evidence, conditional, acquired, missing in rows
    ]


def rescaling_guard_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RG2965_0_coordinate_rescaling",
            "X -> aX",
            "Z_X, f_X, beta_source/test and b_conf must transform together so physical alpha/lambda statements are unchanged",
            "GUARDRAIL_PASS",
            "blocks choosing a normalization after seeing R10/PPN pressure",
            True,
        ),
        (
            "RG2965_1_product_invariant",
            "Z_X f_X^2",
            "the field-space metric/amplitude product, not raw Z_X alone, is the physical normalization target",
            "INVARIANT_IDENTIFIED",
            "matches 2954, 2157, 1847 and 1848 contracts",
            True,
        ),
        (
            "RG2965_2_runner_refusal",
            "N_Xhat prior rows",
            "any N_Xhat value without source path, units and rescaling policy is refused by the 2963 promotion logic",
            "REFUSAL_POLICY_ACTIVE",
            "keeps current rows private/nonclaim",
            True,
        ),
        (
            "RG2965_3_limit",
            "guard cannot pick a number",
            "the guard rejects fake wins but cannot derive G_X, Z_X f_X^2 or f_X by itself",
            "NO_NUMERIC_UNLOCK",
            "field-metric owner remains the next source/derivation target",
            False,
        ),
    ]
    return [
        add_common(
            {
                "guard_id": guard_id,
                "object": obj,
                "statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "guard_useful": useful,
                "accepted_for_scoring": False,
            }
        )
        for guard_id, obj, statement, status, evidence, useful in rows
    ]


def prior_slot_rows() -> list[dict[str, Any]]:
    source_paths = ";".join(
        str(path)
        for path in [
            SRC_2964_SLOTS,
            SRC_2963_PROMOTION,
            SRC_2962_XHAT,
            SRC_2954_FIELD,
            SRC_2197_ZX,
            SRC_2157_METRIC,
            SRC_1847_LOCKS,
            SRC_1848_METRIC,
        ]
    )
    rows = [
        (
            "NXHAT2965_0_N_Xhat_first_prior",
            "N_Xhat",
            "field_normalization",
            "MISSING_FIELD_METRIC_OWNER_OR_NUMERIC_PRIOR",
            "first finite-branch normalization slot; future accepted values must be parent-derived, externally sourced as an explicit prior, or fitted in a nonclaim smoke run with no claim promotion",
            "PROM2963_1_Xhat",
            False,
        ),
        (
            "NXHAT2965_1_ZX_fX_product",
            "Z_X f_X^2",
            "field_metric_times_amplitude_squared",
            "MISSING_PRODUCT_VALUE_OR_THEOREM",
            "same slot in invariant form; this is the lower-scrutiny route because it is coordinate-invariant",
            "LAW2954_2_canonical_metric_contract",
            False,
        ),
        (
            "NXHAT2965_2_rescaling_policy",
            "normalization policy",
            "policy",
            "GUARD_ONLY_NO_VALUE",
            "future row must state how X, Xhat, source derivatives, K_X and b_conf transform under field rescaling",
            "XHAT2962_3_rescaling_guard",
            False,
        ),
        (
            "NXHAT2965_3_acceptance_rule",
            "runner acceptance",
            "policy",
            "NONCLAIM_UNTIL_SOURCE_BACKED",
            "no MISSING markers, real source path, declared units, same branch as lambda_X and source/test charges, valid_for_claim true only after all gates close",
            "PROM2963_1_Xhat",
            False,
        ),
    ]
    return [
        add_common(
            {
                "slot_id": slot_id,
                "symbol": symbol,
                "units": units,
                "numeric_or_theorem_value": value,
                "role": role,
                "runner_hook": hook,
                "source_path": source_paths,
                "source_path_exists": all_semicolon_paths_exist(source_paths),
                "accepted_for_scoring": accepted,
                "no_cancellation_policy": True,
            }
        )
        for slot_id, symbol, units, value, role, hook, accepted in rows
    ]


def runner_patch_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN2965_0_PROM2963_1_status",
            "PROM2963_1_Xhat",
            "KEEP_NOT_SATISFIED",
            "2965 supplies schema and conditional law only; no source-backed N_Xhat value exists",
        ),
        (
            "RUN2965_1_first_prior_slot",
            "NXHAT2965_0_N_Xhat_first_prior",
            "SCHEMA_ACCEPTED_NONCLAIM",
            "this is the row a future smoke runner can update, but it is currently refused for scoring",
        ),
        (
            "RUN2965_2_rescaling",
            "RG2965_*",
            "REFUSAL_GUARD_ACTIVE",
            "rejects normalization laundering and keeps alpha/PPN products invariant",
        ),
        (
            "RUN2965_3_no_claim",
            "finite b_conf branch",
            "CLAIM_FALSE",
            "valid_mts_rows remains zero until N_Xhat or Z_X f_X^2 is source-backed",
        ),
    ]
    return [
        add_common(
            {
                "runner_patch_id": patch_id,
                "target": target,
                "status": status,
                "statement": statement,
            }
        )
        for patch_id, target, status, statement in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2965_0_NXhat_owner", "N_Xhat parent field-metric owner acquired", False, "NXHAT_OWNER_NOT_DERIVED"),
        ("CG2965_1_ZX_fX", "Z_X f_X^2 numeric/theorem value source-backed", False, "PRODUCT_VALUE_MISSING"),
        ("CG2965_2_lambda", "lambda_X same-branch source-backed", False, "BLOCKED_BY_ZX_MX2"),
        ("CG2965_3_runner", "2963 runner can accept a valid MTS row", False, "VALID_MTS_ROWS_ZERO"),
        ("CG2965_4_R10_PPN_clock", "R10/PPN/clock/orbital score allowed", False, "LOCAL_ARENA_CLAIMS_BLOCKED"),
        ("CG2965_5_local_GR", "local GR/Newton reduction claimed", False, "NO_LOCAL_GR_OR_NEWTON_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2965_0_derivation_result",
            "conditional N_Xhat map derived but not parent-owned",
            "N_Xhat=sqrt(G_X) is the right canonical rule once G_X/Z_X and units exist; present corpus does not own G_X",
            "do not promote N_Xhat",
        ),
        (
            "DEC2965_1_low_scrutiny_route",
            "prefer invariant Z_X f_X^2 over raw N_Xhat",
            "the product survives field-coordinate choices and is already the common contract in 2954/2157/1847/1848",
            "hunt the parent metric/source pack for Z_X f_X^2",
        ),
        (
            "DEC2965_2_prior_slot",
            "first prior/source slot emitted",
            "future testing can update one clean slot instead of scattering ad-hoc normalizations across R10/PPN files",
            "keep current slot valid_for_claim=false",
        ),
        (
            "DEC2965_3_next",
            "next target should source the Z_X f_X^2 pack",
            "without this pack, lambda_X, K_X, beta_source/test and b_conf are not invariantly comparable",
            "build 2966 source pack or prior-runner",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2965_0_2966",
                "priority": "selected_primary",
                "next_doc": "2966-Y5-R2FR-ZX-fX-field-metric-source-pack-or-NXhat-prior-runner-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_ZX_fX_field_metric_source_pack_or_NXhat_prior_runner_under_AX1090_2966.py",
                "objective": "Try to source or derive the invariant field-metric/amplitude pack Z_X f_X^2, with parent M_AB/e_X/f_X ownership, stress/Bianchi variation and Schur-complement guard. If it fails, add a nonclaim N_Xhat prior-runner intake row without promoting any local test.",
                "include": "Z_X f_X^2;G_X;M_AB;e_X;f_X;stress/Bianchi variation;Schur complement;N_Xhat prior;runner refusal;source paths;units",
                "exclude": "R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits;raw beta=3 mode-count claim;normalization chosen from local bounds",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("owner_gate_copy", OUTPUTS["owner_gate"], BRANCH_OUTPUTS["owner_gate_copy"]),
        ("prior_slot_copy", OUTPUTS["prior_slot"], BRANCH_OUTPUTS["prior_slot_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2965_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2965_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2965_2_owner_blocked", any(row["gate_id"] == "FM2965_5_verdict" and row["owner_acquired"] is False for row in all_rows["owner_gate"]), "N_Xhat owner verdict remains blocked", True),
        ("VAL2965_3_conditional_map_written", any(row["gate_id"] == "FM2965_0_conditional_canonical_map" and row["conditional_math_available"] is True for row in all_rows["owner_gate"]), "conditional canonical N_Xhat law is recorded", True),
        ("VAL2965_4_rescaling_guard_active", all(row["accepted_for_scoring"] is False for row in all_rows["rescaling"]), "rescaling rows are guardrails only", True),
        ("VAL2965_5_prior_slots_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["prior_slot"]), "N_Xhat prior slots remain nonclaim", True),
        ("VAL2965_6_prior_paths_exist", all(row["source_path_exists"] is True for row in all_rows["prior_slot"]), "N_Xhat prior rows cite existing paths", True),
        ("VAL2965_7_runner_claim_false", all(row["claim_allowed"] is False for row in all_rows["runner_patch"]), "runner patch does not promote claims", True),
        ("VAL2965_8_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2965_9_next_target_written", any(row["next_id"] == "NEXT2965_0_2966" for row in all_rows["next"]), "2966 next target selected", True),
        ("VAL2965_10_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2965_11_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2965_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2965_13_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2965 outputs were written to formalization-workbench", True),
        ("VAL2965_14_doc_written", DOC.exists(), "2965 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2965_OVERALL", "passed": overall, "check": "2965 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2965 - Y5 R2FR: N_Xhat field-metric owner or first prior slot under AX1090

Status: `Y5_R2FR_2965_conditional_NXhat_law_derived_but_field_metric_owner_not_acquired`

Claim ceiling: `no_NXhat_claim_no_ZX_fX_claim_no_lambda_claim_no_R10_PPN_clock_orbital_claim_no_local_GR_no_Newton_no_public_claim`

2965 attacks the first value slot from 2964: the canonical normalization `N_Xhat`.

- Conditional law: if a parent branch supplies a positive field-space metric/restricted kinetic residue, then the canonical coordinate can be written as `Xhat=N_Xhat X`, with `N_Xhat=sqrt(G_X)` up to the declared field-unit convention.
- The useful invariant is not raw `Z_X` or raw `N_Xhat`; it is the parent-owned metric/amplitude pack `Z_X f_X^2` or equivalent `G_X f_X^2`.
- The rescaling guard is active: field-coordinate choices cannot be used to tune R10/PPN/clock results after the fact.
- The owner is not acquired: `M_AB`, `e_X`, `f_X`, stress/Bianchi variation and the Schur-complement/cross-block proof remain unsigned.
- Therefore the first `N_Xhat` prior/source slot is emitted as schema-only and nonclaim.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## N_Xhat Field-Metric Owner Gate

{md_table(all_rows["owner_gate"], ["gate_id", "object", "current_status", "conditional_math_available", "owner_acquired", "missing_for_claim"])}

## Rescaling Guard Audit

{md_table(all_rows["rescaling"], ["guard_id", "object", "current_status", "guard_useful", "accepted_for_scoring", "evidence_summary"])}

## N_Xhat First Prior Slot

{md_table(all_rows["prior_slot"], ["slot_id", "symbol", "numeric_or_theorem_value", "units", "accepted_for_scoring", "role"])}

## Runner Patch Rows

{md_table(all_rows["runner_patch"], ["runner_patch_id", "target", "status", "statement"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "owner_gate": owner_gate_rows(),
        "rescaling": rescaling_guard_rows(),
        "prior_slot": prior_slot_rows(),
        "runner_patch": runner_patch_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2965 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

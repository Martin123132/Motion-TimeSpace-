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

DOC = ROOT / "2848-Y5-R2FR-first-finite-local-PPN-prediction-row-or-parent-theorem-zero-under-AX1090.md"

SRC_2847_DOC = ROOT / "2847-Y5-R2FR-finite-local-PPN-bound-map-dry-run-or-current-owner-retry-under-AX1090.md"
SRC_2847_GATES = RESIDUALS / "P8_Y5_R2FR_2847_PREDICTION_INPUT_GATES.csv"
SRC_2847_MAP = RESIDUALS / "P8_Y5_R2FR_2847_DRY_RUN_BOUND_MAP.csv"
SRC_2847_NEXT = RESIDUALS / "P8_Y5_R2FR_2847_NEXT_TARGET.csv"
SRC_2847_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2847_VALIDATION.csv"
SRC_2846_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2846_FINITE_LOCAL_PPN_INPUT_CONTRACT.csv"
SRC_2846_FORMULA = RESIDUALS / "P8_Y5_R2FR_2846_LOCAL_PPN_FORMULA_PACK_NONCLAIM.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_1883 = ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2848_SOURCE_REGISTER.csv",
    "availability": RESIDUALS / "P8_Y5_R2FR_2848_CORE_AMPLITUDE_INPUT_AVAILABILITY.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_2848_PARENT_THEOREM_ZERO_CERTIFICATE_ATTEMPT.csv",
    "candidate_row": RESIDUALS / "P8_Y5_R2FR_2848_FIRST_PPN_PREDICTION_CANDIDATE_ROW.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2848_PREDICTION_ROW_REFUSAL_LEDGER.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_2848_CORE_AMPLITUDE_ACQUISITION_CONTRACT.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2848_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2848_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2848_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2848_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2848_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "candidate_copy": LOCAL_BOUNDS / "RAB_CAB_first_local_PPN_prediction_candidate_2848_REJECTED_NONCLAIM.csv",
    "acquisition_copy": SOURCE_WEIGHT / "RAB_CAB_core_amplitude_acquisition_contract_2848_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2848_core_amplitude_source_acquisition_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_FIRST_LOCAL_PPN_ROW_2848_REJECTED_NONCLAIM.csv",
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
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2848_0_2847_doc", SRC_2847_DOC, "NEXT2847_0_2848;VAL2847_OVERALL", "2847 selected first prediction row/theorem-zero target"),
        ("SRC2848_1_2847_gates", SRC_2847_GATES, "GATEIN2847_1_A_total;MISSING_COMPUTABLE_INPUTS", "2847 input gates"),
        ("SRC2848_2_2847_map", SRC_2847_MAP, "BM2847_0_gamma;BM2847_9_total", "2847 dry-run bound map"),
        ("SRC2848_3_2847_next", SRC_2847_NEXT, "NEXT2847_0_2848", "2847 handoff"),
        ("SRC2848_4_2847_validation", SRC_2847_VALIDATION, "VAL2847_OVERALL", "2847 validation"),
        ("SRC2848_5_2846_contract", SRC_2846_CONTRACT, "PPN2846_1_Q_CAB;PPN2846_4_A_total;PPN2846_6_q_R_hat", "2846 finite local PPN contract"),
        ("SRC2848_6_2846_formula", SRC_2846_FORMULA, "FORM2846_0_A_total;FORM2846_3_theorem_zero", "2846 local PPN formulas"),
        ("SRC2848_7_2844_flux", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition;Q_CAB=-sigma_R*q_R_eff", "2844 charge-balance identity"),
        ("SRC2848_8_1883", SRC_1883, "DPB1883_0_CR_delta_p;DPB1883_1_QR_delta_p;DPB1883_2_gamma_combo", "1883 delta_p/q_R_hat bridge"),
        ("SRC2848_9_2631", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only;PBOUND2631_0_gamma", "2631 full-vector PPN guard"),
        ("SRC2848_10_local_bounds", SRC_LOCAL_BOUNDS, "Cassini_Shapiro_gamma_2003;Will_2014_PPN_beta_table;LLR_Biskupek_Muller_Torre_2021", "local comparator table"),
    ]
    return [source_row(*spec) for spec in specs]


def availability_rows() -> list[dict[str, Any]]:
    specs = [
        ("AV2848_0_Q_CAB", "Q_CAB", "target-map monopole charge", "MISSING_NUMERIC_OR_THEOREM", "needed for A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)"),
        ("AV2848_1_q_R_eff", "q_R_eff", "delta_R Green charge", "MISSING_NUMERIC_OR_THEOREM", "needed for A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)"),
        ("AV2848_2_sigma_R", "sigma_R", "Green sign convention", "MISSING_SIGN", "needed before q_R_eff can be combined with Q_CAB"),
        ("AV2848_3_GM", "M_source/GM convention", "measured-GM normalization", "MISSING_GM_CONVENTION", "needed for delta_p_const and q_R_hat_const"),
        ("AV2848_4_theorem_zero", "parent theorem-zero", "Q_CAB=-sigma_R*q_R_eff plus tail/full-vector closure", "MISSING_PARENT_THEOREM", "alternative to finite numeric amplitude inputs"),
        ("AV2848_5_b_R", "b_R", "common-frame/no-shadow Weyl response", "MISSING_B_R", "needed for gamma combo if not theorem-zero"),
        ("AV2848_6_tail", "C_AB_reg/H_R/range tails", "regular/range corrections", "MISSING_PROFILE_BOUNDS", "needed before constant-limit score"),
        ("AV2848_7_full_vector", "full PPN vector", "beta/preferred/source/endpoint/readout/q_loc", "MISSING_FULL_VECTOR", "needed to avoid gamma-only pass"),
    ]
    return [
        nonclaim(
            {
                "availability_id": row_id,
                "quantity": quantity,
                "role": role,
                "current_status": status,
                "why_required": why,
                "source_backed_value_present": False,
                "theorem_zero_present": False,
                "control_only": True,
            }
        )
        for row_id, quantity, role, status, why in specs
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    specs = [
        ("TZ2848_0_charge_balance", "Q_CAB=-sigma_R*q_R_eff", "MISSING_PARENT_OWNER", "2844/2846 derive it as condition, not parent theorem"),
        ("TZ2848_1_tail_zero", "C_AB_reg,H_R,finite-range corrections PPN-silent", "MISSING_PROFILE_THEOREM", "constant-limit score needs tail silence or finite terms"),
        ("TZ2848_2_full_vector_zero", "beta/preferred/source/endpoint/readout/q_loc channels zero or bounded", "MISSING_FULL_VECTOR_THEOREM", "local GR cannot be gamma-only"),
        ("TZ2848_3_no_rescaling", "no independent current/source normalization rescaling", "MISSING_CURRENT_OWNER", "otherwise charge-balance can be convention artifact"),
        ("TZ2848_4_verdict", "parent theorem-zero certificate for first local PPN row", "NOT_DERIVED", "no parent-signed source/action path closes all clauses"),
    ]
    return [
        nonclaim(
            {
                "theorem_id": theorem_id,
                "required_clause": clause,
                "status": status,
                "reason": reason,
                "parent_signed": False,
                "theorem_zero_accepted": False,
                "control_only": True,
            }
        )
        for theorem_id, clause, status, reason in specs
    ]


def candidate_row() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "candidate_id": "PRED2848_0_first_gamma_lane",
                "branch": "finite_or_theorem_zero",
                "observable": "gamma_minus_1",
                "comparator_bound": "2.3e-05",
                "comparator_source": "Cassini_Shapiro_gamma_2003",
                "A_total_formula": "A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)",
                "delta_p_formula": "delta_p_const=c^2*A_total/(2*G*M_source)",
                "q_R_hat_formula": "q_R_hat_const=-c^2*A_total/(G*M_source)",
                "gamma_formula": "gamma_obs_minus_1=(delta_p+4*b_R*delta_p)/(1-2*b_R*delta_p)+Delta_gamma_tail+q_loc_gamma",
                "required_inputs": "Q_CAB;q_R_eff;sigma_R;M_source_or_GM;b_R;tail;q_loc_gamma;source_paths;full_vector_closure",
                "row_status": "REJECTED_MISSING_CORE_INPUTS",
                "numeric_prediction_present": False,
                "theorem_zero_present": False,
                "control_only": True,
            }
        )
    ]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2848_0_Q_CAB", "Q_CAB missing", "blocks A_total"),
        ("REF2848_1_q_R_eff", "q_R_eff missing", "blocks A_total"),
        ("REF2848_2_sigma_R", "sigma_R missing", "blocks sign of finite charge"),
        ("REF2848_3_GM", "GM/source convention missing", "blocks delta_p/q_R_hat normalization"),
        ("REF2848_4_theorem_zero", "parent theorem-zero certificate missing", "blocks zero-row alternative"),
        ("REF2848_5_b_R_tail_q_loc", "b_R/tail/q_loc inputs missing", "blocks gamma lane even if A_total existed"),
        ("REF2848_6_full_vector", "full vector closure missing", "blocks local-GR/PPN claim"),
    ]
    return [
        nonclaim(
            {
                "refusal_id": refusal_id,
                "reason": reason,
                "effect": effect,
                "row_rejected": True,
                "control_only": True,
            }
        )
        for refusal_id, reason, effect in specs
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACQ2848_0_Q_CAB", "Q_CAB", "finite numeric charge or parent theorem-zero projection", "charge", "source_path;equation_anchor;Green_convention;units"),
        ("ACQ2848_1_q_R_eff", "q_R_eff", "finite numeric Green charge or parent theorem-zero projection", "charge", "source_path;equation_anchor;Green_convention;units"),
        ("ACQ2848_2_sigma_R", "sigma_R", "parent sign of R-channel Green operator", "dimensionless sign", "source_action_path;operator_sign_anchor"),
        ("ACQ2848_3_GM", "M_source/GM", "same measured source mass used in PPN U=GM/r", "GM or mass", "source_measure_path;GM_convention_anchor"),
        ("ACQ2848_4_b_R", "b_R", "common-frame/no-shadow Weyl response coefficient", "dimensionless", "parent_no_shadow_theorem_or_numeric_source"),
        ("ACQ2848_5_tail", "C_AB_reg/H_R/range", "tail and finite-range correction bound", "profile", "profile_solution_or_projection_bound"),
        ("ACQ2848_6_full_vector", "full PPN residual vector", "all non-gamma local channels", "dimensionless vector", "beta;preferred;source;endpoint;readout;q_loc rows"),
    ]
    return [
        nonclaim(
            {
                "acquisition_id": acquisition_id,
                "quantity": quantity,
                "accepted_forms": forms,
                "units_or_type": units,
                "required_provenance": provenance,
                "current_status": "MISSING",
                "accepted_ready": False,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for acquisition_id, quantity, forms, units, provenance in specs
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    specs = [
        ("CG2848_0_source_register", "source register valid", all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"]), "control source check only"),
        ("CG2848_1_first_prediction", "first local PPN prediction row accepted", False, "candidate row rejected due to missing core inputs"),
        ("CG2848_2_theorem_zero", "parent theorem-zero certificate accepted", False, "parent theorem-zero clauses unsigned"),
        ("CG2848_3_gamma_score", "gamma comparator score", False, "MTS prediction missing"),
        ("CG2848_4_local_GR", "local GR/Newton reduction", False, "full vector still open"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": False,
                "control_check_passed": control_passed,
                "status": "PASS_CONTROL_ONLY" if control_passed and gate_id == "CG2848_0_source_register" else "BLOCKED",
                "reason": reason,
                "control_only": True,
            }
        )
        for gate_id, claim, control_passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2848_0_prediction_attempt", "First local PPN prediction row is rejected.", "REJECTED_NONCLAIM", "Q_CAB, q_R_eff, sigma_R and GM/source normalization are missing"),
        ("DEC2848_1_theorem_attempt", "Parent theorem-zero certificate is rejected.", "NOT_PARENT_SIGNED", "charge-balance condition is known but not owned by a parent action/current theorem"),
        ("DEC2848_2_acquisition", "Core amplitude acquisition is the next useful target.", "SELECTED", "without Q_CAB/q_R_eff/sigma_R/GM, the PPN dry run cannot become a test"),
        ("DEC2848_3_no_claim", "No local-GR/Newton/PPN claim.", "LOCKED", "candidate row is a rejected template, not a prediction"),
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
                "next_id": "NEXT2848_0_2849",
                "status": "selected_primary",
                "target_doc": "2849-Y5-R2FR-core-amplitude-source-acquisition-or-parent-zero-owner-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_core_amplitude_source_acquisition_or_parent_zero_owner_under_AX1090_2849.py",
                "mission": "source or derive the core amplitude pack Q_CAB, q_R_eff, sigma_R and measured-GM convention; accept either parent theorem-zero with source/action anchors or finite numeric rows with units and local paths",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2848_0_candidate", OUTPUTS["candidate_row"], BRANCH_OUTPUTS["candidate_copy"], "rejected first local PPN prediction candidate"),
        ("COPY2848_1_acquisition", OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_copy"], "core amplitude acquisition contract"),
        ("COPY2848_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue handoff"),
        ("COPY2848_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable decision ledger"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(src),
                    "copy_path": str(dst),
                    "purpose": purpose,
                    "exists": dst.exists(),
                }
            )
        )
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
        "accepted_ready",
        "source_backed_value_present",
        "theorem_zero_present",
        "theorem_zero_accepted",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_prediction", "prediction_value", "mts_prediction_value", "A_total_value", "delta_p_value", "q_R_hat_value"}
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("numeric_prediction_present") is True or row.get("numeric_value_present") is True:
                return False
            for key in numeric_keys:
                value = row.get(key)
                if value not in (None, "", "MISSING"):
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
        ("VAL2848_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2848_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2848_2_core_inputs_missing", not any(row["source_backed_value_present"] for row in rows_by_name["availability"]), "core amplitude values remain absent"),
        ("VAL2848_3_theorem_zero_rejected", not any(row["theorem_zero_accepted"] for row in rows_by_name["theorem_attempt"]), "parent theorem-zero certificate remains unaccepted"),
        ("VAL2848_4_candidate_rejected", all(row["row_status"].startswith("REJECTED") for row in rows_by_name["candidate_row"]), "first prediction candidate is rejected"),
        ("VAL2848_5_refusals_present", len(rows_by_name["refusal"]) >= 7, "refusal ledger records every core blocker"),
        ("VAL2848_6_acquisition_contract", len(rows_by_name["acquisition"]) >= 7 and not any(row["accepted_ready"] for row in rows_by_name["acquisition"]), "core acquisition contract exists and remains nonclaim"),
        ("VAL2848_7_next_target_2849", any(row["next_id"] == "NEXT2848_0_2849" and row["selected"] for row in rows_by_name["next"]), "2849 core amplitude acquisition target selected"),
        ("VAL2848_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2848_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2848_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2848_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2848_12_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2848_13_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no MTS numeric prediction rows inserted"),
        ("VAL2848_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2848_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2848_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2848_OVERALL",
            "passed": overall,
            "detail": "2848 attempts the first finite local PPN prediction row, rejects it because Q_CAB/q_R_eff/sigma_R/GM and theorem-zero evidence are missing, and selects core amplitude acquisition as next target.",
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
    content = f"""# 2848 - Y5 R2FR First Finite Local PPN Prediction Row Or Parent Theorem-Zero Under AX1090

Status: `Y5_R2FR_2848_first_PPN_prediction_row_rejected_core_amplitude_missing_nonclaim`

## Private Verdict

2848 tries the first actual local PPN prediction row and rejects it.

The candidate row is structurally clear:

```text
A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)
delta_p_const=c^2*A_total/(2 G M_source)
q_R_hat_const=-c^2*A_total/(G M_source)
```

but the current corpus still lacks the core amplitude pack:

```text
Q_CAB, q_R_eff, sigma_R, measured-GM/source convention
```

and the parent theorem-zero alternative is also not signed. So this checkpoint does not score Cassini, does not claim local GR, and does not pretend a placeholder is a prediction.

The next target is now very concrete: source or derive the core amplitude pack. Once that exists, the 2847 dry-run map can become an actual local PPN smoke runner.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Core Amplitude Input Availability

{markdown_table(rows["availability"], ["availability_id", "quantity", "current_status", "why_required", "source_backed_value_present", "theorem_zero_present", "valid_for_claim"])}

## Parent Theorem-Zero Certificate Attempt

{markdown_table(rows["theorem_attempt"], ["theorem_id", "required_clause", "status", "reason", "parent_signed", "theorem_zero_accepted", "valid_for_claim"])}

## First PPN Prediction Candidate Row

{markdown_table(rows["candidate_row"], ["candidate_id", "observable", "comparator_bound", "row_status", "numeric_prediction_present", "theorem_zero_present", "valid_for_claim"])}

## Prediction Row Refusal Ledger

{markdown_table(rows["refusal"], ["refusal_id", "reason", "effect", "row_rejected", "valid_for_claim"])}

## Core Amplitude Acquisition Contract

{markdown_table(rows["acquisition"], ["acquisition_id", "quantity", "units_or_type", "current_status", "required_provenance", "accepted_ready", "valid_for_claim"])}

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
    rows["availability"] = availability_rows()
    rows["theorem_attempt"] = theorem_attempt_rows()
    rows["candidate_row"] = candidate_row()
    rows["refusal"] = refusal_rows()
    rows["acquisition"] = acquisition_rows()
    rows["claim_gates"] = claim_gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "availability", "theorem_attempt", "candidate_row", "refusal", "acquisition", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2848_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2848_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

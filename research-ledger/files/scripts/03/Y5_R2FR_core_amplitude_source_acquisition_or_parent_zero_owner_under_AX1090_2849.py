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

DOC = ROOT / "2849-Y5-R2FR-core-amplitude-source-acquisition-or-parent-zero-owner-under-AX1090.md"

SRC_2848_DOC = ROOT / "2848-Y5-R2FR-first-finite-local-PPN-prediction-row-or-parent-theorem-zero-under-AX1090.md"
SRC_2848_AVAILABILITY = RESIDUALS / "P8_Y5_R2FR_2848_CORE_AMPLITUDE_INPUT_AVAILABILITY.csv"
SRC_2848_ACQUISITION = RESIDUALS / "P8_Y5_R2FR_2848_CORE_AMPLITUDE_ACQUISITION_CONTRACT.csv"
SRC_2848_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2848_VALIDATION.csv"
SRC_2846_FORMULA = RESIDUALS / "P8_Y5_R2FR_2846_LOCAL_PPN_FORMULA_PACK_NONCLAIM.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2844_CANCEL = RESIDUALS / "P8_Y5_R2FR_2844_CAB_CANCELLATION_THEOREM_ATTEMPT.csv"
SRC_2843_PROFILE = RESIDUALS / "P8_Y5_R2FR_2843_TAUPPN_PROFILE_WITH_CAB_AMPLITUDE.csv"
SRC_2842_PROFILE = RESIDUALS / "P8_Y5_R2FR_2842_FINITE_TAUPPN_PROFILE.csv"
SRC_1883 = ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md"
SRC_1884 = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"
SRC_1063 = ROOT / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md"
SRC_1078 = ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2849_SOURCE_REGISTER.csv",
    "source_scan": RESIDUALS / "P8_Y5_R2FR_2849_CORE_AMPLITUDE_SOURCE_SCAN.csv",
    "parent_zero": RESIDUALS / "P8_Y5_R2FR_2849_PARENT_ZERO_OWNER_ATTEMPT.csv",
    "schema": RESIDUALS / "P8_Y5_R2FR_2849_FINITE_ROW_ACCEPTANCE_SCHEMA.csv",
    "staging": RESIDUALS / "P8_Y5_R2FR_2849_FIRST_ROW_STAGING_TEMPLATE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2849_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2849_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2849_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2849_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2849_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_scan_copy": LOCAL_BOUNDS / "RAB_CAB_core_amplitude_source_scan_2849_NONCLAIM.csv",
    "parent_zero_copy": SOURCE_WEIGHT / "RAB_PARENT_ZERO_OWNER_ATTEMPT_2849_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2849_core_amplitude_parent_equation_hunt_NEXT.csv",
    "schema_copy": BETA_DOCS / "RAB_CORE_AMPLITUDE_ACCEPTANCE_SCHEMA_2849_NONCLAIM.csv",
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
        ("SRC2849_0_2848_doc", SRC_2848_DOC, "NEXT2848_0_2849;VAL2848_OVERALL", "2848 handoff into core amplitude acquisition"),
        ("SRC2849_1_2848_availability", SRC_2848_AVAILABILITY, "AV2848_0_Q_CAB;AV2848_4_theorem_zero", "2848 missing core amplitude availability table"),
        ("SRC2849_2_2848_acquisition", SRC_2848_ACQUISITION, "ACQ2848_0_Q_CAB;ACQ2848_3_GM", "2848 core amplitude acquisition contract"),
        ("SRC2849_3_2848_validation", SRC_2848_VALIDATION, "VAL2848_OVERALL", "2848 validation status"),
        ("SRC2849_4_2846_formula", SRC_2846_FORMULA, "FORM2846_0_A_total;FORM2846_3_theorem_zero", "A_total and theorem-zero symbolic formula pack"),
        ("SRC2849_5_2844_flux", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition;Q_CAB=-sigma_R*q_R_eff", "exact local suppression condition"),
        ("SRC2849_6_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff", "amplitude source pack marks Q_CAB and q_R_eff missing"),
        ("SRC2849_7_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign;CONTRACT2844_6_measured_GM", "parent amplitude contract marks source-current, sign and GM gaps"),
        ("SRC2849_8_2844_cancel", SRC_2844_CANCEL, "CANCEL2844_1_parent_source_identity;CANCEL2844_5_verdict", "cancellation theorem attempt remains parent-proof missing"),
        ("SRC2849_9_2843_profile", SRC_2843_PROFILE, "PROF2843_2_constant_amplitude;PROF2843_3_cancellation_law", "finite tau_PPN profile with CAB amplitude"),
        ("SRC2849_10_2842_profile", SRC_2842_PROFILE, "TAUP2842_3_explicit_profile;TAUP2842_5_constant_limit", "finite tau_PPN profile and constant limit"),
        ("SRC2849_11_1883", SRC_1883, "DPB1883_1_QR_delta_p;DPB1883_2_gamma_combo", "delta_p/q_R_hat and gamma-combo bridge"),
        ("SRC2849_12_1884", SRC_1884, "NBC1884_1_exact_zero_flux_lemma;NBC1884_4_no_boundary_charge_parent_signature", "no-boundary-charge remains parent-signature missing"),
        ("SRC2849_13_2631", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full-vector guard forbids gamma-only claim"),
        ("SRC2849_14_1063", SRC_1063, "NO1063_2_Noether_current_owner;candidate_missing", "Noether/current/source owner remains missing"),
        ("SRC2849_15_1078", SRC_1078, "CO1078_4_verdict;CURRENT_OWNER_NOT_SIGNED", "current owner proof attempt remains unsigned"),
    ]
    return [source_row(*spec) for spec in specs]


def source_scan_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SCAN2849_0_Q_CAB",
            "Q_CAB",
            "target-map monopole charge",
            "PACK2844_0_Q_CAB records Q_CAB=4*pi*A_CAB but marks it MISSING_PARENT_INPUT",
            SRC_2844_PACK,
            "PACK2844_0_Q_CAB",
            "NO_ACCEPTED_SOURCE_FOUND",
            "finite numeric Q_CAB; source_path; equation_anchor; Green convention; units; or parent source-current identity",
        ),
        (
            "SCAN2849_1_q_R_eff",
            "q_R_eff",
            "delta_R Green charge",
            "PACK2844_4_q_R_eff marks finite delta_R Green charge MISSING_SOURCE_NORMALIZATION",
            SRC_2844_PACK,
            "PACK2844_4_q_R_eff",
            "NO_ACCEPTED_SOURCE_FOUND",
            "finite numeric q_R_eff; source_path; equation_anchor; Green convention; units; or parent source-current identity",
        ),
        (
            "SCAN2849_2_sigma_R",
            "sigma_R",
            "R-channel Green sign",
            "CONTRACT2844_5_sign marks the parent-action sign convention missing",
            SRC_2844_CONTRACT,
            "CONTRACT2844_5_sign",
            "NO_ACCEPTED_SOURCE_FOUND",
            "parent action operator sign; equation anchor; branch convention; sigma_R value or theorem-zero owner",
        ),
        (
            "SCAN2849_3_GM",
            "M_source/GM",
            "measured source mass in U=GM/r",
            "CONTRACT2844_6_measured_GM and NO1063_3 both leave measured Newtonian source charge unsigned",
            SRC_2844_CONTRACT,
            "CONTRACT2844_6_measured_GM",
            "NO_ACCEPTED_SOURCE_FOUND",
            "same measured-GM convention as the local PPN source; source measure path; units",
        ),
        (
            "SCAN2849_4_b_R",
            "b_R",
            "common-frame/no-shadow Weyl response",
            "2848 keeps b_R missing, so gamma combo cannot yet be scored",
            SRC_2848_ACQUISITION,
            "ACQ2848_4_b_R",
            "NO_ACCEPTED_SOURCE_FOUND",
            "parent no-shadow theorem or finite numeric b_R row with convention and source",
        ),
        (
            "SCAN2849_5_tail",
            "C_AB_reg/H_R/range tails",
            "regular, homogeneous and finite-range correction control",
            "PACK2844_5_tail_bound marks regular/tail/homogeneous residual bounds missing",
            SRC_2844_PACK,
            "PACK2844_5_tail_bound",
            "NO_ACCEPTED_SOURCE_FOUND",
            "profile solution or projection bound across local arenas",
        ),
        (
            "SCAN2849_6_full_vector",
            "full PPN residual vector",
            "all local non-gamma residual channels",
            "PPNV2631_8_total_abs says the componentwise vector is schema-ready but values/theorem-zeros are missing",
            SRC_2631,
            "PPNV2631_8_total_abs",
            "NO_ACCEPTED_SOURCE_FOUND",
            "beta; preferred-frame; source; endpoint; readout; clock; orbital and q_loc rows",
        ),
        (
            "SCAN2849_7_relation",
            "Q_CAB=-sigma_R*q_R_eff",
            "exact cancellation relation",
            "FLUX2844_5 gives the symbolic suppression condition, not the parent owner of the condition",
            SRC_2844_FLUX,
            "FLUX2844_5_local_suppression_condition",
            "CONDITION_AVAILABLE_PARENT_PROOF_MISSING",
            "single parent current/action theorem that forces the relation and fixes normalization",
        ),
    ]
    return [
        nonclaim(
            {
                "scan_id": scan_id,
                "quantity": quantity,
                "role": role,
                "current_corpus_evidence": evidence,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "current_status": status,
                "missing_for_acceptance": missing,
                "source_backed_value_present": False,
                "numeric_value_present": False,
                "theorem_zero_present": False,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for scan_id, quantity, role, evidence, source_path, anchor, status, missing in specs
    ]


def parent_zero_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PZ2849_0_charge_balance_condition",
            "Q_CAB=-sigma_R*q_R_eff",
            "CONDITION_AVAILABLE_NOT_OWNER_SIGNED",
            "2844 gives the exact cancellation condition but not the parent theorem that enforces it",
            SRC_2844_FLUX,
            "FLUX2844_5_local_suppression_condition",
        ),
        (
            "PZ2849_1_single_current_owner",
            "one parent current owns both Q_CAB and q_R_eff",
            "MISSING_CURRENT_OWNER",
            "1078 leaves the current-owner proof unsigned and the rescaling counterexample alive",
            SRC_1078,
            "CO1078_4_verdict",
        ),
        (
            "PZ2849_2_no_rescaling",
            "no independent source/current normalization rescaling",
            "COUNTEREXAMPLE_SURVIVES",
            "without a signed owner, J_A -> c_A J_A can move normalization into a species/source coefficient",
            SRC_1078,
            "CO1078_3_current_rescaling_counterexample",
        ),
        (
            "PZ2849_3_boundary_source_silence",
            "boundary charge, ordinary source charge, and readout projection are silent",
            "MISSING_BOUNDARY_SOURCE_READOUT_SILENCE",
            "1884 keeps the no-boundary-charge parent signature missing",
            SRC_1884,
            "NBC1884_4_no_boundary_charge_parent_signature",
        ),
        (
            "PZ2849_4_sign_GM_owner",
            "sigma_R and measured-GM convention are fixed by the same branch",
            "MISSING_SIGN_AND_GM_CONVENTION",
            "2844 parent amplitude contract leaves sign and measured-GM unsigned",
            SRC_2844_CONTRACT,
            "CONTRACT2844_5_sign;CONTRACT2844_6_measured_GM",
        ),
        (
            "PZ2849_5_full_vector_closure",
            "all local PPN residual channels are zero or source-bounded in the same convention",
            "MISSING_FULL_VECTOR_CLOSURE",
            "2631 forbids a gamma-only pass",
            SRC_2631,
            "RG2631_0_no_gamma_only",
        ),
        (
            "PZ2849_6_verdict",
            "parent zero-owner theorem for the core amplitude pack",
            "NOT_DERIVED",
            "the symbolic zero condition is clean, but current owner, rescaling, boundary/source/readout, sign, GM and full-vector clauses remain unsigned",
            SRC_2848_DOC,
            "NEXT2848_0_2849",
        ),
    ]
    return [
        nonclaim(
            {
                "parent_zero_id": row_id,
                "required_clause": clause,
                "status": status,
                "reason": reason,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "condition_available": row_id == "PZ2849_0_charge_balance_condition",
                "parent_signed": False,
                "zero_owner_accepted": False,
                "theorem_zero_accepted": False,
                "control_only": True,
            }
        )
        for row_id, clause, status, reason, source_path, anchor in specs
    ]


def schema_rows() -> list[dict[str, Any]]:
    specs = [
        ("SCH2849_0_quantity", "quantity", "all amplitude rows", "must be one of Q_CAB, q_R_eff, sigma_R, M_source/GM, b_R, tail, full_vector", "blank or alias-only quantity"),
        ("SCH2849_1_value", "value", "finite numeric rows", "must be a real finite value with sign convention; zero requires theorem proof", "MISSING, symbolic placeholder, closure-only"),
        ("SCH2849_2_units", "units", "finite numeric rows", "must state charge, dimensionless, GM, mass, profile or vector units as applicable", "unitless when the quantity is dimensional"),
        ("SCH2849_3_source_path", "source_path", "all accepted rows", "must be an existing local file path under post-checkpoint-work or vetted source intake", "missing, web-only, or non-existent local path"),
        ("SCH2849_4_equation_anchor", "equation_anchor", "all accepted rows", "must identify the exact equation/table/row giving the value or theorem", "generic document citation"),
        ("SCH2849_5_green_convention", "green_convention", "Q_CAB and q_R_eff", "must specify Laplacian/Yukawa/common-kernel normalization and 4*pi convention", "unmatched Green normalization"),
        ("SCH2849_6_branch_id", "branch_id", "all rows", "must name the local branch and arena convention used by the PPN map", "global statement with no local branch"),
        ("SCH2849_7_sign_convention", "sign_convention", "sigma_R and charge rows", "must fix source/operator sign before Q_CAB and q_R_eff can be combined", "implicit sign"),
        ("SCH2849_8_GM_convention", "GM_convention", "delta_p/q_R_hat rows", "must state the same measured GM/source mass used in U=GM/r", "bare M with no measured-source convention"),
        ("SCH2849_9_valid_for_claim", "valid_for_claim", "claim gate", "may become true only after every required field is sourced and no missing markers remain", "true while any MISSING_* placeholder remains"),
    ]
    return [
        nonclaim(
            {
                "schema_id": schema_id,
                "field": field,
                "required_for": required_for,
                "acceptance_rule": acceptance_rule,
                "rejection_rule": rejection_rule,
                "schema_only": True,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for schema_id, field, required_for, acceptance_rule, rejection_rule in specs
    ]


def staging_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "staging_id": "STAGE2849_0_first_gamma_row_template",
                "observable": "gamma_minus_1",
                "A_total_formula": "A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)",
                "delta_p_formula": "delta_p_const=c^2*A_total/(2*G*M_source)",
                "q_R_hat_formula": "q_R_hat_const=-c^2*A_total/(G*M_source)",
                "Q_CAB": "MISSING_Q_CAB",
                "q_R_eff": "MISSING_q_R_eff",
                "sigma_R": "MISSING_sigma_R",
                "M_source_or_GM": "MISSING_GM_CONVENTION",
                "b_R": "MISSING_b_R",
                "tail_profile": "MISSING_TAIL_PROFILE",
                "full_vector": "MISSING_FULL_VECTOR",
                "row_status": "STAGED_INVALID_NONCLAIM",
                "finite_row_accepted": False,
                "numeric_prediction_present": False,
                "theorem_zero_present": False,
                "control_only": True,
            }
        )
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_control = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    specs = [
        ("CG2849_0_source_register", "source register valid", "PASS_CONTROL_ONLY" if source_control else "BLOCKED", "control source check only", source_control),
        ("CG2849_1_finite_core_pack", "finite core amplitude pack accepted", "BLOCKED", "Q_CAB/q_R_eff/sigma_R/GM remain unsourced", False),
        ("CG2849_2_parent_zero_owner", "parent zero-owner theorem accepted", "BLOCKED", "current owner, rescaling, boundary/source/readout, sign, GM and full-vector clauses remain unsigned", False),
        ("CG2849_3_first_PPN_row", "first local PPN prediction row accepted", "BLOCKED", "staging row contains explicit MISSING_* markers", False),
        ("CG2849_4_local_GR_Newton", "local GR/Newton reduction claimed", "BLOCKED", "full PPN residual vector is not closed", False),
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
        ("DEC2849_0_scan", "Core amplitude source acquisition was attempted.", "NO_ACCEPTED_SOURCE_FOUND", "the corpus contains formulas and missing-input contracts, not source-backed values for Q_CAB/q_R_eff/sigma_R/GM"),
        ("DEC2849_1_parent_zero", "Parent zero-owner route was attempted.", "NOT_DERIVED", "the exact cancellation condition is available, but the parent current/source owner and normalization proof are unsigned"),
        ("DEC2849_2_schema", "Finite row acceptance schema was made explicit.", "CREATED_NONCLAIM", "future rows now have a concrete source/unit/convention contract instead of vague placeholders"),
        ("DEC2849_3_staging", "First local PPN row remains staged-invalid.", "BLOCKED", "the row intentionally carries MISSING_* markers and cannot be scored"),
        ("DEC2849_4_next", "Next route is a parent source-equation hunt.", "SELECTED_2850", "derivation-first is still cleaner than injecting arbitrary finite amplitudes"),
        ("DEC2849_5_no_claim", "No R10, PPN, local-GR or Newton-limit claim.", "LOCKED", "2849 is acquisition discipline, not evidence"),
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
                "next_id": "NEXT2849_0_2850",
                "status": "selected_primary",
                "target_doc": "2850-Y5-R2FR-core-amplitude-parent-source-equation-hunt-or-manual-source-ledger-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_core_amplitude_parent_source_equation_hunt_or_manual_source_ledger_under_AX1090_2850.py",
                "mission": "locate or derive actual parent equations/source paths for Q_CAB, q_R_eff, sigma_R and measured GM; if absent, produce a manual source ledger instead of fabricating finite rows",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2849_0_scan", OUTPUTS["source_scan"], BRANCH_OUTPUTS["source_scan_copy"], "core amplitude source scan nonclaim copy"),
        ("COPY2849_1_parent_zero", OUTPUTS["parent_zero"], BRANCH_OUTPUTS["parent_zero_copy"], "parent zero-owner attempt nonclaim copy"),
        ("COPY2849_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue handoff to 2850"),
        ("COPY2849_3_schema", OUTPUTS["schema"], BRANCH_OUTPUTS["schema_copy"], "finite row acceptance schema nonclaim copy"),
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
                    "control_only": True,
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
        "zero_owner_accepted",
        "parent_signed",
        "finite_row_accepted",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {
        "numeric_prediction",
        "prediction_value",
        "mts_prediction_value",
        "A_total_value",
        "delta_p_value",
        "q_R_hat_value",
        "Q_CAB_value",
        "q_R_eff_value",
        "sigma_R_value",
        "GM_value",
    }
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
    staging_text = ";".join(str(value) for row in rows_by_name["staging"] for value in row.values())
    checks = [
        ("VAL2849_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2849_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2849_2_no_accepted_core_values", not any(row["accepted_ready"] or row["source_backed_value_present"] or row["numeric_value_present"] for row in rows_by_name["source_scan"]), "source scan found no accepted finite core amplitude values"),
        ("VAL2849_3_parent_zero_not_derived", any(row["parent_zero_id"] == "PZ2849_6_verdict" and row["status"] == "NOT_DERIVED" for row in rows_by_name["parent_zero"]), "parent zero-owner attempt remains not derived"),
        ("VAL2849_4_schema_complete", len(rows_by_name["schema"]) >= 10 and not any(row["accepted_ready"] for row in rows_by_name["schema"]), "finite-row acceptance schema is present and nonclaim"),
        ("VAL2849_5_staging_invalid", "MISSING_Q_CAB" in staging_text and "MISSING_q_R_eff" in staging_text and all(row["row_status"] == "STAGED_INVALID_NONCLAIM" for row in rows_by_name["staging"]), "first row staging template remains explicitly invalid"),
        ("VAL2849_6_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2849_7_next_target_2850", any(row["next_id"] == "NEXT2849_0_2850" and row["selected"] for row in rows_by_name["next"]), "2850 parent source-equation hunt selected"),
        ("VAL2849_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2849_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2849_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2849_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2849_12_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2849_13_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no MTS numeric prediction rows inserted"),
        ("VAL2849_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2849_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2849_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2849_OVERALL",
            "passed": overall,
            "detail": "2849 audits the missing core amplitude pack, rejects parent zero-owner as unsigned, creates a finite-row acceptance schema and selects a parent source-equation hunt for 2850.",
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
    content = f"""# 2849 - Y5 R2FR Core Amplitude Source Acquisition Or Parent Zero-Owner Under AX1090

Status: `Y5_R2FR_2849_core_amplitude_pack_unsourced_parent_zero_owner_not_derived_nonclaim`

## Private Verdict

2849 went straight at the missing local PPN amplitude pack:

```text
A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)
delta_p_const=c^2*A_total/(2 G M_source)
q_R_hat_const=-c^2*A_total/(G M_source)
```

The result is disciplined but not yet victorious: no accepted finite row for `Q_CAB`, `q_R_eff`, `sigma_R`, or measured `GM` was found, and the parent zero-owner route is still unsigned.

The useful progress is that the acceptance contract is now explicit. A future row must carry real source paths, equation anchors, units, Green/sign conventions, and a measured-GM convention. Otherwise it remains a placeholder, no matter how tempting the algebra looks.

The next route is 2850: a narrow parent source-equation hunt. Either we find/derive the equations that own these amplitudes, or we write the manual source ledger saying exactly what must be supplied.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Core Amplitude Source Scan

{markdown_table(rows["source_scan"], ["scan_id", "quantity", "current_status", "current_corpus_evidence", "missing_for_acceptance", "accepted_ready", "valid_for_claim"])}

## Parent Zero-Owner Attempt

{markdown_table(rows["parent_zero"], ["parent_zero_id", "required_clause", "status", "reason", "parent_signed", "zero_owner_accepted", "valid_for_claim"])}

## Finite Row Acceptance Schema

{markdown_table(rows["schema"], ["schema_id", "field", "required_for", "acceptance_rule", "rejection_rule", "valid_for_claim"])}

## First Row Staging Template

{markdown_table(rows["staging"], ["staging_id", "observable", "row_status", "Q_CAB", "q_R_eff", "sigma_R", "M_source_or_GM", "full_vector", "valid_for_claim"])}

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
    rows["source_scan"] = source_scan_rows()
    rows["parent_zero"] = parent_zero_rows()
    rows["schema"] = schema_rows()
    rows["staging"] = staging_rows()
    rows["claim_gates"] = claim_gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "source_scan", "parent_zero", "schema", "staging", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2849_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2849_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
